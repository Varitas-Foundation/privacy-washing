# OPP-115 Statement-Level Contradiction Analysis: Judge-Verified Results

*Generated: 2026-01-29*
*Pipeline: extract → NLI detect → 3-LLM judge verification*

## Executive Summary

The statement-level privacy washing detection pipeline processed the OPP-115 (115 companies) corpus, decomposing segments into **11,111 atomic statements** (3,214 commitment, 7,897 practice). After pairing COMMITMENT × PRACTICE within each company and filtering by category relevance and semantic similarity, pairs were evaluated by DeBERTa v3 NLI. The highest-confidence pairs were then verified by a 3-LLM judge panel.

**Result: 571 judge-confirmed contradictions** across **71 of 96 companies** (74%), from **273 unique commitment statements** spanning **418 unique segment pairs**. The judges rejected 85.9% of NLI-flagged pairs, confirming that NLI over-flags at the atomic statement level and that multi-model judge verification is essential.

### Pipeline Metrics

| Stage | Count | Notes |
|-------|-------|-------|
| Atomic statements extracted | 11,111 | 3,214 COMMITMENT + 7,897 PRACTICE |
| Judge input pairs | 4,062 | NLI-flagged, similarity filtered |
| **Judge-confirmed contradictions** | **571** | **14.1% confirmation rate** |
| Needs review (split verdict) | 2 | — |

### Judge Agreement

| Metric | Value |
|--------|-------|
| Unanimous (3/3) | 81.3% (3,304/4,062) |
| Majority (2/3) | 18.6% (756/4,062) |
| Usable consensus | 100.0% |
| Split/insufficient | 2 |
| Fleiss' kappa | 0.5334 (moderate) |

---

## Top Companies by Contradiction Count

| Rank | Company | Confirmed | Judged | Rate |
|------|---------|-----------|--------|------|
| 1 | kaleidahealth.org | 103 | 429 | 24% |
| 2 | honda.com | 44 | 355 | 12% |
| 3 | barnesandnoble.com | 33 | 317 | 10% |
| 4 | latinpost.com | 20 | 75 | 27% |
| 5 | esquire.com | 17 | 106 | 16% |
| 6 | sltrib.com | 16 | 55 | 29% |
| 7 | jibjab.com | 13 | 299 | 4% |
| 8 | dailynews.com | 13 | 54 | 24% |
| 9 | zacks.com | 13 | 43 | 30% |
| 10 | kraftrecipes.com | 13 | 27 | 48% |
| 11 | chasepaymentech.com | 12 | 63 | 19% |
| 12 | theatlantic.com | 12 | 55 | 22% |
| 13 | pbs.org | 12 | 39 | 31% |
| 14 | allstate.com | 11 | 77 | 14% |
| 15 | timeinc.com | 10 | 38 | 26% |
| 16 | walmart.com | 9 | 147 | 6% |
| 17 | sidearmsports.com | 8 | 54 | 15% |
| 18 | disinfo.com | 8 | 29 | 28% |
| 19 | style.com | 8 | 25 | 32% |
| 20 | vikings.com | 8 | 49 | 16% |

## Per-Company Highlights

### Kaleidahealth.Org — 103 Confirmed (24% rate)

**Example (sim=0.86, nli=1.00, unanimous):**
> **COMMITMENT:** Kaleida Health obtains written authorization before using health information or sharing it outside the hospital....
> **PRACTICE:** Kaleida Health uses and discloses patient health information in the Patient Directory without written authorization....

**Example (sim=0.60, nli=1.00, majority):**
> **COMMITMENT:** Kaleida Health only shares information with someone able to help prevent a serious and imminent threat....
> **PRACTICE:** Kaleida Health discloses health information to organ and tissue procurement organizations upon patient death....

### Honda.Com — 44 Confirmed (12% rate)

**Example (sim=0.61, nli=1.00, unanimous):**
> **COMMITMENT:** Signing up for Honda email notifications and providing personal information is voluntary and user-controlled....
> **PRACTICE:** Personal information collected on co-branded sites is shared with American Honda and all Co-Branded Parties without additional notice or consent....

**Example (sim=0.65, nli=1.00, majority):**
> **COMMITMENT:** Email address is optional when requesting a brochure from Honda Power Equipment....
> **PRACTICE:** American Honda requires personally identifying information such as name and address to provide Internet services like Dealer Locator and brochure requests....

### Barnesandnoble.Com — 33 Confirmed (10% rate)

**Example (sim=0.57, nli=1.00, majority):**
> **COMMITMENT:** Barnes & Noble requires third party entities to obtain customer consent before receiving purchasing information....
> **PRACTICE:** Barnes & Noble automatically collects information from colleges, universities, and business partners....

**Example (sim=0.69, nli=1.00, majority):**
> **COMMITMENT:** Barnes & Noble requires third party entities to obtain customer consent before receiving purchasing information....
> **PRACTICE:** Barnes & Noble may share personal information with other business units and operations even if they are sold....

### Latinpost.Com — 20 Confirmed (27% rate)

**Example (sim=0.74, nli=1.00, unanimous):**
> **COMMITMENT:** Latin Post will not share Personal Information with Advertisers or other third party marketers unless the user opts in to such disclosure....
> **PRACTICE:** latinpost.com discloses user information to protect Parent Companies, Affiliates, and operational service providers, licensors, suppliers, Advertisers, customers, and users....

**Example (sim=0.74, nli=1.00, unanimous):**
> **COMMITMENT:** latinpost.com does not sell, rent, lease, or disclose personal information to third parties....
> **PRACTICE:** latinpost.com discloses personal information to operational service providers for administering and maintaining site services....

### Esquire.Com — 17 Confirmed (16% rate)

**Example (sim=0.64, nli=1.00, majority):**
> **COMMITMENT:** Esquire.com requires service providers not to use personally identifiable information except for hired purposes....
> **PRACTICE:** Esquire.com uses any and all collected information about users for marketing purposes....

**Example (sim=0.82, nli=1.00, unanimous):**
> **COMMITMENT:** Esquire.com asks third-party service providers to maintain confidentiality of personally identifiable information....
> **PRACTICE:** Esquire discloses contact information to third parties to allow them to market their products or services....

---

## Category Analysis

### Category Pair Distribution

| Commitment Category → Practice Category | Count | % |
|----------------------------------------|-------|---|
| THIRD_PARTY -> THIRD_PARTY | 302 | 52.9% |
| FIRST_PARTY -> FIRST_PARTY | 110 | 19.3% |
| FIRST_PARTY -> THIRD_PARTY | 66 | 11.6% |
| SALE_SHARING -> THIRD_PARTY | 35 | 6.1% |
| THIRD_PARTY -> FIRST_PARTY | 30 | 5.3% |
| THIRD_PARTY -> SALE_SHARING | 14 | 2.5% |
| FIRST_PARTY -> TRACKING | 7 | 1.2% |
| THIRD_PARTY -> TRACKING | 2 | 0.4% |
| TRACKING -> THIRD_PARTY | 1 | 0.2% |
| SALE_SHARING -> FIRST_PARTY | 1 | 0.2% |

---

## Signal Quality

### Consensus Strength of Confirmed Contradictions

| Consensus | Count | % |
|-----------|-------|---|
| Unanimous (3/3 CONTRADICTION) | 299 | 52.4% |
| Majority (2/3 CONTRADICTION) | 272 | 47.6% |

### Similarity Distribution of Confirmed Contradictions

| Similarity Range | Count | % |
|-----------------|-------|---|
| 0.85-1.00 | 4 | 0.7% |
| 0.80-0.85 | 16 | 2.8% |
| 0.75-0.80 | 46 | 8.1% |
| 0.70-0.75 | 55 | 9.6% |
| 0.65-0.70 | 77 | 13.5% |
| 0.60-0.65 | 99 | 17.3% |
| 0.55-0.60 | 111 | 19.4% |
| 0.50-0.55 | 163 | 28.5% |

---

## Coverage Analysis

### Companies Without Contradictions

25 companies had zero confirmed contradictions:

abita.com, adweek.com, archives.gov, boardgamegeek.com, dailyillini.com, dcccd.edu, earthkam.org, everydayhealth.com, foodallergy.org, foxsports.com, freep.com, gawker.com, geocaching.com, lodgemfg.com, msn.com, newsbusters.org, post-gazette.com, sci-news.com, sciencemag.org, stlouisfed.org, ticketmaster.com, usa.gov, washingtonian.com, washingtonpost.com, yahoo.com

### Scale Analysis

| Contradictions | Companies | % |
|----------------|-----------|---|
| 0 | 25 | 26% |
| 1-4 | 30 | 31% |
| 5-9 | 26 | 27% |
| 10-19 | 11 | 11% |
| 20+ | 4 | 4% |

---

## Key Takeaways

1. **Scale validation**: 571 confirmed contradictions across 71 companies demonstrates that privacy washing is widespread, not limited to a few bad actors.

2. **Judge verification is essential**: 85.9% rejection rate means that without judges, the pipeline would report 4,062 "contradictions" — 7× the actual count.

3. **THIRD_PARTY → THIRD_PARTY dominates**: 52.9% of all contradictions involve this category pattern.

4. **Lower similarity contains more contradictions**: Cross-topic contradictions (broad commitment vs. specific practice) are the core privacy washing pattern.
