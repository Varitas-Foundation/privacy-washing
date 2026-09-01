"""
Statement-Level Contradiction Detection

Pairs COMMITMENT statements against PRACTICE statements and runs NLI to detect
contradictions.  This replaces the segment-level comparison in detect_contradictions.py
with atomic-statement-level comparison, structurally eliminating false positives
caused by multi-statement paragraphs.

Pairing rules (within same company):
  1. Only COMMITMENT × PRACTICE (never COMMITMENT × COMMITMENT or PRACTICE × PRACTICE)
  2. Must be from different segments (no self-contradiction)
  3. Both sides must be from actionable data-handling categories:
     FIRST_PARTY, THIRD_PARTY, TRACKING, SALE_SHARING, SENSITIVE_DATA, AUTOMATED_DECISIONS
  4. Excluded categories (both sides): SECURITY, RETENTION, USER_RIGHTS, USER_CHOICE, USER_ACCESS
     (these are implementation/procedural, not data-handling commitments or practices)
  5. Semantic similarity pre-filter: same-category threshold 0.3,
     cross-category threshold 0.5

Enhanced filtering (--enhanced-filtering flag, requires v2 statements):
  6. Subject compatibility: Only pairs with compatible subjects can contradict
  7. Aspect compatibility: Use matrix to determine if aspects can genuinely conflict
  8. Scope filter: Exclude LEGAL_REQUIREMENT practices from pairing
  9. Qualifier check: Skip if commitment qualifier covers practice scope

Input:  statements.json (from extract_statements.py)
Output: statement_contradictions.json

Usage:
  python detect_statement_contradictions.py
  python detect_statement_contradictions.py --data-dir ../../opp115_experiment
  python detect_statement_contradictions.py --data-dir ../../opp115_experiment --enhanced-filtering
"""

import argparse
import json
import sys
import time
from pathlib import Path
from datetime import datetime, timezone

import numpy as np
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[1]
STATEMENTS_PATH = REPO_ROOT / "output" / "statements.json"
OUTPUT_PATH = REPO_ROOT / "output" / "statement_contradictions.json"

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Detect contradictions between commitment and practice statements")
    parser.add_argument("--data-dir", type=str, default=None,
                        help="Override data directory (e.g., for OPP-115 experiment)")
    parser.add_argument("--no-similarity-filter", action="store_true",
                        help="Disable semantic similarity pre-filtering")
    parser.add_argument("--enhanced-filtering", action="store_true",
                        help="Enable enhanced filtering using v2 statement metadata (subject, aspect, scope, qualifiers)")
    return parser.parse_args()


# Parse args early to set paths
_ARGS = parse_args()
_DATA_DIR = None
if _ARGS.data_dir:
    _DATA_DIR = Path(_ARGS.data_dir)
if _DATA_DIR:
    if not _DATA_DIR.is_absolute():
        _DATA_DIR = (REPO_ROOT / _DATA_DIR).resolve()
    STATEMENTS_PATH = _DATA_DIR / "statements.json"
    OUTPUT_PATH = _DATA_DIR / "statement_contradictions.json"

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
NLI_MODEL_NAME = "cross-encoder/nli-deberta-v3-base"
SIMILARITY_MODEL_NAME = "all-MiniLM-L6-v2"
SIMILARITY_THRESHOLD_CROSS_CATEGORY = 0.5
SIMILARITY_THRESHOLD_SAME_CATEGORY = 0.3
NLI_CONTRADICTION_THRESHOLD = 0.5
BATCH_SIZE = 32

# Categories whose statements are eligible for pairing (both sides)
# Data-handling categories produce genuine commitment-vs-practice contradictions.
# Excluded: SECURITY, RETENTION, USER_RIGHTS, USER_CHOICE, USER_ACCESS
# (these are implementation/procedural, not data-handling commitments or practices)
ACTIONABLE_CATEGORIES = {
    "FIRST_PARTY", "THIRD_PARTY", "TRACKING", "SALE_SHARING",
    "SENSITIVE_DATA", "AUTOMATED_DECISIONS",
}

# Aliases for backward compatibility in output
ACTIONABLE_PRACTICE_CATEGORIES = ACTIONABLE_CATEGORIES
EXCLUDED_PRACTICE_CATEGORIES = {
    "SECURITY", "RETENTION", "DATA_RETENTION",
    "USER_RIGHTS", "USER_CHOICE", "USER_ACCESS",
}

# ---------------------------------------------------------------------------
# Enhanced Filtering Configuration (v2 statements only)
# ---------------------------------------------------------------------------

# Subject compatibility: Which subjects can genuinely contradict each other
# Key: (commitment_subject, practice_subject) -> can_contradict
SUBJECT_COMPATIBILITY = {
    # COMPANY commitments vs various practice subjects
    ("COMPANY", "COMPANY"): True,          # Same actor
    ("COMPANY", "AFFILIATES"): True,       # Related entities, can contradict
    ("COMPANY", "SERVICE_PROVIDER"): False, # Service providers act on company's behalf, different scope
    ("COMPANY", "THIRD_PARTY"): False,     # Different actors entirely
    ("COMPANY", "USER"): False,            # User actions don't contradict company commitments

    # AFFILIATES
    ("AFFILIATES", "COMPANY"): True,
    ("AFFILIATES", "AFFILIATES"): True,
    ("AFFILIATES", "SERVICE_PROVIDER"): False,
    ("AFFILIATES", "THIRD_PARTY"): False,
    ("AFFILIATES", "USER"): False,

    # SERVICE_PROVIDER commitments (rare but possible)
    ("SERVICE_PROVIDER", "COMPANY"): False,
    ("SERVICE_PROVIDER", "SERVICE_PROVIDER"): True,
    ("SERVICE_PROVIDER", "THIRD_PARTY"): False,
    ("SERVICE_PROVIDER", "AFFILIATES"): False,
    ("SERVICE_PROVIDER", "USER"): False,

    # THIRD_PARTY
    ("THIRD_PARTY", "COMPANY"): False,
    ("THIRD_PARTY", "SERVICE_PROVIDER"): False,
    ("THIRD_PARTY", "THIRD_PARTY"): True,
    ("THIRD_PARTY", "AFFILIATES"): False,
    ("THIRD_PARTY", "USER"): False,

    # USER commitments (extremely rare)
    ("USER", "USER"): True,
    ("USER", "COMPANY"): False,
    ("USER", "THIRD_PARTY"): False,
    ("USER", "SERVICE_PROVIDER"): False,
    ("USER", "AFFILIATES"): False,
}

# Aspect compatibility matrix: Which aspects can genuinely conflict
# True = can contradict, False = different concerns (don't compare)
ASPECT_COMPATIBILITY = {
    # Same aspect always compatible
    ("COLLECTION", "COLLECTION"): True,
    ("USE", "USE"): True,
    ("SHARING", "SHARING"): True,
    ("SALE", "SALE"): True,
    ("RETENTION", "RETENTION"): True,
    ("DELETION", "DELETION"): True,
    ("ACCESS_CONTROL", "ACCESS_CONTROL"): True,
    ("SECURITY", "SECURITY"): True,

    # Related lifecycle stages that can conflict
    ("COLLECTION", "USE"): True,           # What we collect relates to what we use
    ("USE", "COLLECTION"): True,
    ("SHARING", "SALE"): True,             # CCPA treats similarly
    ("SALE", "SHARING"): True,
    ("USE", "SHARING"): True,              # Internal vs external processing
    ("SHARING", "USE"): True,
    ("COLLECTION", "SHARING"): True,       # Collection enables sharing
    ("SHARING", "COLLECTION"): True,
    ("COLLECTION", "SALE"): True,          # Collection relates to sale
    ("SALE", "COLLECTION"): True,
    ("COLLECTION", "RETENTION"): True,     # What we collect vs how long
    ("RETENTION", "COLLECTION"): True,
    ("USE", "SALE"): True,                 # Using data vs selling it
    ("SALE", "USE"): True,

    # Incompatible pairs (don't contradict each other)
    ("ACCESS_CONTROL", "COLLECTION"): False,   # Rights vs practices
    ("COLLECTION", "ACCESS_CONTROL"): False,
    ("ACCESS_CONTROL", "SHARING"): False,
    ("SHARING", "ACCESS_CONTROL"): False,
    ("ACCESS_CONTROL", "USE"): False,
    ("USE", "ACCESS_CONTROL"): False,
    ("ACCESS_CONTROL", "SALE"): False,
    ("SALE", "ACCESS_CONTROL"): False,
    ("SECURITY", "SHARING"): False,            # Different concerns
    ("SHARING", "SECURITY"): False,
    ("SECURITY", "COLLECTION"): False,
    ("COLLECTION", "SECURITY"): False,
    ("SECURITY", "USE"): False,
    ("USE", "SECURITY"): False,
    ("SECURITY", "SALE"): False,
    ("SALE", "SECURITY"): False,
    ("DELETION", "COLLECTION"): False,         # Opposite lifecycle ends
    ("COLLECTION", "DELETION"): False,
    ("DELETION", "SHARING"): False,
    ("SHARING", "DELETION"): False,
    ("DELETION", "SALE"): False,
    ("SALE", "DELETION"): False,
    ("DELETION", "USE"): False,
    ("USE", "DELETION"): False,
    ("RETENTION", "SHARING"): False,
    ("SHARING", "RETENTION"): False,
    ("RETENTION", "SALE"): False,
    ("SALE", "RETENTION"): False,
    ("RETENTION", "USE"): False,
    ("USE", "RETENTION"): False,
    ("RETENTION", "ACCESS_CONTROL"): False,
    ("ACCESS_CONTROL", "RETENTION"): False,
    ("RETENTION", "DELETION"): True,           # Retention and deletion are related
    ("DELETION", "RETENTION"): True,
    ("RETENTION", "SECURITY"): False,
    ("SECURITY", "RETENTION"): False,
    ("DELETION", "ACCESS_CONTROL"): False,
    ("ACCESS_CONTROL", "DELETION"): False,
    ("DELETION", "SECURITY"): False,
    ("SECURITY", "DELETION"): False,
    ("ACCESS_CONTROL", "SECURITY"): False,
    ("SECURITY", "ACCESS_CONTROL"): False,
}

# Qualifier/practice patterns that indicate standard carve-outs
# These are organized by category for clarity

# Legal/regulatory carve-outs
LEGAL_PATTERNS = [
    "required by law",
    "legal requirement",
    "law enforcement",
    "subpoena",
    "court order",
    "comply with law",
    "legal obligation",
    "regulatory",
    "government request",
    "legal process",
    "lawful request",
]

# M&A and business transfer carve-outs
MA_PATTERNS = [
    "merger",
    "acquisition",
    "business transfer",
    "bankruptcy",
    "reorganization",
    "sale of assets",
    "sale of the company",
    "change of control",
    "corporate transaction",
    "business transition",
    "successor",
    "asset sale",
    "divestiture",
]

# Consent-based sharing (standard exception to "don't share")
CONSENT_PATTERNS = [
    "with your consent",
    "with consent",
    "when you consent",
    "if you consent",
    "with your permission",
    "with permission",
    "you authorize",
    "you agree",
    "user consent",
    "provides consent",
    "provide consent",
    "given consent",
    "gives consent",
    "opt in",
    "opted in",
    "you request",
    "at your request",
    "you direct us",
    "as you direct",
    "you instruct",
    "users consent",
    "user consents",
    "customer consent",
]

# Service provider exceptions (acting on company's behalf)
SERVICE_PROVIDER_PATTERNS = [
    "service provider",
    "service providers",
    "on our behalf",
    "on behalf of",
    "processor",
    "processors",
    "contractor",
    "contractors",
    "vendors who",
    "third party service",
    "third-party service",
    "assist us",
    "help us",
    "perform services",
    "provide services",
    "acting for us",
    "under contract",
    "contractual",
    "professional advisor",
    "advisors such as",
    "lawyers",
    "accountants",
    "auditors",
    "legal counsel",
]

# Affiliate/subsidiary sharing (related entities)
AFFILIATE_PATTERNS = [
    "affiliate",
    "affiliates",
    "subsidiary",
    "subsidiaries",
    "parent company",
    "related companies",
    "corporate family",
    "group companies",
]

# Combine all patterns for backward compatibility
LEGAL_QUALIFIER_PATTERNS = (
    LEGAL_PATTERNS + MA_PATTERNS + CONSENT_PATTERNS +
    SERVICE_PROVIDER_PATTERNS + AFFILIATE_PATTERNS
)


def check_subject_compatibility(commit_subject: str, practice_subject: str) -> bool:
    """Check if commitment and practice subjects are compatible for contradiction."""
    key = (commit_subject, practice_subject)
    # Default to True if not in matrix (conservative approach)
    return SUBJECT_COMPATIBILITY.get(key, True)


def check_aspect_compatibility(commit_aspect: str, practice_aspect: str) -> bool:
    """Check if commitment and practice aspects are compatible for contradiction."""
    key = (commit_aspect, practice_aspect)
    # Default to True if not in matrix (conservative approach)
    return ASPECT_COMPATIBILITY.get(key, True)


def check_scope_compatibility(commit_scope: str, practice_scope: str) -> bool:
    """Check if practice scope is compatible for contradiction.

    LEGAL_REQUIREMENT practices should not contradict general commitments
    (standard M&A, law enforcement carve-outs).
    """
    if practice_scope == "LEGAL_REQUIREMENT":
        return False
    return True


def check_practice_is_standard_exception(practice_text: str, practice_scope: str) -> bool:
    """Check if the practice describes a standard exception scenario.

    Returns True if the practice is about a standard carve-out that typically
    doesn't contradict "we don't share/sell" commitments.
    """
    practice_lower = practice_text.lower()

    # Check for M&A scenarios (very common carve-out)
    for pattern in MA_PATTERNS:
        if pattern in practice_lower:
            return True

    # Check for consent-based sharing (standard exception)
    for pattern in CONSENT_PATTERNS:
        if pattern in practice_lower:
            return True

    # Check for service provider sharing (acting on behalf)
    for pattern in SERVICE_PROVIDER_PATTERNS:
        if pattern in practice_lower:
            return True

    # Check scope - LEGAL_REQUIREMENT is already filtered elsewhere but double-check
    if practice_scope == "LEGAL_REQUIREMENT":
        return True

    return False


def check_qualifier_coverage(commit_qualifiers: list, practice_text: str, practice_scope: str) -> bool:
    """Check if commitment qualifiers already cover the practice scenario.

    Returns False (skip pair) if:
    1. Commitment has a qualifier that matches the practice scenario, OR
    2. Practice describes a standard exception (M&A, consent, service providers)

    This prevents false positives like:
    - "We don't sell data" vs "We may transfer data in a merger" (M&A exception)
    - "We don't share data" vs "We share with your consent" (consent exception)
    - "We don't share data" vs "We share with service providers" (processor exception)
    """
    practice_lower = practice_text.lower()

    # First check: Does the practice itself describe a standard exception?
    # These typically don't contradict general commitments
    if check_practice_is_standard_exception(practice_text, practice_scope):
        return False  # Standard exception, skip this pair

    # Second check: Do commitment qualifiers cover this practice?
    if commit_qualifiers:
        for qualifier in commit_qualifiers:
            qualifier_lower = qualifier.lower()

            # Check if qualifier explicitly covers this scenario
            for pattern in LEGAL_QUALIFIER_PATTERNS:
                if pattern in qualifier_lower:
                    # Check if practice matches the carve-out
                    if pattern in practice_lower or practice_scope == "LEGAL_REQUIREMENT":
                        return False  # Qualifier covers the practice, no contradiction

    return True  # No matching exceptions, can still contradict


# ---------------------------------------------------------------------------
# NLI model (reused from detect_contradictions.py)
# ---------------------------------------------------------------------------
def load_nli_model(model_name: str):
    """Load NLI cross-encoder model and tokenizer."""
    print(f"Loading NLI model: {model_name}")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)

    if torch.backends.mps.is_available():
        device = torch.device("mps")
        print("  Using MPS (Apple Silicon GPU)")
    elif torch.cuda.is_available():
        device = torch.device("cuda")
        print("  Using CUDA GPU")
    else:
        device = torch.device("cpu")
        print("  Using CPU")

    model = model.to(device)
    model.eval()
    return tokenizer, model, device


def predict_nli_batch(tokenizer, model, device, pairs: list[tuple[str, str]]) -> np.ndarray:
    """Run NLI prediction on a batch of (premise, hypothesis) pairs.

    Returns array of shape (N, 3) with probabilities for
    [entailment, neutral, contradiction] per pair.

    The model's label mapping:
      0 = contradiction, 1 = entailment, 2 = neutral
    We reorder to: [entailment, neutral, contradiction] for readability.
    """
    premises = [p[0] for p in pairs]
    hypotheses = [p[1] for p in pairs]

    encoded = tokenizer(
        premises, hypotheses,
        padding=True, truncation=True, max_length=512,
        return_tensors="pt"
    ).to(device)

    with torch.no_grad():
        logits = model(**encoded).logits

    probs = torch.softmax(logits, dim=-1).cpu().numpy()
    # Reorder to [entailment, neutral, contradiction]
    reordered = np.stack([probs[:, 1], probs[:, 2], probs[:, 0]], axis=-1)
    return reordered


# ---------------------------------------------------------------------------
# Semantic similarity pre-filter
# ---------------------------------------------------------------------------
def compute_semantic_similarity(pairs: list[dict], device: torch.device):
    """Compute cosine similarity between commitment and practice texts.

    Adds 'semantic_similarity' field to each pair dict in-place.
    """
    from sentence_transformers import SentenceTransformer

    print(f"Loading similarity model: {SIMILARITY_MODEL_NAME}")
    model = SentenceTransformer(SIMILARITY_MODEL_NAME, device=str(device))

    # Collect unique texts
    unique_commitments = list({p["commitment_text"] for p in pairs})
    unique_practices = list({p["practice_text"] for p in pairs})
    print(f"  Encoding {len(unique_commitments)} unique commitments + {len(unique_practices)} unique practices")

    commit_embeds = {t: e for t, e in zip(
        unique_commitments,
        model.encode(unique_commitments, batch_size=64, show_progress_bar=False),
    )}
    practice_embeds = {t: e for t, e in zip(
        unique_practices,
        model.encode(unique_practices, batch_size=64, show_progress_bar=False),
    )}

    for pair in pairs:
        c = commit_embeds[pair["commitment_text"]]
        p = practice_embeds[pair["practice_text"]]
        pair["semantic_similarity"] = round(
            float(np.dot(c, p) / (np.linalg.norm(c) * np.linalg.norm(p))), 4
        )


# ---------------------------------------------------------------------------
# Pair generation
# ---------------------------------------------------------------------------
def generate_pairs(statements: list[dict], enhanced_filtering: bool = False) -> tuple[list[dict], dict]:
    """Generate COMMITMENT × PRACTICE pairs within each company.

    Rules:
      1. Only COMMITMENT × PRACTICE
      2. Different source segments
      3. Both commitment and practice must be from ACTIONABLE_CATEGORIES
         (data-handling categories only — excludes SECURITY, RETENTION, USER_RIGHTS, etc.)

    Enhanced filtering (if enabled, requires v2 statements):
      4. Subject compatibility check
      5. Aspect compatibility check
      6. Scope filter (exclude LEGAL_REQUIREMENT practices)
      7. Qualifier coverage check

    Returns:
      (pairs, filter_statistics)
    """
    # Group by company
    by_company = {}
    for stmt in statements:
        company = stmt["company"]
        if company not in by_company:
            by_company[company] = {"commitments": [], "practices": []}
        if stmt["type"] == "COMMITMENT":
            by_company[company]["commitments"].append(stmt)
        elif stmt["type"] == "PRACTICE":
            by_company[company]["practices"].append(stmt)

    pairs = []
    # Basic filter statistics
    filter_stats = {
        "self_segment_filtered": 0,
        "commitment_category_filtered": 0,
        "practice_category_filtered": 0,
        # Enhanced filter statistics
        "subject_incompatible_filtered": 0,
        "aspect_incompatible_filtered": 0,
        "legal_requirement_scope_filtered": 0,
        "qualifier_coverage_filtered": 0,
    }

    for company, groups in by_company.items():
        commitments = groups["commitments"]
        practices = groups["practices"]

        for commit in commitments:
            # Rule 3a: commitment must be from actionable category
            commit_cat = commit.get("category", "").upper()
            if commit_cat and commit_cat not in ACTIONABLE_CATEGORIES:
                filter_stats["commitment_category_filtered"] += len(practices)
                continue

            for practice in practices:
                # Rule 2: different source segments
                if commit["source_segment_id"] == practice["source_segment_id"]:
                    filter_stats["self_segment_filtered"] += 1
                    continue

                # Rule 3b: practice must be from actionable category
                practice_cat = practice.get("category", "").upper()
                if practice_cat and practice_cat not in ACTIONABLE_CATEGORIES:
                    filter_stats["practice_category_filtered"] += 1
                    continue

                # Enhanced filtering (v2 statements only)
                if enhanced_filtering:
                    # Get v2 fields with defaults
                    commit_subject = commit.get("subject", "COMPANY")
                    practice_subject = practice.get("subject", "COMPANY")
                    commit_aspect = commit.get("aspect", "USE")
                    practice_aspect = practice.get("aspect", "USE")
                    practice_scope = practice.get("scope", "UNIVERSAL")
                    commit_qualifiers = commit.get("qualifiers", [])

                    # Rule 4: Subject compatibility
                    if not check_subject_compatibility(commit_subject, practice_subject):
                        filter_stats["subject_incompatible_filtered"] += 1
                        continue

                    # Rule 5: Aspect compatibility
                    if not check_aspect_compatibility(commit_aspect, practice_aspect):
                        filter_stats["aspect_incompatible_filtered"] += 1
                        continue

                    # Rule 6: Exclude LEGAL_REQUIREMENT practices
                    if not check_scope_compatibility(commit.get("scope", "UNIVERSAL"), practice_scope):
                        filter_stats["legal_requirement_scope_filtered"] += 1
                        continue

                    # Rule 7: Qualifier coverage check
                    if not check_qualifier_coverage(commit_qualifiers, practice["text"], practice_scope):
                        filter_stats["qualifier_coverage_filtered"] += 1
                        continue

                pair_record = {
                    "company": company,
                    "commitment_statement_id": commit["statement_id"],
                    "commitment_text": commit["text"],
                    "commitment_category": commit.get("category", ""),
                    "commitment_source_segment": commit["source_segment_id"],
                    "practice_statement_id": practice["statement_id"],
                    "practice_text": practice["text"],
                    "practice_category": practice.get("category", ""),
                    "practice_source_segment": practice["source_segment_id"],
                    "source_segment_pair": f"{commit['source_segment_id']}_vs_{practice['source_segment_id']}",
                }

                # Include v2 fields if available
                if enhanced_filtering:
                    pair_record["commitment_subject"] = commit.get("subject", "COMPANY")
                    pair_record["commitment_aspect"] = commit.get("aspect", "USE")
                    pair_record["commitment_scope"] = commit.get("scope", "UNIVERSAL")
                    pair_record["commitment_qualifiers"] = commit.get("qualifiers", [])
                    pair_record["practice_subject"] = practice.get("subject", "COMPANY")
                    pair_record["practice_aspect"] = practice.get("aspect", "USE")
                    pair_record["practice_scope"] = practice.get("scope", "UNIVERSAL")

                pairs.append(pair_record)

    total_cat_filtered = filter_stats["commitment_category_filtered"] + filter_stats["practice_category_filtered"]
    print(f"  Generated {len(pairs)} COMMITMENT×PRACTICE pairs")
    print(f"  Filtered (basic): {filter_stats['self_segment_filtered']} same-segment, "
          f"{total_cat_filtered} excluded-category "
          f"({filter_stats['commitment_category_filtered']} commitment-side, "
          f"{filter_stats['practice_category_filtered']} practice-side)")

    if enhanced_filtering:
        enhanced_filtered = (
            filter_stats["subject_incompatible_filtered"] +
            filter_stats["aspect_incompatible_filtered"] +
            filter_stats["legal_requirement_scope_filtered"] +
            filter_stats["qualifier_coverage_filtered"]
        )
        print(f"  Filtered (enhanced): {enhanced_filtered} total")
        print(f"    - Subject incompatible: {filter_stats['subject_incompatible_filtered']}")
        print(f"    - Aspect incompatible: {filter_stats['aspect_incompatible_filtered']}")
        print(f"    - Legal requirement scope: {filter_stats['legal_requirement_scope_filtered']}")
        print(f"    - Qualifier coverage: {filter_stats['qualifier_coverage_filtered']}")

    print(f"  Companies: {len(by_company)}")

    return pairs, filter_stats


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------
def main():
    # Use parsed args
    args = _ARGS

    # Load statements
    print(f"Loading statements from {STATEMENTS_PATH}")
    with open(STATEMENTS_PATH) as f:
        stmt_data = json.load(f)
    statements = stmt_data["statements"]
    print(f"  {len(statements)} statements")
    print(f"  Types: { {k: v for k, v in sorted(dict(zip(*np.unique([s['type'] for s in statements], return_counts=True))).items())} }")

    # Check if statements have v2 fields for enhanced filtering
    prompt_version = stmt_data.get("metadata", {}).get("prompt_version", "v1")
    if args.enhanced_filtering and prompt_version != "v2":
        print("\nWARNING: --enhanced-filtering requires v2 statements (with subject/aspect/scope/qualifiers)")
        print(f"         Current statements use prompt_version={prompt_version}")
        print("         Falling back to basic filtering.")
        args.enhanced_filtering = False
    elif args.enhanced_filtering:
        print(f"\n  Enhanced filtering ENABLED (prompt_version={prompt_version})")

    # Generate pairs
    print("\nGenerating COMMITMENT × PRACTICE pairs...")
    pairs, filter_stats = generate_pairs(statements, enhanced_filtering=args.enhanced_filtering)

    if not pairs:
        print("No pairs generated. Check that statements.json contains both COMMITMENT and PRACTICE types.")
        return

    # Determine device
    if torch.backends.mps.is_available():
        _sim_device = torch.device("mps")
    elif torch.cuda.is_available():
        _sim_device = torch.device("cuda")
    else:
        _sim_device = torch.device("cpu")

    # Semantic similarity pre-filter
    print("\nComputing semantic similarity...")
    compute_semantic_similarity(pairs, _sim_device)
    sim_scores = [p["semantic_similarity"] for p in pairs]
    print(f"  Similarity range: {min(sim_scores):.4f} – {max(sim_scores):.4f}")
    print(f"  Similarity mean: {np.mean(sim_scores):.4f}")

    similarity_filter_active = not args.no_similarity_filter
    pre_filter_count = len(pairs)
    if similarity_filter_active:
        # Category-aware similarity filter:
        # Same-category pairs bypass the filter (category match = topicality signal)
        # Cross-category pairs require higher similarity
        def _passes_similarity(p):
            if p["commitment_category"] == p["practice_category"] and p["commitment_category"]:
                return p["semantic_similarity"] >= SIMILARITY_THRESHOLD_SAME_CATEGORY
            return p["semantic_similarity"] >= SIMILARITY_THRESHOLD_CROSS_CATEGORY

        pairs = [p for p in pairs if _passes_similarity(p)]
        same_cat = sum(1 for p in pairs if p["commitment_category"] == p["practice_category"] and p["commitment_category"])
        cross_cat = len(pairs) - same_cat
        print(f"  Similarity filter: {pre_filter_count} → {len(pairs)} pairs "
              f"(same-cat≥{SIMILARITY_THRESHOLD_SAME_CATEGORY}: {same_cat}, "
              f"cross-cat≥{SIMILARITY_THRESHOLD_CROSS_CATEGORY}: {cross_cat})")
    else:
        print("  Similarity filter DISABLED")

    if not pairs:
        print("No pairs remain after similarity filter.")
        return

    # Load NLI model
    tokenizer, model, device = load_nli_model(NLI_MODEL_NAME)

    # Run NLI inference
    print(f"\nRunning NLI inference on {len(pairs)} pairs (batch_size={BATCH_SIZE})...")
    start_time = time.time()

    all_probs = []
    for batch_start in range(0, len(pairs), BATCH_SIZE):
        batch_end = min(batch_start + BATCH_SIZE, len(pairs))
        batch_pairs = [
            (p["commitment_text"], p["practice_text"])
            for p in pairs[batch_start:batch_end]
        ]
        probs = predict_nli_batch(tokenizer, model, device, batch_pairs)
        all_probs.append(probs)

        if (batch_start // BATCH_SIZE + 1) % 50 == 0:
            elapsed = time.time() - start_time
            pct = batch_end / len(pairs) * 100
            print(f"  {batch_end}/{len(pairs)} pairs ({pct:.0f}%) — {elapsed:.0f}s elapsed")

    all_probs = np.concatenate(all_probs, axis=0)
    elapsed = time.time() - start_time
    print(f"  NLI inference complete in {elapsed:.1f}s ({len(pairs)/max(elapsed, 0.1):.0f} pairs/sec)")

    # Attach NLI scores and classify contradictions
    print("\nClassifying contradictions...")
    contradictions = []
    for i, pair in enumerate(pairs):
        pair["nli_entailment"] = round(float(all_probs[i, 0]), 4)
        pair["nli_neutral"] = round(float(all_probs[i, 1]), 4)
        pair["nli_contradiction_score"] = round(float(all_probs[i, 2]), 4)

        nli_flag = pair["nli_contradiction_score"] >= NLI_CONTRADICTION_THRESHOLD
        pair["is_contradiction"] = nli_flag

        if nli_flag:
            contradictions.append(pair)

    print(f"  Total contradictions: {len(contradictions)}/{len(pairs)}")

    # Per-company summary
    company_summaries = {}
    for company in sorted(set(p["company"] for p in pairs)):
        cp = [p for p in pairs if p["company"] == company]
        cc = [p for p in cp if p["is_contradiction"]]
        company_summaries[company] = {
            "total_pairs": len(cp),
            "total_contradictions": len(cc),
            "contradiction_density": round(len(cc) / max(len(cp), 1), 4),
        }

    # Map contradictions back to source segment pairs for comparison
    segment_pair_contradictions = {}
    for c in contradictions:
        seg_pair = c["source_segment_pair"]
        if seg_pair not in segment_pair_contradictions:
            segment_pair_contradictions[seg_pair] = []
        segment_pair_contradictions[seg_pair].append({
            "commitment_statement_id": c["commitment_statement_id"],
            "practice_statement_id": c["practice_statement_id"],
            "nli_contradiction_score": c["nli_contradiction_score"],
        })

    # Build output
    pairs_output = []
    for p in pairs:
        pair_record = {
            "pair_id": f"{p['commitment_statement_id']}_vs_{p['practice_statement_id']}",
            "company": p["company"],
            "commitment_statement_id": p["commitment_statement_id"],
            "practice_statement_id": p["practice_statement_id"],
            "commitment_text": p["commitment_text"],
            "practice_text": p["practice_text"],
            "commitment_category": p["commitment_category"],
            "practice_category": p["practice_category"],
            "source_segment_pair": p["source_segment_pair"],
            "semantic_similarity": p["semantic_similarity"],
            "nli_contradiction_score": p["nli_contradiction_score"],
            "is_contradiction": p["is_contradiction"],
        }

        # Include v2 fields if present
        if args.enhanced_filtering:
            pair_record["commitment_subject"] = p.get("commitment_subject", "")
            pair_record["commitment_aspect"] = p.get("commitment_aspect", "")
            pair_record["commitment_scope"] = p.get("commitment_scope", "")
            pair_record["commitment_qualifiers"] = p.get("commitment_qualifiers", [])
            pair_record["practice_subject"] = p.get("practice_subject", "")
            pair_record["practice_aspect"] = p.get("practice_aspect", "")
            pair_record["practice_scope"] = p.get("practice_scope", "")

        pairs_output.append(pair_record)

    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "config": {
            "nli_model": NLI_MODEL_NAME,
            "nli_contradiction_threshold": NLI_CONTRADICTION_THRESHOLD,
            "similarity_model": SIMILARITY_MODEL_NAME,
            "similarity_threshold_cross_category": SIMILARITY_THRESHOLD_CROSS_CATEGORY,
            "similarity_threshold_same_category": SIMILARITY_THRESHOLD_SAME_CATEGORY,
            "similarity_filter_active": similarity_filter_active,
            "enhanced_filtering": args.enhanced_filtering,
            "actionable_practice_categories": sorted(ACTIONABLE_PRACTICE_CATEGORIES),
            "excluded_practice_categories": sorted(EXCLUDED_PRACTICE_CATEGORIES),
            "batch_size": BATCH_SIZE,
        },
        "filter_statistics": filter_stats,
        "summary": {
            "total_statements": len(statements),
            "total_generated_pairs": pre_filter_count + (pre_filter_count - len(pairs) if not similarity_filter_active else 0),
            "pre_filter_pairs": pre_filter_count,
            "total_pairs": len(pairs),
            "total_contradictions": len(contradictions),
            "contradiction_rate": round(len(contradictions) / max(len(pairs), 1), 4),
            "mean_semantic_similarity": round(float(np.mean([p["semantic_similarity"] for p in pairs])), 4),
            "mean_nli_contradiction": round(float(all_probs[:, 2].mean()), 4),
            "companies_with_contradictions": sum(
                1 for cs in company_summaries.values() if cs["total_contradictions"] > 0
            ),
            "unique_segment_pairs_with_contradictions": len(segment_pair_contradictions),
        },
        "company_summaries": company_summaries,
        "segment_pair_contradictions": segment_pair_contradictions,
        "pairs": pairs_output,
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nOutput written to {OUTPUT_PATH}")
    print(f"  File size: {OUTPUT_PATH.stat().st_size / 1024:.1f} KB")

    # Top contradictions
    top = sorted(contradictions, key=lambda x: -x["nli_contradiction_score"])[:10]
    print(f"\n--- Top 10 Statement-Level Contradictions ---")
    for c in top:
        print(f"  {c['company']}: {c['commitment_statement_id']} vs {c['practice_statement_id']}")
        print(f"    NLI={c['nli_contradiction_score']:.3f} | sim={c['semantic_similarity']:.3f}")
        print(f"    COMMITMENT: {c['commitment_text']}")
        print(f"    PRACTICE:   {c['practice_text']}")
        print(f"    Segments:   {c['source_segment_pair']}")
        print()


if __name__ == "__main__":
    main()
