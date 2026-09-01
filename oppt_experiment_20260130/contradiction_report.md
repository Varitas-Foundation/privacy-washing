# Privacy Washing Detection Report

---

*Generated: 2026-01-31 05:32 UTC*

---

*Pipeline: linguistic_features → detect_contradictions → privacy_washing_index → contradiction_report*

---

## 1. Executive Summary

We analyzed **17 companies** with claim-practice pair detection,
evaluating **318 segment pairs** for rhetorical contradictions using
an NLI-primary approach. The NLI model (DeBERTa v3) is the sole gate for
contradiction detection; tone gap serves as a severity modifier (up to +30%)
but does not independently flag contradictions.

The NLI model flagged **19 contradictions** (6.0%
of pairs) across **6 companies**.

**Evidence type distribution:**
- NLI + tone gap: 10
- NLI only: 9

**Top 5 privacy washers:** Microsoft (1.000), Tesla (0.736), Linkedin (0.561), Venmo (0.508), Jasper (0.500)

**Enforcement validation (exploratory):**
Enforced companies (n=3) showed mean PWI=0.1869
vs. non-enforced (n=14) mean PWI=0.2175.
The difference is **not statistically significant** (Mann-Whitney U p=1.0000,
Cohen's d=-0.0912 [-0.9923, 1.3277],
ROC-AUC=0.5000 [0.2308, 0.9333]).
This null result indicates that privacy washing as measured by our index does not
predict regulatory enforcement actions in this corpus, consistent with the
exploratory nature of this analysis.

---

## 2. Top 20 Privacy Washers

| Rank | Company | PWI | Density | Severity | Pairs | Contradictions | Enforced |
|------|---------|-----|---------|----------|-------|----------------|----------|
| 1 | Microsoft | 1.0000 | 1.000 | 0.999 | 1 | 1 |  |
| 2 | Tesla | 0.7360 | 0.524 | 0.947 | 21 | 11 |  |
| 3 | Linkedin | 0.5606 | 0.077 | 1.044 | 13 | 1 | Yes |
| 4 | Venmo | 0.5082 | 0.105 | 0.910 | 38 | 4 |  |
| 5 | Jasper | 0.5004 | 0.059 | 0.941 | 17 | 1 |  |
| 6 | Motorola Solutions | 0.2999 | 0.038 | 0.561 | 26 | 1 |  |
| 7 | Anduril | 0.0000 | 0.000 | 0.000 | 1 | 0 |  |
| 8 | Bumble | 0.0000 | 0.000 | 0.000 | 19 | 0 | Yes |
| 9 | Github | 0.0000 | 0.000 | 0.000 | 6 | 0 |  |
| 10 | Hilton | 0.0000 | 0.000 | 0.000 | 12 | 0 |  |
| 11 | Khan Academy | 0.0000 | 0.000 | 0.000 | 4 | 0 |  |
| 12 | Meta | 0.0000 | 0.000 | 0.000 | 99 | 0 | Yes |
| 13 | Northrop Grumman | 0.0000 | 0.000 | 0.000 | 5 | 0 |  |
| 14 | Pimeyes | 0.0000 | 0.000 | 0.000 | 10 | 0 |  |
| 15 | United Airlines | 0.0000 | 0.000 | 0.000 | 19 | 0 |  |
| 16 | Xiaomi | 0.0000 | 0.000 | 0.000 | 17 | 0 |  |
| 17 | Zillow | 0.0000 | 0.000 | 0.000 | 10 | 0 |  |

### Top 5 — Evidence Excerpts

**1. Microsoft** (PWI=1.0000)
- Contradiction 1 [nli_plus_tone] (severity=0.999):
  - *Claim (microsoft_014):* "Microsoft is committed to protecting the security of your personal data. We use a variety of security technologies and procedures to help protect your"
  - *Practice (microsoft_053):* ". Device encryption helps protect the data stored on your device by encrypting it using BitLocker Drive Encryption technology. When device encryption"

**2. Tesla** (PWI=0.7360)
- Contradiction 1 [nli_plus_tone] (severity=1.110):
  - *Claim (tesla_020):* "We may share information with:  - Our service providers, business partners and affiliates - Third parties you authorize - Other third parties as requi"
  - *Practice (tesla_022):* "| Categories of Recipients | Description | Reason for Sharing | |---|---|---| | Financial institutions | Companies that process credit applications fo"
- Contradiction 2 [nli_plus_tone] (severity=1.011):
  - *Claim (tesla_020):* "We may share information with:  - Our service providers, business partners and affiliates - Third parties you authorize - Other third parties as requi"
  - *Practice (tesla_019):* "Except as described here, Tesla may also collect, use, and share information that does not, on its own, personally identify you. Such information may"

**3. Linkedin** (PWI=0.5606)
- Contradiction 1 [nli_plus_tone] (severity=1.044):
  - *Claim (linkedin_034):* "We seek to create economic opportunity for Members of the global workforce and to help them be more productive and successful. We use the personal dat"
  - *Practice (linkedin_009):* "We collect personal data from you when you provide, post or upload it to our Services, such as when you fill out a form, (e.g., with demographic data"

**4. Venmo** (PWI=0.5082)
- Contradiction 1 [nli] (severity=0.989):
  - *Claim (venmo_037):* "2. The categories of third parties to which we (a) disclose such personal information for a business purpose, (b) "share" personal information for "cr"
  - *Practice (venmo_005):* "Your name, street address, email address, date of birth, and Social Security number ("SSN") (or other governmental issued verification numbers)."
- Contradiction 2 [nli] (severity=0.989):
  - *Claim (venmo_037):* "2. The categories of third parties to which we (a) disclose such personal information for a business purpose, (b) "share" personal information for "cr"
  - *Practice (venmo_011):* "Call recordings when you talk to customer service or sales.  Including business information, contact emails, phone numbers and taxpayer ID numbers."

**5. Jasper** (PWI=0.5004)
- Contradiction 1 [nli_plus_tone] (severity=0.941):
  - *Claim (jasper_034):* "We do not sell the personal information of Consumers We actually know are less than 16 years of age, unless We receive affirmative authorization (the"
  - *Practice (jasper_037):* "You have the right to opt-out of the sale of Your personal information. Once We receive and confirm a verifiable consumer request from You, we will st"

---

## 3. Most Common Contradiction Patterns

### Claim Segment Categories (sources of reassurance language)
| Category | Count | % of Contradictions |
|----------|-------|---------------------|
| THIRD_PARTY | 11 | 57.9% |
| SALE_SHARING | 5 | 26.3% |
| INTL_SPECIFIC | 1 | 5.3% |
| FIRST_PARTY | 1 | 5.3% |
| SECURITY | 1 | 5.3% |

### Practice Segment Categories (targets of contradiction)
| Category | Count | % of Contradictions |
|----------|-------|---------------------|
| FIRST_PARTY | 14 | 73.7% |
| THIRD_PARTY | 2 | 10.5% |
| SALE_SHARING | 1 | 5.3% |
| SECURITY | 1 | 5.3% |
| SENSITIVE_DATA | 1 | 5.3% |

### Top 10 Claim → Practice Category Pairs
| Claim Category | Practice Category | Count |
|----------------|-------------------|-------|
| THIRD_PARTY | FIRST_PARTY | 9 |
| SALE_SHARING | FIRST_PARTY | 4 |
| THIRD_PARTY | THIRD_PARTY | 2 |
| INTL_SPECIFIC | SALE_SHARING | 1 |
| FIRST_PARTY | FIRST_PARTY | 1 |
| SECURITY | SECURITY | 1 |
| SALE_SHARING | SENSITIVE_DATA | 1 |

---

## 4. Per-Category Analysis

Which OPPT practice categories exhibit the largest rhetorical contradictions?

| Category | N Pairs | Severity | Tone Gap | NLI Rate | Hedging | Specificity | Vagueness |
|----------|---------|----------|----------|----------|---------|-------------|-----------|
| SALE_SHARING | 9 | 0.1046 | 1.99 | 0.111 | 0.171 | 0.0331 | 0.0135 |
| SENSITIVE_DATA | 10 | 0.0989 | 6.33 | 0.100 | 0.363 | 0.0516 | 0.0227 |
| FIRST_PARTY | 155 | 0.0811 | 6.63 | 0.090 | 0.354 | 0.0287 | 0.0189 |
| SECURITY | 30 | 0.0333 | 3.48 | 0.033 | 0.095 | 0.0239 | 0.0097 |
| THIRD_PARTY | 74 | 0.0284 | 7.85 | 0.027 | 0.398 | 0.0259 | 0.0309 |
| AUTOMATED_DECISIONS | 6 | 0.0000 | 12.50 | 0.000 | 0.312 | 0.0000 | 0.0063 |
| RETENTION | 20 | 0.0000 | 13.93 | 0.000 | 0.519 | 0.0125 | 0.0177 |
| TRACKING | 14 | 0.0000 | 2.51 | 0.000 | 0.280 | 0.0434 | 0.0194 |

**Key findings:**
- **SALE_SHARING** has the highest NLI contradiction rate (11.1%), suggesting the starkest gap between reassuring language and practice disclosures in this category.
- **RETENTION** has the highest mean tone gap (13.93), driven by hedging (0.519) and low specificity (0.0125).
- **RETENTION** has the highest hedging score (0.519) with vagueness (0.0177) — language in this category is most evasive.

---

## 5. Case Studies

### Microsoft (Rank #1, PWI=1.0000)
- **Total segments:** 66
- **Reassurance segments:** 5
- **Claim-practice pairs:** 1
- **Contradictions (NLI-flagged):** 1
- **Categories:** FIRST_PARTY: 38, TRACKING: 8, OTHER: 6, INTL_SPECIFIC: 3, SECURITY: 2

**Top contradictions:**

1. **[nli_plus_tone]** severity=0.999, NLI=0.997
   - *Claim (microsoft_014, SECURITY):* "Microsoft is committed to protecting the security of your personal data. We use a variety of security technologies and procedures to help protect your personal data from unauthorized access, use, or..."
   - *Practice (microsoft_053, SECURITY):* ". Device encryption helps protect the data stored on your device by encrypting it using BitLocker Drive Encryption technology. When device encryption is on, Windows automatically encrypts the drive..."


### Tesla (Rank #2, PWI=0.7360)
- **Total segments:** 30
- **Reassurance segments:** 2
- **Claim-practice pairs:** 21
- **Contradictions (NLI-flagged):** 11
- **Categories:** FIRST_PARTY: 17, THIRD_PARTY: 4, OTHER: 3, USER_CHOICE: 2, REGIONAL: 1

**Top contradictions:**

1. **[nli_plus_tone]** severity=1.110, NLI=0.998
   - *Claim (tesla_020, THIRD_PARTY):* "We may share information with:  - Our service providers, business partners and affiliates - Third parties you authorize - Other third parties as required by law  We limit how, and with who, we share..."
   - *Practice (tesla_022, THIRD_PARTY):* "| Categories of Recipients | Description | Reason for Sharing | |---|---|---| | Financial institutions | Companies that process credit applications for lease and financing offerings | To confirm your..."

2. **[nli_plus_tone]** severity=1.011, NLI=0.958
   - *Claim (tesla_020, THIRD_PARTY):* "We may share information with:  - Our service providers, business partners and affiliates - Third parties you authorize - Other third parties as required by law  We limit how, and with who, we share..."
   - *Practice (tesla_019, FIRST_PARTY):* "Except as described here, Tesla may also collect, use, and share information that does not, on its own, personally identify you. Such information may be used for any purpose, including for example,..."

3. **[nli]** severity=0.998, NLI=0.998
   - *Claim (tesla_020, THIRD_PARTY):* "We may share information with:  - Our service providers, business partners and affiliates - Third parties you authorize - Other third parties as required by law  We limit how, and with who, we share..."
   - *Practice (tesla_007, FIRST_PARTY):* "| Categories of Data | Description | Purpose and Legal Basis | |---|---|---| | Order information | Your purchase details, order agreement, trade-in information, and other pre-delivery documents such..."


### Linkedin (Rank #3, PWI=0.5606)
- **Total segments:** 56
- **Reassurance segments:** 2
- **Claim-practice pairs:** 13
- **Contradictions (NLI-flagged):** 1
- **Categories:** FIRST_PARTY: 18, THIRD_PARTY: 15, OTHER: 6, USER_CHOICE: 5, TRACKING: 3

**Top contradictions:**

1. **[nli_plus_tone]** severity=1.044, NLI=0.999
   - *Claim (linkedin_034, FIRST_PARTY):* "We seek to create economic opportunity for Members of the global workforce and to help them be more productive and successful. We use the personal data available to us to research social, economic..."
   - *Practice (linkedin_009, FIRST_PARTY):* "We collect personal data from you when you provide, post or upload it to our Services, such as when you fill out a form, (e.g., with demographic data or salary), respond to a survey, or submit a..."


---

## 6. Enforcement Validation Statistics

**Sample:** 3 enforcement-actioned companies, 14 non-enforced (total: 17)
**Missing from analysis:** adobe, amazon, att, avast, babel-street, betterhelp, cerebral, clearview-ai, draftkings, epic-games, fanduel, google, gravy-analytics, grindr, kochava, lexisnexis, monument, ngl, premom, roblox, safegraph, t-mobile, tiktok, tinder, uber, verizon, vonage, x-mode-social (no reassurance-practice pairs generated)

| Metric | Value | 95% CI |
|--------|-------|--------|
| Enforced mean PWI | 0.1869 | [0.0000, 0.5606] |
| Non-enforced mean PWI | 0.2175 | [0.0577, 0.3998] |
| Mean difference | -0.0306 | — |
| Mann-Whitney U | 21.0 | p=1.0000 |
| Cohen's d | -0.0912 (negligible) | [-0.9923, 1.3277] |
| ROC-AUC | 0.5000 | [0.2308, 0.9333] |

**Interpretation:** The null result (p=1.00, d=-0.09, AUC=0.50) indicates no detectable
association between privacy washing intensity and enforcement history in this corpus.
Several explanations are plausible:
1. Enforcement actions target observable behaviors and outcomes, not policy rhetoric
2. Companies facing enforcement may have updated their policies post-enforcement
3. The sample size (N=17, 3 enforced) provides limited statistical power
4. PWI captures rhetorical dissonance, which may be orthogonal to enforcement-triggering behaviors

*Results are exploratory/hypothesis-generating given modest sample size (N=17 companies, 3 enforced). Bootstrap N=10,000.*

---

## 7. Methodology Notes

### Pipeline Overview

1. **Linguistic features** (Script 1): Per-segment hedging, reassurance, specificity, commitment
   strength, and readability scores extracted from 3,651 annotated segments.

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

- **Statistical power**: With 17 companies (3 enforced) in the enforcement
  analysis, statistical power is modest. All results should be treated as
  exploratory and hypothesis-generating.

- **Python 3.14 compatibility**: spaCy NER was replaced with regex-based entity
  detection due to a Pydantic v1 incompatibility. This affects the specificity
  score's entity detection component (ORG, DATE, MONEY) but does not fundamentally
  change the metric.
