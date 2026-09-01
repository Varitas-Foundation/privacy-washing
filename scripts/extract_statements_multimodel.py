"""
3-LLM Panel Statement Extraction (High-Performance Parallel Version)

Extracts atomic statements using 3 independent LLMs with consensus merging.
This enhances scientific rigor by reducing single-model extraction bias.

Architecture:
  - 3 LLMs via OpenRouter (configured via MULTIMODEL_1/2/3 in .env)
  - High parallelism: up to 50 concurrent API requests
  - Async queue with backoff for rate limiting
  - Statement matching using semantic similarity
  - Majority-vote consensus for metadata fields (subject, aspect, scope)
  - Agreement metrics tracking

Consensus Strategy:
  - Include statement if extracted by 2+ models (majority threshold)
  - Metadata fields (subject, aspect, scope) determined by majority vote
  - Qualifiers merged from all agreeing models
  - Track per-statement agreement statistics

Input:
  - all_segments.json (segment text + categories)
  - oppt_v2_attribute_review.json (OPPT only — fine-grained annotations)

Output:
  - statements.json (with agreement statistics per statement)

Usage:
  # OPP-115 corpus with 3-LLM panel (50 concurrent requests)
  python extract_statements_multimodel.py --data-dir opp115_experiment_annotation_guided_20260203 --concurrency 50

  # OPPT corpus with 3-LLM panel
  python extract_statements_multimodel.py --output oppt_experiment_enhanced_20260131/statements.json --concurrency 50
"""

import asyncio
import json
import os
import re
import sys
import time
import argparse
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import httpx
import numpy as np
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Paths & environment
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data"
load_dotenv(REPO_ROOT / ".env")

# Default OPPT input paths; override with OPPT_SEGMENTS_PATH /
# OPPT_ATTRIBUTE_REVIEW_PATH env vars if needed.
SEGMENTS_PATH = Path(os.environ.get(
    "OPPT_SEGMENTS_PATH",
    DATA_DIR / "oppt" / "all_segments.json",
))
ATTRIBUTE_REVIEW_PATH = Path(os.environ.get(
    "OPPT_ATTRIBUTE_REVIEW_PATH",
    DATA_DIR / "oppt" / "oppt_v2_attribute_review.json",
))
OUTPUT_PATH = REPO_ROOT / "output" / "statements.json"

SCRIPT_DIR = Path(__file__).parent
PROMPT_FILE_V2 = SCRIPT_DIR / "statement_extraction_prompt_v2.md"

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Load models from environment.
# EXTRACTION_MODEL_1/2/3 take precedence so the extraction panel can be
# configured independently of the judge panel (see judge_statement_contradictions.py,
# which reads JUDGE_MODEL_1/2/3). Falls back to the legacy shared MULTIMODEL_1/2/3
# variables, then to hardcoded defaults, so existing setups keep working.
EXTRACTION_MODELS = [
    os.environ.get("EXTRACTION_MODEL_1", os.environ.get("MULTIMODEL_1", "anthropic/claude-haiku-4.5")),
    os.environ.get("EXTRACTION_MODEL_2", os.environ.get("MULTIMODEL_2", "openai/gpt-4o-mini")),
    os.environ.get("EXTRACTION_MODEL_3", os.environ.get("MULTIMODEL_3", "google/gemini-2.0-flash-001")),
]
# Clean up any quotes in model names
EXTRACTION_MODELS = [m.strip().strip('"').strip("'") for m in EXTRACTION_MODELS if m.strip()]

# Categories that don't produce actionable statements
EXCLUDED_CATEGORIES = {"OTHER", "POLICY_CHANGE", "REGIONAL"}

# Valid values for enhanced schema fields
VALID_SUBJECTS = {"COMPANY", "SERVICE_PROVIDER", "THIRD_PARTY", "AFFILIATES", "USER"}
VALID_ASPECTS = {
    "COLLECTION", "USE", "SHARING", "SALE", "RETENTION",
    "DELETION", "ACCESS_CONTROL", "SECURITY"
}
VALID_SCOPES = {
    "UNIVERSAL", "CONDITIONAL", "CONSENT_BASED",
    "LEGAL_REQUIREMENT", "GEOGRAPHIC_LIMITED"
}

# Similarity threshold for matching statements across models
STATEMENT_MATCH_THRESHOLD = 0.7

# Minimum models that must agree to include a statement
MIN_MODEL_AGREEMENT = 2


# ---------------------------------------------------------------------------
# Async OpenRouter client with queue management
# ---------------------------------------------------------------------------
class AsyncOpenRouterClient:
    """Async client for OpenRouter API with high parallelism and queue management."""

    def __init__(self, api_key: str, timeout: float = 90.0, max_concurrent: int = 50):
        self.api_key = api_key
        self.timeout = timeout
        self.base_url = OPENROUTER_BASE_URL
        self.max_concurrent = max_concurrent
        self.semaphore = None  # Created in async context
        self._client = None

    def _get_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/dark-patterns-research",
            "X-Title": "Privacy Washing Multi-Model Extraction",
        }

    async def _get_client(self):
        """Get or create async HTTP client."""
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=self.timeout)
        return self._client

    async def close(self):
        """Close the HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None

    async def extract(self, prompt: str, model: str, max_retries: int = 5) -> dict:
        """Send extraction request with retry and backoff for rate limits."""
        if self.semaphore is None:
            self.semaphore = asyncio.Semaphore(self.max_concurrent)

        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 2048,
            "temperature": 0,
        }

        last_error = None

        async with self.semaphore:
            for attempt in range(max_retries):
                try:
                    client = await self._get_client()
                    response = await client.post(
                        f"{self.base_url}/chat/completions",
                        headers=self._get_headers(),
                        json=payload,
                    )
                    response.raise_for_status()

                    data = response.json()
                    raw = (data["choices"][0]["message"].get("content") or "").strip()
                    usage = data.get("usage", {})

                    parsed = _parse_extraction_response(raw)

                    return {
                        "raw_response": raw,
                        "statements": parsed.get("statements", []),
                        "valid": parsed.get("valid", False),
                        "usage": usage,
                        "error": None,
                    }

                except httpx.HTTPStatusError as e:
                    last_error = f"HTTP {e.response.status_code}: {e.response.text[:200]}"
                    if e.response.status_code == 429:
                        # Rate limited - exponential backoff with jitter
                        wait = (2 ** attempt) * 2 + np.random.uniform(0, 1)
                        await asyncio.sleep(wait)
                        continue
                    elif e.response.status_code >= 500:
                        # Server error - retry with backoff
                        wait = (2 ** attempt) + np.random.uniform(0, 1)
                        await asyncio.sleep(wait)
                        continue
                    break
                except (httpx.ConnectError, httpx.ReadTimeout) as e:
                    last_error = str(e)
                    wait = (2 ** attempt) + np.random.uniform(0, 1)
                    await asyncio.sleep(wait)
                    continue
                except Exception as e:
                    last_error = str(e)
                    if attempt < max_retries - 1:
                        await asyncio.sleep(2 ** attempt)
                        continue
                    break

        return {
            "raw_response": "",
            "statements": [],
            "valid": False,
            "usage": {},
            "error": last_error,
        }


def _parse_extraction_response(raw: str) -> dict:
    """Extract statements JSON from LLM response, handling markdown fences."""
    text = raw.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        text = "\n".join(lines).strip()

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r'\{[^{}]*"statements"\s*:\s*\[.*?\]\s*\}', text, re.DOTALL)
        if match:
            try:
                parsed = json.loads(match.group())
            except json.JSONDecodeError:
                return {"statements": [], "valid": False}
        else:
            return {"statements": [], "valid": False}

    statements = parsed.get("statements", [])
    valid_statements = []
    for s in statements:
        if isinstance(s, dict) and "text" in s and "type" in s:
            s_type = s["type"].upper() if isinstance(s["type"], str) else ""
            if s_type in ("COMMITMENT", "PRACTICE"):
                s["type"] = s_type
                s["category"] = (s.get("category") or "").upper().replace(" ", "_")

                # Normalize v2 fields
                subject_raw = (s.get("subject") or "").upper().replace(" ", "_")
                s["subject"] = subject_raw if subject_raw in VALID_SUBJECTS else "COMPANY"

                aspect_raw = (s.get("aspect") or "").upper().replace(" ", "_")
                s["aspect"] = aspect_raw if aspect_raw in VALID_ASPECTS else "USE"

                scope_raw = (s.get("scope") or "").upper().replace(" ", "_")
                s["scope"] = scope_raw if scope_raw in VALID_SCOPES else "UNIVERSAL"

                qualifiers = s.get("qualifiers", [])
                s["qualifiers"] = [q for q in qualifiers if isinstance(q, str) and q.strip()] if isinstance(qualifiers, list) else []

                valid_statements.append(s)

    return {"statements": valid_statements, "valid": len(valid_statements) > 0 or len(statements) == 0}


# ---------------------------------------------------------------------------
# Semantic similarity for statement matching
# ---------------------------------------------------------------------------
_similarity_model = None

def get_similarity_model():
    """Lazy-load sentence transformer model."""
    global _similarity_model
    if _similarity_model is None:
        from sentence_transformers import SentenceTransformer
        import torch
        if torch.backends.mps.is_available():
            device = "mps"
        elif torch.cuda.is_available():
            device = "cuda"
        else:
            device = "cpu"
        _similarity_model = SentenceTransformer("all-MiniLM-L6-v2", device=device)
    return _similarity_model


def compute_text_similarity(text1: str, text2: str) -> float:
    """Compute cosine similarity between two texts."""
    model = get_similarity_model()
    embeddings = model.encode([text1, text2])
    similarity = np.dot(embeddings[0], embeddings[1]) / (
        np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1])
    )
    return float(similarity)


def match_statements_across_models(model_results: dict[str, list[dict]]) -> list[dict]:
    """Match statements across models and compute consensus.

    Args:
        model_results: Dict mapping model name to list of extracted statements

    Returns:
        List of merged statements with agreement statistics
    """
    if not model_results:
        return []

    models = list(model_results.keys())
    all_statements = []

    # Collect all statements with their source model
    for model, statements in model_results.items():
        for stmt in statements:
            stmt["_source_model"] = model
            all_statements.append(stmt)

    if not all_statements:
        return []

    # Group statements by similarity
    # Use greedy clustering: assign each statement to most similar existing cluster
    # or create new cluster if no match above threshold

    clusters = []  # List of lists of similar statements

    for stmt in all_statements:
        best_cluster_idx = -1
        best_similarity = 0

        for idx, cluster in enumerate(clusters):
            # Compare to cluster representative (first statement)
            sim = compute_text_similarity(stmt["text"], cluster[0]["text"])
            if sim > best_similarity:
                best_similarity = sim
                best_cluster_idx = idx

        if best_similarity >= STATEMENT_MATCH_THRESHOLD:
            clusters[best_cluster_idx].append(stmt)
        else:
            clusters.append([stmt])

    # Merge clusters into consensus statements
    merged_statements = []

    for cluster in clusters:
        # Count unique models in cluster
        cluster_models = set(s["_source_model"] for s in cluster)
        agreement_count = len(cluster_models)

        # Only include if meets minimum agreement threshold
        if agreement_count < MIN_MODEL_AGREEMENT:
            continue

        # Use majority vote for metadata fields
        types = [s["type"] for s in cluster]
        subjects = [s["subject"] for s in cluster]
        aspects = [s["aspect"] for s in cluster]
        scopes = [s["scope"] for s in cluster]
        categories = [s["category"] for s in cluster]

        # Merge qualifiers from all agreeing models
        all_qualifiers = []
        for s in cluster:
            all_qualifiers.extend(s.get("qualifiers", []))
        unique_qualifiers = list(dict.fromkeys(all_qualifiers))  # Preserve order, remove dupes

        # Select representative text (from most common type)
        type_majority = Counter(types).most_common(1)[0][0]
        representative = next(s for s in cluster if s["type"] == type_majority)

        merged = {
            "text": representative["text"],
            "type": type_majority,
            "subject": Counter(subjects).most_common(1)[0][0],
            "aspect": Counter(aspects).most_common(1)[0][0],
            "scope": Counter(scopes).most_common(1)[0][0],
            "qualifiers": unique_qualifiers,
            "category": Counter(categories).most_common(1)[0][0],
            # Agreement metadata
            "_agreement": {
                "model_count": agreement_count,
                "models": sorted(cluster_models),
                "unanimous": agreement_count == len(models),
                "type_agreement": len(set(types)) == 1,
                "subject_agreement": len(set(subjects)) == 1,
                "aspect_agreement": len(set(aspects)) == 1,
                "scope_agreement": len(set(scopes)) == 1,
            }
        }
        merged_statements.append(merged)

    return merged_statements


# ---------------------------------------------------------------------------
# Annotation block construction (OPPT only)
# ---------------------------------------------------------------------------
def build_annotation_block(segment_id: str, attr_lookup: dict) -> str:
    """Consolidate 3 annotators' attributes into a summary annotation block."""
    seg_data = attr_lookup.get(segment_id)
    if not seg_data:
        return ""

    annotators = seg_data.get("attributes_by_annotator", {})
    if not annotators:
        return ""

    category_info = {}
    for ann_id, ann_cats in annotators.items():
        for cat, attrs in ann_cats.items():
            if cat in EXCLUDED_CATEGORIES or cat == "OTHER":
                continue

            if cat not in category_info:
                category_info[cat] = {
                    "does_does_not_votes": [],
                    "actions": set(),
                    "data_types": set(),
                    "purposes": set(),
                }

            info = category_info[cat]
            ddn = attrs.get("does_does_not", "")
            if ddn:
                info["does_does_not_votes"].append(ddn)

            def _as_list(val):
                if val is None:
                    return []
                if isinstance(val, str):
                    return [val] if val else []
                return list(val)

            for a in _as_list(attrs.get("action")):
                if a and a != "Unspecified":
                    info["actions"].add(a)

            for t in _as_list(attrs.get("personal_information_type")):
                if t and t != "Unspecified":
                    info["data_types"].add(t)

            for p in _as_list(attrs.get("purpose")):
                if p and p != "Unspecified":
                    info["purposes"].add(p)

    if not category_info:
        return ""

    lines = ["ANNOTATIONS (from expert review):"]
    for cat, info in sorted(category_info.items()):
        votes = info["does_does_not_votes"]
        if votes:
            counter = Counter(votes)
            ddn = counter.most_common(1)[0][0]
        else:
            ddn = "Unspecified"

        parts = [f"{cat}: {ddn}"]

        if info["actions"]:
            parts.append(f"Action: {', '.join(sorted(info['actions']))}")
        if info["data_types"]:
            parts.append(f"Data types: {', '.join(sorted(info['data_types']))}")
        if info["purposes"]:
            parts.append(f"Purpose: {', '.join(sorted(info['purposes']))}")

        lines.append(f"- {' | '.join(parts)}")

    lines.append("")
    lines.append('Use these annotations to guide your extraction. "Does" annotations indicate PRACTICE statements;')
    lines.append('"Does Not" annotations indicate COMMITMENT statements.')

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Async multi-model extraction for a single segment
# ---------------------------------------------------------------------------
async def extract_segment_multimodel_async(
    client: AsyncOpenRouterClient,
    segment: dict,
    prompt_template: str,
    models: list[str],
    annotation_block: str = "",
) -> dict:
    """Extract statements from a segment using multiple models concurrently.

    Returns dict with model_results, merged_statements, and statistics.
    """
    seg_id = segment["segment_id"]
    company = segment["company"]
    category = segment.get("primary_category", "UNKNOWN")

    # Build prompt
    prompt = prompt_template.format(
        segment_text=segment["text"],
        company=company,
        category=category,
        annotation_block=annotation_block,
    )

    # Extract with all models concurrently
    async def extract_with_model(model):
        result = await client.extract(prompt, model)
        return model, result

    tasks = [extract_with_model(model) for model in models]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    model_results = {}
    model_usage = {}
    model_errors = {}

    for item in results:
        if isinstance(item, Exception):
            # Handle unexpected exceptions
            continue
        model, result = item
        if result["error"]:
            model_errors[model] = result["error"]
            model_results[model] = []
        else:
            model_results[model] = result["statements"]
            model_usage[model] = result.get("usage", {})

    # Match and merge statements across models
    merged_statements = match_statements_across_models(model_results)

    # Compute agreement statistics
    total_by_model = {m: len(stmts) for m, stmts in model_results.items()}
    unanimous = sum(1 for s in merged_statements if s["_agreement"]["unanimous"])
    majority = len(merged_statements) - unanimous

    return {
        "segment_id": seg_id,
        "model_results": model_results,
        "merged_statements": merged_statements,
        "model_usage": model_usage,
        "model_errors": model_errors,
        "statistics": {
            "statements_by_model": total_by_model,
            "merged_count": len(merged_statements),
            "unanimous_count": unanimous,
            "majority_count": majority,
        }
    }


# ---------------------------------------------------------------------------
# Main pipeline (async with high parallelism)
# ---------------------------------------------------------------------------
def parse_args():
    parser = argparse.ArgumentParser(description="Extract statements using 3-LLM panel with consensus (parallel)")
    parser.add_argument("--data-dir", type=str, default=None,
                        help="Override data directory (e.g., for OPP-115 experiment)")
    parser.add_argument("--companies", type=str, default=None,
                        help="Comma-separated list of companies to process (default: all)")
    parser.add_argument("--output", type=str, default=None,
                        help="Override output file path")
    parser.add_argument("--min-agreement", type=int, default=MIN_MODEL_AGREEMENT,
                        help=f"Minimum models that must agree (default: {MIN_MODEL_AGREEMENT})")
    parser.add_argument("--concurrency", type=int, default=50,
                        help="Max concurrent API requests (default: 50)")
    parser.add_argument("--batch-size", type=int, default=20,
                        help="Segments to process per batch for progress reporting (default: 20)")
    return parser.parse_args()


async def process_segments_parallel(
    client: AsyncOpenRouterClient,
    segments: list[dict],
    prompt_template: str,
    models: list[str],
    attr_lookup: dict,
    has_annotations: bool,
    batch_size: int = 20,
) -> tuple[list[dict], dict, int, int, dict]:
    """Process all segments in parallel with progress reporting.

    Returns: (all_statements, agreement_stats, errors, empty_segments, total_usage)
    """
    all_statements = []
    errors = 0
    empty_segments = 0
    total_usage = {model: {"prompt_tokens": 0, "completion_tokens": 0} for model in models}

    agreement_stats = {
        "unanimous": 0,
        "majority": 0,
        "by_field": {
            "type": {"agree": 0, "disagree": 0},
            "subject": {"agree": 0, "disagree": 0},
            "aspect": {"agree": 0, "disagree": 0},
            "scope": {"agree": 0, "disagree": 0},
        }
    }

    start_time = time.time()
    total_segments = len(segments)

    # Process in batches for progress reporting
    for batch_start in range(0, total_segments, batch_size):
        batch_end = min(batch_start + batch_size, total_segments)
        batch = segments[batch_start:batch_end]

        # Create tasks for all segments in batch
        async def process_segment(seg):
            seg_id = seg["segment_id"]
            annotation_block = ""
            if has_annotations:
                annotation_block = build_annotation_block(seg_id, attr_lookup)

            result = await extract_segment_multimodel_async(
                client, seg, prompt_template, models,
                annotation_block=annotation_block,
            )
            return seg, result

        tasks = [process_segment(seg) for seg in batch]
        batch_results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results
        for item in batch_results:
            if isinstance(item, Exception):
                errors += 1
                print(f"  ERROR: {item}")
                continue

            seg, result = item
            seg_id = seg["segment_id"]
            company = seg["company"]
            category = seg.get("primary_category", "UNKNOWN")
            annotation_block = build_annotation_block(seg_id, attr_lookup) if has_annotations else ""

            # Track errors
            if result["model_errors"]:
                errors += len(result["model_errors"])

            # Track usage
            for model, usage in result["model_usage"].items():
                total_usage[model]["prompt_tokens"] += usage.get("prompt_tokens", 0)
                total_usage[model]["completion_tokens"] += usage.get("completion_tokens", 0)

            # Collect merged statements
            merged = result["merged_statements"]
            if not merged:
                empty_segments += 1

            for s_idx, stmt in enumerate(merged):
                annotation_source = "does_does_not" if has_annotations and annotation_block else "llm_inferred"

                # Track agreement stats
                agreement = stmt["_agreement"]
                if agreement["unanimous"]:
                    agreement_stats["unanimous"] += 1
                else:
                    agreement_stats["majority"] += 1

                for field in ["type", "subject", "aspect", "scope"]:
                    if agreement.get(f"{field}_agreement", False):
                        agreement_stats["by_field"][field]["agree"] += 1
                    else:
                        agreement_stats["by_field"][field]["disagree"] += 1

                all_statements.append({
                    "statement_id": f"{seg_id}_s{s_idx + 1}",
                    "source_segment_id": seg_id,
                    "company": company,
                    "text": stmt["text"],
                    "type": stmt["type"],
                    "subject": stmt["subject"],
                    "aspect": stmt["aspect"],
                    "scope": stmt["scope"],
                    "qualifiers": stmt["qualifiers"],
                    "category": stmt.get("category", category),
                    "annotation_source": annotation_source,
                    "extraction_agreement": {
                        "model_count": agreement["model_count"],
                        "models": agreement["models"],
                        "unanimous": agreement["unanimous"],
                    },
                })

        # Progress report
        elapsed = time.time() - start_time
        rate = batch_end / elapsed if elapsed > 0 else 0
        eta = (total_segments - batch_end) / rate if rate > 0 else 0
        print(f"  {batch_end}/{total_segments} segments — {len(all_statements)} statements "
              f"({rate:.1f} seg/s, ETA {eta/60:.1f}m)")

    return all_statements, agreement_stats, errors, empty_segments, total_usage


async def main_async():
    args = parse_args()

    global MIN_MODEL_AGREEMENT
    MIN_MODEL_AGREEMENT = args.min_agreement

    # Resolve paths
    segments_path = SEGMENTS_PATH
    output_path = OUTPUT_PATH
    is_oppt = True

    if args.data_dir:
        data_dir = Path(args.data_dir)
        if not data_dir.is_absolute():
            data_dir = (REPO_ROOT / data_dir).resolve()
        segments_path = data_dir / "all_segments.json"
        output_path = data_dir / "statements.json"
        is_oppt = False  # Not OPPT corpus, but may still have annotations (OPP-115)

    if args.output:
        output_path = Path(args.output)
        if not output_path.is_absolute():
            output_path = (REPO_ROOT / args.output).resolve()

    # Load API key
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("ERROR: OPENROUTER_API_KEY not found in .env or environment.")
        sys.exit(1)

    # Load prompt template
    if not PROMPT_FILE_V2.exists():
        print(f"ERROR: Prompt file not found: {PROMPT_FILE_V2}")
        sys.exit(1)
    prompt_template = PROMPT_FILE_V2.read_text(encoding="utf-8")

    # Validate models
    print(f"Using 3-LLM extraction panel (parallel, {args.concurrency} concurrent requests):")
    for i, model in enumerate(EXTRACTION_MODELS, 1):
        print(f"  Model {i}: {model}")
    print(f"  Minimum agreement: {MIN_MODEL_AGREEMENT}/{len(EXTRACTION_MODELS)}")
    print()

    # Load segments
    print(f"Loading segments from {segments_path}")
    with open(segments_path) as f:
        seg_data = json.load(f)
    segments = seg_data["segments"]
    print(f"  {len(segments)} total segments")

    # Load attribute review (OPPT or OPP-115 with extracted attributes)
    attr_lookup = {}
    has_annotations = False

    if is_oppt and ATTRIBUTE_REVIEW_PATH.exists():
        # OPPT corpus with LLM-generated attributes
        print(f"Loading OPPT attribute review from {ATTRIBUTE_REVIEW_PATH}")
        with open(ATTRIBUTE_REVIEW_PATH) as f:
            attr_data = json.load(f)
        for seg in attr_data["segments"]:
            attr_lookup[seg["segment_id"]] = seg
        print(f"  {len(attr_lookup)} annotated segments")
        has_annotations = True
    elif is_oppt:
        print("WARNING: OPPT attribute review file not found, running without annotations")
    else:
        # Check for OPP-115 attributes file (extracted from original human annotations)
        opp115_attr_path = data_dir / "opp115_attributes.json"
        if opp115_attr_path.exists():
            print(f"Loading OPP-115 attributes from {opp115_attr_path}")
            with open(opp115_attr_path) as f:
                attr_data = json.load(f)
            for seg in attr_data["segments"]:
                attr_lookup[seg["segment_id"]] = seg
            print(f"  {len(attr_lookup)} annotated segments (from human annotations)")
            print(f"  Stats: {attr_data.get('statistics', {})}")
            has_annotations = True
        else:
            print(f"NOTE: No OPP-115 attributes file found at {opp115_attr_path}")
            print("  Run extract_opp115_attributes.py first to enable annotation-guided extraction")
            print("  Falling back to LLM-inferred statement types")

    # Filter by company if specified
    if args.companies:
        company_filter = {c.strip().lower() for c in args.companies.split(",")}
        segments = [s for s in segments if s["company"].lower() in company_filter]
        print(f"  Filtered to {len(segments)} segments for companies: {args.companies}")

    # Filter out excluded categories
    segments = [s for s in segments if s.get("primary_category", "OTHER") not in EXCLUDED_CATEGORIES]
    print(f"  {len(segments)} segments after excluding categories: {EXCLUDED_CATEGORIES}")

    if not segments:
        print("No segments to process.")
        return

    # Initialize async client with concurrency limit
    # Each segment uses 3 API calls, so divide concurrency by 3 for segment-level parallelism
    client = AsyncOpenRouterClient(api_key, max_concurrent=args.concurrency)

    # Process segments
    print(f"\nExtracting statements from {len(segments)} segments using 3-LLM panel...")
    print(f"  Max concurrent API requests: {args.concurrency}")
    print()

    start_time = time.time()

    try:
        all_statements, agreement_stats, errors, empty_segments, total_usage = await process_segments_parallel(
            client, segments, prompt_template, EXTRACTION_MODELS,
            attr_lookup, has_annotations, batch_size=args.batch_size
        )
    finally:
        await client.close()

    elapsed = time.time() - start_time

    # Summary stats
    total_stmts = len(all_statements)
    type_counts = Counter(s["type"] for s in all_statements)
    subject_counts = Counter(s["subject"] for s in all_statements)
    aspect_counts = Counter(s["aspect"] for s in all_statements)
    scope_counts = Counter(s["scope"] for s in all_statements)
    company_counts = Counter(s["company"] for s in all_statements)

    print(f"\n--- Extraction Summary ---")
    print(f"  Segments processed: {len(segments)}")
    print(f"  Total time: {elapsed/60:.1f} minutes")
    print(f"  Errors: {errors}")
    print(f"  Empty segments (no consensus statements): {empty_segments}")
    print(f"  Total statements: {total_stmts}")
    print(f"  Type distribution: {dict(type_counts)}")
    print(f"  Companies: {len(company_counts)}")

    print(f"\n--- Agreement Statistics ---")
    print(f"  Unanimous (3/3 models): {agreement_stats['unanimous']} ({100*agreement_stats['unanimous']/max(total_stmts,1):.1f}%)")
    print(f"  Majority (2/3 models): {agreement_stats['majority']} ({100*agreement_stats['majority']/max(total_stmts,1):.1f}%)")
    print(f"  Field agreement rates:")
    for field, counts in agreement_stats["by_field"].items():
        total = counts["agree"] + counts["disagree"]
        rate = counts["agree"] / total if total > 0 else 0
        print(f"    {field}: {100*rate:.1f}% agreement")

    print(f"\n--- v2 Field Distributions ---")
    print(f"  Subject: {dict(subject_counts)}")
    print(f"  Aspect: {dict(aspect_counts)}")
    print(f"  Scope: {dict(scope_counts)}")

    # Write output
    corpus_name = "OPP-115" if not is_oppt else "OPPT"
    output = {
        "metadata": {
            "extraction_method": "3-llm-panel",
            "models": EXTRACTION_MODELS,
            "min_agreement": MIN_MODEL_AGREEMENT,
            "extraction_date": datetime.now(timezone.utc).isoformat(),
            "corpus": corpus_name,
            "prompt_version": "v2",
            "prompt_file": str(PROMPT_FILE_V2.name),
            "segments_processed": len(segments),
            "errors": errors,
            "empty_segments": empty_segments,
            "has_annotations": has_annotations,
            "total_usage": total_usage,
            "extraction_time_seconds": round(elapsed, 1),
        },
        "agreement_statistics": agreement_stats,
        "summary": {
            "total_statements": total_stmts,
            "type_distribution": dict(type_counts),
            "subject_distribution": dict(subject_counts),
            "aspect_distribution": dict(aspect_counts),
            "scope_distribution": dict(scope_counts),
            "companies": len(company_counts),
            "unanimous_rate": round(agreement_stats["unanimous"] / max(total_stmts, 1), 4),
            "majority_rate": round(agreement_stats["majority"] / max(total_stmts, 1), 4),
        },
        "statements": all_statements,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nOutput written to {output_path}")
    print(f"  File size: {output_path.stat().st_size / 1024:.1f} KB")


def main():
    """Entry point - run the async main function."""
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
