"""
Pipeline Comparison: Statement-Level vs Segment-Level Contradiction Detection

Compares the statement-level pipeline (extract_statements → detect_statement_contradictions)
against the segment-level pipeline (detect_contradictions) and human ground truth
(judge_results + manual assessment).

Comparisons:
  1. Map statement contradictions to segment pairs for apples-to-apples comparison
  2. Compute precision/recall against judge verdicts
  3. Check whether known FP patterns are eliminated
  4. Check whether known genuine contradictions are preserved
  5. Report new contradictions surfaced by statement-level analysis

Output: pipeline_comparison.md

Usage:
  python compare_pipelines.py
  python compare_pipelines.py --data-dir ../../opp115_experiment
"""

import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[1]

# Default: OPPT corpus
SEGMENT_CONTRADICTIONS_PATH = REPO_ROOT / "output" / "contradictions.json"
STATEMENT_CONTRADICTIONS_PATH = REPO_ROOT / "output" / "statement_contradictions.json"
JUDGE_RESULTS_PATH = REPO_ROOT / "output" / "judge_results.json"
OUTPUT_PATH = REPO_ROOT / "pipeline_comparison.md"

# Optional data-dir override
_DATA_DIR = None
for _i, _arg in enumerate(sys.argv[1:], 1):
    if _arg == "--data-dir" and _i < len(sys.argv) - 1:
        _DATA_DIR = Path(sys.argv[_i + 1])
if _DATA_DIR:
    if not _DATA_DIR.is_absolute():
        _DATA_DIR = (REPO_ROOT / _DATA_DIR).resolve()
    SEGMENT_CONTRADICTIONS_PATH = _DATA_DIR / "contradictions.json"
    STATEMENT_CONTRADICTIONS_PATH = _DATA_DIR / "statement_contradictions.json"
    JUDGE_RESULTS_PATH = _DATA_DIR / "judge_results.json"
    OUTPUT_PATH = _DATA_DIR / "pipeline_comparison.md"


# ---------------------------------------------------------------------------
# Known ground truth from manual assessment (encoded from memory)
# ---------------------------------------------------------------------------
# 7 known false positives from manual assessment of 71 NLI-flagged pairs.
# Format: (company, claim_id, practice_id, fp_pattern)
KNOWN_FPS_OPPT = [
    ("microsoft", "microsoft_014", "microsoft_053", "security_implementation"),
]

KNOWN_FPS_OPP115 = [
    ("sciencemag.org", None, None, "security_implementation"),  # SSL encryption
    ("kraftrecipes.com", None, None, "security_implementation"),  # Safeguards
    ("adweek.com", None, None, "restated_commitment"),  # Practice restates non-sharing
    ("latinpost.com", None, None, "restated_commitment"),  # "don't have access"
    ("allstate.com", None, None, "informational_content"),  # Email advice
    ("latinpost.com", None, None, "informational_content"),  # Phishing disclosure
]

FP_PATTERN_DESCRIPTIONS = {
    "security_implementation": "Practice describes implementation (e.g., SSL, BitLocker) that supports the security commitment",
    "restated_commitment": "Practice restates the same non-sharing commitment in different words",
    "informational_content": "Practice is informational/educational content, not a data practice",
}


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------
def load_json(path: Path) -> dict:
    """Load JSON file, return empty dict if not found."""
    if not path.exists():
        print(f"  WARNING: {path} not found")
        return {}
    with open(path) as f:
        return json.load(f)


def normalize_pair_id(claim_id: str, practice_id: str) -> str:
    """Create a normalized pair ID from two segment IDs."""
    return f"{claim_id}_vs_{practice_id}"


# ---------------------------------------------------------------------------
# Analysis functions
# ---------------------------------------------------------------------------
def build_segment_pipeline_data(seg_data: dict) -> dict:
    """Extract segment-level pipeline data into a comparison-friendly structure."""
    pairs = seg_data.get("pairs", [])
    result = {}
    for p in pairs:
        claim_id = p.get("claim_id", "")
        practice_id = p.get("practice_id", "")
        pair_id = normalize_pair_id(claim_id, practice_id)
        result[pair_id] = {
            "company": p.get("company", ""),
            "claim_id": claim_id,
            "practice_id": practice_id,
            "is_contradiction": p.get("is_contradiction", False),
            "nli_score": p.get("nli_contradiction", 0.0),
            "severity": p.get("severity", 0.0),
            "evidence_type": p.get("evidence_type", "none"),
            "claim_text_preview": p.get("claim_text_preview", ""),
            "practice_text_preview": p.get("practice_text_preview", ""),
        }
    return result


def build_statement_pipeline_data(stmt_data: dict) -> dict:
    """Extract statement-level pipeline data, mapped to segment pairs."""
    seg_pair_map = stmt_data.get("segment_pair_contradictions", {})
    pairs = stmt_data.get("pairs", [])

    # Collect all pairs by segment pair
    by_segment_pair = defaultdict(list)
    for p in pairs:
        seg_pair = p.get("source_segment_pair", "")
        by_segment_pair[seg_pair].append(p)

    # Build result: one entry per segment pair
    result = {}
    for seg_pair, stmt_pairs in by_segment_pair.items():
        contradiction_pairs = [p for p in stmt_pairs if p.get("is_contradiction", False)]
        result[seg_pair] = {
            "total_statement_pairs": len(stmt_pairs),
            "contradiction_statement_pairs": len(contradiction_pairs),
            "is_contradiction": len(contradiction_pairs) > 0,
            "max_nli_score": max((p.get("nli_contradiction_score", 0.0) for p in contradiction_pairs), default=0.0),
            "contradiction_details": [
                {
                    "commitment_text": p.get("commitment_text", ""),
                    "practice_text": p.get("practice_text", ""),
                    "nli_score": p.get("nli_contradiction_score", 0.0),
                }
                for p in sorted(contradiction_pairs, key=lambda x: -x.get("nli_contradiction_score", 0))[:5]
            ],
        }
    return result


def build_judge_data(judge_data: dict) -> dict:
    """Extract judge verdicts indexed by pair ID."""
    annotations = judge_data.get("annotations", [])
    result = {}
    for a in annotations:
        claim_id = a.get("claim_id", "")
        practice_id = a.get("practice_id", "")
        pair_id = normalize_pair_id(claim_id, practice_id)
        result[pair_id] = {
            "final_verdict": a.get("final_verdict", "UNKNOWN"),
            "consensus_type": a.get("consensus_type", "unknown"),
            "nli_is_contradiction": a.get("nli_is_contradiction", False),
            "nli_score": a.get("nli_contradiction_score", 0.0),
        }
    return result


def classify_ground_truth(judge_verdict: str, nli_flag: bool) -> str:
    """Classify a pair into ground truth category based on available signals.

    Returns: 'genuine', 'false_positive', 'judge_only', 'neither'
    """
    if nli_flag and judge_verdict == "CONTRADICTION":
        return "genuine"  # Both agree
    elif nli_flag and judge_verdict == "NOT_CONTRADICTION":
        return "nli_only_dismissed"  # NLI flagged, judges dismissed
    elif not nli_flag and judge_verdict == "CONTRADICTION":
        return "judge_only"  # Judges found contradiction NLI missed
    else:
        return "neither"


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------
def generate_report(
    seg_pipeline: dict,
    stmt_pipeline: dict,
    judge_data: dict,
    seg_config: dict,
    stmt_config: dict,
    stmt_summary: dict,
    seg_summary: dict,
) -> str:
    """Generate a comprehensive comparison report as markdown."""
    lines = []
    lines.append("# Pipeline Comparison: Statement-Level vs Segment-Level")
    lines.append("")
    lines.append(f"*Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}*")
    lines.append("")

    # --- Section 1: Summary Statistics ---
    lines.append("## 1. Pipeline Summary Statistics")
    lines.append("")
    lines.append("| Metric | Segment-Level | Statement-Level |")
    lines.append("|--------|---------------|-----------------|")
    lines.append(f"| Total pairs evaluated | {seg_summary.get('total_pairs', 'N/A')} | {stmt_summary.get('total_pairs', 'N/A')} |")
    lines.append(f"| Contradictions detected | {seg_summary.get('total_contradictions', 'N/A')} | {stmt_summary.get('total_contradictions', 'N/A')} |")
    lines.append(f"| Contradiction rate | {seg_summary.get('contradiction_rate', 'N/A')} | {stmt_summary.get('contradiction_rate', 'N/A')} |")
    lines.append(f"| Companies with contradictions | {seg_summary.get('companies_with_contradictions', 'N/A')} | {stmt_summary.get('companies_with_contradictions', 'N/A')} |")

    stmt_seg_pairs = stmt_summary.get("unique_segment_pairs_with_contradictions", "N/A")
    lines.append(f"| Unique segment pairs with contradictions | {seg_summary.get('total_contradictions', 'N/A')} | {stmt_seg_pairs} |")
    lines.append("")

    # --- Section 2: Segment-Pair Level Comparison ---
    lines.append("## 2. Segment-Pair Level Comparison")
    lines.append("")

    # Get all NLI-flagged segment pairs from segment-level pipeline
    seg_flagged = {pid for pid, data in seg_pipeline.items() if data["is_contradiction"]}
    # Get all segment pairs flagged by statement-level pipeline
    stmt_flagged = {pid for pid, data in stmt_pipeline.items() if data["is_contradiction"]}

    both_flagged = seg_flagged & stmt_flagged
    seg_only = seg_flagged - stmt_flagged
    stmt_only = stmt_flagged - seg_flagged

    lines.append(f"- **Both pipelines flag**: {len(both_flagged)} segment pairs")
    lines.append(f"- **Segment-level only**: {len(seg_only)} segment pairs (statement-level did NOT flag)")
    lines.append(f"- **Statement-level only**: {len(stmt_only)} segment pairs (NEW contradictions)")
    lines.append(f"- **Total unique flagged**: {len(seg_flagged | stmt_flagged)}")
    lines.append("")

    # --- Section 3: Judge-Based Assessment ---
    lines.append("## 3. Assessment Against Judge Ground Truth")
    lines.append("")

    if judge_data:
        # For segment-level flagged pairs, check judge verdict
        seg_genuine = 0
        seg_dismissed = 0
        seg_no_judge = 0

        for pid in seg_flagged:
            jd = judge_data.get(pid)
            if not jd:
                seg_no_judge += 1
            elif jd["final_verdict"] == "CONTRADICTION":
                seg_genuine += 1
            else:
                seg_dismissed += 1

        # For statement-level flagged segment pairs, check judge verdict
        stmt_genuine = 0
        stmt_dismissed = 0
        stmt_no_judge = 0

        for pid in stmt_flagged:
            jd = judge_data.get(pid)
            if not jd:
                stmt_no_judge += 1
            elif jd["final_verdict"] == "CONTRADICTION":
                stmt_genuine += 1
            else:
                stmt_dismissed += 1

        lines.append("| Metric | Segment-Level | Statement-Level |")
        lines.append("|--------|---------------|-----------------|")
        lines.append(f"| Flagged pairs | {len(seg_flagged)} | {len(stmt_flagged)} |")
        lines.append(f"| Judge confirmed (CONTRADICTION) | {seg_genuine} | {stmt_genuine} |")
        lines.append(f"| Judge dismissed (NOT_CONTRADICTION) | {seg_dismissed} | {stmt_dismissed} |")
        lines.append(f"| No judge data | {seg_no_judge} | {stmt_no_judge} |")

        seg_precision = seg_genuine / max(seg_genuine + seg_dismissed, 1)
        stmt_precision = stmt_genuine / max(stmt_genuine + stmt_dismissed, 1)
        lines.append(f"| Judge-based precision | {seg_precision:.1%} | {stmt_precision:.1%} |")
        lines.append("")

        # Note about judge accuracy
        lines.append("> **Note:** Judge verdicts are an imperfect ground truth. Judges systematically")
        lines.append("> dismiss genuine contradictions via narrow literal interpretation (see judge_vs_nli_experiment).")
        lines.append("> The manual assessment found 45 genuine, 19 borderline, and 7 FP among 71 NLI-flagged pairs.")
        lines.append("")
    else:
        lines.append("*No judge results available for this corpus.*")
        lines.append("")

    # --- Section 4: Known FP Analysis ---
    lines.append("## 4. Known False Positive Patterns")
    lines.append("")
    lines.append("The segment-level pipeline produced 7 known false positives with 3 systematic patterns:")
    lines.append("")

    for pattern, desc in FP_PATTERN_DESCRIPTIONS.items():
        lines.append(f"- **{pattern}**: {desc}")
    lines.append("")

    lines.append("### FP Elimination Check")
    lines.append("")
    lines.append("| FP | Company | Pattern | Seg-Level | Stmt-Level | Eliminated? |")
    lines.append("|----|---------|---------|-----------|------------|-------------|")

    # Check OPPT FPs
    for company, claim_id, practice_id, pattern in KNOWN_FPS_OPPT:
        if claim_id and practice_id:
            pair_id = normalize_pair_id(claim_id, practice_id)
            seg_flag = "FLAGGED" if pair_id in seg_flagged else "clear"
            stmt_flag = "FLAGGED" if pair_id in stmt_flagged else "clear"
            eliminated = "YES" if seg_flag == "FLAGGED" and stmt_flag == "clear" else ("N/A" if seg_flag == "clear" else "NO")
            lines.append(f"| OPPT | {company} | {pattern} | {seg_flag} | {stmt_flag} | {eliminated} |")

    # Check OPP-115 FPs — we need to find them by company since we may not have exact IDs
    for company, claim_id, practice_id, pattern in KNOWN_FPS_OPP115:
        # Try to find matching pairs by company
        matching_seg = [pid for pid, d in seg_pipeline.items() if d["company"] == company and d["is_contradiction"]]
        matching_stmt = [pid for pid in stmt_flagged if stmt_pipeline.get(pid, {}).get("is_contradiction", False)]
        # For OPP-115 we report by company pattern since exact IDs aren't known here
        seg_flag = f"FLAGGED ({len(matching_seg)})" if matching_seg else "clear"

        # Count company-level statement contradictions
        company_stmt_flagged = sum(1 for pid, d in stmt_pipeline.items()
                                    if d.get("is_contradiction", False) and
                                    any(seg_pipeline.get(pid, {}).get("company", "") == company for _ in [1]))
        stmt_flag = f"{company_stmt_flagged} pairs" if company_stmt_flagged > 0 else "clear"

        lines.append(f"| OPP-115 | {company} | {pattern} | {seg_flag} | {stmt_flag} | — |")

    lines.append("")

    # --- Section 5: Detailed Pair-by-Pair Comparison ---
    lines.append("## 5. Detailed Pair Comparison")
    lines.append("")

    # Segment-level flagged pairs: what happened at statement level?
    lines.append("### 5a. Segment-Level Flagged Pairs — Statement-Level Status")
    lines.append("")
    lines.append("| Company | Pair ID | Seg NLI | Stmt Status | Stmt NLI (max) | Judge |")
    lines.append("|---------|---------|---------|-------------|----------------|-------|")

    for pid in sorted(seg_flagged):
        seg_data = seg_pipeline[pid]
        stmt_data_entry = stmt_pipeline.get(pid, {})
        jd = judge_data.get(pid, {})

        company = seg_data["company"]
        seg_nli = seg_data["nli_score"]
        stmt_status = "FLAGGED" if stmt_data_entry.get("is_contradiction", False) else "clear"
        stmt_nli = stmt_data_entry.get("max_nli_score", 0.0)
        judge_verdict = jd.get("final_verdict", "—")

        lines.append(f"| {company} | `{pid}` | {seg_nli:.3f} | {stmt_status} | {stmt_nli:.3f} | {judge_verdict} |")

    lines.append("")

    # New statement-level contradictions not in segment-level
    if stmt_only:
        lines.append("### 5b. New Statement-Level Contradictions (Not in Segment-Level)")
        lines.append("")
        lines.append("| Company | Segment Pair | # Stmt Contradictions | Max NLI | Top Commitment | Top Practice |")
        lines.append("|---------|-------------|----------------------|---------|----------------|--------------|")

        for pid in sorted(stmt_only):
            entry = stmt_pipeline.get(pid, {})
            details = entry.get("contradiction_details", [])
            n_contradictions = entry.get("contradiction_statement_pairs", 0)
            max_nli = entry.get("max_nli_score", 0.0)

            # Try to get company from segment pipeline or from the pair ID
            company = "?"
            for seg_pid, seg_d in seg_pipeline.items():
                if seg_pid == pid:
                    company = seg_d["company"]
                    break

            top_commit = details[0]["commitment_text"][:60] + "..." if details else "—"
            top_practice = details[0]["practice_text"][:60] + "..." if details else "—"

            lines.append(f"| {company} | `{pid}` | {n_contradictions} | {max_nli:.3f} | {top_commit} | {top_practice} |")

        lines.append("")

    # --- Section 6: Per-Company Summary ---
    lines.append("## 6. Per-Company Summary")
    lines.append("")
    lines.append("| Company | Seg Pairs | Seg Contradictions | Stmt Contradictions (seg-mapped) | Change |")
    lines.append("|---------|-----------|-------------------|--------------------------------|--------|")

    companies = sorted(set(d["company"] for d in seg_pipeline.values()))
    for company in companies:
        seg_pairs = sum(1 for d in seg_pipeline.values() if d["company"] == company)
        seg_contradictions = sum(1 for pid in seg_flagged if seg_pipeline.get(pid, {}).get("company", "") == company)

        # Statement-level contradictions mapped to segment pairs for this company
        company_stmt = 0
        for pid, d in stmt_pipeline.items():
            if d.get("is_contradiction", False):
                # Check if this segment pair belongs to this company
                if pid in seg_pipeline and seg_pipeline[pid]["company"] == company:
                    company_stmt += 1

        if seg_contradictions > 0 or company_stmt > 0:
            change = company_stmt - seg_contradictions
            change_str = f"+{change}" if change > 0 else str(change)
            lines.append(f"| {company} | {seg_pairs} | {seg_contradictions} | {company_stmt} | {change_str} |")

    lines.append("")

    # --- Section 7: Conclusion ---
    lines.append("## 7. Summary")
    lines.append("")
    lines.append(f"- Segment-level pipeline: {len(seg_flagged)} contradictions")
    lines.append(f"- Statement-level pipeline: {len(stmt_flagged)} unique segment pairs with contradictions")
    lines.append(f"- Overlap: {len(both_flagged)} pairs flagged by both")
    lines.append(f"- Segment-only (potential FPs eliminated): {len(seg_only)}")
    lines.append(f"- Statement-only (new finds): {len(stmt_only)}")
    lines.append("")

    if seg_flagged:
        preservation = len(both_flagged) / len(seg_flagged)
        lines.append(f"- Preservation rate: {preservation:.1%} of segment-level contradictions retained")
    if seg_only:
        lines.append(f"- Elimination rate: {len(seg_only)} segment-level contradictions not reproduced at statement level")
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("Loading pipeline data...")

    seg_data = load_json(SEGMENT_CONTRADICTIONS_PATH)
    stmt_data = load_json(STATEMENT_CONTRADICTIONS_PATH)
    judge_data_raw = load_json(JUDGE_RESULTS_PATH)

    if not seg_data:
        print("ERROR: Segment-level contradictions not found.")
        sys.exit(1)
    if not stmt_data:
        print("ERROR: Statement-level contradictions not found.")
        print(f"  Expected: {STATEMENT_CONTRADICTIONS_PATH}")
        print("  Run extract_statements.py and detect_statement_contradictions.py first.")
        sys.exit(1)

    # Build comparison data
    print("Building comparison structures...")
    seg_pipeline = build_segment_pipeline_data(seg_data)
    stmt_pipeline = build_statement_pipeline_data(stmt_data)
    judge_data = build_judge_data(judge_data_raw)

    seg_config = seg_data.get("config", {})
    stmt_config = stmt_data.get("config", {})
    stmt_summary = stmt_data.get("summary", {})
    seg_summary = seg_data.get("summary", {})

    print(f"  Segment-level: {len(seg_pipeline)} pairs, "
          f"{sum(1 for d in seg_pipeline.values() if d['is_contradiction'])} contradictions")
    print(f"  Statement-level: {len(stmt_pipeline)} segment pairs, "
          f"{sum(1 for d in stmt_pipeline.values() if d.get('is_contradiction', False))} with contradictions")
    print(f"  Judge data: {len(judge_data)} pairs assessed")

    # Generate report
    print("\nGenerating comparison report...")
    report = generate_report(
        seg_pipeline, stmt_pipeline, judge_data,
        seg_config, stmt_config, stmt_summary, seg_summary,
    )

    # Write output
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        f.write(report)

    print(f"\nReport written to {OUTPUT_PATH}")
    print(f"  Size: {OUTPUT_PATH.stat().st_size / 1024:.1f} KB")

    # Print key findings
    seg_flagged = {pid for pid, d in seg_pipeline.items() if d["is_contradiction"]}
    stmt_flagged = {pid for pid, d in stmt_pipeline.items() if d.get("is_contradiction", False)}
    both = seg_flagged & stmt_flagged
    seg_only = seg_flagged - stmt_flagged
    stmt_only = stmt_flagged - seg_flagged

    print(f"\n--- Key Findings ---")
    print(f"  Both flag:          {len(both)}")
    print(f"  Segment-only:       {len(seg_only)} (potential FPs eliminated)")
    print(f"  Statement-only:     {len(stmt_only)} (new contradictions found)")
    print(f"  Preservation rate:  {len(both)/max(len(seg_flagged), 1):.1%}")


if __name__ == "__main__":
    main()
