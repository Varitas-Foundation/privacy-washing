# OPP-115 Statement-Level Contradiction Analysis: Judge-Verified Results

*Generated: 2026-08-31*
*Pipeline: extract → NLI detect → 3-LLM judge verification*

## Executive Summary

The statement-level privacy washing detection pipeline processed the OPP-115 (115 companies) corpus, decomposing segments into **6,485 atomic statements** (1,829 commitment, 4,656 practice). After pairing COMMITMENT × PRACTICE within each company and filtering by category relevance and semantic similarity, pairs were evaluated by DeBERTa v3 NLI. The highest-confidence pairs were then verified by a 3-LLM judge panel.

**Result: 155 judge-confirmed contradictions** across **49 of 97 companies** (51%), from **98 unique commitment statements** spanning **139 unique segment pairs**. The judges rejected 86.6% of NLI-flagged pairs, confirming that NLI over-flags at the atomic statement level and that multi-model judge verification is essential.

### Pipeline Metrics

| Stage | Count | Notes |
|-------|-------|-------|
| Atomic statements extracted | 6,485 | 1,829 COMMITMENT + 4,656 PRACTICE |
| Judge input pairs | 1,177 | NLI-flagged, similarity filtered |
| **Judge-confirmed contradictions** | **155** | **13.2% confirmation rate** |
| Needs review (split verdict) | 3 | — |

### Judge Agreement

| Metric | Value |
|--------|-------|
| Unanimous (3/3) | 86.4% (1,017/1,177) |
| Majority (2/3) | 13.3% (157/1,177) |
| Usable consensus | 99.7% |
| Split/insufficient | 3 |
| Fleiss' kappa | 0.6382 (moderate) |

---

## Top Companies by Contradiction Count

| Rank | Company | Confirmed | Judged | Rate |
|------|---------|-----------|--------|------|
| 1 | honda.com | 24 | 145 | 17% |
| 2 | rockstargames.com | 15 | 59 | 25% |
| 3 | reddit.com | 10 | 64 | 16% |
| 4 | barnesandnoble.com | 7 | 51 | 14% |
| 5 | pbs.org | 7 | 31 | 23% |
| 6 | latinpost.com | 7 | 21 | 33% |
| 7 | esquire.com | 6 | 30 | 20% |
| 8 | fool.com | 6 | 33 | 18% |
| 9 | archives.gov | 5 | 22 | 23% |
| 10 | randomhouse.com | 4 | 34 | 12% |
| 11 | imdb.com | 4 | 20 | 20% |
| 12 | sidearmsports.com | 4 | 13 | 31% |
| 13 | disinfo.com | 3 | 14 | 21% |
| 14 | usa.gov | 3 | 10 | 30% |
| 15 | kraftrecipes.com | 3 | 18 | 17% |
| 16 | sheknows.com | 3 | 23 | 13% |
| 17 | dailynews.com | 3 | 19 | 16% |
| 18 | redorbit.com | 3 | 5 | 60% |
| 19 | jibjab.com | 2 | 21 | 10% |
| 20 | style.com | 2 | 9 | 22% |

## Per-Company Highlights

### Honda.Com — 24 Confirmed (17% rate)

**Example (sim=0.35, nli=1.00, unanimous):**
> **COMMITMENT:** The company uses collected personal information only in a manner appropriate to process requests for pre-approved credit....
> **PRACTICE:** The company uses collected personal information to send email notifications about Honda models, products, offers, and events....

**Example (sim=0.63, nli=1.00, majority):**
> **COMMITMENT:** The company does not store email addresses of friends or family members when users share configurations....
> **PRACTICE:** The company collects user name, email address, and friend's email address for email-to-a-friend functionality....

### Rockstargames.Com — 15 Confirmed (25% rate)

**Example (sim=0.57, nli=1.00, unanimous):**
> **COMMITMENT:** The company does not collect personal information such as name and address....
> **PRACTICE:** The company collects personal information including name, email, phone, photo, mailing address, and payment information....

**Example (sim=0.74, nli=1.00, unanimous):**
> **COMMITMENT:** The company's cookies do not include people's names, email addresses, or other personal information....
> **PRACTICE:** The company's cookies are linked to personal information....

### Reddit.Com — 10 Confirmed (16% rate)

**Example (sim=0.45, nli=1.00, unanimous):**
> **COMMITMENT:** Reddit allows user participation to remain as anonymous as the user chooses....
> **PRACTICE:** Reddit logs and retains indefinitely the IP address from which an account is initially created....

**Example (sim=0.40, nli=1.00, unanimous):**
> **COMMITMENT:** Reddit removes personally identifiable data from activity information after 90 days....
> **PRACTICE:** The company maintains a complete log of all messages sent on the service indefinitely....

### Barnesandnoble.Com — 7 Confirmed (14% rate)

**Example (sim=0.31, nli=1.00, majority):**
> **COMMITMENT:** The company requires third parties to obtain user consent before receiving customer information....
> **PRACTICE:** Barnes & Noble and third-party application providers automatically collect real-time geographic location information about users and their devices....

**Example (sim=0.47, nli=1.00, unanimous):**
> **COMMITMENT:** The company does not allow third party service providers to collect credit card information, email addresses, or passwords....
> **PRACTICE:** The company forwards user name, email address, IP address, and shipping or billing address to content providers in connection with orders....

### Pbs.Org — 7 Confirmed (23% rate)

**Example (sim=0.34, nli=1.00, unanimous):**
> **COMMITMENT:** The company uses collected information only in the aggregate....
> **PRACTICE:** The company uses personally identifiable information for marketing and promotional purposes in support of public broadcasting....

**Example (sim=0.42, nli=1.00, unanimous):**
> **COMMITMENT:** The company uses collected information only in the aggregate....
> **PRACTICE:** The company uses personally identifiable information for activities described in previous sections....

---

## Category Analysis

### Category Pair Distribution

| Commitment Category → Practice Category | Count | % |
|----------------------------------------|-------|---|
| FIRST_PARTY -> FIRST_PARTY | 84 | 54.2% |
| THIRD_PARTY -> THIRD_PARTY | 52 | 33.5% |
| FIRST_PARTY -> THIRD_PARTY | 5 | 3.2% |
| SALE_SHARING -> THIRD_PARTY | 4 | 2.6% |
| THIRD_PARTY -> FIRST_PARTY | 3 | 1.9% |
| FIRST_PARTY -> TRACKING | 2 | 1.3% |
| SALE_SHARING -> FIRST_PARTY | 2 | 1.3% |
| TRACKING -> TRACKING | 2 | 1.3% |
| THIRD_PARTY -> SALE_SHARING | 1 | 0.6% |

---

## Signal Quality

### Consensus Strength of Confirmed Contradictions

| Consensus | Count | % |
|-----------|-------|---|
| Unanimous (3/3 CONTRADICTION) | 101 | 65.2% |
| Majority (2/3 CONTRADICTION) | 54 | 34.8% |

### Similarity Distribution of Confirmed Contradictions

| Similarity Range | Count | % |
|-----------------|-------|---|
| 0.85-1.00 | 0 | 0.0% |
| 0.80-0.85 | 0 | 0.0% |
| 0.75-0.80 | 1 | 0.6% |
| 0.70-0.75 | 4 | 2.6% |
| 0.65-0.70 | 2 | 1.3% |
| 0.60-0.65 | 17 | 11.0% |
| 0.55-0.60 | 17 | 11.0% |
| 0.50-0.55 | 17 | 11.0% |
| <0.50 | 97 | 62.6% |

---

## Coverage Analysis

### Companies Without Contradictions

48 companies had zero confirmed contradictions:

abita.com, allstate.com, amazon.com, aol.com, austincc.edu, bankofamerica.com, boardgamegeek.com, chasepaymentech.com, citizen.org, coffeereview.com, earthkam.org, enthusiastnetwork.com, everydayhealth.com, fredericknewspost.com, freep.com, gamestop.com, gawker.com, geocaching.com, highgearmedia.com, instagram.com, ironhorsevineyards.com, lids.com, lodgemfg.com, minecraft.gamepedia.com, mohegansun.com, msn.com, nbcuniversal.com, newsbusters.org, ocregister.com, playstation.com
... and 18 more

### Scale Analysis

| Contradictions | Companies | % |
|----------------|-----------|---|
| 0 | 48 | 49% |
| 1-4 | 40 | 41% |
| 5-9 | 6 | 6% |
| 10-19 | 2 | 2% |
| 20+ | 1 | 1% |

---

## Key Takeaways

1. **Scale**: 155 panel-confirmed contradictions across 49 companies. Panel confirmation is LLM majority agreement, not human validation; precision against expert judgment is unknown (see the paper's Limitations section).

2. **Judge filtering**: 86.6% of judged pairs were rejected; without the judge stage the pipeline would flag 1,177 candidate pairs, 7x the panel-confirmed count.

3. **Modal category pattern**: FIRST_PARTY -> FIRST_PARTY accounts for 54.2% of panel-confirmed contradictions. Category composition largely reflects the composition of judged pairs and is panel-sensitive (see the paper's category base-rate analysis and stability section).

4. **Similarity distribution**: the concentration of confirmations at lower similarity mirrors the composition of judged pairs; per-bin confirmation rates, not raw counts, are the informative quantity (see the paper).
