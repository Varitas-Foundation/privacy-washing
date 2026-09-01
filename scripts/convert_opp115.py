"""
Convert OPP-115 prepared JSON to pipeline-compatible all_segments.json format.

Reads:  data/opp115/opp115_prepared.json
Writes: opp115_experiment/all_segments.json

Maps OPP-115 categories to OPPT taxonomy and formats segment IDs as
{domain}_{segment_id+1:03d} (e.g., amazon.com_001).
"""

import json
from pathlib import Path
from datetime import datetime, timezone

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data"
INPUT_PATH = DATA_DIR / "opp115" / "opp115_prepared.json"
OUTPUT_PATH = REPO_ROOT / "opp115_experiment" / "all_segments.json"

# OPP-115 → OPPT category mapping
CATEGORY_MAP = {
    "First Party Collection/Use": "FIRST_PARTY",
    "Third Party Sharing/Collection": "THIRD_PARTY",
    "User Choice/Control": "USER_CHOICE",
    "Data Retention": "RETENTION",
    "Data Security": "SECURITY",
    "International and Specific Audiences": "INTL_SPECIFIC",
    "User Access, Edit and Deletion": "USER_ACCESS",
    "Policy Change": "POLICY_CHANGE",
    "Do Not Track": "TRACKING",
    "Other": "OTHER",
}


def convert():
    with open(INPUT_PATH) as f:
        opp115 = json.load(f)

    segments = []
    unmapped = set()

    for policy in opp115["policies"]:
        domain = policy["domain"]
        for seg in policy["segments"]:
            idx = seg["segment_id"]
            seg_id = f"{domain}_{idx + 1:03d}"

            # Map primary category
            raw_cat = seg.get("human_category", "Other")
            primary = CATEGORY_MAP.get(raw_cat)
            if primary is None:
                unmapped.add(raw_cat)
                primary = "OTHER"

            # Map secondary categories (unique human_categories minus primary)
            raw_cats = seg.get("human_categories", [])
            secondary = []
            for rc in raw_cats:
                mapped = CATEGORY_MAP.get(rc, "OTHER")
                if mapped != primary and mapped not in secondary:
                    secondary.append(mapped)

            segments.append({
                "segment_id": seg_id,
                "company": domain,
                "original_id": idx + 1,
                "heading_path": [],
                "start_line": None,
                "end_line": None,
                "text": seg["text"],
                "primary_category": primary,
                "secondary_categories": secondary,
                "confidence": None,
                "reasoning": None,
                "attributes": {},
                "agreement_rate": None,
                "dispute_resolved": False,
            })

    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "OPP-115 corpus (Wilson et al., 2016)",
        "total_segments": len(segments),
        "segments": segments,
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Converted {len(segments)} segments from {len(opp115['policies'])} policies")
    if unmapped:
        print(f"  Unmapped categories (→ OTHER): {unmapped}")
    print(f"  Output: {OUTPUT_PATH}")


if __name__ == "__main__":
    convert()
