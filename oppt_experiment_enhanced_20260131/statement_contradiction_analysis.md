# OPPT Statement-Level Contradiction Analysis: Judge-Verified Results

*Generated: 2026-01-31*
*Pipeline: extract → NLI detect → 3-LLM judge verification*

## Executive Summary

The statement-level privacy washing detection pipeline processed the OPPT (123 companies) corpus, decomposing segments into **6,061 atomic statements** (2,028 commitment, 4,033 practice). After pairing COMMITMENT × PRACTICE within each company and filtering by category relevance and semantic similarity, pairs were evaluated by DeBERTa v3 NLI. The highest-confidence pairs were then verified by a 3-LLM judge panel.

**Result: 33 judge-confirmed contradictions** across **16 of 60 companies** (27%), from **23 unique commitment statements** spanning **31 unique segment pairs**. The judges rejected 88.7% of NLI-flagged pairs, confirming that NLI over-flags at the atomic statement level and that multi-model judge verification is essential.

### Pipeline Metrics

| Stage | Count | Notes |
|-------|-------|-------|
| Atomic statements extracted | 6,061 | 2,028 COMMITMENT + 4,033 PRACTICE |
| Judge input pairs | 293 | NLI-flagged, similarity filtered |
| **Judge-confirmed contradictions** | **33** | **11.3% confirmation rate** |
| Needs review (split verdict) | 0 | — |

### Judge Agreement

| Metric | Value |
|--------|-------|
| Unanimous (3/3) | 83.6% (245/293) |
| Majority (2/3) | 16.4% (48/293) |
| Usable consensus | 100.0% |
| Split/insufficient | 0 |
| Fleiss' kappa | 0.4804 (moderate) |

---

## Top Companies by Contradiction Count

| Rank | Company | Confirmed | Judged | Rate |
|------|---------|-----------|--------|------|
| 1 | duolingo | 4 | 13 | 31% |
| 2 | microsoft | 4 | 30 | 13% |
| 3 | google | 4 | 4 | 100% |
| 4 | roblox | 4 | 10 | 40% |
| 5 | uber | 3 | 11 | 27% |
| 6 | github | 2 | 11 | 18% |
| 7 | walmart | 2 | 6 | 33% |
| 8 | appriss | 2 | 2 | 100% |
| 9 | meta | 1 | 21 | 5% |
| 10 | khan-academy | 1 | 34 | 3% |
| 11 | american-airlines | 1 | 3 | 33% |
| 12 | venmo | 1 | 10 | 10% |
| 13 | tesla | 1 | 8 | 12% |
| 14 | bumble | 1 | 3 | 33% |
| 15 | motorola-solutions | 1 | 4 | 25% |
| 16 | notion | 1 | 3 | 33% |

## Per-Company Highlights

### Duolingo — 4 Confirmed (31% rate)

**Example (sim=0.50, nli=1.00, unanimous):**
> **COMMITMENT:** Duolingo ABC speech data is stored on the user's phone and not shared with Duolingo....
> **PRACTICE:** The company sends user audio to third-party providers like Google, Apple, or AWS for speech recognition....

**Example (sim=0.74, nli=1.00, majority):**
> **COMMITMENT:** Duolingo deletes personal information if unknowingly collected from children under 13....
> **PRACTICE:** Duolingo retains personal information until the user deletes their account to keep it operational....

### Microsoft — 4 Confirmed (13% rate)

**Example (sim=0.51, nli=1.00, unanimous):**
> **COMMITMENT:** Microsoft uses personal data in the least identifiable form necessary and relies on statistical and aggregated pseudonymized data for business operations....
> **PRACTICE:** Microsoft transmits Tailored experiences data to Microsoft servers and stores it with unique identifiers to recognize individual users and understand device patterns....

**Example (sim=0.60, nli=1.00, unanimous):**
> **COMMITMENT:** Microsoft uses personal data in the least identifiable form necessary and relies on statistical and aggregated pseudonymized data for business operations....
> **PRACTICE:** Microsoft collects diagnostic data periodically and transmits it with unique identifiers to recognize individual users....

### Google — 4 Confirmed (100% rate)

**Example (sim=0.54, nli=1.00, majority):**
> **COMMITMENT:** Google does not share personal information with external companies, organizations, or individuals....
> **PRACTICE:** Google shares user information with third parties that integrate with Google's services when the user provides consent....

**Example (sim=0.53, nli=1.00, majority):**
> **COMMITMENT:** Google does not share personal information with external companies, organizations, or individuals....
> **PRACTICE:** Google may show other users publicly visible Google Account information when they have your email address or identifying information....

### Roblox — 4 Confirmed (40% rate)

**Example (sim=0.54, nli=1.00, majority):**
> **COMMITMENT:** Roblox does not collect information from users under 13 years old for targeted advertising purposes....
> **PRACTICE:** The company collects personal information to personalize ads shown to users on Roblox....

**Example (sim=0.51, nli=1.00, unanimous):**
> **COMMITMENT:** Roblox complies with the Children's Online Privacy Protection Act (COPPA) in the United States....
> **PRACTICE:** Roblox discloses user information to third-party advertising companies to select and measure advertisements....

### Uber — 3 Confirmed (27% rate)

**Example (sim=0.50, nli=1.00, unanimous):**
> **COMMITMENT:** Uber does not use Guest Users' data for marketing its services or those of partners....
> **PRACTICE:** Uber uses personal data to understand user interests, preferences, and characteristics for ad personalization....

**Example (sim=0.57, nli=1.00, majority):**
> **COMMITMENT:** Uber does not use Guest Users' data for marketing its services or those of partners....
> **PRACTICE:** Uber uses user data to determine whether app and website usage can be attributed to specific marketing campaigns....

---

## Category Analysis

### Category Pair Distribution

| Commitment Category → Practice Category | Count | % |
|----------------------------------------|-------|---|
| THIRD_PARTY -> THIRD_PARTY | 7 | 21.2% |
| FIRST_PARTY -> FIRST_PARTY | 6 | 18.2% |
| SALE_SHARING -> THIRD_PARTY | 6 | 18.2% |
| FIRST_PARTY -> THIRD_PARTY | 3 | 9.1% |
| TRACKING -> FIRST_PARTY | 2 | 6.1% |
| FIRST_PARTY -> TRACKING | 2 | 6.1% |
| SALE_SHARING -> SALE_SHARING | 2 | 6.1% |
| TRACKING -> SALE_SHARING | 1 | 3.0% |
| THIRD_PARTY -> SALE_SHARING | 1 | 3.0% |
| SALE_SHARING -> FIRST_PARTY | 1 | 3.0% |

---

## Signal Quality

### Consensus Strength of Confirmed Contradictions

| Consensus | Count | % |
|-----------|-------|---|
| Unanimous (3/3 CONTRADICTION) | 12 | 36.4% |
| Majority (2/3 CONTRADICTION) | 21 | 63.6% |

### Similarity Distribution of Confirmed Contradictions

| Similarity Range | Count | % |
|-----------------|-------|---|
| 0.85-1.00 | 0 | 0.0% |
| 0.80-0.85 | 0 | 0.0% |
| 0.75-0.80 | 0 | 0.0% |
| 0.70-0.75 | 2 | 6.1% |
| 0.65-0.70 | 3 | 9.1% |
| 0.60-0.65 | 4 | 12.1% |
| 0.55-0.60 | 11 | 33.3% |
| 0.50-0.55 | 13 | 39.4% |

---

## Coverage Analysis

### Companies Without Contradictions

44 companies had zero confirmed contradictions:

23andme, airbnb, amazon, anthropic, apple, babel-street, bi-incorporated, coursera, delta, discord, draftkings, ebay, epic-games, geo-group, gravy-analytics, grindr, hilton, ihg, jasper, kraken, linkedin, lyft, monument, netflix, openai, peloton, pimeyes, pinterest, reddit, redfin
... and 14 more

### Scale Analysis

| Contradictions | Companies | % |
|----------------|-----------|---|
| 0 | 44 | 73% |
| 1-4 | 16 | 27% |
| 5-9 | 0 | 0% |
| 10-19 | 0 | 0% |
| 20+ | 0 | 0% |

---

## Key Takeaways

1. **Scale validation**: 33 confirmed contradictions across 16 companies demonstrates that privacy washing is widespread, not limited to a few bad actors.

2. **Judge verification is essential**: 88.7% rejection rate means that without judges, the pipeline would report 293 "contradictions" — 8× the actual count.

3. **THIRD_PARTY → THIRD_PARTY dominates**: 21.2% of all contradictions involve this category pattern.

4. **Lower similarity contains more contradictions**: Cross-topic contradictions (broad commitment vs. specific practice) are the core privacy washing pattern.
