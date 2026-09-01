# OPPT Statement-Level Contradiction Analysis: Judge-Verified Results

*Generated: 2026-01-30*
*Pipeline: extract → NLI detect → 3-LLM judge verification*

## Executive Summary

The statement-level privacy washing detection pipeline processed the OPPT (123 companies) corpus, decomposing segments into **18,446 atomic statements** (4,861 commitment, 13,585 practice). After pairing COMMITMENT × PRACTICE within each company and filtering by category relevance and semantic similarity, pairs were evaluated by DeBERTa v3 NLI. The highest-confidence pairs were then verified by a 3-LLM judge panel.

**Result: 602 judge-confirmed contradictions** across **70 of 116 companies** (60%), from **266 unique commitment statements** spanning **419 unique segment pairs**. The judges rejected 92.1% of NLI-flagged pairs, confirming that NLI over-flags at the atomic statement level and that multi-model judge verification is essential.

### Pipeline Metrics

| Stage | Count | Notes |
|-------|-------|-------|
| Atomic statements extracted | 18,446 | 4,861 COMMITMENT + 13,585 PRACTICE |
| Judge input pairs | 7,667 | NLI-flagged, similarity filtered |
| **Judge-confirmed contradictions** | **602** | **7.9% confirmation rate** |
| Needs review (split verdict) | 2 | — |

### Judge Agreement

| Metric | Value |
|--------|-------|
| Unanimous (3/3) | 85.8% (6,582/7,667) |
| Majority (2/3) | 14.1% (1,083/7,667) |
| Usable consensus | 100.0% |
| Split/insufficient | 2 |
| Fleiss' kappa | 0.4542 (moderate) |

---

## Top Companies by Contradiction Count

| Rank | Company | Confirmed | Judged | Rate |
|------|---------|-----------|--------|------|
| 1 | t-mobile | 47 | 367 | 13% |
| 2 | duolingo | 38 | 223 | 17% |
| 3 | meta | 33 | 405 | 8% |
| 4 | delta | 30 | 399 | 8% |
| 5 | equifax | 30 | 132 | 23% |
| 6 | linkedin | 25 | 378 | 7% |
| 7 | khan-academy | 23 | 369 | 6% |
| 8 | adobe | 22 | 97 | 23% |
| 9 | grindr | 21 | 129 | 16% |
| 10 | microsoft | 20 | 272 | 7% |
| 11 | peloton | 17 | 266 | 6% |
| 12 | perplexity | 17 | 52 | 33% |
| 13 | venmo | 16 | 154 | 10% |
| 14 | github | 14 | 112 | 12% |
| 15 | roblox | 14 | 225 | 6% |
| 16 | walmart | 12 | 122 | 10% |
| 17 | monument | 11 | 89 | 12% |
| 18 | bumble | 10 | 293 | 3% |
| 19 | betterhelp | 10 | 45 | 22% |
| 20 | clearview-ai | 10 | 65 | 15% |

## Per-Company Highlights

### T Mobile — 47 Confirmed (13% rate)

**Example (sim=0.67, nli=1.00, unanimous):**
> **COMMITMENT:** T-Mobile only shares data with certain third parties if you provide explicit permission....
> **PRACTICE:** T-Mobile shares generic personal information with other service providers for basic service features....

**Example (sim=0.65, nli=1.00, unanimous):**
> **COMMITMENT:** T-Mobile only shares data with certain third parties if you provide explicit permission....
> **PRACTICE:** T-Mobile shares generic personal information with internet service providers for basic service features....

### Duolingo — 38 Confirmed (17% rate)

**Example (sim=0.53, nli=1.00, majority):**
> **COMMITMENT:** Duolingo does not collect audio for product improvement from Android device or website users....
> **PRACTICE:** Duolingo uses recorded audio and transcripts to train and run its own artificial intelligence models....

**Example (sim=0.52, nli=1.00, unanimous):**
> **COMMITMENT:** Duolingo collects only the minimum information necessary to make the app function for child users....
> **PRACTICE:** FullStory captures and analyzes user activity and provides video session replays to Duolingo....

### Meta — 33 Confirmed (8% rate)

**Example (sim=0.56, nli=1.00, unanimous):**
> **COMMITMENT:** Meta uses sensitive information users provide for service delivery but not to show ads....
> **PRACTICE:** Meta uses collected information to provide personalized experiences including ads across products and devices....

**Example (sim=0.55, nli=1.00, unanimous):**
> **COMMITMENT:** Meta uses sensitive information users provide for service delivery but not to show ads....
> **PRACTICE:** Meta shares information with other Meta Companies to personalize offers, ads and sponsored content....

### Delta — 30 Confirmed (8% rate)

**Example (sim=0.62, nli=1.00, unanimous):**
> **COMMITMENT:** Delta does not receive any biometric information from the facial comparison technology process....
> **PRACTICE:** Delta collects biometric information such as fingerprint, face, voice, or iris data....

**Example (sim=0.56, nli=1.00, unanimous):**
> **COMMITMENT:** Delta uses health and dietary information only when customers have consented to meet special assistance requests....
> **PRACTICE:** Delta discloses customer information to persons discussing or acquiring any part of Delta's business....

### Equifax — 30 Confirmed (23% rate)

**Example (sim=0.68, nli=1.00, majority):**
> **COMMITMENT:** Equifax and its affiliates do not use EWS personal data for purposes such as marketing....
> **PRACTICE:** Equifax collects, uses, and sells personal data for consumer and commercial marketing services....

**Example (sim=0.65, nli=1.00, unanimous):**
> **COMMITMENT:** Equifax and its affiliates agree to use personal data from EWS products only for providing EWS services....
> **PRACTICE:** Equifax shares creditworthiness data among affiliates for everyday business purposes....

---

## Category Analysis

### Category Pair Distribution

| Commitment Category → Practice Category | Count | % |
|----------------------------------------|-------|---|
| THIRD_PARTY -> THIRD_PARTY | 149 | 24.8% |
| FIRST_PARTY -> FIRST_PARTY | 131 | 21.8% |
| SALE_SHARING -> THIRD_PARTY | 104 | 17.3% |
| FIRST_PARTY -> THIRD_PARTY | 91 | 15.1% |
| SALE_SHARING -> SALE_SHARING | 25 | 4.2% |
| FIRST_PARTY -> SALE_SHARING | 22 | 3.7% |
| THIRD_PARTY -> SALE_SHARING | 21 | 3.5% |
| THIRD_PARTY -> FIRST_PARTY | 14 | 2.3% |
| TRACKING -> THIRD_PARTY | 11 | 1.8% |
| TRACKING -> TRACKING | 8 | 1.3% |

---

## Signal Quality

### Consensus Strength of Confirmed Contradictions

| Consensus | Count | % |
|-----------|-------|---|
| Unanimous (3/3 CONTRADICTION) | 256 | 42.5% |
| Majority (2/3 CONTRADICTION) | 346 | 57.5% |

### Similarity Distribution of Confirmed Contradictions

| Similarity Range | Count | % |
|-----------------|-------|---|
| 0.85-1.00 | 0 | 0.0% |
| 0.80-0.85 | 3 | 0.5% |
| 0.75-0.80 | 17 | 2.8% |
| 0.70-0.75 | 45 | 7.5% |
| 0.65-0.70 | 87 | 14.5% |
| 0.60-0.65 | 111 | 18.4% |
| 0.55-0.60 | 165 | 27.4% |
| 0.50-0.55 | 174 | 28.9% |

---

## Coverage Analysis

### Companies Without Contradictions

46 companies had zero confirmed contradictions:

23andme, airbnb, alibaba, anthropic, apple, appriss, avast, babel-street, cellebrite, cerebral, chase, coinbase, corecivic, corsight-ai, cursor, cvs-health, discord, dropbox, eyematch-ai, fanduel, hyatt, kochava, lexisnexis, lyft, ngl, openai, palantir, penlink, premom, realtor
... and 16 more

### Scale Analysis

| Contradictions | Companies | % |
|----------------|-----------|---|
| 0 | 46 | 40% |
| 1-4 | 34 | 29% |
| 5-9 | 15 | 13% |
| 10-19 | 11 | 9% |
| 20+ | 10 | 9% |

---

## Key Takeaways

1. **Scale validation**: 602 confirmed contradictions across 70 companies demonstrates that privacy washing is widespread, not limited to a few bad actors.

2. **Judge verification is essential**: 92.1% rejection rate means that without judges, the pipeline would report 7,667 "contradictions" — 12× the actual count.

3. **THIRD_PARTY → THIRD_PARTY dominates**: 24.8% of all contradictions involve this category pattern.

4. **Lower similarity contains more contradictions**: Cross-topic contradictions (broad commitment vs. specific practice) are the core privacy washing pattern.
