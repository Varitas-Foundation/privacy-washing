"""
3-LLM Judge Verification for Statement-Level Contradictions

Verifies NLI-flagged statement-level contradictions using 3 independent LLM
judges with majority-vote consensus.  This is the quality gate between
NLI detection and analysis — only judge-confirmed contradictions are included
in the final report.

Architecture:
  - 3 LLMs via OpenRouter (configured via MULTIMODEL_1/2/3 in .env)
  - ThreadPoolExecutor parallel execution per pair
  - Majority-vote consensus (unanimous / majority / split)
  - Agreement metrics (Fleiss' kappa, pairwise Cohen's kappa)
  - Pre-filter: only judges NLI-flagged pairs above a similarity threshold

Input:
  - statement_contradictions.json (from detect_statement_contradictions.py)

Output:
  - statement_judge_results.json

Usage:
  python judge_statement_contradictions.py
  python judge_statement_contradictions.py --similarity-threshold 0.6
  python judge_statement_contradictions.py --data-dir ../../opp115_experiment
"""

import json
import os
import sys
import time
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

import httpx
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Paths & environment
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(REPO_ROOT / ".env")

# ===========================================================================
# MODEL CONFIGURATION -- reads JUDGE_MODEL_1/2/3 from .env at project root,
# falling back to the legacy shared MULTIMODEL_1/2/3 variables.
# JUDGE_MODEL_* exists so the judge panel can be configured independently of
# the extraction panel (EXTRACTION_MODEL_* in extract_statements_multimodel.py),
# removing the extractor-judge model overlap.
# Override at runtime with --models flag.
# ===========================================================================
JUDGE_MODELS = [
    os.environ.get("JUDGE_MODEL_1", os.environ.get("MULTIMODEL_1", "")),
    os.environ.get("JUDGE_MODEL_2", os.environ.get("MULTIMODEL_2", "")),
    os.environ.get("JUDGE_MODEL_3", os.environ.get("MULTIMODEL_3", "")),
]
JUDGE_MODELS = [m.strip().strip('"').strip("'") for m in JUDGE_MODELS]
# ===========================================================================

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
VALID_VERDICTS = {"CONTRADICTION", "NOT_CONTRADICTION"}

SCRIPT_DIR = Path(__file__).parent
PROMPT_FILE = SCRIPT_DIR / "judge_statement_prompt.md"

# Default paths (OPPT corpus)
CONTRADICTIONS_PATH = REPO_ROOT / "output" / "statement_contradictions.json"
OUTPUT_PATH = REPO_ROOT / "output" / "statement_judge_results.json"

# Default similarity pre-filter for judge input
DEFAULT_SIMILARITY_THRESHOLD = 0.5


def load_judge_prompt() -> str:
    """Load the judge prompt from external file."""
    if not PROMPT_FILE.exists():
        raise FileNotFoundError(
            f"Judge prompt file not found: {PROMPT_FILE}\n"
            "Expected file: scripts/judge_statement_prompt.md"
        )
    return PROMPT_FILE.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# OpenRouter client
# ---------------------------------------------------------------------------
class OpenRouterClient:
    """Client for OpenRouter API supporting multiple model providers."""

    def __init__(self, api_key: str, timeout: float = 90.0):
        self.api_key = api_key
        self.timeout = timeout
        self.base_url = OPENROUTER_BASE_URL

    def _get_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/dark-patterns-research",
            "X-Title": "Privacy Washing Statement Judge",
        }

    def judge(self, prompt: str, model: str, judge_id: str, max_retries: int = 3) -> dict:
        """Send a contradiction judgment request with retry logic."""
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            # 8192 rather than 1024: reasoning models (e.g. GLM-5.3-Flash) spend
            # reasoning tokens against max_tokens on OpenRouter; a 1024 cap
            # caused empty content on ~13% of responses in the 2026-08-30 run.
            "max_tokens": 8192,
            "temperature": 0,
        }

        last_error = None
        for attempt in range(max_retries):
            try:
                with httpx.Client(timeout=self.timeout) as client:
                    response = client.post(
                        f"{self.base_url}/chat/completions",
                        headers=self._get_headers(),
                        json=payload,
                    )
                    response.raise_for_status()

                    data = response.json()
                    raw = (data["choices"][0]["message"].get("content") or "").strip()
                    usage = data.get("usage", {})

                    # Empty content is a transient serving artifact (e.g. a
                    # reasoning model emitting only reasoning tokens); retry it
                    # like a transport error instead of recording an invalid
                    # verdict immediately.
                    if not raw:
                        last_error = "empty content in response"
                        if attempt < max_retries - 1:
                            time.sleep(2 ** attempt)
                            continue
                        break

                    parsed = _parse_judge_response(raw)

                    return {
                        "verdict": parsed.get("verdict"),
                        "reasoning": parsed.get("reasoning", ""),
                        "raw_response": raw,
                        "valid": parsed.get("verdict") in VALID_VERDICTS,
                        "judge_id": judge_id,
                        "model": model,
                        "provider": model.split("/")[0] if "/" in model else "unknown",
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "usage": usage,
                    }

            except httpx.HTTPStatusError as e:
                last_error = f"HTTP {e.response.status_code}: {e.response.text[:200]}"
                if e.response.status_code == 429:
                    wait = 2 ** attempt * 5
                    print(f"    Rate limited ({judge_id}), waiting {wait}s...")
                    time.sleep(wait)
                    continue
                break
            except Exception as e:
                last_error = str(e)
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                break

        return {
            "verdict": None,
            "reasoning": "",
            "raw_response": "",
            "valid": False,
            "judge_id": judge_id,
            "model": model,
            "provider": model.split("/")[0] if "/" in model else "unknown",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "error": last_error,
        }


def _parse_judge_response(raw: str) -> dict:
    """Extract verdict JSON from LLM response, handling markdown fences."""
    import re

    text = raw.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        text = "\n".join(lines).strip()

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r'\{[^{}]*"verdict"[^{}]*\}', text, re.DOTALL)
        if match:
            try:
                parsed = json.loads(match.group())
            except json.JSONDecodeError:
                return {"verdict": None}
        else:
            return {"verdict": None}

    verdict = parsed.get("verdict", "")
    if isinstance(verdict, str):
        verdict = verdict.strip().upper()
    parsed["verdict"] = verdict if verdict in VALID_VERDICTS else None

    return parsed


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------
def load_flagged_pairs(contradictions_path: Path, similarity_threshold: float) -> list[dict]:
    """
    Load NLI-flagged statement pairs, filtered by similarity threshold.

    Returns list of pair dicts with commitment_text and practice_text.
    """
    with open(contradictions_path) as f:
        data = json.load(f)

    all_pairs = data.get("pairs", [])
    total = len(all_pairs)

    # Filter to NLI-flagged contradictions
    flagged = [p for p in all_pairs if p.get("is_contradiction")]
    print(f"  NLI-flagged contradictions: {len(flagged)} / {total} total pairs")

    # Filter by similarity threshold
    above_threshold = [p for p in flagged if p.get("semantic_similarity", 0) >= similarity_threshold]
    print(f"  Above similarity threshold ({similarity_threshold}): {len(above_threshold)}")

    # Sort by similarity descending (judge strongest first for early signal)
    above_threshold.sort(key=lambda p: p.get("semantic_similarity", 0), reverse=True)

    return above_threshold


# ---------------------------------------------------------------------------
# Prompt construction
# ---------------------------------------------------------------------------
def build_prompt(company: str, commitment_text: str, practice_text: str, template: str) -> str:
    """Insert pair data into the judge prompt template."""
    return template.format(
        company=company,
        commitment_text=commitment_text,
        practice_text=practice_text,
    )


# ---------------------------------------------------------------------------
# Judging
# ---------------------------------------------------------------------------
def judge_pair(client: OpenRouterClient, pair: dict, model: str, judge_id: str, template: str) -> dict:
    """Single API call: judge one pair with one model."""
    prompt = build_prompt(
        pair["company"],
        pair["commitment_text"],
        pair["practice_text"],
        template,
    )
    return client.judge(prompt, model, judge_id)


def judge_pair_three_models(
    client: OpenRouterClient,
    pair: dict,
    models: list[str],
    template: str,
    max_workers: int = 3,
) -> dict:
    """
    Judge a single pair with 3 models in parallel.
    Returns per-judge verdicts, consensus, and metadata.
    """
    judge_ids = ["judge_1", "judge_2", "judge_3"]
    results = {}

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(judge_pair, client, pair, model, jid, template): (jid, model)
            for jid, model in zip(judge_ids, models)
        }

        for future in as_completed(futures):
            jid, model = futures[future]
            try:
                results[jid] = future.result()
            except Exception as e:
                results[jid] = {
                    "verdict": None,
                    "reasoning": "",
                    "raw_response": str(e),
                    "valid": False,
                    "judge_id": jid,
                    "model": model,
                    "error": str(e),
                }

    # -- Consensus analysis --
    valid_verdicts = [
        results[jid]["verdict"]
        for jid in judge_ids
        if results[jid]["valid"]
    ]

    verdict_counts = Counter(valid_verdicts)

    if len(valid_verdicts) < 2:
        consensus_type = "insufficient_valid"
        final_verdict = None
        needs_review = True
    elif len(verdict_counts) == 1:
        consensus_type = "unanimous"
        final_verdict = valid_verdicts[0]
        needs_review = False
    elif verdict_counts.most_common(1)[0][1] >= 2:
        consensus_type = "majority"
        final_verdict = verdict_counts.most_common(1)[0][0]
        needs_review = False
    else:
        consensus_type = "split"
        final_verdict = None
        needs_review = True

    # Pairwise agreement
    pairwise = {}
    for i, jid1 in enumerate(judge_ids):
        for jid2 in judge_ids[i + 1:]:
            key = f"{jid1}_vs_{jid2}"
            if results[jid1]["valid"] and results[jid2]["valid"]:
                pairwise[key] = results[jid1]["verdict"] == results[jid2]["verdict"]
            else:
                pairwise[key] = None

    return {
        "pair_id": pair["pair_id"],
        "company": pair["company"],
        "commitment_statement_id": pair["commitment_statement_id"],
        "practice_statement_id": pair["practice_statement_id"],
        "commitment_text": pair["commitment_text"],
        "practice_text": pair["practice_text"],
        "commitment_category": pair.get("commitment_category", ""),
        "practice_category": pair.get("practice_category", ""),
        "source_segment_pair": pair.get("source_segment_pair", ""),
        "semantic_similarity": pair.get("semantic_similarity", 0.0),
        "nli_contradiction_score": pair.get("nli_contradiction_score", 0.0),
        "nli_is_contradiction": pair.get("is_contradiction", False),
        "judge_1": results["judge_1"],
        "judge_2": results["judge_2"],
        "judge_3": results["judge_3"],
        "consensus_type": consensus_type,
        "final_verdict": final_verdict,
        "verdict_distribution": dict(verdict_counts),
        "pairwise_agreement": pairwise,
        "needs_review": needs_review,
    }


# ---------------------------------------------------------------------------
# Agreement metrics
# ---------------------------------------------------------------------------
def compute_fleiss_kappa(judgments: list[list[str]], categories: list[str]) -> float:
    """Compute Fleiss' kappa for inter-rater agreement."""
    n = len(judgments)
    if n == 0:
        return 0.0
    N = len(judgments[0])
    k = len(categories)

    cat_idx = {c: i for i, c in enumerate(categories)}

    counts = []
    for item_labels in judgments:
        row = [0] * k
        for label in item_labels:
            if label in cat_idx:
                row[cat_idx[label]] += 1
        counts.append(row)

    P_items = []
    for row in counts:
        sum_sq = sum(c * c for c in row)
        P_i = (sum_sq - N) / (N * (N - 1)) if N > 1 else 0.0
        P_items.append(P_i)

    P_bar = sum(P_items) / n if n > 0 else 0.0

    total_assignments = n * N
    P_e = 0.0
    for j in range(k):
        col_sum = sum(counts[i][j] for i in range(n))
        p_j = col_sum / total_assignments if total_assignments > 0 else 0.0
        P_e += p_j * p_j

    if abs(1.0 - P_e) < 1e-10:
        return 1.0 if abs(P_bar - P_e) < 1e-10 else 0.0

    return (P_bar - P_e) / (1.0 - P_e)


def compute_cohens_kappa(labels_a: list[str], labels_b: list[str], categories: list[str]) -> float:
    """Compute Cohen's kappa between two raters."""
    n = len(labels_a)
    if n == 0:
        return 0.0

    cat_idx = {c: i for i, c in enumerate(categories)}
    k = len(categories)

    matrix = [[0] * k for _ in range(k)]
    for la, lb in zip(labels_a, labels_b):
        if la in cat_idx and lb in cat_idx:
            matrix[cat_idx[la]][cat_idx[lb]] += 1

    P_o = sum(matrix[i][i] for i in range(k)) / n

    P_e = 0.0
    for j in range(k):
        row_sum = sum(matrix[j])
        col_sum = sum(matrix[i][j] for i in range(k))
        P_e += (row_sum / n) * (col_sum / n)

    if abs(1.0 - P_e) < 1e-10:
        return 1.0 if abs(P_o - P_e) < 1e-10 else 0.0

    return (P_o - P_e) / (1.0 - P_e)


def compute_agreement(annotations: list[dict], models: list[str]) -> dict:
    """Compute full agreement metrics across all judged pairs."""
    categories = sorted(VALID_VERDICTS)
    judge_ids = ["judge_1", "judge_2", "judge_3"]

    all_valid_labels = []
    per_judge = {jid: [] for jid in judge_ids}

    for ann in annotations:
        if all(ann[jid]["valid"] for jid in judge_ids):
            item_labels = [ann[jid]["verdict"] for jid in judge_ids]
            all_valid_labels.append(item_labels)
            for idx, jid in enumerate(judge_ids):
                per_judge[jid].append(item_labels[idx])

    n_valid = len(all_valid_labels)

    fleiss_k = compute_fleiss_kappa(all_valid_labels, categories) if n_valid > 0 else None

    pairwise_kappa = {}
    pairwise_pairs = [
        ("judge_1", "judge_2"),
        ("judge_1", "judge_3"),
        ("judge_2", "judge_3"),
    ]
    for jid1, jid2 in pairwise_pairs:
        key = f"{jid1}_vs_{jid2}"
        if n_valid > 0:
            pairwise_kappa[key] = {
                "cohens_kappa": compute_cohens_kappa(
                    per_judge[jid1], per_judge[jid2], categories
                ),
                "providers": f"{models[judge_ids.index(jid1)].split('/')[0]} vs "
                             f"{models[judge_ids.index(jid2)].split('/')[0]}",
            }
        else:
            pairwise_kappa[key] = {"cohens_kappa": None, "providers": ""}

    consensus_counts = Counter(ann["consensus_type"] for ann in annotations)
    total = len(annotations)

    pairwise_agree = {
        "judge_1_vs_judge_2": {"agree": 0, "disagree": 0},
        "judge_1_vs_judge_3": {"agree": 0, "disagree": 0},
        "judge_2_vs_judge_3": {"agree": 0, "disagree": 0},
    }
    for ann in annotations:
        for pair_key, agreed in ann["pairwise_agreement"].items():
            if agreed is not None:
                stat = "agree" if agreed else "disagree"
                pairwise_agree[pair_key][stat] += 1

    for pk in pairwise_agree:
        t = pairwise_agree[pk]["agree"] + pairwise_agree[pk]["disagree"]
        pairwise_agree[pk]["rate"] = pairwise_agree[pk]["agree"] / t if t > 0 else 0.0

    return {
        "total_pairs": total,
        "valid_for_kappa": n_valid,
        "fleiss_kappa": round(fleiss_k, 4) if fleiss_k is not None else None,
        "pairwise_cohens_kappa": {
            k: {**v, "cohens_kappa": round(v["cohens_kappa"], 4) if v["cohens_kappa"] is not None else None}
            for k, v in pairwise_kappa.items()
        },
        "consensus_counts": {
            "unanimous": consensus_counts.get("unanimous", 0),
            "majority": consensus_counts.get("majority", 0),
            "split": consensus_counts.get("split", 0),
            "insufficient_valid": consensus_counts.get("insufficient_valid", 0),
        },
        "unanimous_rate": consensus_counts.get("unanimous", 0) / total if total > 0 else 0.0,
        "majority_rate": consensus_counts.get("majority", 0) / total if total > 0 else 0.0,
        "agreement_rate": (
            (consensus_counts.get("unanimous", 0) + consensus_counts.get("majority", 0))
            / total
        ) if total > 0 else 0.0,
        "pairwise_agreement_rates": pairwise_agree,
    }


# ---------------------------------------------------------------------------
# NLI comparison
# ---------------------------------------------------------------------------
def compare_with_nli(annotations: list[dict]) -> dict:
    """
    Analyze how judge verdicts relate to NLI scores.

    Since all input pairs are NLI-flagged, this measures what fraction the
    judges confirm vs reject.  Also correlates NLI score with judge verdict.
    """
    confirmed = []
    rejected = []
    needs_review = []

    for ann in annotations:
        if ann["needs_review"]:
            needs_review.append(ann)
        elif ann["final_verdict"] == "CONTRADICTION":
            confirmed.append(ann)
        else:
            rejected.append(ann)

    # Score distributions
    confirmed_scores = [a["nli_contradiction_score"] for a in confirmed]
    rejected_scores = [a["nli_contradiction_score"] for a in rejected]
    confirmed_sims = [a["semantic_similarity"] for a in confirmed]
    rejected_sims = [a["semantic_similarity"] for a in rejected]

    def _stats(values):
        if not values:
            return {"count": 0, "mean": None, "median": None, "min": None, "max": None}
        s = sorted(values)
        return {
            "count": len(s),
            "mean": round(sum(s) / len(s), 4),
            "median": round(s[len(s) // 2], 4),
            "min": round(s[0], 4),
            "max": round(s[-1], 4),
        }

    # Per-company breakdown
    company_stats = {}
    for ann in annotations:
        company = ann["company"]
        if company not in company_stats:
            company_stats[company] = {"confirmed": 0, "rejected": 0, "needs_review": 0}
        if ann["needs_review"]:
            company_stats[company]["needs_review"] += 1
        elif ann["final_verdict"] == "CONTRADICTION":
            company_stats[company]["confirmed"] += 1
        else:
            company_stats[company]["rejected"] += 1

    return {
        "total_judged": len(annotations),
        "confirmed_contradictions": len(confirmed),
        "rejected_not_contradiction": len(rejected),
        "needs_review": len(needs_review),
        "confirmation_rate": round(len(confirmed) / len(annotations), 4) if annotations else 0.0,
        "nli_score_confirmed": _stats(confirmed_scores),
        "nli_score_rejected": _stats(rejected_scores),
        "similarity_confirmed": _stats(confirmed_sims),
        "similarity_rejected": _stats(rejected_sims),
        "per_company": company_stats,
    }


# ---------------------------------------------------------------------------
# Saving and printing
# ---------------------------------------------------------------------------
def save_results(results: dict, output_path: Path):
    """Save results to JSON."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)


def print_summary(results: dict, models: list[str]):
    """Print summary statistics to console."""
    agreement = results.get("agreement_metrics", {})
    comparison = results.get("nli_comparison", {})

    print("\n" + "=" * 60)
    print("STATEMENT-LEVEL 3-LLM JUDGE VERIFICATION COMPLETE")
    print("=" * 60)

    print(f"\nModels used:")
    for i, model in enumerate(models, 1):
        provider = model.split("/")[0]
        print(f"  Judge {i}: {model} ({provider})")

    print(f"\nJudge Agreement:")
    print(f"  Total pairs judged: {agreement.get('total_pairs', 0)}")
    print(f"  Unanimous (3/3):    {agreement.get('consensus_counts', {}).get('unanimous', 0)} "
          f"({agreement.get('unanimous_rate', 0):.1%})")
    print(f"  Majority (2/3):     {agreement.get('consensus_counts', {}).get('majority', 0)} "
          f"({agreement.get('majority_rate', 0):.1%})")
    print(f"  Usable (>=2/3):     {agreement.get('agreement_rate', 0):.1%}")
    print(f"  Needs review:       "
          f"{agreement.get('consensus_counts', {}).get('split', 0) + agreement.get('consensus_counts', {}).get('insufficient_valid', 0)}")
    fk = agreement.get("fleiss_kappa")
    print(f"  Fleiss' kappa:      {fk:.4f}" if fk is not None else "  Fleiss' kappa:      N/A")

    print(f"\nPairwise Cohen's Kappa:")
    for pair_key, vals in agreement.get("pairwise_cohens_kappa", {}).items():
        ck = vals.get("cohens_kappa")
        provs = vals.get("providers", pair_key)
        print(f"  {provs}: {ck:.4f}" if ck is not None else f"  {provs}: N/A")

    print(f"\nVerification Results (all pairs were NLI-flagged):")
    print(f"  Confirmed contradictions:   {comparison.get('confirmed_contradictions', 0)}")
    print(f"  Rejected (not contradiction): {comparison.get('rejected_not_contradiction', 0)}")
    print(f"  Needs review (split/invalid): {comparison.get('needs_review', 0)}")
    conf_rate = comparison.get('confirmation_rate', 0)
    print(f"  Confirmation rate:          {conf_rate:.1%}")

    print(f"\nNLI Score by Judge Verdict:")
    for label, key in [("Confirmed", "nli_score_confirmed"), ("Rejected", "nli_score_rejected")]:
        stats = comparison.get(key, {})
        if stats.get("count"):
            print(f"  {label}: mean={stats['mean']:.3f}, "
                  f"median={stats['median']:.3f}, "
                  f"range=[{stats['min']:.3f}, {stats['max']:.3f}]")

    print(f"\nPer-Company Results:")
    for company, stats in sorted(comparison.get("per_company", {}).items()):
        total = stats["confirmed"] + stats["rejected"] + stats["needs_review"]
        rate = stats["confirmed"] / total if total > 0 else 0
        print(f"  {company}: {stats['confirmed']} confirmed, "
              f"{stats['rejected']} rejected, "
              f"{stats['needs_review']} review "
              f"({rate:.0%} confirmed)")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def parse_args():
    parser = argparse.ArgumentParser(
        description="3-LLM Judge Verification for Statement-Level Contradictions"
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=None,
        help="Directory containing statement_contradictions.json. "
             "Default: OPPT corpus data directory.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output path for statement_judge_results.json.",
    )
    parser.add_argument(
        "--models",
        nargs=3,
        default=None,
        help="Three OpenRouter model IDs to use as judges.",
    )
    parser.add_argument(
        "--similarity-threshold",
        type=float,
        default=DEFAULT_SIMILARITY_THRESHOLD,
        help=f"Minimum semantic similarity for pairs to judge (default: {DEFAULT_SIMILARITY_THRESHOLD}).",
    )
    parser.add_argument(
        "--no-resume",
        action="store_true",
        help="Start fresh, ignoring existing output.",
    )
    parser.add_argument(
        "--companies",
        nargs="+",
        default=None,
        help="Only judge pairs from these companies.",
    )
    parser.add_argument(
        "--max-pairs",
        type=int,
        default=None,
        help="Maximum number of pairs to judge (useful for testing).",
    )
    parser.add_argument(
        "--rate-limit",
        type=float,
        default=0.3,
        help="Seconds to sleep between pairs (default: 0.3).",
    )
    parser.add_argument(
        "--concurrency",
        type=int,
        default=5,
        help="Number of pairs to judge concurrently (default: 5).",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Resolve paths
    contradictions_path = CONTRADICTIONS_PATH
    output_path = OUTPUT_PATH

    if args.data_dir:
        data_dir = args.data_dir
        if not data_dir.is_absolute():
            data_dir = (REPO_ROOT / data_dir).resolve()
        contradictions_path = data_dir / "statement_contradictions.json"
        output_path = data_dir / "statement_judge_results.json"

    if args.output:
        output_path = args.output

    models = args.models if args.models else JUDGE_MODELS
    resume = not args.no_resume

    # Validate models
    missing = [i + 1 for i, m in enumerate(models) if not m]
    if missing:
        print(f"ERROR: Missing model(s) for judge(s) {missing}.")
        print("Set MULTIMODEL_1/2/3 in .env or use --models.")
        sys.exit(1)
    for m in models:
        print(f"  Judge model: {m}")

    # API key
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("ERROR: OPENROUTER_API_KEY not found in .env or environment.")
        sys.exit(1)

    client = OpenRouterClient(api_key)

    # Load prompt template
    prompt_template = load_judge_prompt()
    print(f"Loaded prompt template: {PROMPT_FILE.name} ({len(prompt_template)} chars)")

    # Load and filter pairs
    print(f"\nLoading contradictions from: {contradictions_path}")
    pairs = load_flagged_pairs(contradictions_path, args.similarity_threshold)

    if args.companies:
        pairs = [p for p in pairs if p["company"] in args.companies]
        print(f"  Filtered to companies {args.companies}: {len(pairs)} pairs")

    if args.max_pairs:
        pairs = pairs[:args.max_pairs]
        print(f"  Limited to {args.max_pairs} pairs")

    if not pairs:
        print("No pairs to judge.")
        return

    # Initialize results structure
    results = {
        "metadata": {
            "methodology": "three_llm_judge_consensus",
            "pipeline_stage": "statement_level_verification",
            "models": models,
            "providers": [m.split("/")[0] for m in models],
            "prompt_file": PROMPT_FILE.name,
            "prompt_hash": hash(prompt_template) % 10**8,
            "similarity_threshold": args.similarity_threshold,
            "input_path": str(contradictions_path),
            "started_at": datetime.now(timezone.utc).isoformat(),
        },
        "annotations": [],
        "agreement_metrics": {},
        "nli_comparison": {},
    }

    # Resume support
    completed_ids = set()
    if resume and output_path.exists():
        with open(output_path) as f:
            existing = json.load(f)
            results["annotations"] = existing.get("annotations", [])
            completed_ids = {a["pair_id"] for a in results["annotations"]}
            print(f"  Resuming: {len(completed_ids)} pairs already completed")

    # Process pairs with concurrency
    remaining = [p for p in pairs if p["pair_id"] not in completed_ids]
    print(f"\n{'=' * 60}")
    print(f"Judging {len(remaining)} pairs with 3 LLM judges (concurrency={args.concurrency})...")
    print(f"{'=' * 60}")

    providers = [m.split("/")[0][:3].upper() for m in models]

    def _short(v):
        if v == "CONTRADICTION":
            return "CONTRA"
        elif v == "NOT_CONTRADICTION":
            return "NOT"
        return "ERR"

    def _judge_one(pair):
        """Judge a single pair (called from thread pool)."""
        return judge_pair_three_models(client, pair, models, prompt_template)

    # Process in batches for clean progress reporting and incremental saves
    batch_size = args.concurrency
    total_remaining = len(remaining)
    batch_num = 0

    for batch_start in range(0, total_remaining, batch_size):
        batch = remaining[batch_start:batch_start + batch_size]
        batch_num += 1

        # Submit batch to thread pool
        with ThreadPoolExecutor(max_workers=batch_size) as executor:
            future_to_pair = {
                executor.submit(_judge_one, pair): pair
                for pair in batch
            }

            for future in as_completed(future_to_pair):
                pair = future_to_pair[future]
                idx = batch_start + batch.index(pair) + 1
                try:
                    result = future.result()
                except Exception as e:
                    print(f"  [{idx}/{total_remaining}] ERROR: {pair['pair_id']}: {e}")
                    continue

                results["annotations"].append(result)

                # Print verdict
                verdicts = [
                    result["judge_1"].get("verdict", "ERR"),
                    result["judge_2"].get("verdict", "ERR"),
                    result["judge_3"].get("verdict", "ERR"),
                ]
                verdict_str = " | ".join(
                    f"{p}:{_short(v)}" for p, v in zip(providers, verdicts)
                )

                if result["consensus_type"] == "unanimous":
                    status = f"UNANIMOUS: {_short(result['final_verdict'])}"
                elif result["consensus_type"] == "majority":
                    status = f"MAJORITY: {_short(result['final_verdict'])}"
                else:
                    status = result["consensus_type"].upper()

                print(f"  [{idx}/{total_remaining}] {pair['pair_id']} "
                      f"sim={pair.get('semantic_similarity', 0):.2f} -> {status}")

        # Incremental save after each batch
        save_results(results, output_path)
        confirmed = sum(1 for a in results["annotations"] if a["final_verdict"] == "CONTRADICTION")
        total_done = len(results["annotations"])
        print(f"  --- Batch {batch_num}: saved {total_done} results, "
              f"{confirmed} confirmed contradictions so far ---")

        # Rate limiting between batches
        if batch_start + batch_size < total_remaining:
            time.sleep(args.rate_limit)

    # Compute final metrics
    print("\nComputing agreement metrics...")
    results["agreement_metrics"] = compute_agreement(results["annotations"], models)
    results["nli_comparison"] = compare_with_nli(results["annotations"])
    results["metadata"]["completed_at"] = datetime.now(timezone.utc).isoformat()
    results["metadata"]["total_pairs_judged"] = len(results["annotations"])

    # Final save
    save_results(results, output_path)
    print(f"\nResults saved to: {output_path}")
    print(f"  File size: {output_path.stat().st_size / 1024:.1f} KB")

    # Print summary
    print_summary(results, models)


if __name__ == "__main__":
    main()
