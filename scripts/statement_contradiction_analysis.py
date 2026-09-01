"""
Statement-Level Contradiction Analysis Report Generator

Generates comprehensive analysis reports from statement-level judge results.
Produces detailed per-company breakdowns, category analysis, and quality metrics.

Input:  statement_judge_results.json, statements.json
Output: statement_contradiction_analysis.md

Usage:
  python statement_contradiction_analysis.py --data-dir oppt_experiment
  python statement_contradiction_analysis.py --data-dir opp115_experiment
"""

import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

# Parse --data-dir argument
_DATA_DIR = None
for _i, _arg in enumerate(sys.argv[1:], 1):
    if _arg == "--data-dir" and _i < len(sys.argv) - 1:
        _DATA_DIR = Path(sys.argv[_i + 1])

if _DATA_DIR:
    if not _DATA_DIR.is_absolute():
        _DATA_DIR = (REPO_ROOT / _DATA_DIR).resolve()
    JUDGE_RESULTS_PATH = _DATA_DIR / "statement_judge_results.json"
    STATEMENTS_PATH = _DATA_DIR / "statements.json"
    OUTPUT_PATH = _DATA_DIR / "statement_contradiction_analysis.md"
else:
    JUDGE_RESULTS_PATH = REPO_ROOT / "output" / "statement_judge_results.json"
    STATEMENTS_PATH = REPO_ROOT / "output" / "statements.json"
    OUTPUT_PATH = REPO_ROOT / "output" / "statement_contradiction_analysis.md"


def load_data():
    """Load judge results and statements."""
    print(f"Loading judge results from: {JUDGE_RESULTS_PATH}")
    with open(JUDGE_RESULTS_PATH) as f:
        judge_data = json.load(f)

    print(f"Loading statements from: {STATEMENTS_PATH}")
    with open(STATEMENTS_PATH) as f:
        statements_data = json.load(f)

    return judge_data, statements_data


def compute_stats(judge_data, statements_data):
    """Compute all statistics for the report."""
    annotations = judge_data.get("annotations", [])
    metadata = judge_data.get("metadata", {})
    agreement = judge_data.get("agreement_metrics", {})
    nli_comparison = judge_data.get("nli_comparison", {})

    statements = statements_data.get("statements", [])

    # Basic counts
    total_statements = len(statements)
    commitment_count = sum(1 for s in statements if s.get("type") == "COMMITMENT")
    practice_count = sum(1 for s in statements if s.get("type") == "PRACTICE")

    # Confirmed contradictions
    confirmed = [a for a in annotations if a.get("final_verdict") == "CONTRADICTION"]
    rejected = [a for a in annotations if a.get("final_verdict") == "NOT_CONTRADICTION"]
    needs_review = [a for a in annotations if a.get("needs_review")]

    # Per-company stats
    company_stats = defaultdict(lambda: {"confirmed": 0, "rejected": 0, "total": 0})
    for a in annotations:
        company = a.get("company", "unknown")
        company_stats[company]["total"] += 1
        if a.get("final_verdict") == "CONTRADICTION":
            company_stats[company]["confirmed"] += 1
        elif a.get("final_verdict") == "NOT_CONTRADICTION":
            company_stats[company]["rejected"] += 1

    # Category pair distribution
    category_pairs = Counter()
    for a in confirmed:
        commitment_cat = a.get("commitment_category", "UNKNOWN")
        practice_cat = a.get("practice_category", "UNKNOWN")
        category_pairs[f"{commitment_cat} -> {practice_cat}"] += 1

    # Consensus distribution
    unanimous_confirmed = sum(1 for a in confirmed if a.get("consensus_type") == "unanimous")
    majority_confirmed = sum(1 for a in confirmed if a.get("consensus_type") == "majority")

    # Similarity distribution
    similarity_buckets = defaultdict(int)
    for a in confirmed:
        sim = a.get("semantic_similarity", 0)
        if sim >= 0.85:
            similarity_buckets["0.85-1.00"] += 1
        elif sim >= 0.80:
            similarity_buckets["0.80-0.85"] += 1
        elif sim >= 0.75:
            similarity_buckets["0.75-0.80"] += 1
        elif sim >= 0.70:
            similarity_buckets["0.70-0.75"] += 1
        elif sim >= 0.65:
            similarity_buckets["0.65-0.70"] += 1
        elif sim >= 0.60:
            similarity_buckets["0.60-0.65"] += 1
        elif sim >= 0.55:
            similarity_buckets["0.55-0.60"] += 1
        elif sim >= 0.50:
            similarity_buckets["0.50-0.55"] += 1
        else:
            # Below the historical judge-submission threshold; occurs when the
            # judge stage is run with --similarity-threshold below 0.5.
            similarity_buckets["<0.50"] += 1

    # Unique commitments in contradictions
    unique_commitments = set(a.get("commitment_statement_id") for a in confirmed)
    unique_segment_pairs = set(a.get("source_segment_pair", "") for a in confirmed if a.get("source_segment_pair"))

    # Companies with contradictions
    companies_with_contradictions = sum(1 for c, s in company_stats.items() if s["confirmed"] > 0)
    total_companies = len(company_stats)

    return {
        "total_statements": total_statements,
        "commitment_count": commitment_count,
        "practice_count": practice_count,
        "total_judged": len(annotations),
        "confirmed": len(confirmed),
        "rejected": len(rejected),
        "needs_review": len(needs_review),
        "confirmation_rate": len(confirmed) / len(annotations) if annotations else 0,
        "rejection_rate": len(rejected) / len(annotations) if annotations else 0,
        "company_stats": dict(company_stats),
        "companies_with_contradictions": companies_with_contradictions,
        "total_companies": total_companies,
        "category_pairs": category_pairs,
        "unanimous_confirmed": unanimous_confirmed,
        "majority_confirmed": majority_confirmed,
        "similarity_buckets": dict(similarity_buckets),
        "unique_commitments": len(unique_commitments),
        "unique_segment_pairs": len(unique_segment_pairs),
        "agreement": agreement,
        "metadata": metadata,
        "confirmed_list": confirmed,
    }


def get_top_examples(confirmed_list, company, limit=3):
    """Get top examples for a company by NLI score, skipping display duplicates.

    Distinct pairs can share identical (truncated) commitment and practice
    text when near-duplicate statements are extracted from different
    segments; showing both is uninformative in the report.
    """
    company_examples = [a for a in confirmed_list if a.get("company") == company]
    company_examples.sort(key=lambda x: x.get("nli_contradiction_score", 0), reverse=True)
    seen = set()
    unique = []
    for a in company_examples:
        key = (a.get("commitment_text", "")[:200], a.get("practice_text", "")[:200])
        if key in seen:
            continue
        seen.add(key)
        unique.append(a)
        if len(unique) == limit:
            break
    return unique


def generate_report(stats):
    """Generate the markdown report."""
    lines = []

    # Detect corpus from path
    corpus_name = "OPPT" if "oppt" in str(_DATA_DIR or "").lower() else "OPP-115"
    if "oppt" in str(_DATA_DIR or "").lower():
        corpus_desc = f"OPPT (123 companies)"
    else:
        corpus_desc = f"OPP-115 (115 companies)"

    lines.append(f"# {corpus_name} Statement-Level Contradiction Analysis: Judge-Verified Results")
    lines.append("")
    lines.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d')}*")
    lines.append("*Pipeline: extract → NLI detect → 3-LLM judge verification*")
    lines.append("")

    # Executive Summary
    lines.append("## Executive Summary")
    lines.append("")
    lines.append(f"The statement-level privacy washing detection pipeline processed the {corpus_desc} corpus, "
                 f"decomposing segments into **{stats['total_statements']:,} atomic statements** "
                 f"({stats['commitment_count']:,} commitment, {stats['practice_count']:,} practice). "
                 f"After pairing COMMITMENT × PRACTICE within each company and filtering by category relevance "
                 f"and semantic similarity, pairs were evaluated by DeBERTa v3 NLI. "
                 f"The highest-confidence pairs were then verified by a 3-LLM judge panel.")
    lines.append("")
    lines.append(f"**Result: {stats['confirmed']} judge-confirmed contradictions** across "
                 f"**{stats['companies_with_contradictions']} of {stats['total_companies']} companies** "
                 f"({stats['companies_with_contradictions']/stats['total_companies']*100:.0f}%), "
                 f"from **{stats['unique_commitments']} unique commitment statements** "
                 f"spanning **{stats['unique_segment_pairs']} unique segment pairs**. "
                 f"The judges rejected {stats['rejection_rate']*100:.1f}% of NLI-flagged pairs, "
                 f"confirming that NLI over-flags at the atomic statement level and that "
                 f"multi-model judge verification is essential.")
    lines.append("")

    # Pipeline Metrics
    lines.append("### Pipeline Metrics")
    lines.append("")
    lines.append("| Stage | Count | Notes |")
    lines.append("|-------|-------|-------|")
    lines.append(f"| Atomic statements extracted | {stats['total_statements']:,} | "
                 f"{stats['commitment_count']:,} COMMITMENT + {stats['practice_count']:,} PRACTICE |")
    lines.append(f"| Judge input pairs | {stats['total_judged']:,} | NLI-flagged, similarity filtered |")
    lines.append(f"| **Judge-confirmed contradictions** | **{stats['confirmed']}** | "
                 f"**{stats['confirmation_rate']*100:.1f}% confirmation rate** |")
    lines.append(f"| Needs review (split verdict) | {stats['needs_review']} | — |")
    lines.append("")

    # Judge Agreement
    agreement = stats.get("agreement", {})
    lines.append("### Judge Agreement")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|--------|-------|")

    consensus = agreement.get("consensus_counts", {})
    unanimous = consensus.get("unanimous", 0)
    majority = consensus.get("majority", 0)
    total = stats["total_judged"]

    if total > 0:
        lines.append(f"| Unanimous (3/3) | {unanimous/total*100:.1f}% ({unanimous:,}/{total:,}) |")
        lines.append(f"| Majority (2/3) | {majority/total*100:.1f}% ({majority:,}/{total:,}) |")
        lines.append(f"| Usable consensus | {(unanimous+majority)/total*100:.1f}% |")
        lines.append(f"| Split/insufficient | {consensus.get('split', 0) + consensus.get('insufficient_valid', 0)} |")

    fk = agreement.get("fleiss_kappa")
    if fk is not None:
        lines.append(f"| Fleiss' kappa | {fk:.4f} (moderate) |")
    lines.append("")

    # Top Companies
    lines.append("---")
    lines.append("")
    lines.append("## Top Companies by Contradiction Count")
    lines.append("")

    sorted_companies = sorted(
        stats["company_stats"].items(),
        key=lambda x: x[1]["confirmed"],
        reverse=True
    )

    lines.append("| Rank | Company | Confirmed | Judged | Rate |")
    lines.append("|------|---------|-----------|--------|------|")

    for rank, (company, cs) in enumerate(sorted_companies[:20], 1):
        if cs["confirmed"] > 0:
            rate = cs["confirmed"] / cs["total"] * 100 if cs["total"] > 0 else 0
            lines.append(f"| {rank} | {company} | {cs['confirmed']} | {cs['total']} | {rate:.0f}% |")

    lines.append("")

    # Per-Company Highlights (top 5)
    lines.append("## Per-Company Highlights")
    lines.append("")

    for company, cs in sorted_companies[:5]:
        if cs["confirmed"] == 0:
            continue

        rate = cs["confirmed"] / cs["total"] * 100 if cs["total"] > 0 else 0
        lines.append(f"### {company.replace('-', ' ').title()} — {cs['confirmed']} Confirmed ({rate:.0f}% rate)")
        lines.append("")

        examples = get_top_examples(stats["confirmed_list"], company, 2)
        for ex in examples:
            commitment = ex.get("commitment_text", "")[:200]
            practice = ex.get("practice_text", "")[:200]
            sim = ex.get("semantic_similarity", 0)
            nli = ex.get("nli_contradiction_score", 0)
            consensus = ex.get("consensus_type", "")

            lines.append(f"**Example (sim={sim:.2f}, nli={nli:.2f}, {consensus}):**")
            lines.append(f"> **COMMITMENT:** {commitment}...")
            lines.append(f"> **PRACTICE:** {practice}...")
            lines.append("")

    # Category Analysis
    lines.append("---")
    lines.append("")
    lines.append("## Category Analysis")
    lines.append("")
    lines.append("### Category Pair Distribution")
    lines.append("")
    lines.append("| Commitment Category → Practice Category | Count | % |")
    lines.append("|----------------------------------------|-------|---|")

    total_confirmed = stats["confirmed"]
    for pair, count in stats["category_pairs"].most_common(10):
        pct = count / total_confirmed * 100 if total_confirmed > 0 else 0
        lines.append(f"| {pair} | {count} | {pct:.1f}% |")

    lines.append("")

    # Signal Quality
    lines.append("---")
    lines.append("")
    lines.append("## Signal Quality")
    lines.append("")
    lines.append("### Consensus Strength of Confirmed Contradictions")
    lines.append("")
    lines.append("| Consensus | Count | % |")
    lines.append("|-----------|-------|---|")

    if stats["confirmed"] > 0:
        lines.append(f"| Unanimous (3/3 CONTRADICTION) | {stats['unanimous_confirmed']} | "
                     f"{stats['unanimous_confirmed']/stats['confirmed']*100:.1f}% |")
        lines.append(f"| Majority (2/3 CONTRADICTION) | {stats['majority_confirmed']} | "
                     f"{stats['majority_confirmed']/stats['confirmed']*100:.1f}% |")

    lines.append("")
    lines.append("### Similarity Distribution of Confirmed Contradictions")
    lines.append("")
    lines.append("| Similarity Range | Count | % |")
    lines.append("|-----------------|-------|---|")

    for bucket in ["0.85-1.00", "0.80-0.85", "0.75-0.80", "0.70-0.75",
                   "0.65-0.70", "0.60-0.65", "0.55-0.60", "0.50-0.55", "<0.50"]:
        count = stats["similarity_buckets"].get(bucket, 0)
        pct = count / stats["confirmed"] * 100 if stats["confirmed"] > 0 else 0
        lines.append(f"| {bucket} | {count} | {pct:.1f}% |")

    lines.append("")

    # Coverage Analysis
    lines.append("---")
    lines.append("")
    lines.append("## Coverage Analysis")
    lines.append("")
    lines.append("### Companies Without Contradictions")
    lines.append("")

    zero_companies = [c for c, s in stats["company_stats"].items() if s["confirmed"] == 0]
    if zero_companies:
        lines.append(f"{len(zero_companies)} companies had zero confirmed contradictions:")
        lines.append("")
        lines.append(", ".join(sorted(zero_companies)[:30]))
        if len(zero_companies) > 30:
            lines.append(f"... and {len(zero_companies) - 30} more")

    lines.append("")

    # Scale Analysis
    lines.append("### Scale Analysis")
    lines.append("")
    lines.append("| Contradictions | Companies | % |")
    lines.append("|----------------|-----------|---|")

    scale_buckets = {"0": 0, "1-4": 0, "5-9": 0, "10-19": 0, "20+": 0}
    for company, cs in stats["company_stats"].items():
        c = cs["confirmed"]
        if c == 0:
            scale_buckets["0"] += 1
        elif c <= 4:
            scale_buckets["1-4"] += 1
        elif c <= 9:
            scale_buckets["5-9"] += 1
        elif c <= 19:
            scale_buckets["10-19"] += 1
        else:
            scale_buckets["20+"] += 1

    total_cos = stats["total_companies"]
    for bucket, count in scale_buckets.items():
        pct = count / total_cos * 100 if total_cos > 0 else 0
        lines.append(f"| {bucket} | {count} | {pct:.0f}% |")

    lines.append("")

    # Key Takeaways
    lines.append("---")
    lines.append("")
    lines.append("## Key Takeaways")
    lines.append("")

    top_cat = stats["category_pairs"].most_common(1)
    if top_cat:
        top_cat_name, top_cat_count = top_cat[0]
        top_cat_pct = top_cat_count / stats["confirmed"] * 100 if stats["confirmed"] > 0 else 0

    lines.append(f"1. **Scale**: {stats['confirmed']} panel-confirmed contradictions across "
                 f"{stats['companies_with_contradictions']} companies. Panel confirmation is LLM "
                 f"majority agreement, not human validation; precision against expert judgment "
                 f"is unknown (see the paper's Limitations section).")
    lines.append("")
    lines.append(f"2. **Judge filtering**: {stats['rejection_rate']*100:.1f}% of judged pairs were "
                 f"rejected; without the judge stage the pipeline would flag {stats['total_judged']:,} "
                 f"candidate pairs, {stats['total_judged']//max(1,stats['confirmed'])}x the "
                 f"panel-confirmed count.")
    lines.append("")
    if top_cat:
        lines.append(f"3. **Modal category pattern**: {top_cat_name.replace(' -> ', ' -> ')} accounts for "
                     f"{top_cat_pct:.1f}% of panel-confirmed contradictions. Category composition "
                     f"largely reflects the composition of judged pairs and is panel-sensitive "
                     f"(see the paper's category base-rate analysis and stability section).")
    lines.append("")
    lines.append(f"4. **Similarity distribution**: the concentration of confirmations at lower "
                 f"similarity mirrors the composition of judged pairs; per-bin confirmation rates, "
                 f"not raw counts, are the informative quantity (see the paper).")
    lines.append("")

    return "\n".join(lines)


def main():
    print(f"Statement-Level Contradiction Analysis Report Generator")
    print(f"=" * 60)

    judge_data, statements_data = load_data()

    print("Computing statistics...")
    stats = compute_stats(judge_data, statements_data)

    print("Generating report...")
    report = generate_report(stats)

    print(f"Writing report to: {OUTPUT_PATH}")
    with open(OUTPUT_PATH, "w") as f:
        f.write(report)

    print(f"\nReport generated: {len(report):,} characters")
    print(f"  Confirmed contradictions: {stats['confirmed']}")
    print(f"  Companies with contradictions: {stats['companies_with_contradictions']}/{stats['total_companies']}")
    print(f"  Confirmation rate: {stats['confirmation_rate']*100:.1f}%")


if __name__ == "__main__":
    main()
