"""
Extract fine-grained attributes from raw OPP-115 annotation CSVs.

Creates an attribute file in the same format as oppt_v2_attribute_review.json,
enabling annotation-guided statement extraction for OPP-115.

Key insight: OPP-115 HAS Does/Does Not polarity annotations:
  - 13,464 "Does" annotations (95.1%)
  - 692 "Does Not" annotations (4.9%)

This was previously overlooked, leading to unnecessary LLM inference.

Input:  data/opp115/OPP-115/annotations/*.csv
Output: opp115_experiment_*/opp115_attributes.json
"""

import csv
import json
import os
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data"
OPP115_ANNOTATIONS_DIR = DATA_DIR / "opp115" / "OPP-115" / "annotations"

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


def parse_opp115_csv(filepath: Path) -> list[dict]:
    """Parse a single OPP-115 annotation CSV file.

    CSV columns:
    0: annotation_id
    1: batch_id
    2: annotator_id
    3: policy_id
    4: segment_id (0-indexed)
    5: category_name
    6: attribute-value pairs (JSON)
    7: policy_url
    8: date
    """
    annotations = []

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 7:
                continue

            try:
                annotation_id = row[0]
                annotator_id = row[2]
                policy_id = row[3]
                segment_id = int(row[4])
                category = row[5]
                attrs_json = row[6]

                # Parse attributes JSON
                try:
                    attrs = json.loads(attrs_json)
                except json.JSONDecodeError:
                    attrs = {}

                annotations.append({
                    "annotation_id": annotation_id,
                    "annotator_id": annotator_id,
                    "policy_id": policy_id,
                    "segment_id": segment_id,
                    "category": category,
                    "attributes": attrs,
                })
            except (ValueError, IndexError):
                continue

    return annotations


def extract_attribute_value(attrs: dict, attr_name: str) -> str | list | None:
    """Extract a single attribute value from OPP-115 attribute dict.

    OPP-115 attributes have structure:
    {
        "Attribute Name": {
            "value": "the value",
            "selectedText": "...",
            "startIndexInSegment": N,
            "endIndexInSegment": M
        }
    }
    """
    if attr_name not in attrs:
        return None

    attr_data = attrs[attr_name]
    if isinstance(attr_data, dict):
        return attr_data.get("value")
    return attr_data


def convert_opp115_attributes(attrs: dict, category: str) -> dict:
    """Convert OPP-115 attribute format to OPPT format."""
    result = {}

    # Does/Does Not → does_does_not
    does_val = extract_attribute_value(attrs, "Does/Does Not")
    if does_val:
        result["does_does_not"] = does_val

    # Action fields (category-specific)
    if category == "First Party Collection/Use":
        action = extract_attribute_value(attrs, "Action First-Party")
        if action and action != "not-selected":
            result["action"] = [action]
    elif category == "Third Party Sharing/Collection":
        action = extract_attribute_value(attrs, "Action Third Party")
        if action and action != "not-selected":
            result["action"] = [action]

    # Personal Information Type
    pi_type = extract_attribute_value(attrs, "Personal Information Type")
    if pi_type and pi_type not in ("not-selected", "Unspecified"):
        result["personal_information_type"] = [pi_type]

    # Purpose
    purpose = extract_attribute_value(attrs, "Purpose")
    if purpose and purpose not in ("not-selected", "Unspecified"):
        result["purpose"] = [purpose]

    # Collection Mode
    coll_mode = extract_attribute_value(attrs, "Collection Mode")
    if coll_mode and coll_mode not in ("not-selected", "Unspecified"):
        result["collection_mode"] = coll_mode

    # Identifiability
    ident = extract_attribute_value(attrs, "Identifiability")
    if ident and ident not in ("not-selected", "Unspecified"):
        result["identifiability"] = ident

    # User Type
    user_type = extract_attribute_value(attrs, "User Type")
    if user_type and user_type not in ("not-selected", "Unspecified"):
        result["user_type"] = user_type

    # Third Party Entity (for third party category)
    if category == "Third Party Sharing/Collection":
        tp_entity = extract_attribute_value(attrs, "Third Party Entity")
        if tp_entity and tp_entity not in ("not-selected", "Unspecified"):
            result["third_party_entity"] = tp_entity

    # Choice Type/Scope
    choice_type = extract_attribute_value(attrs, "Choice Type")
    if choice_type and choice_type not in ("not-selected", "Unspecified"):
        result["choice_type"] = choice_type

    choice_scope = extract_attribute_value(attrs, "Choice Scope")
    if choice_scope and choice_scope not in ("not-selected", "Unspecified"):
        result["choice_scope"] = choice_scope

    return result


def build_segment_attributes(all_annotations: list[dict]) -> dict:
    """Group annotations by policy/segment and build attribute structure.

    Returns dict mapping segment_id → segment data with attributes_by_annotator.
    """
    # Group by policy_id + segment_id
    segments = defaultdict(lambda: {
        "annotations": [],
        "categories": [],
    })

    for ann in all_annotations:
        key = (ann["policy_id"], ann["segment_id"])
        segments[key]["annotations"].append(ann)
        segments[key]["categories"].append(ann["category"])

    # Build output structure
    result = {}

    for (policy_id, seg_idx), seg_data in segments.items():
        # Extract domain from policy_id (e.g., "3736" from annotations → domain from filename)
        # The segment_id format should be domain_NNN
        # We need to track the domain separately

        # Determine primary category (majority vote)
        from collections import Counter
        cat_counts = Counter(seg_data["categories"])
        primary_cat = cat_counts.most_common(1)[0][0]

        # Group annotations by annotator
        annotator_attrs = defaultdict(dict)
        annotator_ids = set()

        for ann in seg_data["annotations"]:
            ann_id = ann["annotator_id"]
            annotator_ids.add(ann_id)
            cat = ann["category"]
            oppt_cat = CATEGORY_MAP.get(cat, "OTHER")

            # Convert attributes
            converted = convert_opp115_attributes(ann["attributes"], cat)
            if converted:
                # Merge with existing (in case multiple annotations for same category)
                if oppt_cat in annotator_attrs[ann_id]:
                    existing = annotator_attrs[ann_id][oppt_cat]
                    for k, v in converted.items():
                        if k not in existing:
                            existing[k] = v
                        elif isinstance(v, list) and isinstance(existing[k], list):
                            existing[k] = list(set(existing[k] + v))
                else:
                    annotator_attrs[ann_id][oppt_cat] = converted

        # Build segment entry
        oppt_primary = CATEGORY_MAP.get(primary_cat, "OTHER")

        # Rename annotators to annotator_1, annotator_2, annotator_3
        sorted_annotators = sorted(annotator_ids)
        renamed_attrs = {}
        for i, ann_id in enumerate(sorted_annotators[:3], 1):
            renamed_attrs[f"annotator_{i}"] = dict(annotator_attrs[ann_id])

        result[(policy_id, seg_idx)] = {
            "policy_id": policy_id,
            "segment_id": seg_idx,
            "primary_category": oppt_primary,
            "attributes_by_annotator": renamed_attrs,
            "annotators_with_attributes": list(renamed_attrs.keys()),
        }

    return result


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Extract OPP-115 fine-grained attributes")
    parser.add_argument("--output-dir", type=str, required=True,
                        help="Output directory for opp115_attributes.json")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    if not output_dir.is_absolute():
        output_dir = (REPO_ROOT / output_dir).resolve()

    print(f"Parsing OPP-115 annotations from {OPP115_ANNOTATIONS_DIR}")

    # Parse all annotation CSVs
    all_annotations = []
    policy_domains = {}  # Map policy_id → domain

    for csv_file in sorted(OPP115_ANNOTATIONS_DIR.glob("*.csv")):
        # Extract domain from filename (e.g., "26_nytimes.com.csv" → "nytimes.com")
        filename = csv_file.stem
        parts = filename.split("_", 1)
        if len(parts) == 2:
            policy_num, domain = parts
            policy_domains[policy_num] = domain

        annotations = parse_opp115_csv(csv_file)
        all_annotations.extend(annotations)
        print(f"  {csv_file.name}: {len(annotations)} annotations")

    print(f"\nTotal annotations: {len(all_annotations)}")

    # Count Does/Does Not usage
    does_count = 0
    does_not_count = 0
    for ann in all_annotations:
        does_val = extract_attribute_value(ann["attributes"], "Does/Does Not")
        if does_val == "Does":
            does_count += 1
        elif does_val == "Does Not":
            does_not_count += 1

    print(f"\nDoes/Does Not distribution:")
    print(f"  Does: {does_count}")
    print(f"  Does Not: {does_not_count}")

    # Build segment-level attributes
    print("\nBuilding segment-level attributes...")
    segment_attrs = build_segment_attributes(all_annotations)
    print(f"  {len(segment_attrs)} segments with attributes")

    # Convert to list format matching OPPT structure
    segments_list = []
    for (policy_id, seg_idx), seg_data in sorted(segment_attrs.items()):
        domain = policy_domains.get(policy_id, f"unknown_{policy_id}")
        segment_id = f"{domain}_{seg_idx + 1:03d}"

        segments_list.append({
            "segment_id": segment_id,
            "company": domain,
            "primary_category": seg_data["primary_category"],
            "secondary_categories": [],
            "attributes_by_annotator": seg_data["attributes_by_annotator"],
            "annotators_with_attributes": seg_data["annotators_with_attributes"],
        })

    # Count segments with Does/Does Not
    segments_with_does = 0
    segments_with_does_not = 0
    for seg in segments_list:
        has_does = False
        has_does_not = False
        for ann_attrs in seg["attributes_by_annotator"].values():
            for cat_attrs in ann_attrs.values():
                ddn = cat_attrs.get("does_does_not")
                if ddn == "Does":
                    has_does = True
                elif ddn == "Does Not":
                    has_does_not = True
        if has_does:
            segments_with_does += 1
        if has_does_not:
            segments_with_does_not += 1

    print(f"\nSegment-level polarity:")
    print(f"  Segments with 'Does': {segments_with_does}")
    print(f"  Segments with 'Does Not': {segments_with_does_not}")

    # Write output
    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "purpose": "OPP-115 fine-grained attributes extracted from original annotations",
        "source": "OPP-115 corpus (Wilson et al., 2016)",
        "annotator_mapping": {
            "annotator_1": "OPP-115 human annotator 1",
            "annotator_2": "OPP-115 human annotator 2",
            "annotator_3": "OPP-115 human annotator 3",
        },
        "statistics": {
            "total_segments": len(segments_list),
            "segments_with_does": segments_with_does,
            "segments_with_does_not": segments_with_does_not,
            "total_does_annotations": does_count,
            "total_does_not_annotations": does_not_count,
        },
        "segments": segments_list,
    }

    output_path = output_dir / "opp115_attributes.json"
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nOutput written to {output_path}")
    print(f"  File size: {output_path.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
