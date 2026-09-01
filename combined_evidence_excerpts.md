# Combined Evidence Excerpts — Privacy Washing Detection

*Both corpora, NLI-primary pipeline, 2026-01-26*

---

## Overview

| Corpus | Companies | Pairs | Contradictions | Rate | Enforced |
|--------|-----------|-------|----------------|------|----------|
| OPP-115 | 43 | 820 | 52 | 6.3% | 0 of 43 |
| OPPT (main) | 17 | 318 | 19 | 6.0% | 3 of 17 |
| **Total** | **60** | **1,138** | **71** | **6.2%** | **3 of 60** |

---

## Human Verification Summary

All 71 NLI-flagged contradictions were manually assessed for validity.

| Category | OPPT | OPP-115 | Total | % |
|----------|------|---------|-------|---|
| **Genuine contradiction** | 14 | 31 | **45** | **63.4%** |
| **Borderline/weak** | 4 | 15 | **19** | **26.8%** |
| **False positive** | 1 | 6 | **7** | **9.9%** |
| **Total** | 19 | 52 | 71 | 100% |

**Strict false positive rate: 9.9%** (practice clearly supports or is unrelated to claim).

**Precision interpretations:**
- Strictest (genuine only): 63.4%
- Moderate (genuine + defensible borderline): ~75-80%
- Clear false positive rate: 9.9%

### Systematic False Positive Patterns (7 cases)

1. **Security implementation supporting security claim** (3 cases):
   - Microsoft: BitLocker encryption supports "committed to protecting security"
   - ScienceMag: SSL encryption supports "reasonable technical measures"
   - KraftRecipes: "administrative, technical safeguards" supports "do not disclose"

2. **Practice restating same non-sharing commitment** (2 cases):
   - Adweek: Practice says "we do NOT allow third-party companies to collect PII" — consistent with claim
   - LatinPost #14: Practice says third parties "do not have access" — supports claim

3. **Informational/educational content** (2 cases):
   - Allstate: Email security advice (send via mail/fax) — not about selling data
   - LatinPost #22: Phishing disclosure is educational, not a contradictory practice

---

## Corpus 1: OPPT (Main — 17 Companies)

### 1. Microsoft (PWI=1.000, Rank #1) — FALSE POSITIVE

- 66 segments, 1 pair, 1 contradiction
- **Edge case**: Only 1 pair survived filtering, and it was flagged. PWI=1.0 is an artifact of the 1/1 denominator.

**Contradiction 1** [nli_plus_tone] severity=0.999, NLI=0.997
- *Claim (microsoft_014, SECURITY):* "Microsoft is committed to protecting the security of your personal data. We use a variety of security technologies and procedures to help protect your personal data from unauthorized access, use, or disclosure."
- *Practice (microsoft_053, SECURITY):* "Device encryption helps protect the data stored on your device by encrypting it using BitLocker Drive Encryption technology. When device encryption is on, Windows automatically encrypts the drive..."

**Verdict: FALSE POSITIVE.** The NLI model sees a security commitment contradicted by a specific implementation detail (BitLocker). In reality, the implementation *supports* the commitment.

---

### 2. Tesla (PWI=0.736, Rank #2) — GENUINE (9 of 11), BORDERLINE (2 of 11)

- 30 segments, 21 pairs, 11 contradictions (52.4% density)
- All contradictions stem from one claim: "We may share information with: service providers, business partners, affiliates... **We limit how, and with who, we share your data.**"

| # | Practice | NLI | Verdict |
|---|----------|-----|---------|
| 5 | Website visit, store, event, test drive collection | 0.862 | **Genuine** |
| 6 | Order info, purchase details, trade-in data tables | 0.998 | **Genuine** |
| 7 | Vehicle type, VIN, configuration data tables | 0.986 | **Genuine** |
| 8 | Energy installation data, home details, roof dimensions | 0.842 | **Genuine** |
| 9 | Diagnostic logs ("minimum level necessary") | 0.584 | **Borderline** — practice actually says "minimum necessary," partially consistent |
| 10 | Contests, events, promotions | 0.858 | **Genuine** |
| 11 | Complete purchase, process payment, financing | 0.964 | **Borderline** — standard business purposes |
| 12 | Conduct research, develop new products | 0.956 | **Genuine** |
| 13 | Non-PII "used for any purpose" | 0.958 | **Genuine** — "any purpose" directly contradicts "limit" |
| 14 | Affiliates and subsidiaries sharing table | 0.991 | **Genuine** |
| 15 | Financial institutions, credit applications table | 0.998 | **Genuine** |

---

### 3. LinkedIn (PWI=0.561, Rank #3) [ENFORCED] — GENUINE

- 56 segments, 13 pairs, 1 contradiction

**Contradiction 1** [nli_plus_tone] severity=1.044, NLI=0.999
- *Claim (linkedin_034, FIRST_PARTY):* "We seek to create economic opportunity for Members of the global workforce and to help them be more productive and successful. We use the personal data available to us to research social, economic..."
- *Practice (linkedin_009, FIRST_PARTY):* "We collect personal data from you when you provide, post or upload it to our Services, such as when you fill out a form, (e.g., with demographic data or salary), respond to a survey, or submit a resume..."

**Verdict: GENUINE.** The claim frames data use altruistically ("economic opportunity for Members"), but the practice reveals broad collection including demographics, salary, survey responses — data that primarily serves LinkedIn's business model.

---

### 4. Venmo (PWI=0.508, Rank #4) — GENUINE (3 of 4), BORDERLINE (1 of 4)

- 45 segments, 38 pairs, 4 contradictions
- All from one CCPA compliance claim about "categories of third parties to which we disclose/share/sell"

| # | Practice | NLI | Verdict |
|---|----------|-----|---------|
| 16 | SSN and government ID collection | 0.989 | **Genuine** — extremely sensitive data |
| 17 | Call recordings and taxpayer IDs | 0.989 | **Genuine** |
| 18 | Name, birthday, address, phone, email | 0.970 | **Genuine** |
| 19 | CCPA category table (identifiers) | 0.693 | **Borderline** — both are compliance language |

---

### 5. Jasper (PWI=0.500, Rank #5) — GENUINE

**Contradiction 1** [nli_plus_tone] severity=0.941, NLI=0.930
- *Claim (jasper_034, SALE_SHARING):* "We do not sell the personal information of Consumers We actually know are less than 16 years of age, unless We receive affirmative authorization..."
- *Practice (jasper_037, SALE_SHARING):* "You have the right to opt-out of the sale of Your personal information. Once We receive and confirm a verifiable consumer request from You, we will stop selling Your personal information."

**Verdict: GENUINE.** Claims not to sell children's data, but practice describes opt-out mechanism for data sales — implying sales are the default state.

---

### 6. Motorola Solutions (PWI=0.300, Rank #6) — BORDERLINE

**Contradiction 1** [nli_plus_tone] severity=0.561, NLI=0.560
- *Claim:* "We disclose all categories of personal data... our disclosure does not constitute a 'sale'"
- *Practice:* "We collect contact information: name, alias, title, company, phone, email..."

**Verdict: BORDERLINE.** NLI barely above threshold. Disclosure framing vs collection categories — weak tension.

---

### Enforced Companies

| Company | PWI | Rank | Contradictions | Notes |
|---------|-----|------|----------------|-------|
| LinkedIn | 0.561 | #3 | 1 | **Genuine.** Altruistic framing vs broad collection. |
| Bumble | 0.000 | #8 | 0 | 19 pairs, zero contradictions. Clean policy. |
| Meta | 0.000 | #12 | 0 | 99 pairs (!), zero contradictions. Avoids reassurance language entirely. |

---

## Corpus 2: OPP-115 (43 Companies)

### 1. ScienceMag.org (PWI=1.000, Rank #1) — FALSE POSITIVE

- 36 segments, 1 pair, 1 contradiction. Same 1/1 artifact.

**Contradiction 1** [nli_plus_tone] severity=0.972, NLI=0.966
- *Claim (SECURITY):* "We implement reasonable technical and organizational measures designed to secure your personal information..."
- *Practice (SECURITY):* "The SSL encrypts, or translates, your order information into a highly indecipherable code..."

**Verdict: FALSE POSITIVE.** SSL encryption implements the security measures claimed.

---

### 2. SheKnows.com (PWI=0.631, Rank #2) — BORDERLINE

**Contradiction 1** [nli] severity=0.995, NLI=0.995
- *Claim (SECURITY):* "To protect your privacy and security, we take reasonable steps (such as requesting a unique password) to verify your identity..."
- *Practice (SECURITY):* "Compromise of Personal Information — In the event that personal information is compromised as a result of a breach..."

**Verdict: BORDERLINE.** Breach notification is a responsible contingency, not a contradiction of protection commitment.

---

### 3. LatinPost.com (PWI=0.621, Rank #3) — GENUINE (6 of 15), BORDERLINE (7 of 15), FP (2 of 15)

- 89 segments, 57 pairs, 15 contradictions
- Primary claim: "Latin Post will not use a wireless telephone number, email address, or other Information submitted for its wireless marketing services for any [unauthorized purpose]"

| # | Practice Summary | NLI | Verdict |
|---|-----------------|-----|---------|
| 10 | Broad applicability statement | 0.980 | **Borderline** — loose topical match |
| 11 | "Personal Information" definition | 0.910 | **Borderline** — definitional text |
| 12 | Email collected during user registration | 0.943 | **Genuine** |
| 13 | Cookies and tracking technologies | 0.941 | **Borderline** — different mechanism than email/phone |
| 14 | "Third parties do not have access" | 0.975 | **FALSE POSITIVE** — supports the claim |
| 15 | "Use Personal Information in a variety of ways" | 0.967 | **Genuine** |
| 16 | "Sending marketing and promotional emails" | 0.975 | **Genuine** — direct contradiction |
| 17 | "Contacting you regarding use of the Site" | 0.975 | **Genuine** |
| 18 | "Other Information... used in a variety of ways" | 0.993 | **Genuine** |
| 19 | Third-party ad providers may collect info | 0.963 | **Genuine** |
| 20 | Double opt-in mechanism description | 0.895 | **Borderline** — consent mechanism |
| 21 | Legal enforcement exception | 0.954 | **Borderline** — standard carve-out |
| 22 | Phishing disclosure | 0.998 | **FALSE POSITIVE** — educational content |
| 23 | Second claim, broad applicability | 0.981 | **Borderline** (from second claim) |
| 24 | Second claim, user registration | 0.911 | **Borderline** (collection ≠ disclosure) |

---

### 4. TaylorSwift.com (PWI=0.613, Rank #4) — GENUINE (2 of 3), BORDERLINE (1 of 3)

Claim: "We will not share your information with third parties for the purposes of their direct marketing unless you affirmatively agree."

| # | Practice | NLI | Verdict |
|---|----------|-----|---------|
| 2 | Message boards/forums make info public | 0.897 | **Borderline** — different vector (public posting vs marketing) |
| 3 | "May disclose to employees, agents, contractors, affiliates" | 0.997 | **Genuine** — affiliate/contractor carve-out contradicts "will not share" |
| 4 | "We will share under the following circumstances:" | 0.955 | **Genuine** — near-explicit contradiction |

---

### 5. Meredith.com (PWI=0.587, Rank #5) — GENUINE (3 of 4), BORDERLINE (1 of 4)

Claim: "If you use our Services to sign up for special email offers from third-party advertisers, we will also share your email address..." [conditional framing]

| # | Practice | NLI | Verdict |
|---|----------|-----|---------|
| 39 | "Analyze, operate, improve services, send email newsletters" | 0.998 | **Genuine** — unconditional vs conditional |
| 40 | "Advertising tailored to your interests" | 0.999 | **Genuine** — unconditional targeting |
| 41 | "For any other purposes... pursuant to your consent" | 0.842 | **Borderline** — catch-all clause |
| 42 | "Share email addresses with service providers for targeted advertising" | 0.995 | **Genuine** — direct |

---

### Remaining OPP-115 Companies (Ranks 6-20)

**Allstate (#13)** — 1 contradiction — **FALSE POSITIVE.** "Do not sell your personal information" vs email security advice. Practice is not about sharing.

**Adweek (#7)** — 1 contradiction — **FALSE POSITIVE.** Practice says "we do NOT allow third parties to collect PII" — *consistent* with claim.

**KraftRecipes (#17)** — 1 contradiction — **FALSE POSITIVE.** Security safeguards support the no-disclosure claim.

**SIDEARM Sports (#18)** — 3 contradictions — **ALL GENUINE.**
- "Will not sell, rent, swap email" vs cookies/beacons (genuine)
- vs targeted advertising (genuine)
- CAN-SPAM compliance vs non-PII advertising transmission (genuine)

**NYTimes (#12)** — 4 contradictions — **ALL GENUINE.**
- "Will not sell, rent, swap email" vs cookies/tracking (genuine)
- vs non-PII transmission to third parties for advertising (genuine)
- vs "demographic info for targeted advertising" (genuine)
- vs "share audience info in aggregate" (genuine)

**TheAtlantic (#6)** — 2 contradictions — **BOTH GENUINE.**
- "Will not disclose PII" vs "may disclose non-PII" (non-PII loophole)
- vs contests/sweepstakes data collection

**VoxMedia (#9)** — 2 contradictions — **BOTH GENUINE.**
- Non-PII sharing limit vs ad companies collecting clickstream data
- Non-identification promise vs ad companies collecting browser data

**Barnes & Noble (#10)** — 1 contradiction — **GENUINE.** "Don't sell or rent personal info" vs extensive purchase data collection.

**ABCNews (#11)** — 1 contradiction — **GENUINE.** "Won't share outside Disney except..." vs broad collection from forums.

**PBS (#14)** — 1 contradiction — **GENUINE.** "Won't willfully disclose PII" vs user comments made publicly available.

**Reddit (#16)** — 2 contradictions — **1 GENUINE, 1 BORDERLINE.**
- "Private info never for sale" vs payment data storage (genuine)
- "We collect some info for your account" vs PayPal email/transaction numbers (borderline — standard for purchases)

**Lynda.com (#15)** — 6 contradictions — **4 GENUINE, 2 BORDERLINE.**
- "Share PII only as described in this policy" vs "partner cookies NOT covered by our policy" (genuine x2)
- vs third-party ad networks (genuine x2)
- "Won't share PII for marketing" vs automatic device info collection (borderline)
- Same restriction vs general sharing framework (borderline — tautological)

**OCRegister (#8)** — 1 contradiction — **GENUINE.** "Won't sell, share, rent personal info" vs third-party ad companies.

**MLB (#20)** — 1 contradiction — **BORDERLINE.** NLI=0.655. Contacts list access vs policy-compliant sharing framing.

**Lids (#19)** — 1 contradiction — **BORDERLINE.** NLI=0.660. "Improve shopping experience" vs "store any information."

---

## Cross-Corpus Patterns

### Most Convincing Detections

1. **Tesla** (OPPT): "We limit sharing" vs detailed sharing tables — 9/11 genuine, 52% density
2. **TaylorSwift** (OPP-115): "Will not share" vs "We will share" — near-explicit
3. **LatinPost** (OPP-115): "Will not use email" vs marketing emails — direct, 6/15 genuine
4. **LinkedIn** (OPPT, enforced): Altruistic framing vs broad collection
5. **Venmo** (OPPT): CCPA compliance framing vs SSN/call recording collection
6. **NYTimes** (OPP-115): "Won't sell/rent email" vs targeted advertising — all 4 genuine
7. **Meredith** (OPP-115): Conditional sharing framing vs unconditional advertising — 3/4 genuine

### Claim Category Sources

| Category | OPP-115 | OPPT |
|----------|---------|------|
| THIRD_PARTY | 86.5% | 57.9% |
| SALE_SHARING | 0% | 26.3% |
| FIRST_PARTY | 7.7% | 5.3% |
| SECURITY | 3.8% | 5.3% |

### Known Remaining Issues

1. **Small sample inflation**: 1/1 pair companies get PWI=1.0 (ScienceMag, Microsoft)
2. **Security implementation FPs**: NLI interprets security details as contradicting security commitments (3 cases, all identifiable by SECURITY/SECURITY same-category pairing)
3. **LatinPost dominance**: 15 of 52 OPP-115 contradictions (29%) come from one company with one claim — statistical concentration
