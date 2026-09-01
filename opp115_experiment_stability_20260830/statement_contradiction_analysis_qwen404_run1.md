# OPP-115 Statement-Level Contradiction Analysis: Judge-Verified Results

*Generated: 2026-08-31*
*Pipeline: extract → NLI detect → 3-LLM judge verification*

## Executive Summary

The statement-level privacy washing detection pipeline processed the OPP-115 (115 companies) corpus, decomposing segments into **6,485 atomic statements** (1,829 commitment, 4,656 practice). After pairing COMMITMENT × PRACTICE within each company and filtering by category relevance and semantic similarity, pairs were evaluated by DeBERTa v3 NLI. The highest-confidence pairs were then verified by a 3-LLM judge panel.

**Result: 64 judge-confirmed contradictions** across **28 of 97 companies** (29%), from **41 unique commitment statements** spanning **54 unique segment pairs**. The judges rejected 75.1% of NLI-flagged pairs, confirming that NLI over-flags at the atomic statement level and that multi-model judge verification is essential.

### Pipeline Metrics

| Stage | Count | Notes |
|-------|-------|-------|
| Atomic statements extracted | 6,485 | 1,829 COMMITMENT + 4,656 PRACTICE |
| Judge input pairs | 1,177 | NLI-flagged, similarity filtered |
| **Judge-confirmed contradictions** | **64** | **5.4% confirmation rate** |
| Needs review (split verdict) | 229 | — |

### Judge Agreement

| Metric | Value |
|--------|-------|
| Unanimous (3/3) | 80.5% (948/1,177) |
| Majority (2/3) | 0.0% (0/1,177) |
| Usable consensus | 80.5% |
| Split/insufficient | 229 |

---

## Top Companies by Contradiction Count

| Rank | Company | Confirmed | Judged | Rate |
|------|---------|-----------|--------|------|
| 1 | rockstargames.com | 11 | 59 | 19% |
| 2 | honda.com | 10 | 145 | 7% |
| 3 | reddit.com | 6 | 64 | 9% |
| 4 | pbs.org | 6 | 31 | 19% |
| 5 | latinpost.com | 3 | 21 | 14% |
| 6 | disinfo.com | 2 | 14 | 14% |
| 7 | kraftrecipes.com | 2 | 18 | 11% |
| 8 | archives.gov | 2 | 22 | 9% |
| 9 | military.com | 2 | 20 | 10% |
| 10 | acbj.com | 2 | 10 | 20% |
| 11 | lynda.com | 1 | 20 | 5% |
| 12 | abcnews.com | 1 | 10 | 10% |
| 13 | randomhouse.com | 1 | 34 | 3% |
| 14 | internetbrands.com | 1 | 15 | 7% |
| 15 | si.edu | 1 | 8 | 12% |
| 16 | fortune.com | 1 | 8 | 12% |
| 17 | sltrib.com | 1 | 9 | 11% |
| 18 | neworleansonline.com | 1 | 4 | 25% |
| 19 | foodallergy.org | 1 | 3 | 33% |
| 20 | buffalowildwings.com | 1 | 5 | 20% |

## Per-Company Highlights

### Rockstargames.Com — 11 Confirmed (19% rate)

**Example (sim=0.57, nli=1.00, unanimous):**
> **COMMITMENT:** The company does not collect personal information such as name and address....
> **PRACTICE:** The company collects personal information including name, email, phone, photo, mailing address, and payment information....

**Example (sim=0.47, nli=1.00, unanimous):**
> **COMMITMENT:** The company uses information from requests only to respond to questions or comments and provide customer support....
> **PRACTICE:** The company uses personal information for internal marketing and demographic studies....

### Honda.Com — 10 Confirmed (7% rate)

**Example (sim=0.35, nli=1.00, unanimous):**
> **COMMITMENT:** The company uses collected personal information only in a manner appropriate to process requests for pre-approved credit....
> **PRACTICE:** The company uses collected personal information to send email notifications about Honda models, products, offers, and events....

**Example (sim=0.35, nli=1.00, unanimous):**
> **COMMITMENT:** The company uses collected personal information only in a manner appropriate to process requests for pre-approved credit....
> **PRACTICE:** The company uses collected personal information to send email notifications about Honda models, products, offers, and events....

### Reddit.Com — 6 Confirmed (9% rate)

**Example (sim=0.32, nli=1.00, unanimous):**
> **COMMITMENT:** Reddit removes information that could identify an individual user after 90 days....
> **PRACTICE:** The company maintains a complete log of all messages sent on the service indefinitely....

**Example (sim=0.39, nli=1.00, unanimous):**
> **COMMITMENT:** Reddit does not allow other parties to collect personally identifiable information from users on its platform....
> **PRACTICE:** Reddit shares users’ IP addresses with advertising partners to understand mobile ad clicks and avoid repeatedly showing the same ad....

### Pbs.Org — 6 Confirmed (19% rate)

**Example (sim=0.34, nli=1.00, unanimous):**
> **COMMITMENT:** The company uses collected information only in the aggregate....
> **PRACTICE:** The company uses personally identifiable information for marketing and promotional purposes in support of public broadcasting....

**Example (sim=0.42, nli=1.00, unanimous):**
> **COMMITMENT:** The company uses collected information only in the aggregate....
> **PRACTICE:** The company uses personally identifiable information for activities described in previous sections....

### Latinpost.Com — 3 Confirmed (14% rate)

**Example (sim=0.32, nli=1.00, unanimous):**
> **COMMITMENT:** The company does not collect personal information as part of the tracking technology process....
> **PRACTICE:** The company saves user ID and personal information to avoid requiring re-entry on subsequent site visits....

**Example (sim=0.61, nli=1.00, unanimous):**
> **COMMITMENT:** The company does not sell, rent, lease, or disclose personal information to third parties....
> **PRACTICE:** The company discloses personal information to parent companies and affiliates for marketing purposes....

---

## Category Analysis

### Category Pair Distribution

| Commitment Category → Practice Category | Count | % |
|----------------------------------------|-------|---|
| FIRST_PARTY -> FIRST_PARTY | 38 | 59.4% |
| THIRD_PARTY -> THIRD_PARTY | 19 | 29.7% |
| FIRST_PARTY -> THIRD_PARTY | 2 | 3.1% |
| THIRD_PARTY -> FIRST_PARTY | 2 | 3.1% |
| FIRST_PARTY -> TRACKING | 1 | 1.6% |
| SALE_SHARING -> THIRD_PARTY | 1 | 1.6% |
| TRACKING -> TRACKING | 1 | 1.6% |

---

## Signal Quality

### Consensus Strength of Confirmed Contradictions

| Consensus | Count | % |
|-----------|-------|---|
| Unanimous (3/3 CONTRADICTION) | 64 | 100.0% |
| Majority (2/3 CONTRADICTION) | 0 | 0.0% |

### Similarity Distribution of Confirmed Contradictions

| Similarity Range | Count | % |
|-----------------|-------|---|
| 0.85-1.00 | 0 | 0.0% |
| 0.80-0.85 | 0 | 0.0% |
| 0.75-0.80 | 1 | 1.6% |
| 0.70-0.75 | 0 | 0.0% |
| 0.65-0.70 | 0 | 0.0% |
| 0.60-0.65 | 9 | 14.1% |
| 0.55-0.60 | 8 | 12.5% |
| 0.50-0.55 | 46 | 71.9% |

---

## Coverage Analysis

### Companies Without Contradictions

69 companies had zero confirmed contradictions:

abita.com, adweek.com, allstate.com, amazon.com, aol.com, austincc.edu, bankofamerica.com, barnesandnoble.com, boardgamegeek.com, chasepaymentech.com, citizen.org, coffeereview.com, earthkam.org, enthusiastnetwork.com, esquire.com, everydayhealth.com, fool.com, fredericknewspost.com, freep.com, gamestop.com, gawker.com, geocaching.com, highgearmedia.com, imdb.com, instagram.com, ironhorsevineyards.com, jibjab.com, kaleidahealth.org, lids.com, lodgemfg.com
... and 39 more

### Scale Analysis

| Contradictions | Companies | % |
|----------------|-----------|---|
| 0 | 69 | 71% |
| 1-4 | 24 | 25% |
| 5-9 | 2 | 2% |
| 10-19 | 2 | 2% |
| 20+ | 0 | 0% |

---

## Key Takeaways

1. **Scale validation**: 64 confirmed contradictions across 28 companies demonstrates that privacy washing is widespread, not limited to a few bad actors.

2. **Judge verification is essential**: 75.1% rejection rate means that without judges, the pipeline would report 1,177 "contradictions" — 18× the actual count.

3. **FIRST_PARTY → FIRST_PARTY dominates**: 59.4% of all contradictions involve this category pattern.

4. **Lower similarity contains more contradictions**: Cross-topic contradictions (broad commitment vs. specific practice) are the core privacy washing pattern.
