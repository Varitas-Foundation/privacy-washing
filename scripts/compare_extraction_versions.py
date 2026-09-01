"""
Compare Extraction Versions (v1 vs v2)

Generates comparison analysis between basic extraction (v1) and enhanced
extraction (v2) with subject/aspect/scope/qualifier metadata. Used to
validate that enhanced filtering reduces false positives while preserving
true contradictions.

Usage:
  python compare_extraction_versions.py \
    --v1-dir opp115_experiment \
    --v2-dir opp115_experiment_annotation_guided_20260203

Output:
  comparison_report.md in v2 directory
"""

import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def parse_args():
    parser = argparse.ArgumentParser(description="Compare v1 and v2 extraction results")
    parser.add_argument("--v1-dir", type=str, required=True,
                        help="Directory with v1 extraction results (baseline)")
    parser.add_argument("--v2-dir", type=str, required=True,
                        help="Directory with v2 extraction results (enhanced)")
    parser.add_argument("--output", type=str, default=None,
                        help="Output file path (default: v2_dir/comparison_report.md)")
    return parser.parse_args()


def load_experiment_data(data_dir: Path) -> dict:
    """Load statements and contradictions from an experiment directory."""
    statements_path = data_dir / "statements.json"
    contradictions_path = data_dir / "statement_contradictions.json"
    judge_results_path = data_dir / "statement_judge_results.json"

    data = {"dir": str(data_dir)}

    if statements_path.exists():
        with open(statements_path) as f:
            stmt_data = json.load(f)
        data["statements"] = stmt_data["statements"]
        data["statement_metadata"] = stmt_data.get("metadata", {})
        data["statement_summary"] = stmt_data.get("summary", {})
    else:
        data["statements"] = []
        data["statement_metadata"] = {}
        data["statement_summary"] = {}

    if contradictions_path.exists():
        with open(contradictions_path) as f:
            contra_data = json.load(f)
        data["pairs"] = contra_data.get("pairs", [])
        data["contradictions"] = [p for p in data["pairs"] if p.get("is_contradiction")]
        data["contradiction_config"] = contra_data.get("config", {})
        data["filter_statistics"] = contra_data.get("filter_statistics", {})
        data["contradiction_summary"] = contra_data.get("summary", {})
    else:
        data["pairs"] = []
        data["contradictions"] = []
        data["contradiction_config"] = {}
        data["filter_statistics"] = {}
        data["contradiction_summary"] = {}

    if judge_results_path.exists():
        with open(judge_results_path) as f:
            judge_data = json.load(f)
        data["judge_results"] = judge_data.get("results", [])
        data["judge_summary"] = judge_data.get("summary", {})
    else:
        data["judge_results"] = []
        data["judge_summary"] = {}

    return data


def compute_field_distributions(statements: list) -> dict:
    """Compute distributions for v2 fields."""
    if not statements:
        return {}

    # Check if statements have v2 fields
    sample = statements[0]
    has_v2 = "subject" in sample

    if not has_v2:
        return {"v2_fields": False}

    return {
        "v2_fields": True,
        "subject": dict(Counter(s.get("subject", "UNKNOWN") for s in statements)),
        "aspect": dict(Counter(s.get("aspect", "UNKNOWN") for s in statements)),
        "scope": dict(Counter(s.get("scope", "UNKNOWN") for s in statements)),
        "has_qualifiers": sum(1 for s in statements if s.get("qualifiers")),
    }


def find_overlap_contradictions(v1_contradictions: list, v2_contradictions: list) -> dict:
    """Analyze overlap between v1 and v2 detected contradictions."""
    # Build sets of pair IDs
    v1_pairs = {p["pair_id"] for p in v1_contradictions}
    v2_pairs = {p["pair_id"] for p in v2_contradictions}

    common = v1_pairs & v2_pairs
    v1_only = v1_pairs - v2_pairs
    v2_only = v2_pairs - v1_pairs

    return {
        "common": len(common),
        "v1_only": len(v1_only),
        "v2_only": len(v2_only),
        "v1_only_list": sorted(v1_only)[:20],  # Sample
        "v2_only_list": sorted(v2_only)[:20],
    }


def generate_report(v1_data: dict, v2_data: dict) -> str:
    """Generate markdown comparison report."""
    lines = []
    lines.append("# Extraction Version Comparison Report")
    lines.append(f"\nGenerated: {datetime.now(timezone.utc).isoformat()}")
    lines.append("")

    # Directories
    lines.append("## Experiment Directories")
    lines.append(f"- **v1 (baseline):** `{v1_data['dir']}`")
    lines.append(f"- **v2 (enhanced):** `{v2_data['dir']}`")
    lines.append("")

    # Statement Extraction Comparison
    lines.append("## Statement Extraction")
    lines.append("")
    lines.append("| Metric | v1 | v2 | Delta |")
    lines.append("|--------|----|----|-------|")

    v1_total = len(v1_data["statements"])
    v2_total = len(v2_data["statements"])
    delta = v2_total - v1_total
    lines.append(f"| Total statements | {v1_total:,} | {v2_total:,} | {delta:+,} |")

    v1_commits = sum(1 for s in v1_data["statements"] if s["type"] == "COMMITMENT")
    v2_commits = sum(1 for s in v2_data["statements"] if s["type"] == "COMMITMENT")
    lines.append(f"| COMMITMENT | {v1_commits:,} | {v2_commits:,} | {v2_commits - v1_commits:+,} |")

    v1_practices = sum(1 for s in v1_data["statements"] if s["type"] == "PRACTICE")
    v2_practices = sum(1 for s in v2_data["statements"] if s["type"] == "PRACTICE")
    lines.append(f"| PRACTICE | {v1_practices:,} | {v2_practices:,} | {v2_practices - v1_practices:+,} |")

    lines.append("")

    # v2 Field Distributions
    v2_dist = compute_field_distributions(v2_data["statements"])
    if v2_dist.get("v2_fields"):
        lines.append("### v2 Enhanced Field Distributions")
        lines.append("")

        lines.append("**Subject Distribution:**")
        for subject, count in sorted(v2_dist["subject"].items(), key=lambda x: -x[1]):
            pct = 100 * count / v2_total if v2_total else 0
            lines.append(f"- {subject}: {count:,} ({pct:.1f}%)")
        lines.append("")

        lines.append("**Aspect Distribution:**")
        for aspect, count in sorted(v2_dist["aspect"].items(), key=lambda x: -x[1]):
            pct = 100 * count / v2_total if v2_total else 0
            lines.append(f"- {aspect}: {count:,} ({pct:.1f}%)")
        lines.append("")

        lines.append("**Scope Distribution:**")
        for scope, count in sorted(v2_dist["scope"].items(), key=lambda x: -x[1]):
            pct = 100 * count / v2_total if v2_total else 0
            lines.append(f"- {scope}: {count:,} ({pct:.1f}%)")
        lines.append("")

        qual_pct = 100 * v2_dist["has_qualifiers"] / v2_total if v2_total else 0
        lines.append(f"**Statements with qualifiers:** {v2_dist['has_qualifiers']:,} ({qual_pct:.1f}%)")
        lines.append("")

    # Contradiction Detection Comparison
    lines.append("## Contradiction Detection")
    lines.append("")

    v1_pairs = len(v1_data["pairs"])
    v2_pairs = len(v2_data["pairs"])
    v1_contras = len(v1_data["contradictions"])
    v2_contras = len(v2_data["contradictions"])

    lines.append("| Metric | v1 | v2 | Delta | % Reduction |")
    lines.append("|--------|----|----|-------|-------------|")
    lines.append(f"| Total pairs evaluated | {v1_pairs:,} | {v2_pairs:,} | {v2_pairs - v1_pairs:+,} | {100*(v1_pairs - v2_pairs)/v1_pairs if v1_pairs else 0:.1f}% |")
    lines.append(f"| Contradictions detected | {v1_contras:,} | {v2_contras:,} | {v2_contras - v1_contras:+,} | {100*(v1_contras - v2_contras)/v1_contras if v1_contras else 0:.1f}% |")

    v1_rate = v1_contras / v1_pairs if v1_pairs else 0
    v2_rate = v2_contras / v2_pairs if v2_pairs else 0
    lines.append(f"| Contradiction rate | {100*v1_rate:.2f}% | {100*v2_rate:.2f}% | {100*(v2_rate - v1_rate):+.2f}% | - |")
    lines.append("")

    # Enhanced Filter Statistics
    if v2_data["filter_statistics"]:
        lines.append("### Enhanced Filtering Impact (v2)")
        lines.append("")
        lines.append("| Filter | Pairs Excluded |")
        lines.append("|--------|----------------|")
        for key, count in sorted(v2_data["filter_statistics"].items()):
            if count > 0:
                lines.append(f"| {key.replace('_', ' ').title()} | {count:,} |")
        lines.append("")

    # Contradiction Overlap Analysis
    overlap = find_overlap_contradictions(v1_data["contradictions"], v2_data["contradictions"])
    lines.append("### Contradiction Overlap Analysis")
    lines.append("")
    lines.append(f"- **Common to both:** {overlap['common']:,} (preserved true positives)")
    lines.append(f"- **v1 only (filtered by v2):** {overlap['v1_only']:,} (potential FP reduction)")
    lines.append(f"- **v2 only (new in v2):** {overlap['v2_only']:,}")
    lines.append("")

    if overlap["v1_only_list"]:
        lines.append("**Sample pairs removed by v2 filtering (potential FPs):**")
        for pair_id in overlap["v1_only_list"][:10]:
            lines.append(f"- `{pair_id}`")
        lines.append("")

    # Judge Verification Comparison (if available)
    if v1_data["judge_results"] and v2_data["judge_results"]:
        lines.append("## Judge Verification Comparison")
        lines.append("")

        v1_js = v1_data["judge_summary"]
        v2_js = v2_data["judge_summary"]

        lines.append("| Metric | v1 | v2 | Delta |")
        lines.append("|--------|----|----|-------|")

        v1_confirmed = v1_js.get("total_confirmed", 0)
        v2_confirmed = v2_js.get("total_confirmed", 0)
        lines.append(f"| Judge-confirmed contradictions | {v1_confirmed:,} | {v2_confirmed:,} | {v2_confirmed - v1_confirmed:+,} |")

        v1_precision = v1_js.get("confirmation_rate", 0)
        v2_precision = v2_js.get("confirmation_rate", 0)
        lines.append(f"| Confirmation rate (precision) | {100*v1_precision:.1f}% | {100*v2_precision:.1f}% | {100*(v2_precision - v1_precision):+.1f}% |")
        lines.append("")

    # Summary and Recommendations
    lines.append("## Summary")
    lines.append("")

    pairs_reduction = 100 * (v1_pairs - v2_pairs) / v1_pairs if v1_pairs else 0
    contra_reduction = 100 * (v1_contras - v2_contras) / v1_contras if v1_contras else 0

    lines.append(f"The enhanced v2 extraction with metadata-based filtering:")
    lines.append(f"- Reduced pairs evaluated by **{pairs_reduction:.1f}%** ({v1_pairs - v2_pairs:,} pairs)")
    lines.append(f"- Reduced detected contradictions by **{contra_reduction:.1f}%** ({v1_contras - v2_contras:,} contradictions)")
    lines.append(f"- Preserved **{overlap['common']:,}** contradictions from v1 baseline")
    lines.append("")

    if v1_data["judge_results"] and v2_data["judge_results"]:
        precision_delta = (v2_js.get("confirmation_rate", 0) - v1_js.get("confirmation_rate", 0)) * 100
        lines.append(f"- Judge confirmation rate changed by **{precision_delta:+.1f}%**")
        lines.append("")

    return "\n".join(lines)


def main():
    args = parse_args()

    # Resolve directories
    v1_dir = Path(args.v1_dir)
    if not v1_dir.is_absolute():
        v1_dir = (REPO_ROOT / v1_dir).resolve()

    v2_dir = Path(args.v2_dir)
    if not v2_dir.is_absolute():
        v2_dir = (REPO_ROOT / v2_dir).resolve()

    print(f"Loading v1 data from {v1_dir}")
    v1_data = load_experiment_data(v1_dir)
    print(f"  Statements: {len(v1_data['statements'])}")
    print(f"  Contradictions: {len(v1_data['contradictions'])}")

    print(f"\nLoading v2 data from {v2_dir}")
    v2_data = load_experiment_data(v2_dir)
    print(f"  Statements: {len(v2_data['statements'])}")
    print(f"  Contradictions: {len(v2_data['contradictions'])}")

    # Generate report
    print("\nGenerating comparison report...")
    report = generate_report(v1_data, v2_data)

    # Write output
    output_path = Path(args.output) if args.output else v2_dir / "comparison_report.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report)
    print(f"\nReport written to {output_path}")


if __name__ == "__main__":
    main()
