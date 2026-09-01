#!/usr/bin/env python3
"""
Threshold Sensitivity Analysis for Privacy Washing Pipeline

Analyzes how varying the semantic similarity threshold affects:
1. Number of pairs reaching the judge panel
2. Number/rate of confirmed contradictions among judged pairs
3. Per-company contradiction counts

Uses judge annotations as the authoritative source for all judged pairs,
supplemented by the pairs file for unjudged pairs. Excludes contradictions
involving statements reclassified in the three-class audit.
"""

import json
import sys
from pathlib import Path
from collections import defaultdict

# Paths
BASE = Path(__file__).resolve().parent.parent
OPPT_PAIRS = BASE / "oppt_experiment_enhanced_20260131" / "statement_contradictions.json"
OPPT_JUDGES = BASE / "oppt_experiment_enhanced_20260131" / "statement_judge_results.json"
OPP115_PAIRS = BASE / "opp115_experiment_annotation_guided_20260203" / "statement_contradictions.json"
OPP115_JUDGES = BASE / "opp115_experiment_annotation_guided_20260203" / "statement_judge_results.json"
AUDIT_PATH = BASE / "audits" / "paper1_contradiction_audit.json"

# Thresholds to sweep
SIM_THRESHOLDS = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70]
NLI_THRESHOLD = 0.5  # Fixed; paper uses 0.5


def load_reclassified_statements():
    """Load statement IDs reclassified in the three-class audit."""
    with open(AUDIT_PATH) as f:
        audit = json.load(f)
    excluded = {}
    for corpus in ["oppt", "opp115"]:
        excluded[corpus] = set()
        for r in audit["results"][corpus]:
            if r["reclassified_as"] != "COMPANY_COMMITMENT":
                excluded[corpus].add(r["statement_id"])
    return excluded


def load_corpus(pairs_path, judges_path, reclassified_stmts):
    """Load pairs and judge verdicts. Uses judge annotations as the
    authoritative source for judged pairs (fixes missing-pair join bug).
    Excludes pairs whose commitment statement was reclassified."""
    with open(pairs_path) as f:
        pairs_data = json.load(f)
    with open(judges_path) as f:
        judges_data = json.load(f)

    # Build pair lookup from pairs file
    pairs_by_id = {p["pair_id"]: p for p in pairs_data["pairs"]}

    # Build unified pair list: use pairs file entries where available,
    # but fill in from judge annotations for any judged pairs missing
    # from the pairs file (fixes OPPT 30-pair gap).
    annotations = judges_data["annotations"]
    for a in annotations:
        if a["pair_id"] not in pairs_by_id:
            pairs_by_id[a["pair_id"]] = {
                "pair_id": a["pair_id"],
                "company": a["company"],
                "commitment_statement_id": a["commitment_statement_id"],
                "practice_statement_id": a["practice_statement_id"],
                "commitment_text": a["commitment_text"],
                "practice_text": a["practice_text"],
                "commitment_category": a.get("commitment_category", ""),
                "practice_category": a.get("practice_category", ""),
                "semantic_similarity": a["semantic_similarity"],
                "nli_contradiction_score": a["nli_contradiction_score"],
            }

    pairs = list(pairs_by_id.values())

    # Build judge verdict lookup, excluding reclassified contradictions
    judge_verdicts = {}
    for a in annotations:
        verdict = a["final_verdict"]
        if verdict is None:
            verdict = "NOT_CONTRADICTION"  # Split verdicts count as judged, not confirmed
        if verdict == "CONTRADICTION" and a["commitment_statement_id"] in reclassified_stmts:
            verdict = "RECLASSIFIED"  # Treat as non-contradiction
        judge_verdicts[a["pair_id"]] = verdict

    return pairs, judge_verdicts


def passes_similarity(pair, threshold):
    """Apply the uniform judge-submission similarity threshold.

    The differentiated thresholds (0.5 cross-category, 0.3 same-category) belong
    to the detection stage only and affect which pairs receive NLI scores; judge
    submission applies a single uniform threshold (see
    judge_statement_contradictions.py, DEFAULT_SIMILARITY_THRESHOLD). Sweeping a
    differentiated threshold here would leave same-category pairs in
    [0.50, threshold) counted as judged at rows where a real uniform threshold
    would have excluded them.
    """
    return pair["semantic_similarity"] >= threshold


def analyze_threshold(pairs, judge_verdicts, sim_threshold, nli_threshold=0.5):
    """Analyze results at a given uniform judge-submission similarity threshold."""
    eligible = [p for p in pairs if passes_similarity(p, sim_threshold)]

    # Among eligible, which pass NLI?
    nli_flagged = [p for p in eligible if p["nli_contradiction_score"] >= nli_threshold]

    # Among NLI-flagged, which have judge verdicts?
    judged = []
    confirmed = []
    for p in nli_flagged:
        verdict = judge_verdicts.get(p["pair_id"])
        if verdict is not None:
            judged.append(p)
            if verdict == "CONTRADICTION":
                confirmed.append(p)

    # Per-company analysis
    companies_with_contradictions = set()
    for p in confirmed:
        companies_with_contradictions.add(p["company"])

    # Unique companies in eligible pairs
    all_companies = set(p["company"] for p in eligible)

    return {
        "sim_threshold": sim_threshold,
        "eligible_pairs": len(eligible),
        "nli_flagged": len(nli_flagged),
        "judged": len(judged),
        "confirmed": len(confirmed),
        "confirmation_rate": len(confirmed) / len(judged) * 100 if judged else 0,
        "companies_with_contradictions": len(companies_with_contradictions),
        "total_companies": len(all_companies),
        "company_rate": len(companies_with_contradictions) / len(all_companies) * 100 if all_companies else 0,
    }


def similarity_distribution(pairs, judge_verdicts):
    """Show distribution of confirmed contradictions by similarity bucket."""
    confirmed_sims = []
    for p in pairs:
        verdict = judge_verdicts.get(p["pair_id"])
        if verdict == "CONTRADICTION":
            confirmed_sims.append(p["semantic_similarity"])

    if not confirmed_sims:
        return {}

    buckets = defaultdict(int)
    for s in confirmed_sims:
        bucket = f"{s:.2f}"[:3] + "0-" + f"{s:.2f}"[:3] + "5"
        # Use 0.05-wide buckets
        lower = int(s * 20) / 20
        upper = lower + 0.05
        bucket = f"{lower:.2f}-{upper:.2f}"
        buckets[bucket] += 1

    return dict(sorted(buckets.items()))


def nli_sensitivity(pairs, judge_verdicts):
    """Analyze NLI threshold sensitivity at the fixed uniform similarity threshold of 0.5."""
    nli_thresholds = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    results = []
    for nli_t in nli_thresholds:
        eligible = [p for p in pairs if passes_similarity(p, 0.50)]
        nli_flagged = [p for p in eligible if p["nli_contradiction_score"] >= nli_t]
        judged = []
        confirmed = []
        for p in nli_flagged:
            verdict = judge_verdicts.get(p["pair_id"])
            if verdict is not None:
                judged.append(p)
                if verdict == "CONTRADICTION":
                    confirmed.append(p)
        results.append({
            "nli_threshold": nli_t,
            "nli_flagged": len(nli_flagged),
            "judged": len(judged),
            "confirmed": len(confirmed),
        })
    return results


def print_table(results, corpus_name):
    """Print a formatted table of sensitivity results."""
    print(f"\n{'='*90}")
    print(f"  SIMILARITY THRESHOLD SENSITIVITY: {corpus_name}")
    print(f"  (NLI threshold fixed at {NLI_THRESHOLD})")
    print(f"{'='*90}")
    print(f"{'Sim':>6} | {'Eligible':>10} | {'NLI-flagged':>12} | {'Judged':>8} | {'Confirmed':>10} | {'Rate':>7} | {'Companies':>10}")
    print(f"{'-'*6}-+-{'-'*10}-+-{'-'*12}-+-{'-'*8}-+-{'-'*10}-+-{'-'*7}-+-{'-'*10}")

    for r in results:
        marker = " <--" if r["sim_threshold"] == 0.50 else ""
        print(
            f"{r['sim_threshold']:>6.2f} | {r['eligible_pairs']:>10,} | {r['nli_flagged']:>12,} | "
            f"{r['judged']:>8} | {r['confirmed']:>10} | {r['confirmation_rate']:>6.1f}% | "
            f"{r['companies_with_contradictions']:>4}/{r['total_companies']:<4}{marker}"
        )

    # Key observations
    current = next(r for r in results if r["sim_threshold"] == 0.50)
    lower = next((r for r in results if r["sim_threshold"] == 0.40), None)
    higher = next((r for r in results if r["sim_threshold"] == 0.60), None)

    print(f"\n  Current threshold (0.50): {current['confirmed']} confirmed contradictions")
    if lower:
        gained = lower["nli_flagged"] - current["nli_flagged"]
        print(f"  At 0.40: {lower['nli_flagged'] - current['nli_flagged']:+d} NLI-flagged pairs, "
              f"{lower['confirmed'] - current['confirmed']:+d} confirmed")
    if higher:
        print(f"  At 0.60: {higher['nli_flagged'] - current['nli_flagged']:+d} NLI-flagged pairs, "
              f"{higher['confirmed'] - current['confirmed']:+d} confirmed")


def print_sim_distribution(dist, corpus_name):
    """Print similarity distribution of confirmed contradictions."""
    if not dist:
        return
    print(f"\n  Similarity Distribution of Confirmed Contradictions ({corpus_name}):")
    total = sum(dist.values())
    for bucket, count in sorted(dist.items()):
        bar = "#" * (count * 2)
        print(f"    {bucket}: {count:>3} ({count/total*100:>5.1f}%) {bar}")


def print_nli_sensitivity(results, corpus_name):
    """Print NLI threshold sensitivity."""
    print(f"\n  NLI THRESHOLD SENSITIVITY ({corpus_name}, similarity fixed at 0.50):")
    print(f"  {'NLI':>6} | {'NLI-flagged':>12} | {'Judged':>8} | {'Confirmed':>10}")
    print(f"  {'-'*6}-+-{'-'*12}-+-{'-'*8}-+-{'-'*10}")
    for r in results:
        marker = " <--" if r["nli_threshold"] == 0.5 else ""
        print(f"  {r['nli_threshold']:>6.1f} | {r['nli_flagged']:>12,} | {r['judged']:>8} | {r['confirmed']:>10}{marker}")


def main():
    print("Loading data...")

    # Load reclassification exclusions
    reclassified = load_reclassified_statements()
    print(f"Reclassified statements: OPPT={len(reclassified['oppt'])}, OPP-115={len(reclassified['opp115'])}")

    # Load both corpora (post-reclassification)
    oppt_pairs, oppt_verdicts = load_corpus(OPPT_PAIRS, OPPT_JUDGES, reclassified["oppt"])
    opp115_pairs, opp115_verdicts = load_corpus(OPP115_PAIRS, OPP115_JUDGES, reclassified["opp115"])

    print(f"OPPT: {len(oppt_pairs):,} pairs, {len(oppt_verdicts)} judge verdicts")
    print(f"OPP-115: {len(opp115_pairs):,} pairs, {len(opp115_verdicts)} judge verdicts")

    # Run similarity threshold sensitivity
    oppt_results = [analyze_threshold(oppt_pairs, oppt_verdicts, t, NLI_THRESHOLD) for t in SIM_THRESHOLDS]
    opp115_results = [analyze_threshold(opp115_pairs, opp115_verdicts, t, NLI_THRESHOLD) for t in SIM_THRESHOLDS]

    print_table(oppt_results, "OPPT (123 companies, 2026)")
    print_table(opp115_results, "OPP-115 (115 companies, 2014)")

    # Similarity distribution of confirmed contradictions
    oppt_dist = similarity_distribution(oppt_pairs, oppt_verdicts)
    opp115_dist = similarity_distribution(opp115_pairs, opp115_verdicts)
    print_sim_distribution(oppt_dist, "OPPT")
    print_sim_distribution(opp115_dist, "OPP-115")

    # NLI threshold sensitivity
    oppt_nli = nli_sensitivity(oppt_pairs, oppt_verdicts)
    opp115_nli = nli_sensitivity(opp115_pairs, opp115_verdicts)
    print_nli_sensitivity(oppt_nli, "OPPT")
    print_nli_sensitivity(opp115_nli, "OPP-115")

    # Key finding summary
    print(f"\n{'='*90}")
    print("  SUMMARY")
    print(f"{'='*90}")

    oppt_50 = next(r for r in oppt_results if r["sim_threshold"] == 0.50)
    oppt_40 = next(r for r in oppt_results if r["sim_threshold"] == 0.40)
    oppt_60 = next(r for r in oppt_results if r["sim_threshold"] == 0.60)
    opp_50 = next(r for r in opp115_results if r["sim_threshold"] == 0.50)
    opp_40 = next(r for r in opp115_results if r["sim_threshold"] == 0.40)
    opp_60 = next(r for r in opp115_results if r["sim_threshold"] == 0.60)

    print(f"\n  Confirmed contradictions are {'STABLE' if oppt_40['confirmed'] == oppt_50['confirmed'] == oppt_60['confirmed'] else 'SENSITIVE'} "
          f"to threshold changes in OPPT ({oppt_40['confirmed']}/{oppt_50['confirmed']}/{oppt_60['confirmed']} at 0.4/0.5/0.6)")
    print(f"  Confirmed contradictions are {'STABLE' if opp_40['confirmed'] == opp_50['confirmed'] == opp_60['confirmed'] else 'SENSITIVE'} "
          f"to threshold changes in OPP-115 ({opp_40['confirmed']}/{opp_50['confirmed']}/{opp_60['confirmed']} at 0.4/0.5/0.6)")

    # Note about limitation
    print(f"\n  NOTE: Judge verdicts exist only for pairs that passed the ORIGINAL threshold")
    print(f"  (similarity >= 0.50 cross-category). Pairs at lower thresholds that were")
    print(f"  never judged show as 'not judged' rather than 'not contradiction'.")
    print(f"  A full sensitivity analysis (Option B) would require judging these new pairs.")


if __name__ == "__main__":
    main()
