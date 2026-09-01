# OPP-115 Statement-Level Contradiction Analysis: Judge-Verified Results

*Generated: 2026-02-03*
*Pipeline: extract → NLI detect → 3-LLM judge verification*

## Executive Summary

The statement-level privacy washing detection pipeline processed the OPP-115 (115 companies) corpus, decomposing segments into **4,975 atomic statements** (1,678 commitment, 3,297 practice). After pairing COMMITMENT × PRACTICE within each company and filtering by category relevance and semantic similarity, pairs were evaluated by DeBERTa v3 NLI. The highest-confidence pairs were then verified by a 3-LLM judge panel.

**Result: 99 judge-confirmed contradictions** across **46 of 82 companies** (56%), from **77 unique commitment statements** spanning **96 unique segment pairs**. The judges rejected 84.9% of NLI-flagged pairs, confirming that NLI over-flags at the atomic statement level and that multi-model judge verification is essential.

### Pipeline Metrics

| Stage | Count | Notes |
|-------|-------|-------|
| Atomic statements extracted | 4,975 | 1,678 COMMITMENT + 3,297 PRACTICE |
| Judge input pairs | 663 | NLI-flagged, similarity filtered |
| **Judge-confirmed contradictions** | **99** | **14.9% confirmation rate** |
| Needs review (split verdict) | 1 | — |

### Judge Agreement

| Metric | Value |
|--------|-------|
| Unanimous (3/3) | 81.4% (540/663) |
| Majority (2/3) | 18.4% (122/663) |
| Usable consensus | 99.8% |
| Split/insufficient | 1 |
| Fleiss' kappa | 0.5660 (moderate) |

---

## Top Companies by Contradiction Count

| Rank | Company | Confirmed | Judged | Rate |
|------|---------|-----------|--------|------|
| 1 | kaleidahealth.org | 9 | 61 | 15% |
| 2 | acbj.com | 5 | 12 | 42% |
| 3 | honda.com | 4 | 83 | 5% |
| 4 | abcnews.com | 4 | 8 | 50% |
| 5 | rockstargames.com | 4 | 11 | 36% |
| 6 | imdb.com | 4 | 15 | 27% |
| 7 | allstate.com | 4 | 11 | 36% |
| 8 | zacks.com | 4 | 8 | 50% |
| 9 | jibjab.com | 3 | 19 | 16% |
| 10 | lynda.com | 3 | 18 | 17% |
| 11 | usa.gov | 3 | 4 | 75% |
| 12 | reddit.com | 3 | 23 | 13% |
| 13 | style.com | 3 | 8 | 38% |
| 14 | timeinc.com | 3 | 10 | 30% |
| 15 | barnesandnoble.com | 2 | 21 | 10% |
| 16 | esquire.com | 2 | 13 | 15% |
| 17 | meredith.com | 2 | 9 | 22% |
| 18 | pbs.org | 2 | 15 | 13% |
| 19 | sciencemag.org | 2 | 3 | 67% |
| 20 | nbcuniversal.com | 2 | 8 | 25% |

## Per-Company Highlights

### Kaleidahealth.Org — 9 Confirmed (15% rate)

**Example (sim=0.86, nli=1.00, unanimous):**
> **COMMITMENT:** Kaleida Health obtains written authorization before using or sharing health information with external parties....
> **PRACTICE:** Kaleida Health uses and discloses patient health information in the Patient Directory without written authorization....

**Example (sim=0.77, nli=1.00, unanimous):**
> **COMMITMENT:** Kaleida Health obtains written authorization before using or sharing health information with external parties....
> **PRACTICE:** Kaleida Health may use and disclose health information when unable to obtain written consent due to substantial communication barriers....

### Acbj.Com — 5 Confirmed (42% rate)

**Example (sim=0.65, nli=1.00, majority):**
> **COMMITMENT:** The company collects personally identifiable information with user specific knowledge and consent....
> **PRACTICE:** The company merges or co-mingles anonymous and non-personally identifiable data with registration information....

**Example (sim=0.56, nli=1.00, unanimous):**
> **COMMITMENT:** The company collects personally identifiable information with user specific knowledge and consent....
> **PRACTICE:** The company automatically collects geographic location information of users and their devices....

### Honda.Com — 4 Confirmed (5% rate)

**Example (sim=0.59, nli=1.00, unanimous):**
> **COMMITMENT:** Users can visit Honda web sites without providing personally identifiable information....
> **PRACTICE:** The company collects a user's name and address exactly as on the Honda Red Rider mailing label if the user does not know their HRCA member number....

**Example (sim=0.59, nli=1.00, unanimous):**
> **COMMITMENT:** Users can visit Honda's websites without sharing personally identifiable information....
> **PRACTICE:** The company collects a user's name and address exactly as on the Honda Red Rider mailing label if the user does not know their HRCA member number....

### Abcnews.Com — 4 Confirmed (50% rate)

**Example (sim=0.54, nli=1.00, majority):**
> **COMMITMENT:** The company limits collection of personal information from children to only what is reasonably necessary for online activity participation....
> **PRACTICE:** Personal information provided in public forums may be publicly posted without limitation on use....

**Example (sim=0.51, nli=1.00, majority):**
> **COMMITMENT:** Users may request access to personal information held by the company and request amendment or deletion....
> **PRACTICE:** Personal information provided in public forums may be publicly posted without limitation on use....

### Rockstargames.Com — 4 Confirmed (36% rate)

**Example (sim=0.58, nli=1.00, unanimous):**
> **COMMITMENT:** This Privacy Policy applies only to information submitted and collected online through the Online Services....
> **PRACTICE:** The company uses gameplay information as set forth in the privacy policy regardless of service registration or online login status....

**Example (sim=0.68, nli=1.00, unanimous):**
> **COMMITMENT:** The company's cookies do not include people's names, email addresses, or other personal information....
> **PRACTICE:** The company links its cookies to personal information collected from users....

---

## Category Analysis

### Category Pair Distribution

| Commitment Category → Practice Category | Count | % |
|----------------------------------------|-------|---|
| THIRD_PARTY -> THIRD_PARTY | 34 | 34.3% |
| FIRST_PARTY -> FIRST_PARTY | 31 | 31.3% |
| FIRST_PARTY -> THIRD_PARTY | 14 | 14.1% |
| SALE_SHARING -> THIRD_PARTY | 9 | 9.1% |
| THIRD_PARTY -> FIRST_PARTY | 4 | 4.0% |
| FIRST_PARTY -> TRACKING | 3 | 3.0% |
| THIRD_PARTY -> TRACKING | 2 | 2.0% |
| SALE_SHARING -> FIRST_PARTY | 1 | 1.0% |
| THIRD_PARTY -> SALE_SHARING | 1 | 1.0% |

---

## Signal Quality

### Consensus Strength of Confirmed Contradictions

| Consensus | Count | % |
|-----------|-------|---|
| Unanimous (3/3 CONTRADICTION) | 61 | 61.6% |
| Majority (2/3 CONTRADICTION) | 38 | 38.4% |

### Similarity Distribution of Confirmed Contradictions

| Similarity Range | Count | % |
|-----------------|-------|---|
| 0.85-1.00 | 2 | 2.0% |
| 0.80-0.85 | 0 | 0.0% |
| 0.75-0.80 | 4 | 4.0% |
| 0.70-0.75 | 2 | 2.0% |
| 0.65-0.70 | 12 | 12.1% |
| 0.60-0.65 | 17 | 17.2% |
| 0.55-0.60 | 26 | 26.3% |
| 0.50-0.55 | 36 | 36.4% |

---

## Coverage Analysis

### Companies Without Contradictions

36 companies had zero confirmed contradictions:

adweek.com, amazon.com, aol.com, archives.gov, austincc.edu, cbsinteractive.com, dailynews.com, disinfo.com, enthusiastnetwork.com, everydayhealth.com, fredericknewspost.com, freep.com, gamestop.com, gawker.com, geocaching.com, highgearmedia.com, ironhorsevineyards.com, kraftrecipes.com, lids.com, miaminewtimes.com, minecraft.gamepedia.com, mlb.mlb.com, newsbusters.org, playstation.com, post-gazette.com, randomhouse.com, redorbit.com, reference.com, sci-news.com, steampowered.com
... and 6 more

### Scale Analysis

| Contradictions | Companies | % |
|----------------|-----------|---|
| 0 | 36 | 44% |
| 1-4 | 44 | 54% |
| 5-9 | 2 | 2% |
| 10-19 | 0 | 0% |
| 20+ | 0 | 0% |

---

## Key Takeaways

1. **Scale validation**: 99 confirmed contradictions across 46 companies demonstrates that privacy washing is widespread, not limited to a few bad actors.

2. **Judge verification is essential**: 84.9% rejection rate means that without judges, the pipeline would report 663 "contradictions" — 6× the actual count.

3. **THIRD_PARTY → THIRD_PARTY dominates**: 34.3% of all contradictions involve this category pattern.

4. **Lower similarity contains more contradictions**: Cross-topic contradictions (broad commitment vs. specific practice) are the core privacy washing pattern.
