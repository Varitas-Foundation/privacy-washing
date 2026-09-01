#!/usr/bin/env python3
"""
Prepare the OPP-115 corpus for the contradiction detection pipeline.

Parses the sanitized policy HTML files and annotation CSVs from the original
OPP-115 distribution into the prepared JSON format the pipeline consumes
(data/opp115/opp115_prepared.json). OPP-115 is not redistributed with this
repository; download it from https://usableprivacy.org/data and unpack it so
the corpus sits at data/opp115/OPP-115/ (containing sanitized_policies/ and
annotations/).

Usage:
  python scripts/prepare_opp115.py

This reproduces the preparation step used for the paper; the parsing and
majority-vote logic is unchanged from the as-run implementation.
"""

import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data"
OPP115_DIR = DATA_DIR / "opp115" / "OPP-115"
SANITIZED_DIR = OPP115_DIR / "sanitized_policies"
ANNOTATIONS_DIR = OPP115_DIR / "annotations"
OUTPUT_PATH = DATA_DIR / "opp115" / "opp115_prepared.json"

# OPP-115 uses these 10 categories (as they appear in annotation files)
OPP115_CATEGORIES = {
    "First Party Collection/Use",
    "Third Party Sharing/Collection",
    "User Choice/Control",
    "User Access, Edit and Deletion",
    "Data Retention",
    "Data Security",
    "Policy Change",
    "Do Not Track",
    "International and Specific Audiences",
    "Other",
}

# Canonical order, used for tie-breaking in majority votes
OPP115_CATEGORY_ORDER = [
    "First Party Collection/Use",
    "Third Party Sharing/Collection",
    "User Choice/Control",
    "User Access, Edit and Deletion",
    "Data Retention",
    "Data Security",
    "Policy Change",
    "Do Not Track",
    "International and Specific Audiences",
    "Other",
]


def parse_sanitized_policy(html_path: Path) -> list[dict]:
    """
    Parse a sanitized policy HTML file into segments.
    Segments are separated by '|||' in the file.

    Returns list of {segment_id, text} dicts.
    """
    text = html_path.read_text(encoding="utf-8", errors="replace")

    # Split on the segment separator
    raw_segments = text.split("|||")

    segments = []
    for i, seg in enumerate(raw_segments):
        # Clean up HTML tags
        clean = re.sub(r"<[^>]+>", " ", seg)
        clean = re.sub(r"\s+", " ", clean).strip()

        if clean:  # Skip empty segments
            segments.append({
                "segment_id": i,
                "text": clean
            })

    return segments


def parse_annotations(csv_path: Path) -> dict[int, list[str]]:
    """
    Parse an OPP-115 annotation CSV file.

    Returns dict mapping segment_id -> list of categories assigned by annotators.
    Multiple annotators may assign different categories to the same segment,
    and each annotator may assign multiple data practices to one segment.
    """
    segment_categories = defaultdict(list)

    with open(csv_path, "r", encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 6:
                continue

            try:
                segment_id = int(row[4])  # Column E (0-indexed as 4)
                category = row[5]  # Column F

                if category in OPP115_CATEGORIES:
                    segment_categories[segment_id].append(category)
            except (ValueError, IndexError):
                continue

    return dict(segment_categories)


def get_majority_category(categories: list[str]) -> Optional[str]:
    """
    Get the majority category from a list of annotations.

    OPP-115 has 3 annotators per policy. For a segment, we take the
    most frequent category. If there's a tie, we pick the first in our
    canonical order.
    """
    if not categories:
        return None

    counts = Counter(categories)
    max_count = max(counts.values())

    # Get all categories with the max count (handles ties)
    top_categories = [cat for cat, cnt in counts.items() if cnt == max_count]

    if len(top_categories) == 1:
        return top_categories[0]

    # Break ties using canonical order
    for cat in OPP115_CATEGORY_ORDER:
        if cat in top_categories:
            return cat

    return top_categories[0]


def prepare_opp115_data() -> dict:
    """
    Parse all OPP-115 data and prepare for the pipeline.

    Returns a dict with:
    - policies: list of {policy_id, domain, segments: [{segment_id, text, human_category}]}
    - statistics: summary stats
    """
    if not OPP115_DIR.exists():
        raise FileNotFoundError(
            f"OPP-115 corpus not found at {OPP115_DIR}\n"
            "Download from https://usableprivacy.org/data"
        )

    policies = []
    total_segments = 0
    segments_with_annotations = 0

    # Find all policies
    for html_file in sorted(SANITIZED_DIR.glob("*.html")):
        policy_id = html_file.stem  # e.g., "105_amazon.com"
        parts = policy_id.split("_", 1)
        numeric_id = parts[0]
        domain = parts[1] if len(parts) > 1 else policy_id

        # Parse segments
        segments = parse_sanitized_policy(html_file)
        total_segments += len(segments)

        # Parse annotations
        csv_file = ANNOTATIONS_DIR / f"{policy_id}.csv"
        if csv_file.exists():
            annotations = parse_annotations(csv_file)
        else:
            annotations = {}

        # Match segments with their human annotations
        for seg in segments:
            seg_id = seg["segment_id"]
            if seg_id in annotations:
                seg["human_categories"] = annotations[seg_id]
                seg["human_category"] = get_majority_category(annotations[seg_id])
                segments_with_annotations += 1
            else:
                seg["human_categories"] = []
                seg["human_category"] = None

        policies.append({
            "policy_id": policy_id,
            "numeric_id": numeric_id,
            "domain": domain,
            "segments": segments
        })

    return {
        "policies": policies,
        "statistics": {
            "total_policies": len(policies),
            "total_segments": total_segments,
            "segments_with_annotations": segments_with_annotations,
            "annotation_coverage": segments_with_annotations / total_segments if total_segments > 0 else 0
        }
    }


def main():
    print("Preparing OPP-115 data...")
    data = prepare_opp115_data()

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(data, f, indent=2)

    stats = data["statistics"]
    print("\nStatistics:")
    print(f"  Total policies: {stats['total_policies']}")
    print(f"  Total segments: {stats['total_segments']}")
    print(f"  Annotated segments: {stats['segments_with_annotations']}")
    print(f"  Coverage: {stats['annotation_coverage']:.1%}")
    print(f"\nSaved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
