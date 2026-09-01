"""
Script 4: Contradiction Report Generator

Generates paper-ready analysis report from privacy washing detection pipeline.

Sections:
  1. Executive summary
  2. Top 20 privacy washers with evidence excerpts
  3. Most common contradiction patterns
  4. Per-category analysis (which OPPT topics are most washed)
  5. Case studies: Meta, Microsoft, Netflix
  6. Enforcement validation statistics
  7. Methodology notes

Output:
  - contradiction_report.md (human-readable)
  - contradiction_report_tables.tex (LaTeX tables)
  - figures/*.csv (plot data)

Input: all_segments.json, linguistic_features.json, contradictions.json, privacy_washing_index.json
"""

import json
import csv
import os
import sys
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter

import numpy as np

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[1]
SEGMENTS_PATH = DATA_DIR / "oppt" / "all_segments.json"
FEATURES_PATH = REPO_ROOT / "output" / "linguistic_features.json"
CONTRADICTIONS_PATH = REPO_ROOT / "output" / "contradictions.json"
PWI_PATH = REPO_ROOT / "output" / "privacy_washing_index.json"

OUTPUT_DIR = REPO_ROOT / "output"
FIGURES_DIR = OUTPUT_DIR / "figures"

# Optional --data-dir override: read/write all files from a custom directory
_DATA_DIR = None
for _i, _arg in enumerate(sys.argv[1:], 1):
    if _arg == "--data-dir" and _i < len(sys.argv) - 1:
        _DATA_DIR = Path(sys.argv[_i + 1])
if _DATA_DIR:
    SEGMENTS_PATH = _DATA_DIR / "all_segments.json"
    FEATURES_PATH = _DATA_DIR / "linguistic_features.json"
    CONTRADICTIONS_PATH = _DATA_DIR / "contradictions.json"
    PWI_PATH = _DATA_DIR / "privacy_washing_index.json"
    OUTPUT_DIR = _DATA_DIR
    FIGURES_DIR = _DATA_DIR / "figures"

# Enforcement set (same as Script 3)
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


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def slugify(name: str) -> str:
    """Convert company slug to display name."""
    return name.replace("-", " ").title()


def truncate(text: str, max_len: int = 200) -> str:
    """Truncate text with ellipsis."""
    text = text.replace("\n", " ").strip()
    if len(text) <= max_len:
        return text
    return text[:max_len].rsplit(" ", 1)[0] + "..."


def escape_latex(text: str) -> str:
    """Escape special LaTeX characters."""
    for char in ["&", "%", "$", "#", "_", "{", "}"]:
        text = text.replace(char, "\\" + char)
    text = text.replace("~", "\\textasciitilde{}")
    text = text.replace("^", "\\textasciicircum{}")
    return text


# ---------------------------------------------------------------------------
# Report sections
# ---------------------------------------------------------------------------

def section_executive_summary(pwi_data: dict, contra_data: dict) -> str:
    """Generate executive summary."""
    summary = pwi_data["summary"]
    config = pwi_data["config"]
    enforcement = pwi_data["enforcement_validation"]
    contra_summary = contra_data["summary"]

    n_companies = summary["companies_scored"]
    mean_pwi = summary["mean_pwi"]
    n_pairs = contra_summary["total_pairs"]

    # NLI-flagged contradiction count
    n_contradictions = sum(r["n_contradictions"] for r in pwi_data["company_rankings"])
    contradiction_rate = n_contradictions / max(n_pairs, 1)
    companies_with = sum(1 for r in pwi_data["company_rankings"] if r["n_contradictions"] > 0)

    # Evidence type breakdown from P90 contradictions
    ev_totals = {"nli_plus_tone": 0, "nli": 0}
    for r in pwi_data["company_rankings"]:
        for et in ev_totals:
            ev_totals[et] += r.get("evidence_type_counts", {}).get(et, 0)

    # Top 5
    top5 = pwi_data["company_rankings"][:5]
    top5_str = ", ".join(f"{slugify(r['company'])} ({r['pwi']:.3f})" for r in top5)

    # Enforcement result — handle case with no enforcement overlap
    enf_mean = enforcement["enforced_pwi_mean"]
    nonenf_mean = enforcement["non_enforced_pwi_mean"]
    mw_p = enforcement["mann_whitney_p"]
    d = enforcement["cohens_d"]
    auc = enforcement["roc_auc"]
    n_enforced = enforcement["n_enforced"]

    if n_enforced > 0 and enf_mean is not None and auc is not None:
        enforcement_text = (
            f"Enforced companies (n={n_enforced}) showed mean PWI={enf_mean:.4f}\n"
            f"vs. non-enforced (n={enforcement['n_non_enforced']}) mean PWI={nonenf_mean:.4f}.\n"
            f"The difference is **not statistically significant** (Mann-Whitney U p={mw_p:.4f},\n"
            f"Cohen's d={d:.4f} [{enforcement['cohens_d_ci_95'][0]:.4f}, {enforcement['cohens_d_ci_95'][1]:.4f}],\n"
            f"ROC-AUC={auc:.4f} [{enforcement['roc_auc_ci_95'][0]:.4f}, {enforcement['roc_auc_ci_95'][1]:.4f}]).\n"
            "This null result indicates that privacy washing as measured by our index does not\n"
            "predict regulatory enforcement actions in this corpus, consistent with the\n"
            "exploratory nature of this analysis."
        )
    else:
        enforcement_text = (
            f"No enforcement-actioned companies overlap with this corpus (0 of {enforcement['n_non_enforced']} scored).\n"
            "Enforcement validation is not applicable for this dataset."
        )

    nli_flagged = contra_summary.get("nli_flagged_count", contra_summary["total_contradictions"])

    return f"""## 1. Executive Summary

We analyzed **{n_companies} companies** with claim-practice pair detection,
evaluating **{n_pairs:,} segment pairs** for rhetorical contradictions using
an NLI-primary approach. The NLI model (DeBERTa v3) is the sole gate for
contradiction detection; tone gap serves as a severity modifier (up to +30%)
but does not independently flag contradictions.

The NLI model flagged **{n_contradictions:,} contradictions** ({contradiction_rate*100:.1f}%
of pairs) across **{companies_with} companies**.

**Evidence type distribution:**
- NLI + tone gap: {ev_totals['nli_plus_tone']}
- NLI only: {ev_totals['nli']}

**Top 5 privacy washers:** {top5_str}

**Enforcement validation (exploratory):**
{enforcement_text}
"""


def section_top20(pwi_data: dict) -> str:
    """Generate top 20 privacy washers table."""
    rankings = pwi_data["company_rankings"][:20]

    lines = ["## 2. Top 20 Privacy Washers\n"]
    lines.append("| Rank | Company | PWI | Density | Severity | Pairs | Contradictions | Enforced |")
    lines.append("|------|---------|-----|---------|----------|-------|----------------|----------|")

    for r in rankings:
        enforced = "Yes" if r["company"] in ENFORCEMENT_COMPANIES else ""
        lines.append(
            f"| {r['rank']} | {slugify(r['company'])} | {r['pwi']:.4f} | "
            f"{r['contradiction_density']:.3f} | {r['avg_severity']:.3f} | "
            f"{r['n_pairs']} | {r['n_contradictions']} | {enforced} |"
        )

    lines.append("")

    # Evidence excerpts for top 5
    lines.append("### Top 5 — Evidence Excerpts\n")
    for r in rankings[:5]:
        lines.append(f"**{r['rank']}. {slugify(r['company'])}** (PWI={r['pwi']:.4f})")
        for j, c in enumerate(r.get("top_3_contradictions", [])[:2], 1):
            lines.append(f"- Contradiction {j} [{c['evidence_type']}] (severity={c['severity']:.3f}):")
            lines.append(f'  - *Claim ({c["claim_id"]}):* "{truncate(c["claim_preview"], 150)}"')
            lines.append(f'  - *Practice ({c["practice_id"]}):* "{truncate(c["practice_preview"], 150)}"')
        lines.append("")

    return "\n".join(lines)


def section_patterns(contra_data: dict, segments_lookup: dict) -> str:
    """Analyze most common contradiction patterns by claim type."""
    pairs = contra_data["pairs"]

    # Get NLI-flagged contradictions
    contradictions = [p for p in pairs if p.get("is_contradiction", False)]

    # Cluster by claim category
    claim_cats = Counter(c["claim_category"] for c in contradictions)
    practice_cats = Counter(c["practice_category"] for c in contradictions)

    # Cluster by claim-practice category pairs
    pair_cats = Counter(
        (c["claim_category"], c["practice_category"]) for c in contradictions
    )
    top_pairs = pair_cats.most_common(10)

    lines = ["## 3. Most Common Contradiction Patterns\n"]
    lines.append("### Claim Segment Categories (sources of reassurance language)")
    lines.append("| Category | Count | % of Contradictions |")
    lines.append("|----------|-------|---------------------|")
    for cat, count in claim_cats.most_common():
        pct = count / len(contradictions) * 100
        lines.append(f"| {cat} | {count} | {pct:.1f}% |")

    lines.append("")
    lines.append("### Practice Segment Categories (targets of contradiction)")
    lines.append("| Category | Count | % of Contradictions |")
    lines.append("|----------|-------|---------------------|")
    for cat, count in practice_cats.most_common():
        pct = count / len(contradictions) * 100
        lines.append(f"| {cat} | {count} | {pct:.1f}% |")

    lines.append("")
    lines.append("### Top 10 Claim → Practice Category Pairs")
    lines.append("| Claim Category | Practice Category | Count |")
    lines.append("|----------------|-------------------|-------|")
    for (claim_cat, practice_cat), count in top_pairs:
        lines.append(f"| {claim_cat} | {practice_cat} | {count} |")

    lines.append("")
    return "\n".join(lines)


def section_categories(pwi_data: dict) -> str:
    """Per-category analysis."""
    cats = pwi_data["category_analysis"]

    lines = ["## 4. Per-Category Analysis\n"]
    lines.append("Which OPPT practice categories exhibit the largest rhetorical contradictions?\n")
    lines.append("| Category | N Pairs | Severity | Tone Gap | NLI Rate | Hedging | Specificity | Vagueness |")
    lines.append("|----------|---------|----------|----------|----------|---------|-------------|-----------|")

    sorted_cats = sorted(cats.items(), key=lambda x: -x[1]["mean_severity"])
    for cat, s in sorted_cats:
        lines.append(
            f"| {cat} | {s['n_pairs']} | {s['mean_severity']:.4f} | "
            f"{s['mean_tone_gap']:.2f} | {s['nli_contradiction_rate']:.3f} | "
            f"{s['mean_hedging']:.3f} | {s['mean_specificity']:.4f} | {s['mean_vagueness']:.4f} |"
        )

    lines.append("")
    lines.append("**Key findings:**")

    # Data-driven findings: identify top categories by NLI rate, tone gap, hedging
    if sorted_cats:
        top_nli = max(sorted_cats, key=lambda x: x[1].get("nli_contradiction_rate", 0))
        top_tone = max(sorted_cats, key=lambda x: x[1].get("mean_tone_gap", 0))
        top_hedge = max(sorted_cats, key=lambda x: x[1].get("mean_hedging", 0))

        lines.append(
            f"- **{top_nli[0]}** has the highest NLI contradiction rate "
            f"({top_nli[1]['nli_contradiction_rate']:.1%}), suggesting the starkest gap "
            f"between reassuring language and practice disclosures in this category."
        )
        lines.append(
            f"- **{top_tone[0]}** has the highest mean tone gap "
            f"({top_tone[1]['mean_tone_gap']:.2f}), driven by hedging "
            f"({top_tone[1]['mean_hedging']:.3f}) and low specificity "
            f"({top_tone[1]['mean_specificity']:.4f})."
        )
        lines.append(
            f"- **{top_hedge[0]}** has the highest hedging score "
            f"({top_hedge[1]['mean_hedging']:.3f}) with vagueness "
            f"({top_hedge[1]['mean_vagueness']:.4f}) — language in this category is most evasive."
        )
    lines.append("")

    return "\n".join(lines)


def section_case_studies(contra_data: dict, features_lookup: dict,
                        segments_lookup: dict, pwi_data: dict) -> str:
    """Case studies for top-ranked companies."""
    pairs = contra_data["pairs"]
    company_rankings = {r["company"]: r for r in pwi_data["company_rankings"]}

    # Use top 3 PWI-ranked companies (with at least 1 contradiction)
    case_companies = [
        r["company"] for r in pwi_data["company_rankings"]
        if r["n_contradictions"] > 0
    ][:3]
    lines = ["## 5. Case Studies\n"]

    for company in case_companies:
        company_pairs = [p for p in pairs if p["company"] == company]
        if not company_pairs:
            lines.append(f"### {slugify(company)}")
            lines.append(f"No claim-practice pairs generated (no reassurance language detected).\n")
            continue

        ranking = company_rankings.get(company, {})
        pwi = ranking.get("pwi", 0)
        rank = ranking.get("rank", "N/A")

        # Company segments
        company_segs = [s for s in segments_lookup.values() if s.get("company") == company]
        company_feats = [features_lookup[s["segment_id"]] for s in company_segs if s["segment_id"] in features_lookup]

        # Category distribution
        cat_dist = Counter(s["primary_category"] for s in company_segs)

        # NLI-flagged contradictions
        company_contradictions = sorted(
            [p for p in company_pairs if p.get("is_contradiction", False)],
            key=lambda x: -x["severity"]
        )

        # Reassurance segments
        reassurance_segs = [f for f in company_feats if f["reassurance_count"] > 0]

        lines.append(f"### {slugify(company)} (Rank #{rank}, PWI={pwi:.4f})")
        lines.append(f"- **Total segments:** {len(company_segs)}")
        lines.append(f"- **Reassurance segments:** {len(reassurance_segs)}")
        lines.append(f"- **Claim-practice pairs:** {len(company_pairs)}")
        lines.append(f"- **Contradictions (NLI-flagged):** {len(company_contradictions)}")
        lines.append(f"- **Categories:** {', '.join(f'{cat}: {n}' for cat, n in cat_dist.most_common(5))}")
        lines.append("")

        if company_contradictions:
            lines.append(f"**Top contradictions:**\n")
            for i, c in enumerate(company_contradictions[:3], 1):
                claim_text = segments_lookup.get(c["claim_id"], {}).get("text", c.get("claim_text_preview", ""))
                practice_text = segments_lookup.get(c["practice_id"], {}).get("text", c.get("practice_text_preview", ""))
                lines.append(f"{i}. **[{c['evidence_type']}]** severity={c['severity']:.3f}, NLI={c['nli_contradiction']:.3f}")
                lines.append(f'   - *Claim ({c["claim_id"]}, {c["claim_category"]}):* "{truncate(claim_text, 200)}"')
                lines.append(f'   - *Practice ({c["practice_id"]}, {c["practice_category"]}):* "{truncate(practice_text, 200)}"')
                lines.append("")

        lines.append("")

    return "\n".join(lines)


def section_enforcement(pwi_data: dict) -> str:
    """Enforcement validation statistics."""
    e = pwi_data["enforcement_validation"]

    lines = ["## 6. Enforcement Validation Statistics\n"]

    n_enforced = e['n_enforced']
    n_total = n_enforced + e['n_non_enforced']
    lines.append(f"**Sample:** {n_enforced} enforcement-actioned companies, {e['n_non_enforced']} non-enforced (total: {n_total})")

    # If no enforcement companies overlap, emit a short note and return
    if n_enforced == 0 or e.get("enforced_pwi_mean") is None:
        if e.get("enforcement_companies_missing_from_analysis"):
            lines.append(f"**Missing from analysis:** {', '.join(e['enforcement_companies_missing_from_analysis'])} (no reassurance-practice pairs generated)")
        lines.append("")
        lines.append("No enforcement-actioned companies overlap with this corpus. Enforcement validation is not applicable.")
        lines.append("")
        return "\n".join(lines)

    if e.get("enforcement_companies_missing_from_analysis"):
        lines.append(f"**Missing from analysis:** {', '.join(e['enforcement_companies_missing_from_analysis'])} (no reassurance-practice pairs generated)")
    lines.append("")

    lines.append("| Metric | Value | 95% CI |")
    lines.append("|--------|-------|--------|")
    lines.append(f"| Enforced mean PWI | {e['enforced_pwi_mean']:.4f} | [{e['enforced_pwi_ci_95'][0]:.4f}, {e['enforced_pwi_ci_95'][1]:.4f}] |")
    lines.append(f"| Non-enforced mean PWI | {e['non_enforced_pwi_mean']:.4f} | [{e['non_enforced_pwi_ci_95'][0]:.4f}, {e['non_enforced_pwi_ci_95'][1]:.4f}] |")
    lines.append(f"| Mean difference | {e['mean_difference']:.4f} | — |")
    lines.append(f"| Mann-Whitney U | {e['mann_whitney_u']:.1f} | p={e['mann_whitney_p']:.4f} |")
    lines.append(f"| Cohen's d | {e['cohens_d']:.4f} ({e['cohens_d_interpretation']}) | [{e['cohens_d_ci_95'][0]:.4f}, {e['cohens_d_ci_95'][1]:.4f}] |")

    if e.get("roc_auc") is not None:
        lines.append(f"| ROC-AUC | {e['roc_auc']:.4f} | [{e['roc_auc_ci_95'][0]:.4f}, {e['roc_auc_ci_95'][1]:.4f}] |")

    lines.append("")
    lines.append(f"**Interpretation:** The null result (p={e['mann_whitney_p']:.2f}, d={e['cohens_d']:.2f}, AUC={e.get('roc_auc', 0.5):.2f}) indicates no detectable")
    lines.append("association between privacy washing intensity and enforcement history in this corpus.")
    lines.append("Several explanations are plausible:")
    lines.append("1. Enforcement actions target observable behaviors and outcomes, not policy rhetoric")
    lines.append("2. Companies facing enforcement may have updated their policies post-enforcement")
    lines.append(f"3. The sample size (N={n_total}, {n_enforced} enforced) provides limited statistical power")
    lines.append("4. PWI captures rhetorical dissonance, which may be orthogonal to enforcement-triggering behaviors")
    lines.append("")
    lines.append(f"*{e.get('note', '')}*")
    lines.append("")

    return "\n".join(lines)


def section_methodology(pwi_data: dict = None, n_segments: int = 0) -> str:
    """Methodology notes."""
    e = pwi_data.get("enforcement_validation", {}) if pwi_data else {}
    n_total = e.get("n_enforced", 0) + e.get("n_non_enforced", 0) if e else "N"
    n_enforced = e.get("n_enforced", "?") if e else "?"
    return f"""## 7. Methodology Notes

### Pipeline Overview

1. **Linguistic features** (Script 1): Per-segment hedging, reassurance, specificity, commitment
   strength, and readability scores extracted from {n_segments:,} annotated segments.

2. **Contradiction detection** (Script 2): Cross-segment analysis within each company.
   Claim segments (any reassurance language) paired with practice segments
   (FIRST_PARTY, THIRD_PARTY, TRACKING, SALE_SHARING, SENSITIVE_DATA,
   AUTOMATED_DECISIONS, RETENTION, SECURITY). NLI-primary scoring:
   - **NLI** (primary signal): DeBERTa v3 base fine-tuned on SNLI+MultiNLI
     (cross-encoder/nli-deberta-v3-base). Only NLI flags contradictions.
   - **Tone gap** (severity modifier): reassurance(claim) x hedging(practice)
     / specificity(practice). Boosts severity of NLI-flagged pairs by up to 30%
     but does not independently flag contradictions.

3. **Privacy Washing Index** (Script 3): Per-company metric combining contradiction
   density and severity, min-max normalized to [0,1].

4. **Report** (Script 4): This document.

### Known Limitations

- **NLI domain mismatch**: Model trained on general NLI data, not legal/policy text.
  Performance on legal entailment tasks is known to degrade significantly
  (66% on COLIEE statute law vs 90% on MNLI). Tone gap serves as a severity
  modifier to partially compensate for NLI uncertainty.

- **Hedge keyword overcount**: ~90% of potential hedge keywords are not actual hedges
  in context (Vincze et al., 2008). Scores represent upper-bound estimates, useful
  for relative comparisons.

- **Readability metrics**: Flesch-Kincaid is a shallow surface feature. NLP-based
  alternatives (Crossley et al., 2017, 2019) would be more accurate but less
  comparable with prior work.

- **Reassurance lexicon**: No validated lexicon exists for privacy policies. Our
  lexicon is constructed from manual inspection and should be considered preliminary.

- **Statistical power**: With {n_total} companies ({n_enforced} enforced) in the enforcement
  analysis, statistical power is modest. All results should be treated as
  exploratory and hypothesis-generating.

- **Python 3.14 compatibility**: spaCy NER was replaced with regex-based entity
  detection due to a Pydantic v1 incompatibility. This affects the specificity
  score's entity detection component (ORG, DATE, MONEY) but does not fundamentally
  change the metric.
"""


# ---------------------------------------------------------------------------
# LaTeX tables
# ---------------------------------------------------------------------------

def generate_latex_tables(pwi_data: dict, contra_data: dict) -> str:
    """Generate LaTeX tables for paper."""
    lines = []

    # Table 1: Top 20 Privacy Washers
    lines.append("% Table 1: Top 20 Privacy Washers")
    lines.append("\\begin{table*}[t]")
    lines.append("\\centering")
    lines.append("\\caption{Top 20 companies by Privacy Washing Index (PWI). Enforcement-actioned companies marked with $\\dagger$.}")
    lines.append("\\label{tab:top20}")
    lines.append("\\begin{tabular}{rlccccl}")
    lines.append("\\toprule")
    lines.append("Rank & Company & PWI & Density & Severity & Pairs & Evidence \\\\")
    lines.append("\\midrule")

    for r in pwi_data["company_rankings"][:20]:
        name = escape_latex(slugify(r["company"]))
        if r["company"] in ENFORCEMENT_COMPANIES:
            name += "$^\\dagger$"
        ev = r.get("evidence_type_counts", {})
        ev_str = f"NT:{ev.get('nli_plus_tone',0)} N:{ev.get('nli',0)}"
        lines.append(
            f"{r['rank']} & {name} & {r['pwi']:.3f} & {r['contradiction_density']:.3f} & "
            f"{r['avg_severity']:.3f} & {r['n_pairs']} & {ev_str} \\\\"
        )

    lines.append("\\bottomrule")
    lines.append("\\end{tabular}")
    lines.append("\\end{table*}")
    lines.append("")

    # Table 2: Per-category analysis
    lines.append("% Table 2: Per-OPPT Category Contradiction Analysis")
    lines.append("\\begin{table}[t]")
    lines.append("\\centering")
    lines.append("\\caption{Rhetorical contradiction metrics by OPPT practice category, sorted by severity.}")
    lines.append("\\label{tab:categories}")
    lines.append("\\begin{tabular}{lccccc}")
    lines.append("\\toprule")
    lines.append("Category & Pairs & Severity & NLI Rate & Hedging & Specificity \\\\")
    lines.append("\\midrule")

    sorted_cats = sorted(
        pwi_data["category_analysis"].items(),
        key=lambda x: -x[1]["mean_severity"]
    )
    for cat, s in sorted_cats:
        cat_name = escape_latex(cat.replace("_", "\\_"))
        lines.append(
            f"{cat_name} & {s['n_pairs']} & {s['mean_severity']:.4f} & "
            f"{s['nli_contradiction_rate']:.3f} & {s['mean_hedging']:.3f} & {s['mean_specificity']:.4f} \\\\"
        )

    lines.append("\\bottomrule")
    lines.append("\\end{tabular}")
    lines.append("\\end{table}")
    lines.append("")

    # Table 3: Enforcement validation
    e = pwi_data["enforcement_validation"]
    lines.append("% Table 3: Enforcement Validation")
    lines.append("\\begin{table}[t]")
    lines.append("\\centering")
    lines.append("\\caption{Privacy Washing Index vs. regulatory enforcement history. Bootstrap 95\\% CIs (N=10,000).}")
    lines.append("\\label{tab:enforcement}")
    lines.append("\\begin{tabular}{lcc}")
    lines.append("\\toprule")
    lines.append("Metric & Value & 95\\% CI \\\\")
    lines.append("\\midrule")
    lines.append(f"Enforced mean PWI (n={e['n_enforced']}) & {e['enforced_pwi_mean']:.4f} & [{e['enforced_pwi_ci_95'][0]:.4f}, {e['enforced_pwi_ci_95'][1]:.4f}] \\\\")
    lines.append(f"Non-enforced mean PWI (n={e['n_non_enforced']}) & {e['non_enforced_pwi_mean']:.4f} & [{e['non_enforced_pwi_ci_95'][0]:.4f}, {e['non_enforced_pwi_ci_95'][1]:.4f}] \\\\")
    lines.append(f"Mann-Whitney U & {e['mann_whitney_u']:.1f} & $p={e['mann_whitney_p']:.4f}$ \\\\")
    lines.append(f"Cohen's $d$ & {e['cohens_d']:.4f} & [{e['cohens_d_ci_95'][0]:.4f}, {e['cohens_d_ci_95'][1]:.4f}] \\\\")
    if e.get("roc_auc") is not None:
        lines.append(f"ROC-AUC & {e['roc_auc']:.4f} & [{e['roc_auc_ci_95'][0]:.4f}, {e['roc_auc_ci_95'][1]:.4f}] \\\\")
    lines.append("\\bottomrule")
    lines.append("\\end{tabular}")
    lines.append("\\end{table}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Figure CSVs
# ---------------------------------------------------------------------------

def generate_figure_csvs(pwi_data: dict, contra_data: dict, features: list[dict]):
    """Generate CSV data for plots."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    # 1. PWI distribution
    with open(FIGURES_DIR / "pwi_distribution.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["company", "pwi", "rank", "enforced", "n_pairs", "n_contradictions", "density", "severity"])
        for r in pwi_data["company_rankings"]:
            writer.writerow([
                r["company"], r["pwi"], r["rank"],
                1 if r["company"] in ENFORCEMENT_COMPANIES else 0,
                r["n_pairs"], r["n_contradictions"],
                r["contradiction_density"], r["avg_severity"],
            ])

    # 2. Category analysis
    with open(FIGURES_DIR / "category_analysis.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["category", "n_pairs", "severity", "tone_gap", "nli_rate", "hedging", "specificity", "vagueness"])
        for cat, s in sorted(pwi_data["category_analysis"].items(), key=lambda x: -x[1]["mean_severity"]):
            writer.writerow([
                cat, s["n_pairs"], s["mean_severity"], s["mean_tone_gap"],
                s["nli_contradiction_rate"], s["mean_hedging"], s["mean_specificity"], s["mean_vagueness"],
            ])

    # 3. Enforcement comparison (for box plot)
    with open(FIGURES_DIR / "enforcement_comparison.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["company", "pwi", "group"])
        for r in pwi_data["company_rankings"]:
            group = "enforced" if r["company"] in ENFORCEMENT_COMPANIES else "non-enforced"
            writer.writerow([r["company"], r["pwi"], group])

    # 4. Feature distributions per category
    with open(FIGURES_DIR / "feature_by_category.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["segment_id", "company", "category", "hedging", "reassurance", "specificity", "commitment", "vague_ratio", "fk_grade"])
        for feat in features:
            writer.writerow([
                feat["segment_id"], feat["company"], feat["primary_category"],
                feat["hedging_score"], feat["reassurance_score"], feat["specificity_score"],
                feat["commitment_strength"], feat["vague_ratio"], feat["flesch_kincaid_grade"],
            ])

    print(f"  Figure CSVs written to {FIGURES_DIR}/")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    # Load all data
    print("Loading data...")
    with open(SEGMENTS_PATH) as f:
        seg_data = json.load(f)
    segments_lookup = {s["segment_id"]: s for s in seg_data["segments"]}

    with open(FEATURES_PATH) as f:
        feat_data = json.load(f)
    features = feat_data["features"]
    features_lookup = {f["segment_id"]: f for f in features}

    with open(CONTRADICTIONS_PATH) as f:
        contra_data = json.load(f)

    with open(PWI_PATH) as f:
        pwi_data = json.load(f)

    print(f"  Segments: {len(segments_lookup)}")
    print(f"  Features: {len(features)}")
    print(f"  Pairs: {len(contra_data['pairs'])}")
    print(f"  Companies ranked: {len(pwi_data['company_rankings'])}")

    # Generate report sections
    print("\nGenerating report...")
    report_parts = [
        f"# Privacy Washing Detection Report\n",
        f"*Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}*\n",
        f"*Pipeline: linguistic_features → detect_contradictions → privacy_washing_index → contradiction_report*\n",
        section_executive_summary(pwi_data, contra_data),
        section_top20(pwi_data),
        section_patterns(contra_data, segments_lookup),
        section_categories(pwi_data),
        section_case_studies(contra_data, features_lookup, segments_lookup, pwi_data),
        section_enforcement(pwi_data),
        section_methodology(pwi_data, n_segments=len(segments_lookup)),
    ]

    report = "\n---\n\n".join(report_parts)

    # Write markdown report
    report_path = OUTPUT_DIR / "contradiction_report.md"
    with open(report_path, "w") as f:
        f.write(report)
    print(f"  Report written to {report_path}")

    # Generate LaTeX tables
    print("Generating LaTeX tables...")
    latex = generate_latex_tables(pwi_data, contra_data)
    latex_path = OUTPUT_DIR / "contradiction_report_tables.tex"
    with open(latex_path, "w") as f:
        f.write(latex)
    print(f"  LaTeX tables written to {latex_path}")

    # Generate figure CSVs
    print("Generating figure CSVs...")
    generate_figure_csvs(pwi_data, contra_data, features)

    print("\nDone.")


if __name__ == "__main__":
    main()
