# Privacy Washing Detection Report

---

*Generated: 2026-01-26 21:27 UTC*

---

*Pipeline: linguistic_features → detect_contradictions → privacy_washing_index → contradiction_report*

---

## 1. Executive Summary

We analyzed **43 companies** with claim-practice pair detection,
evaluating **820 segment pairs** for rhetorical contradictions using
an NLI-primary approach. The NLI model (DeBERTa v3) is the sole gate for
contradiction detection; tone gap serves as a severity modifier (up to +30%)
but does not independently flag contradictions.

The NLI model flagged **52 contradictions** (6.3%
of pairs) across **20 companies**.

**Evidence type distribution:**
- NLI + tone gap: 35
- NLI only: 17

**Top 5 privacy washers:** Sciencemag.Org (1.000), Sheknows.Com (0.631), Latinpost.Com (0.621), Taylorswift.Com (0.613), Meredith.Com (0.587)

**Enforcement validation (exploratory):**
No enforcement-actioned companies overlap with this corpus (0 of 43 scored).
Enforcement validation is not applicable for this dataset.

---

## 2. Top 20 Privacy Washers

| Rank | Company | PWI | Density | Severity | Pairs | Contradictions | Enforced |
|------|---------|-----|---------|----------|-------|----------------|----------|
| 1 | Sciencemag.Org | 1.0000 | 1.000 | 0.972 | 1 | 1 |  |
| 2 | Sheknows.Com | 0.6311 | 0.250 | 0.995 | 4 | 1 |  |
| 3 | Latinpost.Com | 0.6210 | 0.263 | 0.962 | 57 | 15 |  |
| 4 | Taylorswift.Com | 0.6131 | 0.250 | 0.959 | 12 | 3 |  |
| 5 | Meredith.Com | 0.5873 | 0.167 | 0.992 | 24 | 4 |  |
| 6 | Theatlantic.Com | 0.5731 | 0.118 | 1.013 | 17 | 2 |  |
| 7 | Adweek.Com | 0.5681 | 0.100 | 1.020 | 10 | 1 |  |
| 8 | Ocregister.Com | 0.5629 | 0.083 | 1.027 | 12 | 1 |  |
| 9 | Voxmedia.Com | 0.5495 | 0.067 | 1.017 | 30 | 2 |  |
| 10 | Barnesandnoble.Com | 0.5494 | 0.024 | 1.059 | 41 | 1 |  |
| 11 | Abcnews.Com | 0.5421 | 0.062 | 1.007 | 16 | 1 |  |
| 12 | Nytimes.Com | 0.5365 | 0.075 | 0.983 | 53 | 4 |  |
| 13 | Allstate.Com | 0.5361 | 0.056 | 1.002 | 18 | 1 |  |
| 14 | Pbs.Org | 0.5236 | 0.053 | 0.980 | 19 | 1 |  |
| 15 | Lynda.Com | 0.4971 | 0.082 | 0.898 | 73 | 6 |  |
| 16 | Reddit.Com | 0.4819 | 0.033 | 0.917 | 60 | 2 |  |
| 17 | Kraftrecipes.Com | 0.4815 | 0.030 | 0.919 | 33 | 1 |  |
| 18 | Sidearmsports.Com | 0.4134 | 0.056 | 0.760 | 54 | 3 |  |
| 19 | Lids.Com | 0.3853 | 0.100 | 0.660 | 10 | 1 |  |
| 20 | Mlb.Mlb.Com | 0.3586 | 0.048 | 0.660 | 21 | 1 |  |

### Top 5 — Evidence Excerpts

**1. Sciencemag.Org** (PWI=1.0000)
- Contradiction 1 [nli_plus_tone] (severity=0.972):
  - *Claim (sciencemag.org_030):* "SECURITY We implement reasonable technical and organizational measures designed to secure your personal information from accidental loss and from unau"
  - *Practice (sciencemag.org_031):* "The SSL encrypts, or translates, your order information into a highly indecipherable code, which is processed immediately. When you've finished your t"

**2. Sheknows.Com** (PWI=0.6311)
- Contradiction 1 [nli] (severity=0.995):
  - *Claim (sheknows.com_032):* "To protect your privacy and security, we take reasonable steps (such as requesting a unique password) to verify your identity before granting you acce"
  - *Practice (sheknows.com_033):* "Compromise of Personal Information In the event that personal information is compromised as a result of a breach of security, Company will take commer"

**3. Latinpost.Com** (PWI=0.6210)
- Contradiction 1 [nli] (severity=0.998):
  - *Claim (latinpost.com_057):* "d. Use of Information. Latin Post will not use a wireless telephone number, wireless or conventional Internet email address, or other Information subm"
  - *Practice (latinpost.com_078):* "Phishing. Phishing attacks attempt to steal consumers' personal identity data and financial account credentials. "Phishers" use 'spoofed' e-mails to l"
- Contradiction 2 [nli_plus_tone] (severity=0.996):
  - *Claim (latinpost.com_057):* "d. Use of Information. Latin Post will not use a wireless telephone number, wireless or conventional Internet email address, or other Information subm"
  - *Practice (latinpost.com_018):* "Sending marketing and promotional e-mails or, subject to the "Wireless Marketing Services and Associated Promotional Opportunities" Section below, tex"

**4. Taylorswift.Com** (PWI=0.6131)
- Contradiction 1 [nli_plus_tone] (severity=1.025):
  - *Claim (taylorswift.com_023):* "We will not share your information with third parties for the purposes of their direct marketing unless you affirmatively agree to such disclosure."
  - *Practice (taylorswift.com_017):* "We may disclose your personally-identifiable information with our employees, agents, contractors and sub-contractors, and our related and affiliated e"
- Contradiction 2 [nli] (severity=0.955):
  - *Claim (taylorswift.com_023):* "We will not share your information with third parties for the purposes of their direct marketing unless you affirmatively agree to such disclosure."
  - *Practice (taylorswift.com_018):* "We will share your personally-identifiable information with other parties under the following circumstances:"

**5. Meredith.Com** (PWI=0.5873)
- Contradiction 1 [nli_plus_tone] (severity=1.099):
  - *Claim (meredith.com_054):* "If you use our Services to sign up for special email offers from third-party advertisers, we will also share your email address and any other informat"
  - *Practice (meredith.com_046):* "Control the display of advertising and develop and deliver advertising tailored to your interests, including advertising that you see on our Services,"
- Contradiction 2 [nli_plus_tone] (severity=1.028):
  - *Claim (meredith.com_054):* "If you use our Services to sign up for special email offers from third-party advertisers, we will also share your email address and any other informat"
  - *Practice (meredith.com_053):* "Email. We share our users' email addresses with service providers that send email messages and deliver targeted advertising in our emails on our behal"

---

## 3. Most Common Contradiction Patterns

### Claim Segment Categories (sources of reassurance language)
| Category | Count | % of Contradictions |
|----------|-------|---------------------|
| THIRD_PARTY | 45 | 86.5% |
| FIRST_PARTY | 4 | 7.7% |
| SECURITY | 2 | 3.8% |
| OTHER | 1 | 1.9% |

### Practice Segment Categories (targets of contradiction)
| Category | Count | % of Contradictions |
|----------|-------|---------------------|
| FIRST_PARTY | 24 | 46.2% |
| THIRD_PARTY | 23 | 44.2% |
| SECURITY | 5 | 9.6% |

### Top 10 Claim → Practice Category Pairs
| Claim Category | Practice Category | Count |
|----------------|-------------------|-------|
| THIRD_PARTY | THIRD_PARTY | 22 |
| THIRD_PARTY | FIRST_PARTY | 20 |
| FIRST_PARTY | FIRST_PARTY | 4 |
| THIRD_PARTY | SECURITY | 3 |
| SECURITY | SECURITY | 2 |
| OTHER | THIRD_PARTY | 1 |

---

## 4. Per-Category Analysis

Which OPPT practice categories exhibit the largest rhetorical contradictions?

| Category | N Pairs | Severity | Tone Gap | NLI Rate | Hedging | Specificity | Vagueness |
|----------|---------|----------|----------|----------|---------|-------------|-----------|
| THIRD_PARTY | 297 | 0.0728 | 12.52 | 0.077 | 0.542 | 0.0402 | 0.0334 |
| FIRST_PARTY | 392 | 0.0575 | 8.85 | 0.061 | 0.463 | 0.0453 | 0.0246 |
| SECURITY | 112 | 0.0436 | 6.68 | 0.045 | 0.160 | 0.0527 | 0.0102 |
| RETENTION | 18 | 0.0000 | 8.60 | 0.000 | 0.344 | 0.0444 | 0.0170 |
| TRACKING | 1 | 0.0000 | 3.56 | 0.000 | 0.500 | 0.0702 | 0.0175 |

**Key findings:**
- **THIRD_PARTY** has the highest NLI contradiction rate (7.7%), suggesting the starkest gap between reassuring language and practice disclosures in this category.
- **THIRD_PARTY** has the highest mean tone gap (12.52), driven by hedging (0.542) and low specificity (0.0402).
- **THIRD_PARTY** has the highest hedging score (0.542) with vagueness (0.0334) — language in this category is most evasive.

---

## 5. Case Studies

### Sciencemag.Org (Rank #1, PWI=1.0000)
- **Total segments:** 36
- **Reassurance segments:** 2
- **Claim-practice pairs:** 1
- **Contradictions (NLI-flagged):** 1
- **Categories:** OTHER: 10, USER_CHOICE: 8, FIRST_PARTY: 7, THIRD_PARTY: 6, SECURITY: 2

**Top contradictions:**

1. **[nli_plus_tone]** severity=0.972, NLI=0.966
   - *Claim (sciencemag.org_030, SECURITY):* "SECURITY We implement reasonable technical and organizational measures designed to secure your personal information from accidental loss and from unauthorized access, use, alteration, or disclosure...."
   - *Practice (sciencemag.org_031, SECURITY):* "The SSL encrypts, or translates, your order information into a highly indecipherable code, which is processed immediately. When you've finished your transactions and begin the checkout process, you..."


### Sheknows.Com (Rank #2, PWI=0.6311)
- **Total segments:** 46
- **Reassurance segments:** 2
- **Claim-practice pairs:** 4
- **Contradictions (NLI-flagged):** 1
- **Categories:** THIRD_PARTY: 14, FIRST_PARTY: 13, OTHER: 9, USER_CHOICE: 4, SECURITY: 3

**Top contradictions:**

1. **[nli]** severity=0.995, NLI=0.995
   - *Claim (sheknows.com_032, SECURITY):* "To protect your privacy and security, we take reasonable steps (such as requesting a unique password) to verify your identity before granting you access to your account. You are responsible for..."
   - *Practice (sheknows.com_033, SECURITY):* "Compromise of Personal Information In the event that personal information is compromised as a result of a breach of security, Company will take commercially reasonable measures to promptly notify..."


### Latinpost.Com (Rank #3, PWI=0.6210)
- **Total segments:** 89
- **Reassurance segments:** 2
- **Claim-practice pairs:** 57
- **Contradictions (NLI-flagged):** 15
- **Categories:** FIRST_PARTY: 23, USER_CHOICE: 20, THIRD_PARTY: 19, OTHER: 12, INTL_SPECIFIC: 7

**Top contradictions:**

1. **[nli]** severity=0.998, NLI=0.998
   - *Claim (latinpost.com_057, THIRD_PARTY):* "d. Use of Information. Latin Post will not use a wireless telephone number, wireless or conventional Internet email address, or other Information submitted for its wireless marketing services for any..."
   - *Practice (latinpost.com_078, SECURITY):* "Phishing. Phishing attacks attempt to steal consumers' personal identity data and financial account credentials. "Phishers" use 'spoofed' e-mails to lead consumers to counterfeit websites designed to..."

2. **[nli_plus_tone]** severity=0.996, NLI=0.975
   - *Claim (latinpost.com_057, THIRD_PARTY):* "d. Use of Information. Latin Post will not use a wireless telephone number, wireless or conventional Internet email address, or other Information submitted for its wireless marketing services for any..."
   - *Practice (latinpost.com_018, FIRST_PARTY):* "Sending marketing and promotional e-mails or, subject to the "Wireless Marketing Services and Associated Promotional Opportunities" Section below, text messages offering the purchase of goods and/or..."

3. **[nli]** severity=0.993, NLI=0.993
   - *Claim (latinpost.com_057, THIRD_PARTY):* "d. Use of Information. Latin Post will not use a wireless telephone number, wireless or conventional Internet email address, or other Information submitted for its wireless marketing services for any..."
   - *Practice (latinpost.com_029, FIRST_PARTY):* "ii. Other Information Collected by Us. We, and/or our Parent Companies and Affiliates, use the Other Information we collect from you in a variety of ways, including: Keeping count of your return..."


---

## 6. Enforcement Validation Statistics

**Sample:** 0 enforcement-actioned companies, 43 non-enforced (total: 43)
**Missing from analysis:** adobe, amazon, att, avast, babel-street, betterhelp, bumble, cerebral, clearview-ai, draftkings, epic-games, fanduel, google, gravy-analytics, grindr, kochava, lexisnexis, linkedin, meta, monument, ngl, premom, roblox, safegraph, t-mobile, tiktok, tinder, uber, verizon, vonage, x-mode-social (no reassurance-practice pairs generated)

No enforcement-actioned companies overlap with this corpus. Enforcement validation is not applicable.

---

## 7. Methodology Notes

### Pipeline Overview

1. **Linguistic features** (Script 1): Per-segment hedging, reassurance, specificity, commitment
   strength, and readability scores extracted from 3,792 annotated segments.

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

- **Statistical power**: With 43 companies (0 enforced) in the enforcement
  analysis, statistical power is modest. All results should be treated as
  exploratory and hypothesis-generating.

- **Python 3.14 compatibility**: spaCy NER was replaced with regex-based entity
  detection due to a Pydantic v1 incompatibility. This affects the specificity
  score's entity detection component (ORG, DATE, MONEY) but does not fundamentally
  change the metric.
