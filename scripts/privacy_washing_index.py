"""
Script 3: Privacy Washing Index (PWI) & Enforcement Validation

Aggregates per-company metrics from contradiction detection and validates
against regulatory enforcement outcomes.

PWI(company) = 0.5 * contradiction_density + 0.5 * avg_severity
  - contradiction_density = num_contradictions / num_pairs
  - avg_severity = mean(severity) across NLI-flagged contradictions
  - severity = nli_contradiction * (1 + 0.3 * tone_gap_normalized)
  - Min-max normalized to [0, 1] across corpus

Enforcement validation:
  - Mann-Whitney U test (enforced vs non-enforced)
  - Cohen's d effect size
  - ROC-AUC
  - Bootstrap 95% confidence intervals (N=10,000)

Input:  contradictions.json + linguistic_features.json
Output: output/privacy_washing_index.json
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timezone

import numpy as np
from scipy import stats
from sklearn.metrics import roc_auc_score

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[1]
CONTRADICTIONS_PATH = REPO_ROOT / "output" / "contradictions.json"
FEATURES_PATH = REPO_ROOT / "output" / "linguistic_features.json"
OUTPUT_PATH = REPO_ROOT / "output" / "privacy_washing_index.json"

# Optional --data-dir override: read/write all files from a custom directory
_DATA_DIR = None
for _i, _arg in enumerate(sys.argv[1:], 1):
    if _arg == "--data-dir" and _i < len(sys.argv) - 1:
        _DATA_DIR = Path(sys.argv[_i + 1])
if _DATA_DIR:
    CONTRADICTIONS_PATH = _DATA_DIR / "contradictions.json"
    FEATURES_PATH = _DATA_DIR / "linguistic_features.json"
    OUTPUT_PATH = _DATA_DIR / "privacy_washing_index.json"

# ---------------------------------------------------------------------------
# Enforcement-actioned companies in our 123-company corpus
# Sourced from: .serena/memories/notorious_companies_privacy_research.md
# Includes Tier 1-3 companies with documented enforcement actions
# ---------------------------------------------------------------------------
ENFORCEMENT_COMPANIES = {
    "clearview-ai", "kochava", "gravy-analytics", "safegraph",
    "x-mode-social", "lexisnexis", "babel-street",
    "betterhelp", "premom", "cerebral", "monument",
    "grindr", "bumble", "tinder",
    "vonage", "adobe", "amazon",
    "ngl", "epic-games", "roblox", "draftkings", "fanduel",
    "avast",
    "meta", "tiktok", "linkedin", "google",
    "uber", "verizon", "att", "t-mobile",
}

# With NLI-primary scoring, contradictions are identified by the
# is_contradiction field (NLI >= 0.5). No percentile threshold needed
# because NLI is already a sparse, high-quality signal.
# The old P90 combined_score approach was a workaround for tone-only noise.


# ---------------------------------------------------------------------------
# PWI computation
# ---------------------------------------------------------------------------

def compute_pwi(pairs: list[dict]) -> dict:
    """Compute per-company Privacy Washing Index.

    Uses is_contradiction (NLI-flagged) to identify contradictions, and
    severity for the severity component. No percentile threshold needed.

    Returns dict of company -> {pwi, contradiction_density, avg_severity, ...}
    """
    # Group pairs by company
    by_company = {}
    for p in pairs:
        company = p["company"]
        if company not in by_company:
            by_company[company] = []
        by_company[company].append(p)

    company_metrics = {}
    for company, company_pairs in by_company.items():
        contradictions = [p for p in company_pairs if p.get("is_contradiction", False)]

        n_pairs = len(company_pairs)
        n_contradictions = len(contradictions)
        density = n_contradictions / max(n_pairs, 1)

        if contradictions:
            avg_sev = np.mean([p["severity"] for p in contradictions])
        else:
            avg_sev = 0.0

        # Raw PWI (before normalization)
        raw_pwi = 0.5 * density + 0.5 * avg_sev

        # Evidence type breakdown
        evidence_counts = {"nli_plus_tone": 0, "nli": 0, "none": 0}
        for p in contradictions:
            et = p.get("evidence_type", "none")
            evidence_counts[et] = evidence_counts.get(et, 0) + 1

        # NLI statistics
        nli_scores = [p["nli_contradiction"] for p in company_pairs]
        mean_nli = np.mean(nli_scores) if nli_scores else 0.0
        max_nli = max(nli_scores) if nli_scores else 0.0

        # Top contradiction details
        top_3 = sorted(contradictions, key=lambda x: -x["severity"])[:3]

        company_metrics[company] = {
            "raw_pwi": round(float(raw_pwi), 6),
            "contradiction_density": round(float(density), 4),
            "avg_severity": round(float(avg_sev), 4),
            "n_pairs": n_pairs,
            "n_contradictions": n_contradictions,
            "mean_nli_contradiction": round(float(mean_nli), 4),
            "max_nli_contradiction": round(float(max_nli), 4),
            "evidence_type_counts": evidence_counts,
            "top_3_contradictions": [
                {
                    "claim_id": c["claim_id"],
                    "practice_id": c["practice_id"],
                    "severity": c["severity"],
                    "nli_contradiction": c["nli_contradiction"],
                    "tone_gap": c["tone_gap"],
                    "evidence_type": c["evidence_type"],
                    "claim_preview": c.get("claim_text_preview", "")[:150],
                    "practice_preview": c.get("practice_text_preview", "")[:150],
                }
                for c in top_3
            ],
        }

    # Min-max normalize PWI to [0, 1]
    raw_values = [m["raw_pwi"] for m in company_metrics.values()]
    min_pwi = min(raw_values) if raw_values else 0
    max_pwi = max(raw_values) if raw_values else 1
    pwi_range = max_pwi - min_pwi if max_pwi > min_pwi else 1.0

    for company, metrics in company_metrics.items():
        metrics["pwi"] = round((metrics["raw_pwi"] - min_pwi) / pwi_range, 4)

    return company_metrics


# ---------------------------------------------------------------------------
# Per-category analysis
# ---------------------------------------------------------------------------

def compute_category_analysis(pairs: list[dict], features: list[dict]) -> dict:
    """Analyze tone gap and contradiction rate per OPPT practice category."""
    # Build features lookup
    feat_lookup = {f["segment_id"]: f for f in features}

    by_category = {}
    for p in pairs:
        cat = p["practice_category"]
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(p)

    category_stats = {}
    for cat, cat_pairs in sorted(by_category.items()):
        severities = [p["severity"] for p in cat_pairs]
        tone_gaps = [p["tone_gap"] for p in cat_pairs]
        nli_scores = [p["nli_contradiction"] for p in cat_pairs]

        # Get practice segment features for this category
        practice_ids = set(p["practice_id"] for p in cat_pairs)
        practice_features = [feat_lookup[pid] for pid in practice_ids if pid in feat_lookup]

        category_stats[cat] = {
            "n_pairs": len(cat_pairs),
            "n_practice_segments": len(practice_ids),
            "mean_severity": round(float(np.mean(severities)), 4),
            "mean_tone_gap": round(float(np.mean(tone_gaps)), 4),
            "median_tone_gap": round(float(np.median(tone_gaps)), 4),
            "mean_nli_contradiction": round(float(np.mean(nli_scores)), 4),
            "nli_contradiction_rate": round(float(np.mean(np.array(nli_scores) > 0.5)), 4),
            "mean_hedging": round(float(np.mean([f["hedging_score"] for f in practice_features])), 4) if practice_features else 0,
            "mean_specificity": round(float(np.mean([f["specificity_score"] for f in practice_features])), 4) if practice_features else 0,
            "mean_vagueness": round(float(np.mean([f["vague_ratio"] for f in practice_features])), 4) if practice_features else 0,
        }

    return category_stats


# ---------------------------------------------------------------------------
# Enforcement validation
# ---------------------------------------------------------------------------

def cohens_d(group1: np.ndarray, group2: np.ndarray) -> float:
    """Compute Cohen's d effect size (pooled standard deviation)."""
    n1, n2 = len(group1), len(group2)
    if n1 < 2 or n2 < 2:
        return 0.0
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
    pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    if pooled_std == 0:
        return 0.0
    return float((np.mean(group1) - np.mean(group2)) / pooled_std)


def bootstrap_ci(data: np.ndarray, stat_func, n_bootstrap: int = 10000,
                 ci: float = 0.95, seed: int = 42) -> tuple[float, float, float]:
    """Bootstrap confidence interval for a statistic.

    Returns (point_estimate, ci_lower, ci_upper).
    """
    rng = np.random.RandomState(seed)
    point = stat_func(data)
    boot_stats = []
    for _ in range(n_bootstrap):
        sample = rng.choice(data, size=len(data), replace=True)
        boot_stats.append(stat_func(sample))
    boot_stats = np.array(boot_stats)
    alpha = (1 - ci) / 2
    lower = float(np.percentile(boot_stats, 100 * alpha))
    upper = float(np.percentile(boot_stats, 100 * (1 - alpha)))
    return float(point), lower, upper


def bootstrap_two_sample(group1: np.ndarray, group2: np.ndarray, stat_func,
                         n_bootstrap: int = 10000, ci: float = 0.95,
                         seed: int = 42) -> tuple[float, float, float]:
    """Bootstrap CI for a two-sample statistic (e.g., difference in means, Cohen's d)."""
    rng = np.random.RandomState(seed)
    point = stat_func(group1, group2)
    boot_stats = []
    for _ in range(n_bootstrap):
        s1 = rng.choice(group1, size=len(group1), replace=True)
        s2 = rng.choice(group2, size=len(group2), replace=True)
        boot_stats.append(stat_func(s1, s2))
    boot_stats = np.array(boot_stats)
    alpha = (1 - ci) / 2
    lower = float(np.percentile(boot_stats, 100 * alpha))
    upper = float(np.percentile(boot_stats, 100 * (1 - alpha)))
    return float(point), lower, upper


def enforcement_validation(company_metrics: dict) -> dict:
    """Validate PWI against enforcement action history.

    Compares enforced vs non-enforced companies using:
    - Mann-Whitney U test
    - Cohen's d effect size
    - ROC-AUC
    - Bootstrap 95% CIs for all metrics
    """
    enforced_pwi = []
    non_enforced_pwi = []
    all_labels = []  # 1 = enforced, 0 = not
    all_pwi = []

    for company, metrics in company_metrics.items():
        pwi = metrics["pwi"]
        if company in ENFORCEMENT_COMPANIES:
            enforced_pwi.append(pwi)
            all_labels.append(1)
        else:
            non_enforced_pwi.append(pwi)
            all_labels.append(0)
        all_pwi.append(pwi)

    enforced = np.array(enforced_pwi)
    non_enforced = np.array(non_enforced_pwi)
    labels = np.array(all_labels)
    scores = np.array(all_pwi)

    print(f"\n--- Enforcement Validation ---")
    print(f"  Enforced companies in analysis: {len(enforced)} (of {len(ENFORCEMENT_COMPANIES)} total)")
    print(f"  Non-enforced companies: {len(non_enforced)}")

    # Companies in enforcement list but not in contradiction analysis
    # (no claim-practice pairs = no reassurance language detected)
    missing = ENFORCEMENT_COMPANIES - set(company_metrics.keys())
    if missing:
        print(f"  Enforcement companies without pairs: {sorted(missing)}")

    # Descriptive statistics with bootstrap CIs
    enf_mean, enf_ci_lo, enf_ci_hi = bootstrap_ci(enforced, np.mean)
    nonenf_mean, nonenf_ci_lo, nonenf_ci_hi = bootstrap_ci(non_enforced, np.mean)
    print(f"  Enforced PWI:     {enf_mean:.4f} [{enf_ci_lo:.4f}, {enf_ci_hi:.4f}]")
    print(f"  Non-enforced PWI: {nonenf_mean:.4f} [{nonenf_ci_lo:.4f}, {nonenf_ci_hi:.4f}]")

    # Mann-Whitney U test
    u_stat, u_pvalue = stats.mannwhitneyu(enforced, non_enforced, alternative="two-sided")
    print(f"  Mann-Whitney U: U={u_stat:.1f}, p={u_pvalue:.4f}")

    # Cohen's d with bootstrap CI
    d_point, d_ci_lo, d_ci_hi = bootstrap_two_sample(
        enforced, non_enforced, cohens_d
    )
    print(f"  Cohen's d: {d_point:.4f} [{d_ci_lo:.4f}, {d_ci_hi:.4f}]")

    # ROC-AUC with bootstrap CI
    try:
        auc_point = roc_auc_score(labels, scores)
        # Bootstrap AUC
        rng = np.random.RandomState(42)
        auc_boots = []
        for _ in range(10000):
            idx = rng.choice(len(labels), size=len(labels), replace=True)
            if len(np.unique(labels[idx])) < 2:
                continue  # skip degenerate samples
            auc_boots.append(roc_auc_score(labels[idx], scores[idx]))
        auc_boots = np.array(auc_boots)
        auc_ci_lo = float(np.percentile(auc_boots, 2.5))
        auc_ci_hi = float(np.percentile(auc_boots, 97.5))
        print(f"  ROC-AUC: {auc_point:.4f} [{auc_ci_lo:.4f}, {auc_ci_hi:.4f}]")
    except Exception as e:
        auc_point = None
        auc_ci_lo, auc_ci_hi = None, None
        print(f"  ROC-AUC: Error — {e}")

    # Effect size interpretation
    d_abs = abs(d_point)
    if d_abs < 0.2:
        effect_label = "negligible"
    elif d_abs < 0.5:
        effect_label = "small"
    elif d_abs < 0.8:
        effect_label = "medium"
    else:
        effect_label = "large"

    return {
        "n_enforced": len(enforced),
        "n_non_enforced": len(non_enforced),
        "enforcement_companies_missing_from_analysis": sorted(missing),
        "enforced_pwi_mean": round(enf_mean, 4),
        "enforced_pwi_ci_95": [round(enf_ci_lo, 4), round(enf_ci_hi, 4)],
        "non_enforced_pwi_mean": round(nonenf_mean, 4),
        "non_enforced_pwi_ci_95": [round(nonenf_ci_lo, 4), round(nonenf_ci_hi, 4)],
        "mean_difference": round(enf_mean - nonenf_mean, 4),
        "mann_whitney_u": round(float(u_stat), 2),
        "mann_whitney_p": round(float(u_pvalue), 6),
        "cohens_d": round(d_point, 4),
        "cohens_d_ci_95": [round(d_ci_lo, 4), round(d_ci_hi, 4)],
        "cohens_d_interpretation": effect_label,
        "roc_auc": round(auc_point, 4) if auc_point is not None else None,
        "roc_auc_ci_95": [round(auc_ci_lo, 4), round(auc_ci_hi, 4)] if auc_ci_lo is not None else None,
        "note": f"Results are exploratory/hypothesis-generating given modest sample size (N={len(enforced) + len(non_enforced)} companies, {len(enforced)} enforced). Bootstrap N=10,000.",
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    # Load data
    print(f"Loading contradictions from {CONTRADICTIONS_PATH}")
    with open(CONTRADICTIONS_PATH) as f:
        contra_data = json.load(f)
    pairs = contra_data["pairs"]
    print(f"  {len(pairs)} pairs")

    print(f"Loading features from {FEATURES_PATH}")
    with open(FEATURES_PATH) as f:
        feat_data = json.load(f)
    features = feat_data["features"]
    print(f"  {len(features)} feature records")

    # Count NLI-flagged contradictions
    n_contradictions = sum(1 for p in pairs if p.get("is_contradiction", False))
    print(f"\nNLI-flagged contradictions: {n_contradictions}/{len(pairs)} ({100*n_contradictions/len(pairs):.1f}%)")

    # Compute PWI (uses is_contradiction directly, no percentile threshold)
    print("\nComputing Privacy Washing Index...")
    company_metrics = compute_pwi(pairs)
    print(f"  Companies scored: {len(company_metrics)}")

    # Sort by PWI
    ranked = sorted(company_metrics.items(), key=lambda x: -x[1]["pwi"])
    print(f"\n--- Top 20 Privacy Washers ---")
    for i, (company, m) in enumerate(ranked[:20], 1):
        enforced = "***" if company in ENFORCEMENT_COMPANIES else "   "
        print(f"  {i:2d}. {enforced} {company:30s} PWI={m['pwi']:.4f} (density={m['contradiction_density']:.3f}, severity={m['avg_severity']:.3f}, pairs={m['n_pairs']}, contradictions={m['n_contradictions']})")

    print(f"\n  *** = enforcement-actioned company")

    # Per-category analysis
    print("\nComputing per-category analysis...")
    category_analysis = compute_category_analysis(pairs, features)
    print(f"\n--- Per-Category Analysis (OPPT practice categories) ---")
    for cat, stats_dict in sorted(category_analysis.items(), key=lambda x: -x[1]["mean_severity"]):
        print(f"  {cat:25s}: severity={stats_dict['mean_severity']:.4f}, tone_gap={stats_dict['mean_tone_gap']:.2f}, nli_rate={stats_dict['nli_contradiction_rate']:.3f}, hedging={stats_dict['mean_hedging']:.3f}, specificity={stats_dict['mean_specificity']:.4f}")

    # Enforcement validation
    enforcement_results = enforcement_validation(company_metrics)

    # Build output
    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "config": {
            "contradiction_detection": "NLI-primary: is_contradiction = (nli_contradiction >= 0.5)",
            "pwi_formula": "0.5 * contradiction_density + 0.5 * avg_severity",
            "severity_formula": "nli_contradiction * (1 + 0.3 * tone_gap_normalized)",
            "normalization": "min-max to [0, 1]",
            "enforcement_companies_total": len(ENFORCEMENT_COMPANIES),
        },
        "summary": {
            "companies_scored": len(company_metrics),
            "mean_pwi": round(float(np.mean([m["pwi"] for m in company_metrics.values()])), 4),
            "median_pwi": round(float(np.median([m["pwi"] for m in company_metrics.values()])), 4),
            "std_pwi": round(float(np.std([m["pwi"] for m in company_metrics.values()])), 4),
        },
        "company_rankings": [
            {"rank": i + 1, "company": company, **metrics}
            for i, (company, metrics) in enumerate(ranked)
        ],
        "category_analysis": category_analysis,
        "enforcement_validation": enforcement_results,
    }

    # Write output
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nOutput written to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
