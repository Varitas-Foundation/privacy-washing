"""
Script 2: Cross-Segment Contradiction Detection

Detects rhetorical contradictions between reassuring "claim" segments and
substantive "practice" segments within each company's privacy policy.

Detection signals:
  1. Semantic similarity pre-filter (all-MiniLM-L6-v2) — ensures topical relevance
  2. NLI model (cross-encoder/nli-deberta-v3-base) — contradiction probability
     This is the PRIMARY signal: only NLI flags contradictions.
  3. Tone gap — reassurance(claim) × hedging(practice) / specificity(practice)
     This is a SEVERITY MODIFIER: boosts severity of NLI-flagged pairs by up to
     30%, but does NOT independently flag contradictions.

Rationale: Tone gap alone flags ~75% of all pairs (baseline noise — all privacy
policies use hedgy language), producing mostly false positives. NLI is sparse
but high-quality, flagging only genuine semantic contradictions.

Evidence types: nli | nli_plus_tone | none

Input:  all_segments.json + linguistic_features.json (Script 1)
Output: output/contradictions.json
"""

import json
import re
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
SEGMENTS_PATH = DATA_DIR / "oppt" / "all_segments.json"
FEATURES_PATH = REPO_ROOT / "output" / "linguistic_features.json"
OUTPUT_PATH = REPO_ROOT / "output" / "contradictions.json"

# Optional CLI flags
_DATA_DIR = None
_NO_SIMILARITY_FILTER = "--no-similarity-filter" in sys.argv
for _i, _arg in enumerate(sys.argv[1:], 1):
    if _arg == "--data-dir" and _i < len(sys.argv) - 1:
        _DATA_DIR = Path(sys.argv[_i + 1])
if _DATA_DIR:
    SEGMENTS_PATH = _DATA_DIR / "all_segments.json"
    FEATURES_PATH = _DATA_DIR / "linguistic_features.json"
    OUTPUT_PATH = _DATA_DIR / "contradictions.json"

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
NLI_MODEL_NAME = "cross-encoder/nli-deberta-v3-base"
SIMILARITY_MODEL_NAME = "all-MiniLM-L6-v2"
SIMILARITY_THRESHOLD = 0.3  # pairs below this cosine similarity are filtered out
MIN_REASSURANCE_SCORE = 0.2  # claim must have reassurance in ≥1/5 sentences

# Negative commitment patterns — claims that make testable promises
# ("we will not X").  Cross-category pairing is only allowed for these,
# because generic assurances ("we protect your data") don't contradict
# data-collection practices in a different OPPT category.
NEGATIVE_COMMITMENT_PATTERNS = [
    r"we\s+(?:will\s+)?never\s+sell",
    r"we\s+do\s+not\s+sell",
    r"we\s+don'?t\s+sell",
    r"we\s+will\s+not\s+(?:share|sell|disclose|use|rent|trade)",
    r"we\s+do\s+not\s+(?:share|sell|disclose|rent|trade)",
    r"we\s+don'?t\s+(?:share|sell|disclose|rent|trade)",
]

# OPPT categories considered "substantive practice" disclosures
PRACTICE_CATEGORIES = {
    "FIRST_PARTY", "THIRD_PARTY", "TRACKING", "SALE_SHARING",
    "SENSITIVE_DATA", "AUTOMATED_DECISIONS", "RETENTION", "SECURITY",
}

# Thresholds
NLI_CONTRADICTION_THRESHOLD = 0.5   # P(contradiction) above this → flagged
# Tone gap is a severity modifier, not an independent signal.
# It boosts severity of NLI-flagged pairs by up to 30% but does NOT
# independently flag contradictions. The old TONE_GAP_THRESHOLD,
# COMBINED_WEIGHT_NLI, and COMBINED_WEIGHT_TONE constants have been
# removed because tone gap alone produced ~75% false positive rate.

# Batch size for NLI inference
BATCH_SIZE = 32


# ---------------------------------------------------------------------------
# NLI model
# ---------------------------------------------------------------------------

def load_nli_model(model_name: str):
    """Load NLI cross-encoder model and tokenizer."""
    print(f"Loading NLI model: {model_name}")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)

    # Use MPS (Apple Silicon GPU) if available, else CPU
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

    # Model outputs: [contradiction, entailment, neutral]
    probs = torch.softmax(logits, dim=-1).cpu().numpy()

    # Reorder to [entailment, neutral, contradiction]
    reordered = np.stack([probs[:, 1], probs[:, 2], probs[:, 0]], axis=-1)
    return reordered


# ---------------------------------------------------------------------------
# Pair generation
# ---------------------------------------------------------------------------

def _has_negative_commitment(text: str) -> bool:
    """Check whether text contains a negative commitment pattern."""
    for pat in NEGATIVE_COMMITMENT_PATTERNS:
        if re.search(pat, text, re.IGNORECASE):
            return True
    return False


def generate_pairs(segments: list[dict], features: list[dict]) -> list[dict]:
    """Generate claim × practice pairs within each company.

    Claim segments: segments with reassurance_score >= MIN_REASSURANCE_SCORE
      (filters out segments where reassurance is incidental — e.g. 1 match
      buried in 8+ sentences of descriptive text)
    Practice segments: segments in substantive OPPT categories

    Cross-category pairing rule: if the claim and practice are in different
    OPPT categories, the claim must contain a negative commitment ("we will
    not share/sell/disclose").  Generic assurances ("we protect your data")
    only pair within their own category, because security promises do not
    contradict data-collection practices.

    Returns list of pair dicts with metadata for both segments.
    """
    # Build lookup: segment_id -> features
    feat_lookup = {f["segment_id"]: f for f in features}

    # Group segments by company
    by_company = {}
    for seg in segments:
        company = seg["company"]
        if company not in by_company:
            by_company[company] = []
        by_company[company].append(seg)

    pairs = []
    cross_category_skipped = 0
    for company, company_segments in by_company.items():
        # Identify claims (reassurance detected)
        claims = []
        practices = []
        for seg in company_segments:
            sid = seg["segment_id"]
            feat = feat_lookup.get(sid)
            if not feat:
                continue

            if feat["reassurance_score"] >= MIN_REASSURANCE_SCORE:
                claims.append((seg, feat))

            if seg["primary_category"] in PRACTICE_CATEGORIES:
                practices.append((seg, feat))

        # Generate directional pairs: claim → practice
        for claim_seg, claim_feat in claims:
            claim_text = claim_seg["text"]
            claim_cat = claim_seg["primary_category"]
            has_neg = _has_negative_commitment(claim_text)

            for practice_seg, practice_feat in practices:
                # Skip self-pairs (a segment can be both claim and practice)
                if claim_seg["segment_id"] == practice_seg["segment_id"]:
                    continue

                # Cross-category rule: require negative commitment
                practice_cat = practice_seg["primary_category"]
                if claim_cat != practice_cat and not has_neg:
                    cross_category_skipped += 1
                    continue

                pairs.append({
                    "company": company,
                    "claim_id": claim_seg["segment_id"],
                    "claim_category": claim_cat,
                    "claim_text": claim_text,
                    "has_negative_commitment": has_neg,
                    "practice_id": practice_seg["segment_id"],
                    "practice_category": practice_cat,
                    "practice_text": practice_seg["text"],
                    # Features for tone gap computation
                    "claim_reassurance": claim_feat["reassurance_score"],
                    "practice_hedging": practice_feat["hedging_score"],
                    "practice_specificity": practice_feat["specificity_score"],
                    "practice_vague_ratio": practice_feat["vague_ratio"],
                })

    if cross_category_skipped:
        print(f"  Cross-category filter: skipped {cross_category_skipped} pairs (claim lacked negative commitment)")

    return pairs


# ---------------------------------------------------------------------------
# Semantic similarity pre-filter
# ---------------------------------------------------------------------------

def compute_semantic_similarity(pairs: list[dict], device: torch.device):
    """Compute cosine similarity between claim and practice texts using bi-encoder.

    Adds a 'semantic_similarity' field to each pair dict in-place.
    Uses unique-text deduplication to avoid redundant encoding.
    """
    from sentence_transformers import SentenceTransformer

    print(f"Loading similarity model: {SIMILARITY_MODEL_NAME}")
    model = SentenceTransformer(SIMILARITY_MODEL_NAME, device=str(device))

    # Collect unique texts to avoid redundant encoding
    unique_claims = list({p["claim_text"] for p in pairs})
    unique_practices = list({p["practice_text"] for p in pairs})
    print(f"  Encoding {len(unique_claims)} unique claims + {len(unique_practices)} unique practices")

    claim_embeds = {t: e for t, e in zip(
        unique_claims,
        model.encode(unique_claims, batch_size=64, show_progress_bar=False),
    )}
    practice_embeds = {t: e for t, e in zip(
        unique_practices,
        model.encode(unique_practices, batch_size=64, show_progress_bar=False),
    )}

    # Compute cosine similarity per pair
    for pair in pairs:
        c = claim_embeds[pair["claim_text"]]
        p = practice_embeds[pair["practice_text"]]
        pair["semantic_similarity"] = round(
            float(np.dot(c, p) / (np.linalg.norm(c) * np.linalg.norm(p))), 4
        )


# ---------------------------------------------------------------------------
# Tone gap
# ---------------------------------------------------------------------------

def compute_tone_gap(pair: dict) -> float:
    """Compute tone gap for a claim-practice pair.

    tone_gap = reassurance(claim) × hedging(practice) / specificity(practice)

    High when: high reassurance + high hedging + low specificity
    This captures: company makes big promises (reassurance) but practices
    are hedged and vague (low specificity).
    """
    reassurance = pair["claim_reassurance"]
    hedging = pair["practice_hedging"]
    specificity = pair["practice_specificity"]

    # Avoid division by zero: use small epsilon for specificity
    # Lower specificity → higher tone gap (more vague = more suspicious)
    specificity_denom = max(specificity, 0.01)

    return reassurance * hedging / specificity_denom


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def main():
    # Load data
    print(f"Loading segments from {SEGMENTS_PATH}")
    with open(SEGMENTS_PATH) as f:
        seg_data = json.load(f)
    segments = seg_data["segments"]
    print(f"  {len(segments)} segments")

    print(f"Loading features from {FEATURES_PATH}")
    with open(FEATURES_PATH) as f:
        feat_data = json.load(f)
    features = feat_data["features"]
    print(f"  {len(features)} feature records")

    # Generate pairs
    print("\nGenerating claim × practice pairs...")
    pairs = generate_pairs(segments, features)
    total_generated = len(pairs)
    print(f"  Generated {total_generated} pairs across {len(set(p['company'] for p in pairs))} companies")

    # Determine device early for similarity model (same logic as NLI)
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

    similarity_filter_active = not _NO_SIMILARITY_FILTER
    pre_filter_count = len(pairs)
    if similarity_filter_active:
        pairs = [p for p in pairs if p["semantic_similarity"] >= SIMILARITY_THRESHOLD]
        print(f"  Similarity filter: {pre_filter_count} → {len(pairs)} pairs (threshold={SIMILARITY_THRESHOLD})")
    else:
        print(f"  Similarity filter DISABLED (--no-similarity-filter)")

    # Compute tone gap for all pairs
    print("\nComputing tone gap scores...")
    for pair in pairs:
        pair["tone_gap"] = round(compute_tone_gap(pair), 6)

    # Tone gap statistics
    tone_gaps = [p["tone_gap"] for p in pairs]
    tone_gap_nonzero = [t for t in tone_gaps if t > 0]
    print(f"  Non-zero tone gaps: {len(tone_gap_nonzero)}/{len(tone_gaps)}")
    if tone_gap_nonzero:
        print(f"  Tone gap range: {min(tone_gap_nonzero):.4f} – {max(tone_gap_nonzero):.4f}")
        print(f"  Tone gap mean (non-zero): {np.mean(tone_gap_nonzero):.4f}")

    # Load NLI model
    tokenizer, model, device = load_nli_model(NLI_MODEL_NAME)

    # Run NLI inference in batches
    print(f"\nRunning NLI inference on {len(pairs)} pairs (batch_size={BATCH_SIZE})...")
    start_time = time.time()

    all_probs = []
    for batch_start in range(0, len(pairs), BATCH_SIZE):
        batch_end = min(batch_start + BATCH_SIZE, len(pairs))
        batch_pairs = [
            (p["claim_text"], p["practice_text"])
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
    print(f"  NLI inference complete in {elapsed:.0f}s ({len(pairs)/elapsed:.0f} pairs/sec)")

    # Attach NLI scores to pairs
    for i, pair in enumerate(pairs):
        pair["nli_entailment"] = round(float(all_probs[i, 0]), 4)
        pair["nli_neutral"] = round(float(all_probs[i, 1]), 4)
        pair["nli_contradiction"] = round(float(all_probs[i, 2]), 4)

    # Normalize tone gap to [0, 1] for combining with NLI
    tone_gaps_array = np.array([p["tone_gap"] for p in pairs])
    if tone_gaps_array.max() > 0:
        tone_gaps_normalized = tone_gaps_array / tone_gaps_array.max()
    else:
        tone_gaps_normalized = tone_gaps_array

    # Classify contradictions using NLI as the primary signal.
    # Tone gap is a severity modifier only — it does NOT independently flag.
    print("\nClassifying contradictions (NLI-primary)...")
    contradictions = []
    for i, pair in enumerate(pairs):
        nli_score = pair["nli_contradiction"]
        tone_norm = float(tone_gaps_normalized[i])
        pair["tone_gap_normalized"] = round(tone_norm, 4)

        # NLI is the sole gate for contradiction detection
        nli_flag = nli_score >= NLI_CONTRADICTION_THRESHOLD
        pair["is_contradiction"] = nli_flag

        # Evidence type: tone gap can amplify but not independently flag
        if nli_flag and tone_norm > 0:
            pair["evidence_type"] = "nli_plus_tone"
        elif nli_flag:
            pair["evidence_type"] = "nli"
        else:
            pair["evidence_type"] = "none"

        # Severity score for NLI-flagged contradictions:
        # Tone gap boosts severity by up to 30% but doesn't independently flag.
        # A pair with NLI=0.95 and high tone gap scores higher than NLI=0.95 alone,
        # which is correct — contradictions backed by hedgy/vague practice language are worse.
        if nli_flag:
            pair["severity"] = round(nli_score * (1 + 0.3 * tone_norm), 4)
        else:
            pair["severity"] = 0.0

        if pair["is_contradiction"]:
            contradictions.append(pair)

    print(f"  Total contradictions detected: {len(contradictions)}/{len(pairs)}")
    print(f"    - nli_plus_tone: {sum(1 for c in contradictions if c['evidence_type'] == 'nli_plus_tone')}")
    print(f"    - nli: {sum(1 for c in contradictions if c['evidence_type'] == 'nli')}")

    # Per-company summary
    company_summaries = {}
    companies_in_pairs = set(p["company"] for p in pairs)
    for company in sorted(companies_in_pairs):
        company_pairs = [p for p in pairs if p["company"] == company]
        company_contradictions = [p for p in company_pairs if p["is_contradiction"]]
        company_summaries[company] = {
            "total_pairs": len(company_pairs),
            "total_contradictions": len(company_contradictions),
            "contradiction_density": round(len(company_contradictions) / max(len(company_pairs), 1), 4),
            "mean_severity": round(
                np.mean([p["severity"] for p in company_contradictions]), 4
            ) if company_contradictions else 0,
            "evidence_type_counts": {
                "nli_plus_tone": sum(1 for c in company_contradictions if c["evidence_type"] == "nli_plus_tone"),
                "nli": sum(1 for c in company_contradictions if c["evidence_type"] == "nli"),
            },
        }

    # Build output (exclude full text from pairs to reduce file size)
    pairs_output = []
    for p in pairs:
        p_copy = {k: v for k, v in p.items() if k not in ("claim_text", "practice_text")}
        # Include truncated text for inspection
        p_copy["claim_text_preview"] = p["claim_text"][:200]
        p_copy["practice_text_preview"] = p["practice_text"][:200]
        pairs_output.append(p_copy)

    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "config": {
            "nli_model": NLI_MODEL_NAME,
            "nli_contradiction_threshold": NLI_CONTRADICTION_THRESHOLD,
            "scoring": "NLI-primary: tone gap is severity modifier (up to +30%), not independent signal",
            "practice_categories": sorted(PRACTICE_CATEGORIES),
            "batch_size": BATCH_SIZE,
            "min_reassurance_score": MIN_REASSURANCE_SCORE,
            "similarity_model": SIMILARITY_MODEL_NAME,
            "similarity_threshold": SIMILARITY_THRESHOLD,
            "similarity_filter_active": similarity_filter_active,
        },
        "summary": {
            "total_generated_pairs": total_generated,
            "pre_filter_pairs": pre_filter_count,
            "total_pairs": len(pairs),
            "total_contradictions": len(contradictions),
            "contradiction_rate": round(len(contradictions) / max(len(pairs), 1), 4),
            "nli_flagged_count": len(contradictions),
            "evidence_type_distribution": {
                "nli_plus_tone": sum(1 for c in contradictions if c["evidence_type"] == "nli_plus_tone"),
                "nli": sum(1 for c in contradictions if c["evidence_type"] == "nli"),
            },
            "mean_semantic_similarity": round(float(np.mean([p["semantic_similarity"] for p in pairs])), 4),
            "mean_nli_contradiction": round(float(all_probs[:, 2].mean()), 4),
            "mean_tone_gap": round(float(tone_gaps_array.mean()), 4),
            "mean_severity": round(float(np.mean([p["severity"] for p in contradictions])), 4) if contradictions else 0,
            "companies_with_contradictions": sum(
                1 for cs in company_summaries.values() if cs["total_contradictions"] > 0
            ),
        },
        "company_summaries": company_summaries,
        "pairs": pairs_output,
    }

    # Write output
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nOutput written to {OUTPUT_PATH}")
    print(f"  File size: {OUTPUT_PATH.stat().st_size / (1024*1024):.1f} MB")

    # Top 10 contradictions by severity
    top_contradictions = sorted(contradictions, key=lambda x: -x["severity"])[:10]
    print(f"\n--- Top 10 Contradictions (by severity) ---")
    for c in top_contradictions:
        print(f"  {c['company']}: {c['claim_id']} → {c['practice_id']}")
        print(f"    sim={c['semantic_similarity']:.3f} | NLI={c['nli_contradiction']:.3f} | tone_gap={c['tone_gap']:.3f} | severity={c['severity']:.3f} [{c['evidence_type']}]")
        print(f"    claim: {c['claim_text'][:80]}...")
        print(f"    practice: {c['practice_text'][:80]}...")
        print()


if __name__ == "__main__":
    main()
