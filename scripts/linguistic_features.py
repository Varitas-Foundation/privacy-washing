"""
Script 1: Linguistic Feature Extraction for Privacy Washing Detection

Extracts per-segment linguistic features from all 3,651 OPPT-annotated segments:
  - Hedging score (CoNLL-2010/BioScope grounded)
  - Reassurance score (trust/commitment phrases)
  - Specificity score (NER entities + data types + timeframes + named third parties)
  - Commitment strength (strong vs weak modals)
  - Readability (Flesch-Kincaid, sentence stats)

Reuses word lists from archive/src/data/feature_extraction.py and extends with
new reassurance lexicon and commitment strength analysis.

Input:  data/oppt/all_segments.json
Output: output/linguistic_features.json
"""

import json
import re
import sys
import os
from pathlib import Path
from datetime import datetime, timezone

import textstat
import nltk

# Ensure NLTK data is available
for resource in ["tokenizers/punkt_tab"]:
    try:
        nltk.data.find(resource)
    except LookupError:
        nltk.download(resource.split("/")[-1], quiet=True)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[1]
SEGMENTS_PATH = DATA_DIR / "oppt" / "all_segments.json"
OUTPUT_PATH = REPO_ROOT / "output" / "linguistic_features.json"

# Optional --data-dir override: read/write all files from a custom directory
_DATA_DIR = None
for _i, _arg in enumerate(sys.argv[1:], 1):
    if _arg == "--data-dir" and _i < len(sys.argv) - 1:
        _DATA_DIR = Path(sys.argv[_i + 1])
if _DATA_DIR:
    SEGMENTS_PATH = _DATA_DIR / "all_segments.json"
    OUTPUT_PATH = _DATA_DIR / "linguistic_features.json"

# ---------------------------------------------------------------------------
# Word lists — reused from archive/src/data/feature_extraction.py
# ---------------------------------------------------------------------------
VAGUE_TERMS = [
    "may", "might", "could", "possibly", "sometimes", "occasionally",
    "certain", "some", "various", "other", "etc", "and more", "among others",
    "partners", "affiliates", "third parties", "service providers", "vendors",
    "contractors", "trusted companies", "selected partners",
    "legitimate interests", "business purposes", "improve services",
    "enhance experience", "operational purposes", "internal purposes", "reasonable purposes",
    "from time to time", "periodically", "as needed", "when necessary", "at our discretion",
]

LEGAL_TERMS = [
    "pursuant", "herein", "thereof", "whereas", "notwithstanding", "aforementioned",
    "hereunder", "herewith", "thereto", "hereby", "foregoing", "stipulate",
    "indemnify", "liability", "jurisdiction", "arbitration", "severability",
    "supersede", "waiver",
]

SPECIFICITY_INDICATORS = [
    "email address", "phone number", "mailing address", "ip address",
    "device identifier", "cookie", "browser type", "location data",
    "payment information", "credit card", "social security", "date of birth",
    "name", "username", "password",
]

# ---------------------------------------------------------------------------
# NEW: Hedge words — grounded in CoNLL-2010 Shared Task / BioScope literature
# These are words/phrases that weaken the force of a statement.
# Note: keyword matching will overcount (~90% of keyword hits are not actual
# hedges in context per Vincze et al. 2008). Scores are useful for *relative*
# comparisons across segments.
# ---------------------------------------------------------------------------
HEDGE_WORDS = [
    # Epistemic modals (weak)
    "may", "might", "could", "possibly", "perhaps", "probably",
    # Frequency hedges
    "sometimes", "occasionally", "generally", "typically", "usually", "often",
    "frequently", "commonly", "normally", "tends to",
    # Approximators
    "approximately", "about", "around", "roughly", "nearly", "almost",
    "up to", "as many as", "estimated",
    # Plausibility shields
    "it is possible", "it is likely", "it appears", "it seems",
    "we believe", "we expect", "we anticipate", "we estimate",
    "to our knowledge", "as far as we know",
    # Scope limiters
    "in some cases", "in certain circumstances", "under certain conditions",
    "from time to time", "at our discretion", "as appropriate",
    "as needed", "when necessary", "where applicable", "where appropriate",
    "where required", "as permitted", "to the extent",
    # Attribution hedges
    "we understand", "we recognize", "we acknowledge",
]

# ---------------------------------------------------------------------------
# NEW: Reassurance phrases — trust/commitment language in privacy policies
# Constructed from manual inspection + Fuoli (2018) stance marker methodology.
# Belcheva et al. (2023) independently identified similar "pacifying phrases."
# ---------------------------------------------------------------------------
REASSURANCE_PHRASES = [
    # Direct value claims
    r"we\s+value\s+your\s+privacy",
    r"your\s+privacy\s+is\s+important",
    r"we\s+care\s+about\s+your\s+privacy",
    r"we\s+respect\s+your\s+privacy",
    r"privacy\s+is\s+(?:a\s+)?(?:top|our)\s+priority",
    r"we\s+(?:(?:\w+\s+){0,3})?take\s+(?:your\s+)?privacy\s+seriously",
    r"we\s+(?:(?:\w+\s+){0,3})?(?:are\s+)?committed\s+to\s+protect",
    r"committed\s+to\s+(?:your\s+)?(?:privacy|security|protecting)",
    r"dedicated\s+to\s+(?:your\s+)?(?:privacy|security|protecting)",
    # Trust language
    r"your\s+trust\s+(?:is|means)",
    r"we\s+(?:have\s+)?earn(?:ed)?\s+your\s+trust",
    r"maintain(?:ing)?\s+your\s+trust",
    r"trust\s+(?:is\s+)?important\s+to\s+us",
    r"transparency\s+is\s+important",
    r"we\s+believe\s+in\s+transparency",
    # Control/empowerment claims
    r"you\s+(?:are|remain)\s+in\s+control",
    r"give\s+you\s+(?:more\s+)?control",
    r"we\s+(?:(?:\w+\s+){0,3})?(?:want\s+to\s+)?empower\s+you",
    r"we\s+(?:(?:\w+\s+){0,3})?(?:want\s+to\s+)?help\s+you\s+(?:(?:\w+\s+){0,2})?(?:control|protect|manage|understand|exercise|delete|access)",
    r"your\s+(?:choices?|rights?)\s+(?:matter|are\s+important)",
    # Removed: r"you\s+(?:can\s+)?choose" — fires on conditional collection
    # ("if you choose to provide it") which is not reassurance. 245/265 matches
    # were false positives. Genuine empowerment covered by "in control" patterns.
    # Negative commitments
    r"we\s+(?:will\s+)?never\s+sell",
    r"we\s+do\s+not\s+sell",
    r"we\s+don'?t\s+sell",
    r"we\s+will\s+not\s+(?:share|sell|disclose)",
    # Security assurance
    r"we\s+(?:use|employ|implement)\s+(?:industry[- ]standard|reasonable|appropriate)\s+(?:security|safeguards|measures)",
    r"we\s+(?:take\s+)?(?:reasonable|appropriate)\s+(?:steps|measures|precautions)",
    r"(?<!measures )(?<!steps )(?<!efforts )we\s+(?:\w+\s+){0,3}?protect(?:ing)?\s+your\s+(?:personal\s+)?(?:information|data)",
    # Minimization claims
    r"we\s+(?:only\s+)?collect\s+(?:only\s+)?(?:what|the\s+minimum|the\s+data)\s+(?:we\s+need|is\s+necessary)",
    r"we\s+(?:\w+\s+){0,2}?limit\s+(?:the\s+)?(?:collection|use|sharing)(?!\s+of\s+your\s+sensitive)",
    r"minim(?:iz|is)(?:e|ing)\s+(?:the\s+)?(?:data|collection|information)",
    # Understanding/help framing
    r"we\s+(?:(?:\w+\s+){0,3})?want\s+you\s+to\s+understand",
    # Removed: r"(?:this|our)\s+(?:\w+\s+)?(?:policy|notice|statement)\s+(?:explains|describes)\s+(?:how|what)"
    # — fires on standard document navigation text ("This policy describes how we handle...").
    # Every privacy policy opens this way; it's meta-description, not reassurance.
    r"(?:easy|simple)\s+to\s+understand",
    # Broad reassurance markers
    r"designed\s+to\s+(?:protect|safeguard|secure)\s+your",
    r"we\s+(?:have\s+)?(?:put|built|implemented)\s+(?:\w+\s+)?(?:safeguards|protections|controls)",
]

# ---------------------------------------------------------------------------
# Commitment strength — strong vs weak modals (Palmer 2001)
# ---------------------------------------------------------------------------
STRONG_MODALS = [
    r"\bwill\b", r"\bshall\b", r"\bmust\b", r"\balways\b", r"\bnever\b",
    r"\bensure\b", r"\bguarantee\b", r"\bcommit\b",
]

WEAK_MODALS = [
    r"\bmay\b", r"\bmight\b", r"\bcould\b", r"\bpossibly\b",
    r"\bperhaps\b", r"\bprobably\b", r"\bgenerally\b", r"\btypically\b",
]

# ---------------------------------------------------------------------------
# Specificity: date patterns, money patterns, third-party org patterns
# ---------------------------------------------------------------------------
DATE_PATTERNS = [
    r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",  # 01/01/2024
    r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b",
    r"\b\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b",
    r"\b(?:Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\.?\s+\d{1,2},?\s+\d{4}\b",
    r"\b\d+\s+(?:days?|months?|years?|hours?|weeks?)\b",  # "30 days", "12 months"
]

MONEY_PATTERNS = [
    r"\$\s?\d[\d,]*(?:\.\d{2})?(?:\s?(?:million|billion|thousand))?",
    r"\b\d[\d,]*(?:\.\d{2})?\s+(?:dollars?|USD|EUR|GBP)",
]

# Named third parties — regex for org-like entities
ORG_PATTERNS = [
    r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b",  # Capitalized multi-word (e.g., "Google Analytics")
    r"\b(?:Inc|LLC|Corp|Ltd|Co|GmbH|S\.A\.)\.?\b",  # Corporate suffixes
    r"\b[A-Z]{2,}\b",  # Acronyms (e.g., "GDPR", "CCPA", "FTC")
]

# Concrete timeframe patterns (retention periods, deadlines)
TIMEFRAME_PATTERNS = [
    r"\b\d+\s+(?:calendar\s+)?(?:days?|months?|years?|hours?|weeks?)\b",
    r"\b(?:annually|quarterly|monthly|weekly|daily)\b",
    r"\bwithin\s+\d+\s+(?:days?|business\s+days?|hours?)\b",
]


# ---------------------------------------------------------------------------
# Feature extraction
# ---------------------------------------------------------------------------

def count_pattern_matches(text: str, patterns: list[str], flags: int = re.IGNORECASE) -> int:
    """Count total regex matches across a list of patterns."""
    total = 0
    for pattern in patterns:
        total += len(re.findall(pattern, text, flags))
    return total


def count_substring_matches(text_lower: str, terms: list[str]) -> int:
    """Count how many terms from a list appear in lowercased text."""
    return sum(1 for term in terms if term in text_lower)


def extract_features(segment: dict) -> dict:
    """Extract all linguistic features for a single segment.

    Returns a dict with the segment's metadata + computed features.
    """
    text = segment["text"]
    text_lower = text.lower()

    # Tokenize
    sentences = nltk.sent_tokenize(text)
    num_sentences = max(len(sentences), 1)
    words = nltk.word_tokenize(text)
    word_count = len([w for w in words if w.isalnum()])
    word_count = max(word_count, 1)  # avoid division by zero

    # --- Hedging score ---
    hedge_count = count_substring_matches(text_lower, HEDGE_WORDS)
    hedging_score = hedge_count / num_sentences  # normalized by sentence count

    # --- Reassurance score ---
    reassurance_count = count_pattern_matches(text, REASSURANCE_PHRASES)
    reassurance_score = reassurance_count / num_sentences

    # --- Specificity score ---
    # Component 1: NER-like entities (regex-based, same approach as existing codebase)
    ner_count = count_pattern_matches(text, ORG_PATTERNS, flags=0)  # case-sensitive
    date_count = count_pattern_matches(text, DATE_PATTERNS)
    money_count = count_pattern_matches(text, MONEY_PATTERNS)

    # Component 2: specific data type mentions
    data_type_count = count_substring_matches(text_lower, SPECIFICITY_INDICATORS)

    # Component 3: concrete timeframe patterns
    timeframe_count = count_pattern_matches(text, TIMEFRAME_PATTERNS)

    # Composite specificity: all concrete detail markers, normalized by word count
    total_specificity = ner_count + date_count + money_count + data_type_count + timeframe_count
    specificity_score = total_specificity / word_count

    # --- Commitment strength ---
    strong_count = count_pattern_matches(text, STRONG_MODALS)
    weak_count = count_pattern_matches(text, WEAK_MODALS)
    # Ratio: strong / (strong + weak). 1.0 = all strong, 0.0 = all weak, 0.5 = balanced
    commitment_strength = strong_count / max(strong_count + weak_count, 1)

    # --- Readability ---
    try:
        flesch_kincaid_grade = textstat.flesch_kincaid_grade(text)
    except Exception:
        flesch_kincaid_grade = 12.0
    flesch_kincaid_grade = max(0.0, min(30.0, flesch_kincaid_grade))

    try:
        flesch_reading_ease = textstat.flesch_reading_ease(text)
    except Exception:
        flesch_reading_ease = 50.0
    flesch_reading_ease = max(0.0, min(100.0, flesch_reading_ease))

    sentence_lengths = [len(nltk.word_tokenize(s)) for s in sentences]
    avg_sentence_length = sum(sentence_lengths) / num_sentences

    # --- Vagueness (from existing lexicon) ---
    vague_count = count_substring_matches(text_lower, VAGUE_TERMS)
    vague_ratio = vague_count / word_count

    # --- Legal jargon ---
    legal_count = count_substring_matches(text_lower, LEGAL_TERMS)
    legal_density = legal_count / word_count

    return {
        # Metadata passthrough
        "segment_id": segment["segment_id"],
        "company": segment["company"],
        "primary_category": segment["primary_category"],
        "secondary_categories": segment.get("secondary_categories", []),
        # Core privacy washing features
        "hedging_score": round(hedging_score, 4),
        "reassurance_score": round(reassurance_score, 4),
        "specificity_score": round(specificity_score, 4),
        "commitment_strength": round(commitment_strength, 4),
        # Readability
        "flesch_kincaid_grade": round(flesch_kincaid_grade, 2),
        "flesch_reading_ease": round(flesch_reading_ease, 2),
        "avg_sentence_length": round(avg_sentence_length, 2),
        "num_sentences": num_sentences,
        # Vagueness & legal
        "vague_count": vague_count,
        "vague_ratio": round(vague_ratio, 4),
        "legal_count": legal_count,
        "legal_density": round(legal_density, 4),
        # Raw counts (for transparency / debugging)
        "hedge_count": hedge_count,
        "reassurance_count": reassurance_count,
        "strong_modal_count": strong_count,
        "weak_modal_count": weak_count,
        "ner_count": ner_count,
        "date_count": date_count,
        "money_count": money_count,
        "data_type_count": data_type_count,
        "timeframe_count": timeframe_count,
        "word_count": word_count,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print(f"Loading segments from {SEGMENTS_PATH}")
    with open(SEGMENTS_PATH) as f:
        data = json.load(f)

    segments = data["segments"]
    print(f"  Total segments: {len(segments)}")

    # Extract features for all segments
    print("Extracting linguistic features...")
    features = []
    for i, seg in enumerate(segments):
        feat = extract_features(seg)
        features.append(feat)
        if (i + 1) % 500 == 0:
            print(f"  Processed {i + 1}/{len(segments)} segments")

    print(f"  Done. Processed {len(features)} segments.")

    # Summary statistics
    companies = set(f["company"] for f in features)
    categories = {}
    for f in features:
        cat = f["primary_category"]
        categories[cat] = categories.get(cat, 0) + 1

    reassurance_segments = [f for f in features if f["reassurance_count"] > 0]
    high_hedge = [f for f in features if f["hedging_score"] > 2.0]

    summary = {
        "total_segments": len(features),
        "total_companies": len(companies),
        "category_distribution": dict(sorted(categories.items())),
        "segments_with_reassurance": len(reassurance_segments),
        "segments_with_high_hedging": len(high_hedge),
        "mean_hedging_score": round(sum(f["hedging_score"] for f in features) / len(features), 4),
        "mean_reassurance_score": round(sum(f["reassurance_score"] for f in features) / len(features), 4),
        "mean_specificity_score": round(sum(f["specificity_score"] for f in features) / len(features), 4),
        "mean_commitment_strength": round(sum(f["commitment_strength"] for f in features) / len(features), 4),
        "mean_flesch_kincaid_grade": round(sum(f["flesch_kincaid_grade"] for f in features) / len(features), 2),
    }

    # Build output
    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": summary,
        "features": features,
    }

    # Write output
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nOutput written to {OUTPUT_PATH}")
    print(f"\n--- Summary ---")
    for k, v in summary.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
