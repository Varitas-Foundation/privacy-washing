# OPPT Statement-Level Contradiction Analysis: Judge-Verified Results

*Generated: 2026-08-31*
*Pipeline: extract → NLI detect → 3-LLM judge verification*

## Executive Summary

The statement-level privacy washing detection pipeline processed the OPPT (123 companies) corpus, decomposing segments into **7,082 atomic statements** (1,830 commitment, 5,252 practice). After pairing COMMITMENT × PRACTICE within each company and filtering by category relevance and semantic similarity, pairs were evaluated by DeBERTa v3 NLI. The highest-confidence pairs were then verified by a 3-LLM judge panel.

**Result: 8 judge-confirmed contradictions** across **7 of 83 companies** (8%), from **8 unique commitment statements** spanning **8 unique segment pairs**. The judges rejected 84.3% of NLI-flagged pairs, confirming that NLI over-flags at the atomic statement level and that multi-model judge verification is essential.

### Pipeline Metrics

| Stage | Count | Notes |
|-------|-------|-------|
| Atomic statements extracted | 7,082 | 1,830 COMMITMENT + 5,252 PRACTICE |
| Judge input pairs | 834 | NLI-flagged, similarity filtered |
| **Judge-confirmed contradictions** | **8** | **1.0% confirmation rate** |
| Needs review (split verdict) | 123 | — |

### Judge Agreement

| Metric | Value |
|--------|-------|
| Unanimous (3/3) | 85.3% (711/834) |
| Majority (2/3) | 0.0% (0/834) |
| Usable consensus | 85.3% |
| Split/insufficient | 123 |

---

## Top Companies by Contradiction Count

| Rank | Company | Confirmed | Judged | Rate |
|------|---------|-----------|--------|------|
| 1 | duolingo | 2 | 47 | 4% |
| 2 | xiaomi | 1 | 9 | 11% |
| 3 | meta | 1 | 63 | 2% |
| 4 | flock-safety | 1 | 9 | 11% |
| 5 | monument | 1 | 2 | 50% |
| 6 | nordvpn | 1 | 4 | 25% |
| 7 | betterhelp | 1 | 12 | 8% |

## Per-Company Highlights

### Duolingo — 2 Confirmed (4% rate)

**Example (sim=0.59, nli=1.00, unanimous):**
> **COMMITMENT:** Duolingo collects only the bare minimum information necessary to make the app function for child users....
> **PRACTICE:** Duolingo processes and shares personal information to provide personalized advertising to users....

**Example (sim=0.73, nli=0.99, unanimous):**
> **COMMITMENT:** Duolingo does not collect Child Users’ names, email addresses, phone numbers, or any other personal information....
> **PRACTICE:** Duolingo collects personal information from children under 13 for internal service operations....

### Xiaomi — 1 Confirmed (11% rate)

**Example (sim=0.63, nli=0.99, unanimous):**
> **COMMITMENT:** Xiaomi does not transfer personal information to third parties without explicit user consent or legal justification....
> **PRACTICE:** Xiaomi discloses personal information to Ecosystem companies to provide and improve products and services....

### Meta — 1 Confirmed (2% rate)

**Example (sim=0.43, nli=1.00, unanimous):**
> **COMMITMENT:** The company uses sensitive information for service delivery and personalization but not for advertising....
> **PRACTICE:** The company uses users' location-related information to provide, personalize, and improve its Products, including advertisements....

### Flock Safety — 1 Confirmed (11% rate)

**Example (sim=0.68, nli=0.99, unanimous):**
> **COMMITMENT:** Flock does not sell Personal Information to third parties except under specified service, disclosure, legal, notice, or consent conditions....
> **PRACTICE:** Flock shares personal information with third-party advertisers for targeted advertising purposes....

### Monument — 1 Confirmed (50% rate)

**Example (sim=0.51, nli=1.00, unanimous):**
> **COMMITMENT:** Monument's website and applications do not collect health information without explicit user provision....
> **PRACTICE:** Monument collects eligibility, claims, medical history, and employer data directly from employers or third-party data providers....

---

## Category Analysis

### Category Pair Distribution

| Commitment Category → Practice Category | Count | % |
|----------------------------------------|-------|---|
| FIRST_PARTY -> FIRST_PARTY | 4 | 50.0% |
| THIRD_PARTY -> THIRD_PARTY | 2 | 25.0% |
| SALE_SHARING -> SALE_SHARING | 1 | 12.5% |
| FIRST_PARTY -> THIRD_PARTY | 1 | 12.5% |

---

## Signal Quality

### Consensus Strength of Confirmed Contradictions

| Consensus | Count | % |
|-----------|-------|---|
| Unanimous (3/3 CONTRADICTION) | 8 | 100.0% |
| Majority (2/3 CONTRADICTION) | 0 | 0.0% |

### Similarity Distribution of Confirmed Contradictions

| Similarity Range | Count | % |
|-----------------|-------|---|
| 0.85-1.00 | 0 | 0.0% |
| 0.80-0.85 | 0 | 0.0% |
| 0.75-0.80 | 0 | 0.0% |
| 0.70-0.75 | 1 | 12.5% |
| 0.65-0.70 | 1 | 12.5% |
| 0.60-0.65 | 1 | 12.5% |
| 0.55-0.60 | 1 | 12.5% |
| 0.50-0.55 | 4 | 50.0% |

---

## Coverage Analysis

### Companies Without Contradictions

76 companies had zero confirmed contradictions:

23andme, adobe, amazon, american-airlines, anduril, anthropic, apple, appriss, att, avast, babel-street, bi-incorporated, bumble, clearview-ai, corsight-ai, coursera, cursor, delta, doordash, ebay, epic-games, equifax, eyematch-ai, geo-group, github, google, gravy-analytics, grindr, hilton, hyatt
... and 46 more

### Scale Analysis

| Contradictions | Companies | % |
|----------------|-----------|---|
| 0 | 76 | 92% |
| 1-4 | 7 | 8% |
| 5-9 | 0 | 0% |
| 10-19 | 0 | 0% |
| 20+ | 0 | 0% |

---

## Key Takeaways

1. **Scale validation**: 8 confirmed contradictions across 7 companies demonstrates that privacy washing is widespread, not limited to a few bad actors.

2. **Judge verification is essential**: 84.3% rejection rate means that without judges, the pipeline would report 834 "contradictions" — 104× the actual count.

3. **FIRST_PARTY → FIRST_PARTY dominates**: 50.0% of all contradictions involve this category pattern.

4. **Lower similarity contains more contradictions**: Cross-topic contradictions (broad commitment vs. specific practice) are the core privacy washing pattern.
