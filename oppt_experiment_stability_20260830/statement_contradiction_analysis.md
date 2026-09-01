# OPPT Statement-Level Contradiction Analysis: Judge-Verified Results

*Generated: 2026-08-31*
*Pipeline: extract → NLI detect → 3-LLM judge verification*

## Executive Summary

The statement-level privacy washing detection pipeline processed the OPPT (123 companies) corpus, decomposing segments into **7,082 atomic statements** (1,830 commitment, 5,252 practice). After pairing COMMITMENT × PRACTICE within each company and filtering by category relevance and semantic similarity, pairs were evaluated by DeBERTa v3 NLI. The highest-confidence pairs were then verified by a 3-LLM judge panel.

**Result: 56 judge-confirmed contradictions** across **25 of 83 companies** (30%), from **38 unique commitment statements** spanning **52 unique segment pairs**. The judges rejected 93.3% of NLI-flagged pairs, confirming that NLI over-flags at the atomic statement level and that multi-model judge verification is essential.

### Pipeline Metrics

| Stage | Count | Notes |
|-------|-------|-------|
| Atomic statements extracted | 7,082 | 1,830 COMMITMENT + 5,252 PRACTICE |
| Judge input pairs | 834 | NLI-flagged, similarity filtered |
| **Judge-confirmed contradictions** | **56** | **6.7% confirmation rate** |
| Needs review (split verdict) | 0 | — |

### Judge Agreement

| Metric | Value |
|--------|-------|
| Unanimous (3/3) | 91.4% (762/834) |
| Majority (2/3) | 8.6% (72/834) |
| Usable consensus | 100.0% |
| Split/insufficient | 0 |
| Fleiss' kappa | 0.5731 (moderate) |

---

## Top Companies by Contradiction Count

| Rank | Company | Confirmed | Judged | Rate |
|------|---------|-----------|--------|------|
| 1 | duolingo | 9 | 47 | 19% |
| 2 | meta | 7 | 63 | 11% |
| 3 | roblox | 4 | 53 | 8% |
| 4 | uber | 4 | 32 | 12% |
| 5 | xiaomi | 3 | 9 | 33% |
| 6 | t-mobile | 3 | 46 | 7% |
| 7 | microsoft | 3 | 133 | 2% |
| 8 | github | 2 | 15 | 13% |
| 9 | venmo | 2 | 30 | 7% |
| 10 | perplexity | 2 | 10 | 20% |
| 11 | ngl | 2 | 4 | 50% |
| 12 | betterhelp | 2 | 12 | 17% |
| 13 | khan-academy | 1 | 62 | 2% |
| 14 | twitch | 1 | 12 | 8% |
| 15 | flock-safety | 1 | 9 | 11% |
| 16 | geo-group | 1 | 4 | 25% |
| 17 | stripe | 1 | 7 | 14% |
| 18 | sosi | 1 | 2 | 50% |
| 19 | walmart | 1 | 11 | 9% |
| 20 | peloton | 1 | 17 | 6% |

## Per-Company Highlights

### Duolingo — 9 Confirmed (19% rate)

**Example (sim=0.77, nli=1.00, majority):**
> **COMMITMENT:** Duolingo does not collect Child Users’ names, email addresses, phone numbers, or any other personal information....
> **PRACTICE:** Duolingo collects username, age, and email address when users register for an account....

**Example (sim=0.47, nli=1.00, majority):**
> **COMMITMENT:** Duolingo ABC does not collect any personal information from children....
> **PRACTICE:** Duolingo retains personal information until the user deletes their account to keep it operational....

### Meta — 7 Confirmed (11% rate)

**Example (sim=0.50, nli=1.00, majority):**
> **COMMITMENT:** The company uses sensitive information for service delivery and personalization but not for advertising....
> **PRACTICE:** The company uses collected information for advertising purposes....

**Example (sim=0.43, nli=1.00, unanimous):**
> **COMMITMENT:** The company uses sensitive information for service delivery and personalization but not for advertising....
> **PRACTICE:** The company uses users' location-related information to provide, personalize, and improve its Products, including advertisements....

### Roblox — 4 Confirmed (8% rate)

**Example (sim=0.54, nli=1.00, unanimous):**
> **COMMITMENT:** Roblox does not collect information from users under 13 years old for targeted advertising purposes....
> **PRACTICE:** The company collects personal information to personalize ads shown to users on Roblox....

**Example (sim=0.55, nli=0.99, majority):**
> **COMMITMENT:** Roblox does not show behaviorally targeted ads to users under 13 years old....
> **PRACTICE:** The company collects personal information to personalize ads shown to users on Roblox....

### Uber — 4 Confirmed (12% rate)

**Example (sim=0.50, nli=1.00, majority):**
> **COMMITMENT:** Uber does not use Guest Users' data for marketing its services or those of partners....
> **PRACTICE:** Uber uses personal data to understand user interests, preferences, and characteristics for ad personalization....

**Example (sim=0.48, nli=1.00, unanimous):**
> **COMMITMENT:** Uber does not use Guest Users' data for marketing its services or those of partners....
> **PRACTICE:** Uber uses collected interaction data for advertising purposes....

### Xiaomi — 3 Confirmed (33% rate)

**Example (sim=0.55, nli=0.99, unanimous):**
> **COMMITMENT:** Xiaomi does not transfer personal information to third parties without explicit user consent or legal justification....
> **PRACTICE:** Xiaomi collects and shares user information with third-party attribution companies to generate advertising reports....

**Example (sim=0.63, nli=0.99, majority):**
> **COMMITMENT:** Xiaomi does not transfer personal information to third parties without explicit user consent or legal justification....
> **PRACTICE:** Xiaomi discloses personal information to Ecosystem companies to provide and improve products and services....

---

## Category Analysis

### Category Pair Distribution

| Commitment Category → Practice Category | Count | % |
|----------------------------------------|-------|---|
| FIRST_PARTY -> FIRST_PARTY | 30 | 53.6% |
| THIRD_PARTY -> THIRD_PARTY | 10 | 17.9% |
| SALE_SHARING -> THIRD_PARTY | 5 | 8.9% |
| SALE_SHARING -> SALE_SHARING | 4 | 7.1% |
| FIRST_PARTY -> THIRD_PARTY | 2 | 3.6% |
| TRACKING -> TRACKING | 2 | 3.6% |
| SALE_SHARING -> FIRST_PARTY | 2 | 3.6% |
| THIRD_PARTY -> FIRST_PARTY | 1 | 1.8% |

---

## Signal Quality

### Consensus Strength of Confirmed Contradictions

| Consensus | Count | % |
|-----------|-------|---|
| Unanimous (3/3 CONTRADICTION) | 27 | 48.2% |
| Majority (2/3 CONTRADICTION) | 29 | 51.8% |

### Similarity Distribution of Confirmed Contradictions

| Similarity Range | Count | % |
|-----------------|-------|---|
| 0.85-1.00 | 0 | 0.0% |
| 0.80-0.85 | 0 | 0.0% |
| 0.75-0.80 | 2 | 3.6% |
| 0.70-0.75 | 2 | 3.6% |
| 0.65-0.70 | 4 | 7.1% |
| 0.60-0.65 | 3 | 5.4% |
| 0.55-0.60 | 7 | 12.5% |
| 0.50-0.55 | 11 | 19.6% |
| <0.50 | 27 | 48.2% |

---

## Coverage Analysis

### Companies Without Contradictions

58 companies had zero confirmed contradictions:

23andme, adobe, amazon, american-airlines, anduril, anthropic, apple, appriss, att, avast, babel-street, bi-incorporated, bumble, clearview-ai, corsight-ai, coursera, cursor, delta, doordash, ebay, epic-games, equifax, eyematch-ai, google, gravy-analytics, grindr, hyatt, ihg, lexisnexis, linkedin
... and 28 more

### Scale Analysis

| Contradictions | Companies | % |
|----------------|-----------|---|
| 0 | 58 | 70% |
| 1-4 | 23 | 28% |
| 5-9 | 2 | 2% |
| 10-19 | 0 | 0% |
| 20+ | 0 | 0% |

---

## Key Takeaways

1. **Scale**: 56 panel-confirmed contradictions across 25 companies. Panel confirmation is LLM majority agreement, not human validation; precision against expert judgment is unknown (see the paper's Limitations section).

2. **Judge filtering**: 93.3% of judged pairs were rejected; without the judge stage the pipeline would flag 834 candidate pairs, 14x the panel-confirmed count.

3. **Modal category pattern**: FIRST_PARTY -> FIRST_PARTY accounts for 53.6% of panel-confirmed contradictions. Category composition largely reflects the composition of judged pairs and is panel-sensitive (see the paper's category base-rate analysis and stability section).

4. **Similarity distribution**: the concentration of confirmations at lower similarity mirrors the composition of judged pairs; per-bin confirmation rates, not raw counts, are the informative quantity (see the paper).
