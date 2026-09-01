"""
3-LLM-Judge Contradiction Detection Experiment

Replaces the NLI-based contradiction detector with a 3-LLM-judge system
(same methodology as the OPPT corpus annotation in annotate_multimodel.py)
and compares results against the NLI pipeline and human assessment.

Architecture:
  - 3 LLMs via OpenRouter (user-configurable at top of script)
  - ThreadPoolExecutor parallel execution per pair
  - Majority-vote consensus
  - Agreement metrics (Fleiss' kappa, pairwise Cohen's kappa)
  - Comparison framework vs NLI pipeline

Input:
  - all_segments.json   (full segment text)
  - contradictions.json (pair definitions with claim_id/practice_id)
  - Both loaded via --data-dir flag

Output:
  - judge_results.json with per-pair verdicts, agreement, and NLI comparison
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
DATA_DIR = REPO_ROOT / "data"
load_dotenv(REPO_ROOT / ".env")

# ===========================================================================
# MODEL CONFIGURATION -- reads MULTIMODEL_1/2/3 from .env at project root.
# Override at runtime with --models flag.
# ===========================================================================
JUDGE_MODELS = [
    os.environ.get("MULTIMODEL_1", ""),
    os.environ.get("MULTIMODEL_2", ""),
    os.environ.get("MULTIMODEL_3", ""),
]
# Strip stray quotes that some .env editors leave behind
JUDGE_MODELS = [m.strip().strip('"').strip("'") for m in JUDGE_MODELS]
# ===========================================================================

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

VALID_VERDICTS = {"CONTRADICTION", "NOT_CONTRADICTION"}
SCRIPT_DIR = Path(__file__).parent
PROMPT_FILE = SCRIPT_DIR / "judge_contradiction_prompt.md"
SEGMENTS_PATH = DATA_DIR / "oppt" / "all_segments.json"
CONTRADICTIONS_PATH = REPO_ROOT / "output" / "contradictions.json"
OUTPUT_PATH = REPO_ROOT / "output" / "judge_results.json"


def load_judge_prompt() -> str:
    """Load the judge prompt from external file."""
    if not PROMPT_FILE.exists():
        raise FileNotFoundError(
            f"Judge prompt file not found: {PROMPT_FILE}\n"
            "Expected file: scripts/judge_contradiction_prompt.md"
        )
    return PROMPT_FILE.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# OpenRouter client (adapted from annotate_multimodel.py)
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
            "X-Title": "Privacy Washing Contradiction Judge",
        }

    def judge(self, prompt: str, model: str, judge_id: str) -> dict:
        """
        Send a contradiction judgment request to OpenRouter.

        Returns:
            dict with verdict, reasoning, raw_response, validity, and metadata.
        """
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 2048,  # Reasoning models need headroom for chain-of-thought
            "temperature": 0,
        }

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

                # Parse JSON from response
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
            return {
                "verdict": None,
                "reasoning": "",

                "raw_response": str(e),
                "valid": False,
                "judge_id": judge_id,
                "model": model,
                "provider": model.split("/")[0] if "/" in model else "unknown",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "error": f"HTTP {e.response.status_code}: {e.response.text}",
            }
        except Exception as e:
            return {
                "verdict": None,
                "reasoning": "",

                "raw_response": str(e),
                "valid": False,
                "judge_id": judge_id,
                "model": model,
                "provider": model.split("/")[0] if "/" in model else "unknown",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "error": str(e),
            }


def _parse_judge_response(raw: str) -> dict:
    """Extract verdict JSON from LLM response, handling markdown fences."""
    text = raw.strip()
    # Strip markdown code fences if present
    if text.startswith("```"):
        lines = text.split("\n")
        # Remove first line (```json or ```) and last line (```)
        lines = [l for l in lines if not l.strip().startswith("```")]
        text = "\n".join(lines).strip()

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        # Try to extract JSON object from surrounding text
        import re
        match = re.search(r'\{[^{}]*"verdict"[^{}]*\}', text, re.DOTALL)
        if match:
            try:
                parsed = json.loads(match.group())
            except json.JSONDecodeError:
                return {"verdict": None}
        else:
            return {"verdict": None}

    # Normalize verdict to uppercase
    verdict = parsed.get("verdict", "")
    if isinstance(verdict, str):
        verdict = verdict.strip().upper()
    parsed["verdict"] = verdict if verdict in VALID_VERDICTS else None

    return parsed


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------
def load_pairs_with_full_text(segments_path: Path, contradictions_path: Path) -> list[dict]:
    """
    Join contradictions.json pairs with all_segments.json full text.

    Returns list of pair dicts augmented with claim_text and practice_text.
    """
    with open(segments_path) as f:
        segments_data = json.load(f)

    # Build lookup: segment_id -> full text
    seg_lookup = {}
    for seg in segments_data["segments"]:
        seg_lookup[seg["segment_id"]] = seg["text"]

    with open(contradictions_path) as f:
        contradictions_data = json.load(f)

    pairs = contradictions_data["pairs"]

    # Augment each pair with full text
    enriched = []
    missing = 0
    for pair in pairs:
        claim_text = seg_lookup.get(pair["claim_id"])
        practice_text = seg_lookup.get(pair["practice_id"])
        if claim_text is None or practice_text is None:
            missing += 1
            continue
        enriched.append({
            **pair,
            "claim_text": claim_text,
            "practice_text": practice_text,
        })

    if missing:
        print(f"Warning: {missing} pairs skipped (segment text not found)")

    print(f"Loaded {len(enriched)} pairs with full text")
    print(f"  NLI-flagged contradictions: {sum(1 for p in enriched if p.get('is_contradiction'))}")
    print(f"  Non-contradictions: {sum(1 for p in enriched if not p.get('is_contradiction'))}")

    return enriched


# ---------------------------------------------------------------------------
# Prompt construction
# ---------------------------------------------------------------------------
def build_prompt(company: str, claim_text: str, practice_text: str, template: str) -> str:
    """Insert pair data into the judge prompt template."""
    return template.format(
        company=company,
        claim_text=claim_text,
        practice_text=practice_text,
    )


# ---------------------------------------------------------------------------
# Judging
# ---------------------------------------------------------------------------
def judge_pair(client: OpenRouterClient, pair: dict, model: str, judge_id: str, template: str) -> dict:
    """Single API call: judge one pair with one model."""
    prompt = build_prompt(pair["company"], pair["claim_text"], pair["practice_text"], template)
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

    pair_id = f"{pair['claim_id']}_vs_{pair['practice_id']}"

    return {
        "pair_id": pair_id,
        "company": pair["company"],
        "claim_id": pair["claim_id"],
        "practice_id": pair["practice_id"],
        "nli_is_contradiction": pair.get("is_contradiction", False),
        "nli_contradiction_score": pair.get("nli_contradiction", 0.0),
        "nli_severity": pair.get("severity", 0.0),
        "nli_evidence_type": pair.get("evidence_type", "none"),
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
    """
    Compute Fleiss' kappa for inter-rater agreement.

    Args:
        judgments: list of items, each item is a list of rater labels
        categories: list of possible category labels

    Returns:
        Fleiss' kappa value
    """
    n = len(judgments)  # number of items
    if n == 0:
        return 0.0
    N = len(judgments[0])  # number of raters
    k = len(categories)

    cat_idx = {c: i for i, c in enumerate(categories)}

    # Build n x k matrix of category counts per item
    counts = []
    for item_labels in judgments:
        row = [0] * k
        for label in item_labels:
            if label in cat_idx:
                row[cat_idx[label]] += 1
        counts.append(row)

    # P_i for each item
    P_items = []
    for row in counts:
        sum_sq = sum(c * c for c in row)
        P_i = (sum_sq - N) / (N * (N - 1)) if N > 1 else 0.0
        P_items.append(P_i)

    P_bar = sum(P_items) / n if n > 0 else 0.0

    # P_e: proportion of all assignments per category
    total_assignments = n * N
    P_e = 0.0
    for j in range(k):
        col_sum = sum(counts[i][j] for i in range(n))
        p_j = col_sum / total_assignments if total_assignments > 0 else 0.0
        P_e += p_j * p_j

    if abs(1.0 - P_e) < 1e-10:
        return 1.0 if abs(P_bar - P_e) < 1e-10 else 0.0

    kappa = (P_bar - P_e) / (1.0 - P_e)
    return kappa


def compute_cohens_kappa(labels_a: list[str], labels_b: list[str], categories: list[str]) -> float:
    """
    Compute Cohen's kappa between two raters.

    Args:
        labels_a: list of labels from rater A
        labels_b: list of labels from rater B
        categories: possible labels

    Returns:
        Cohen's kappa value
    """
    n = len(labels_a)
    if n == 0:
        return 0.0

    cat_idx = {c: i for i, c in enumerate(categories)}
    k = len(categories)

    # Confusion matrix
    matrix = [[0] * k for _ in range(k)]
    for la, lb in zip(labels_a, labels_b):
        if la in cat_idx and lb in cat_idx:
            matrix[cat_idx[la]][cat_idx[lb]] += 1

    # Observed agreement
    P_o = sum(matrix[i][i] for i in range(k)) / n

    # Expected agreement
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

    # Collect per-item label lists (only items where all 3 are valid)
    all_valid_labels = []  # each entry: [j1_label, j2_label, j3_label]
    per_judge = {jid: [] for jid in judge_ids}

    for ann in annotations:
        if all(ann[jid]["valid"] for jid in judge_ids):
            item_labels = [ann[jid]["verdict"] for jid in judge_ids]
            all_valid_labels.append(item_labels)
            for idx, jid in enumerate(judge_ids):
                per_judge[jid].append(item_labels[idx])

    n_valid = len(all_valid_labels)

    # Fleiss' kappa
    fleiss_k = compute_fleiss_kappa(all_valid_labels, categories) if n_valid > 0 else None

    # Pairwise Cohen's kappa
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

    # Consensus counts
    consensus_counts = Counter(ann["consensus_type"] for ann in annotations)
    total = len(annotations)

    # Pairwise raw agreement rates
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
    Build confusion matrix: judge consensus vs NLI is_contradiction.

    Also computes precision/recall for each method assuming
    judge consensus as one view and NLI as another.
    """
    # 2x2: (judge_says_contradiction, nli_says_contradiction)
    matrix = {"TP": 0, "FP": 0, "FN": 0, "TN": 0}
    # TP = both say contradiction
    # FP = judge says contradiction, NLI says not
    # FN = judge says not contradiction, NLI says contradiction
    # TN = both say not contradiction

    judge_flagged = []
    nli_flagged = []
    judge_only = []
    nli_only = []
    both_flagged = []

    for ann in annotations:
        judge_contra = ann["final_verdict"] == "CONTRADICTION"
        nli_contra = ann["nli_is_contradiction"]

        if judge_contra and nli_contra:
            matrix["TP"] += 1
            both_flagged.append(ann["pair_id"])
        elif judge_contra and not nli_contra:
            matrix["FP"] += 1
            judge_only.append(ann["pair_id"])
        elif not judge_contra and nli_contra:
            matrix["FN"] += 1
            nli_only.append(ann["pair_id"])
        else:
            matrix["TN"] += 1

        if judge_contra:
            judge_flagged.append(ann["pair_id"])
        if nli_contra:
            nli_flagged.append(ann["pair_id"])

    total = sum(matrix.values())

    # Agreement between the two methods
    agreement = (matrix["TP"] + matrix["TN"]) / total if total > 0 else 0.0

    return {
        "confusion_matrix": {
            "description": "Rows=Judge, Cols=NLI. TP=both contradiction, TN=both not.",
            **matrix,
        },
        "agreement_rate": round(agreement, 4),
        "judge_total_flagged": len(judge_flagged),
        "nli_total_flagged": len(nli_flagged),
        "both_flagged": len(both_flagged),
        "judge_only_flagged": len(judge_only),
        "nli_only_flagged": len(nli_only),
        "judge_only_pairs": judge_only,
        "nli_only_pairs": nli_only,
        "summary": (
            f"Judge flagged {len(judge_flagged)} contradictions, "
            f"NLI flagged {len(nli_flagged)}. "
            f"Overlap: {len(both_flagged)}. "
            f"Judge-only: {len(judge_only)}. "
            f"NLI-only: {len(nli_only)}."
        ),
    }


# ---------------------------------------------------------------------------
# Saving and printing
# ---------------------------------------------------------------------------
def save_results(results: dict, output_path: Path):
    """Save results to JSON with incremental support."""
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)


def print_summary(results: dict, models: list[str]):
    """Print summary statistics to console."""
    agreement = results.get("agreement_metrics", {})
    comparison = results.get("nli_comparison", {})

    print("\n" + "=" * 60)
    print("3-LLM JUDGE CONTRADICTION EXPERIMENT COMPLETE")
    print("=" * 60)

    print(f"\nModels used:")
    for i, model in enumerate(models, 1):
        provider = model.split("/")[0]
        print(f"  Judge {i}: {model} ({provider})")

    print(f"\nAgreement Metrics:")
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

    print(f"\nPairwise Raw Agreement:")
    for pair_key, vals in agreement.get("pairwise_agreement_rates", {}).items():
        print(f"  {pair_key}: {vals.get('rate', 0):.1%}")

    print(f"\nNLI Comparison:")
    cm = comparison.get("confusion_matrix", {})
    print(f"  Both flagged:     {comparison.get('both_flagged', 0)}")
    print(f"  Judge-only:       {comparison.get('judge_only_flagged', 0)}")
    print(f"  NLI-only:         {comparison.get('nli_only_flagged', 0)}")
    print(f"  Neither flagged:  {cm.get('TN', 0)}")
    print(f"  Method agreement: {comparison.get('agreement_rate', 0):.1%}")

    # Verdict distribution
    annotations = results.get("annotations", [])
    verdict_dist = Counter(
        ann["final_verdict"] for ann in annotations if ann["final_verdict"]
    )
    print(f"\nJudge Verdict Distribution:")
    for v, c in verdict_dist.most_common():
        print(f"  {v}: {c}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="3-LLM-Judge Contradiction Detection Experiment"
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=None,
        help="Directory containing all_segments.json and contradictions.json. "
             "Default: OPPT corpus paths.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output path for judge_results.json. Default: same dir as contradictions.",
    )
    parser.add_argument(
        "--models",
        nargs=3,
        default=None,
        help="Three OpenRouter model IDs to use as judges.",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        default=True,
        help="Resume from existing output file (default: True).",
    )
    parser.add_argument(
        "--no-resume",
        action="store_true",
        help="Start fresh, ignoring existing output.",
    )
    parser.add_argument(
        "--only-flagged",
        action="store_true",
        help="Only judge NLI-flagged pairs (is_contradiction=True).",
    )
    parser.add_argument(
        "--companies",
        nargs="+",
        default=None,
        help="Only judge pairs from these companies (e.g., --companies tesla venmo).",
    )
    parser.add_argument(
        "--rate-limit",
        type=float,
        default=1.0,
        help="Seconds to sleep between pairs (default: 1.0).",
    )
    args = parser.parse_args()

    # Resolve paths
    segments_path = SEGMENTS_PATH
    contradictions_path = CONTRADICTIONS_PATH
    output_path = OUTPUT_PATH

    if args.data_dir:
        segments_path = args.data_dir / "all_segments.json"
        contradictions_path = args.data_dir / "contradictions.json"
        output_path = args.data_dir / "judge_results.json"

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

    # API key (loaded from .env by dotenv)
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("ERROR: OPENROUTER_API_KEY not found in .env or environment.")
        sys.exit(1)

    client = OpenRouterClient(api_key)

    # Load prompt template
    prompt_template = load_judge_prompt()
    print(f"Loaded prompt template: {PROMPT_FILE.name} ({len(prompt_template)} chars)")

    # Load data
    print(f"Loading segments from: {segments_path}")
    print(f"Loading contradictions from: {contradictions_path}")
    pairs = load_pairs_with_full_text(segments_path, contradictions_path)

    if args.companies:
        pairs = [p for p in pairs if p["company"] in args.companies]
        print(f"Filtering to companies {args.companies}: {len(pairs)} pairs")

    if args.only_flagged:
        pairs = [p for p in pairs if p.get("is_contradiction")]
        print(f"Filtering to NLI-flagged pairs only: {len(pairs)} pairs")

    # Initialize results structure
    results = {
        "metadata": {
            "methodology": "three_llm_judge_consensus",
            "models": models,
            "providers": [m.split("/")[0] for m in models],
            "prompt_file": PROMPT_FILE.name,
            "prompt_hash": hash(prompt_template) % 10**8,
            "started_at": datetime.now(timezone.utc).isoformat(),
            "segments_path": str(segments_path),
            "contradictions_path": str(contradictions_path),
            "only_flagged": args.only_flagged,
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
            print(f"Resuming: {len(completed_ids)} pairs already completed")

    # Process each pair
    total = len(pairs)
    providers = [m.split("/")[0][:3].upper() for m in models]

    for i, pair in enumerate(pairs):
        pair_id = f"{pair['claim_id']}_vs_{pair['practice_id']}"

        if pair_id in completed_ids:
            continue

        print(f"[{i + 1}/{total}] Judging {pair_id} ({pair['company']})...")

        result = judge_pair_three_models(client, pair, models, prompt_template)
        results["annotations"].append(result)

        # Print progress
        verdicts = [
            result["judge_1"].get("verdict", "ERR"),
            result["judge_2"].get("verdict", "ERR"),
            result["judge_3"].get("verdict", "ERR"),
        ]
        # Abbreviate verdict for display
        def _short(v):
            if v == "CONTRADICTION":
                return "CONTRA"
            elif v == "NOT_CONTRADICTION":
                return "NOT"
            return "ERR"

        verdict_str = " | ".join(
            f"{p}:{_short(v)}" for p, v in zip(providers, verdicts)
        )

        nli_flag = "NLI:Y" if pair.get("is_contradiction") else "NLI:N"

        if result["consensus_type"] == "unanimous":
            status = f"UNANIMOUS: {_short(result['final_verdict'])}"
        elif result["consensus_type"] == "majority":
            status = f"MAJORITY: {_short(result['final_verdict'])}"
        else:
            status = result["consensus_type"].upper()

        print(f"    [{verdict_str}] -> {status} ({nli_flag})")

        # Incremental save every 5 pairs
        if (len(results["annotations"])) % 5 == 0:
            save_results(results, output_path)
            print(f"    (saved {len(results['annotations'])} results)")

        # Rate limiting
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

    # Print summary
    print_summary(results, models)


if __name__ == "__main__":
    main()
