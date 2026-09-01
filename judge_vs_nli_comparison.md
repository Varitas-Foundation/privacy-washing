# Judge vs NLI — Comprehensive Evaluation

*3-LLM Judge (Claude Haiku 4.5, GPT-5-mini, Gemini 3 Flash) vs NLI (DeBERTa v3)*
*Both corpora: OPPT (17 companies, 318 pairs) + OPP-115 (43 companies, 820 pairs)*

## 1. Overall Statistics

| Category | OPPT | OPP-115 | Total |
|----------|------|---------|-------|
| Both flag contradiction | 2 | 12 | 14 |
| NLI flagged, judges dismissed | 17 | 40 | 57 |
| Judges found, NLI missed | 26 | 86 | 112 |
| Both say not contradiction | 273 | 682 | 955 |

**NLI total**: 71 contradictions
**Judge total**: 126 contradictions
**Overlap**: 14 (20% of NLI, 11% of judges)
**Jaccard similarity**: 7.7%

> **Key finding**: The two methods show almost no overlap (7.7% Jaccard). Of the 71 NLI-flagged
> contradictions, judges dismissed 57 (80.3%) and confirmed only 14 (19.7%). Meanwhile, judges
> found 112 new contradictions NLI missed. The methods are detecting fundamentally different things.

---

## 2. Did Judges Fix the 7 Known NLI False Positives?

These 7 pairs were manually assessed as false positives in the NLI pipeline.

| # | Company | FP Pattern | Judge Verdict | Consensus | Fixed? |
|---|---------|------------|---------------|-----------|--------|
| 1 | Microsoft | Security implementation (BitLocker) | NOT_CONTRADICTION | unanimous | YES |
| 2 | ScienceMag | Security implementation (SSL) | NOT_CONTRADICTION | unanimous | YES |
| 3 | KraftRecipes | Security safeguards | NOT_CONTRADICTION | unanimous | YES |
| 4 | Adweek | Practice restates non-sharing | NOT_CONTRADICTION | unanimous | YES |
| 5 | LatinPost | Practice restates non-sharing (third parties don't have access) | CONTRADICTION | majority | **NO** |
| 6 | Allstate | Informational (email advice) | NOT_CONTRADICTION | majority | YES |
| 7 | LatinPost | Informational (phishing disclosure) | NOT_CONTRADICTION | unanimous | YES |

**Result: 6/7 known false positives correctly dismissed by judges.**

### The 1 Unfixed False Positive

#### latinpost.com_057_vs_latinpost.com_015
**Company**: latinpost.com (OPP-115)
**NLI**: CONTRADICTION (score=0.975)
**Judges**: CONTRADICTION (majority)

**Claim** (latinpost.com_057):
> d. Use of Information. Latin Post will not use a wireless telephone number, wireless or conventional Internet email address, or other Information submitted for its wireless marketing services for any other purpose but to provide the service requested, unless we provide advance notice of any other use. We will not share any Personal Information with Advertisers or other third party marketers unless you opt-in to such disclosure. We will share Personal Information with the operational service providers that assist us in delivering these wireless services to you and with the Parent Companies and ...

**Practice** (latinpost.com_015):
> These Third Party Advertising Service Providers do not have access to Tracking Technologies set by the Site except to the extent necessary to provide services to the Site. The Third Party Advertising Service Providers, as well as Advertisers, may themselves set and access their own Tracking Technologies on your Device if you choose to have Tracking Technologies enabled in your browser (or, for Flash cookies, if you have not removed them) and/or they may otherwise have access to Other Information about you.

  - **anthropic/claude-haiku-4.5**: CONTRADICTION — The claim states that Personal Information will not be shared with Advertisers unless you opt-in, but the practice describes Third Party Advertising Service Providers and Advertisers setting and accessing Tracking Technologies on your device based on browser settings rather than explicit opt-in consent. This represents a sharing/access mechanism that operates independently of the opt-in requirement promised in the claim.
  - **openai/gpt-5-mini**: not contradiction — Segment B describes third-party advertisers setting and accessing their own tracking technologies (subject to the user enabling tracking) and possibly obtaining other information independently; it does not state that Latin Post shares users' Personal Information with advertisers without opt-in, so it does not contradict the promise in Segment A.
  - **google/gemini-3-flash-preview**: CONTRADICTION — The claim promises that personal information will not be shared with advertisers without an opt-in, but the practice reveals that advertisers may set tracking technologies and access information about the user if browser settings allow it, bypassing the promised opt-in requirement.


### The 6 Correctly Fixed False Positives

#### Microsoft: Security implementation (BitLocker)
**Company**: microsoft (OPPT)
**NLI**: CONTRADICTION (score=0.997)
**Judges**: NOT_CONTRADICTION (unanimous)

**Claim** (microsoft_014):
> Microsoft is committed to protecting the security of your personal data. We use a variety of security technologies and procedures to help protect your personal data from unauthorized access, use, or disclosure. For example, we store the personal data you provide on computer systems that have limited access and are in controlled facilities. When we transmit highly confidential data (such as a credit card number or password) over the internet, we protect it through the use of encryption. Microsoft complies with applicable data protection laws, including applicable security breach notification la...

**Practice** (microsoft_053):
> . Device encryption helps protect the data stored on your device by encrypting it using BitLocker Drive Encryption technology. When device encryption is on, Windows automatically encrypts the drive Windows is installed on and generates a recovery key. The BitLocker recovery key for your personal device is automatically backed up online in your personal Microsoft OneDrive account. Microsoft doesn't use your individual recovery keys for any purpose.
Malicious Software Removal Tool
. The Malicious Software Removal Tool (MSRT) runs on your device at least once per month as part of Windows Update. ...

  - **anthropic/claude-haiku-4.5**: not contradiction — The practice describes specific security implementations (BitLocker encryption, Microsoft Defender SmartScreen, Smart App Control, and Microsoft Defender Antivirus) that support and operationalize the claim's commitment to protecting personal data through security technologies and procedures. The data collection described is limited to security purposes and is consistent with the claim's promise to protect data from unauthorized access, use, or disclosure.
  - **openai/gpt-5-mini**: not contradiction — Segment B describes concrete security measures (BitLocker, Defender, SmartScreen) and telemetry used for threat detection, including safeguards like prompting before sending reports that may contain personal data and the ability to opt out; these practices support rather than contradict Microsoft’s commitment to protect personal data and use encryption and controlled access.
  - **google/gemini-3-flash-preview**: not contradiction — The practice segment describes specific security features and tools, such as BitLocker, MSRT, and Microsoft Defender, which implement and support the general commitment to data security and unauthorized access prevention made in the claim.

---

#### ScienceMag: Security implementation (SSL)
**Company**: sciencemag.org (OPP-115)
**NLI**: CONTRADICTION (score=0.966)
**Judges**: NOT_CONTRADICTION (unanimous)

**Claim** (sciencemag.org_030):
> SECURITY We implement reasonable technical and organizational measures designed to secure your personal information from accidental loss and from unauthorized access, use, alteration, or disclosure. In addition, all credit transactions occur in a secure area of our site, to protect you from any loss, misuse, or alteration of information collected. However, we cannot guarantee that unauthorized third parties will never be able to defeat those measures or use your personal information for improper purposes. When you place an order online at any of the Science websites, your credit card informati...

**Practice** (sciencemag.org_031):
> The SSL encrypts, or translates, your order information into a highly indecipherable code, which is processed immediately. When you've finished your transactions and begin the checkout process, you will move into the secure area of our site. A warning window may pop up to notify you that you are entering this "safe" area. Once you've entered, the page address (URL) will change from http to https, to let you know you are in a secure area. Also, a key or closed lock will appear in the lower left-hand corner of your screen to notify you of this change. You will remain in this secure zone for the ...

  - **anthropic/claude-haiku-4.5**: not contradiction — The practice describes specific SSL encryption implementation, secure checkout procedures, and credit card protection measures that directly support and implement the security commitment made in the claim. The practice provides concrete examples of the 'reasonable technical and organizational measures' promised in the claim.
  - **openai/gpt-5-mini**: not contradiction — The practice elaborates on and implements the security commitments in the claim (SSL encryption, secure checkout area, visual indicators, limited on-screen card digits, and secure transmission to the card processor). There is no statement in the practice that contradicts or undermines the claim's assurances or its caveat about absolute guarantees.
  - **google/gemini-3-flash-preview**: not contradiction — The practice segment provides specific technical details, such as SSL encryption and HTTPS protocols, that implement and support the security commitments made in the claim.

---

#### KraftRecipes: Security safeguards
**Company**: kraftrecipes.com (OPP-115)
**NLI**: CONTRADICTION (score=0.919)
**Judges**: NOT_CONTRADICTION (unanimous)

**Claim** (kraftrecipes.com_019):
> How We Share Your Information We do not sell or otherwise disclose personally identifiable information about our website visitors, except as described here. We do not share your personally identifiable information with unaffiliated third parties for their own marketing purposes without your consent. For California residents, please see "Your California Privacy Rights" below.

**Practice** (kraftrecipes.com_029):
> How We Protect Your Information The security of personally-identifiable information is important to us. We maintain administrative, technical and physical safeguards to protect against unauthorized use, disclosure, alteration or destruction of the personally-identifiable information we collect on this website. While we make every effort to help ensure the integrity and security of our network and systems, we cannot guarantee our security measures.

  - **anthropic/claude-haiku-4.5**: not contradiction — The claim commits to not selling or disclosing personally identifiable information without consent, and the practice describes security safeguards that protect the data from unauthorized disclosure. The practice supports the claim by explaining how the company protects the information it commits not to improperly share.
  - **openai/gpt-5-mini**: not contradiction — Segment B describes security safeguards to protect personally-identifiable information, which supports rather than contradicts the commitment in Segment A not to sell or share PII with unaffiliated third parties for marketing without consent.
  - **google/gemini-3-flash-preview**: not contradiction — The practice describes the security measures and safeguards used to protect data, which supports and is consistent with the claim's commitment to not disclosing information improperly.

---

#### Adweek: Practice restates non-sharing
**Company**: adweek.com (OPP-115)
**NLI**: CONTRADICTION (score=0.986)
**Judges**: NOT_CONTRADICTION (unanimous)

**Claim** (adweek.com_008):
> We do not sell Personally Identifiable Information or other information you make available to the Websites, or share such information with third parties, except as described below.

**Practice** (adweek.com_005):
> No Personally Identifiable Information (see below) is collected through our cookies or Web beacons nor do we allow third-party companies to collect such information from cookies or web beacons on our Website. We may, however, from time to time, allow third-party companies to serve ads and/or collect certain Non-Personally Identifiable Information when you visit our Website. These companies may use Non-Personally Identifiable Information (e.g. click stream information, browser type, time and date, subject of advertisements clicked or scrolled over) during your visits to this and other websites ...

  - **anthropic/claude-haiku-4.5**: not contradiction — The claim states the company does not sell or share Personally Identifiable Information except as described, and the practice confirms that no PII is collected through cookies or shared with third parties for that purpose. The practice describes collection of Non-Personally Identifiable Information (non-PII) by third parties for behavioral advertising, which is a separate category and does not contradict the commitment regarding PII.
  - **openai/gpt-5-mini**: not contradiction — The practice explicitly states that no PII is collected or shared via cookies/web beacons and only non-personally identifiable information is shared with third-party advertisers for behavioral ads, which aligns with the claim's promise not to sell or share PII (subject to the described exceptions). There is no statement in the practice that contradicts the no-PII sale/share commitment.
  - **google/gemini-3-flash-preview**: not contradiction — The claim promises not to sell or share information except as described in the policy, and the practice explicitly clarifies that only non-personally identifiable information is shared with third-party advertisers while maintaining the protection of personally identifiable information.

---

#### Allstate: Informational (email advice)
**Company**: allstate.com (OPP-115)
**NLI**: CONTRADICTION (score=0.985)
**Judges**: NOT_CONTRADICTION (majority)

**Claim** (allstate.com_004):
> Our Privacy Assurance We do not sell your personal or medical information to anyone. We do not share your information with non-affiliate companies that would use it to contact you about their own products and services, unless permitted pursuant to a joint marketing agreement. We require persons or organizations that represent or assist us in servicing your policy and claims to keep your information confidential. We require our employees to protect your personal information and keep it confidential.

**Practice** (allstate.com_028):
> You should exercise discretion with respect to the submission of any personal or financial information via e-mail. If you are concerned about the security of your communication, we encourage you to send your correspondence through the postal service or use the telephone to speak directly to us. We are not responsible for the security or confidentiality of communications you send to us through the Internet using e-mail messages.

  - **anthropic/claude-haiku-4.5**: not contradiction — The claim makes commitments about how Allstate handles personal information internally and with third parties. The practice describes security risks associated with email communication and disclaims responsibility for internet-based transmissions, which is informational guidance that does not contradict the data handling commitments made in the claim.
  - **openai/gpt-5-mini**: not contradiction — Segment B is a disclaimer about the security of e-mail transmissions and the user's responsibility for sending sensitive data; it does not state the company sells or shares personal/medical information or contradict the commitments to keep information confidential and restrict sharing. The practice addresses transmission risk, not a breach of the promised data-sharing protections.
  - **google/gemini-3-flash-preview**: CONTRADICTION — The claim promises that the company requires employees and partners to keep information confidential, but the practice explicitly disclaims responsibility for the confidentiality of information sent via email. This undermines the broad assurance of confidentiality by shifting the burden and risk entirely to the consumer for a standard communication channel.

---

#### LatinPost: Informational (phishing disclosure)
**Company**: latinpost.com (OPP-115)
**NLI**: CONTRADICTION (score=0.998)
**Judges**: NOT_CONTRADICTION (unanimous)

**Claim** (latinpost.com_057):
> d. Use of Information. Latin Post will not use a wireless telephone number, wireless or conventional Internet email address, or other Information submitted for its wireless marketing services for any other purpose but to provide the service requested, unless we provide advance notice of any other use. We will not share any Personal Information with Advertisers or other third party marketers unless you opt-in to such disclosure. We will share Personal Information with the operational service providers that assist us in delivering these wireless services to you and with the Parent Companies and ...

**Practice** (latinpost.com_078):
> Phishing. Phishing attacks attempt to steal consumers' personal identity data and financial account credentials. "Phishers" use 'spoofed' e-mails to lead consumers to counterfeit websites designed to trick recipients into divulging Information such as credit card numbers, account usernames, passwords and social security numbers. WE DO NOT SEND EMAILS ASKING YOU TO PROVIDE OR CONFIRM CREDIT CARD NUMBERS, SOCIAL SECURITY NUMBERS OR YOUR USERNAME OR PASSWORD! If you receive such email communication, please forward it immediately to the Site's Privacy Administrator at admin@latinpost.com, and then...

  - **anthropic/claude-haiku-4.5**: not contradiction — The practice segment is educational content warning users about phishing attacks and does not describe any actual data handling practice by Latin Post that conflicts with the claim. The claim addresses how Latin Post uses and shares information, while the practice segment addresses how to identify fraudulent third-party emails impersonating Latin Post.
  - **openai/gpt-5-mini**: not contradiction — The phishing notice is an informational security warning stating the company will not request sensitive credentials via email and instructs users how to report fraud; it does not conflict with the claim about limiting use/sharing of personal information and in fact supports the stated protections.
  - **google/gemini-3-flash-preview**: not contradiction — The practice segment provides educational information regarding phishing and a commitment to not request sensitive credentials via email, which does not conflict with the claim's rules regarding data usage and third-party sharing.

---

## 3. Did Judges Confirm Known Genuine Contradictions?

From our human assessment, 45 of 71 NLI-flagged pairs were genuine contradictions.
We check whether judges confirmed or dismissed these.

### Per-Company: NLI-Flagged Pairs vs Judge Verdict vs Human Assessment

| Company | NLI flagged | Human: Genuine | Human: Borderline | Human: FP | Judge confirmed | Judge dismissed |
|---------|-------------|----------------|-------------------|-----------|----------------|----------------|
| tesla | 11 | 9 | 2 | 0 | 0 | 11 |
| latinpost.com | 15 | 6 | 7 | 2 | 6 | 9 |
| nytimes.com | 4 | 4 | 0 | 0 | 0 | 4 |
| lynda.com | 6 | 4 | 2 | 0 | 1 | 5 |
| venmo | 4 | 3 | 1 | 0 | 1 | 3 |
| meredith.com | 4 | 3 | 1 | 0 | 1 | 3 |
| sidearmsports.com | 3 | 3 | 0 | 0 | 0 | 3 |
| taylorswift.com | 3 | 2 | 1 | 0 | 2 | 1 |
| theatlantic.com | 2 | 2 | 0 | 0 | 1 | 1 |
| voxmedia.com | 2 | 2 | 0 | 0 | 0 | 2 |
| linkedin | 1 | 1 | 0 | 0 | 0 | 1 |
| jasper | 1 | 1 | 0 | 0 | 1 | 0 |
| barnesandnoble.com | 1 | 1 | 0 | 0 | 0 | 1 |
| abcnews.com | 1 | 1 | 0 | 0 | 0 | 1 |
| pbs.org | 1 | 1 | 0 | 0 | 0 | 1 |
| ocregister.com | 1 | 1 | 0 | 0 | 1 | 0 |
| reddit.com | 2 | 1 | 1 | 0 | 0 | 2 |
| motorola-solutions | 1 | 0 | 1 | 0 | 0 | 1 |
| microsoft | 1 | 0 | 0 | 1 | 0 | 1 |
| sciencemag.org | 1 | 0 | 0 | 1 | 0 | 1 |
| sheknows.com | 1 | 0 | 1 | 0 | 0 | 1 |
| allstate.com | 1 | 0 | 0 | 1 | 0 | 1 |
| adweek.com | 1 | 0 | 0 | 1 | 0 | 1 |
| kraftrecipes.com | 1 | 0 | 0 | 1 | 0 | 1 |
| mlb.mlb.com | 1 | 0 | 1 | 0 | 0 | 1 |
| lids.com | 1 | 0 | 1 | 0 | 0 | 1 |

### Key Observations

**Companies where judges dismissed ALL genuine contradictions (complete misses):**

- **abcnews.com**: 1 genuine contradictions, judges confirmed 0
- **barnesandnoble.com**: 1 genuine contradictions, judges confirmed 0
- **linkedin**: 1 genuine contradictions, judges confirmed 0
- **nytimes.com**: 4 genuine contradictions, judges confirmed 0
- **pbs.org**: 1 genuine contradictions, judges confirmed 0
- **reddit.com**: 1 genuine contradictions, judges confirmed 0
- **sidearmsports.com**: 3 genuine contradictions, judges confirmed 0
- **tesla**: 9 genuine contradictions, judges confirmed 0
- **voxmedia.com**: 2 genuine contradictions, judges confirmed 0

**Companies where judges confirmed at least some genuine contradictions:**

- **jasper**: 1 genuine, judges confirmed 1
- **latinpost.com**: 6 genuine, judges confirmed 6 (judge confirmations counted over all 15 flagged pairs, not only the genuine ones)
- **lynda.com**: 4 genuine, judges confirmed 1
- **meredith.com**: 3 genuine, judges confirmed 1
- **ocregister.com**: 1 genuine, judges confirmed 1
- **taylorswift.com**: 2 genuine, judges confirmed 2
- **theatlantic.com**: 2 genuine, judges confirmed 1
- **venmo**: 3 genuine, judges confirmed 1

---

## 4. Systematic Judge Failure Analysis

The judges exhibit a consistent failure mode when dismissing genuine contradictions.
Analysis of the reasoning reveals three patterns:

### Pattern A: Narrow Literal Interpretation

Judges interpret claims extremely narrowly, then dismiss practices that don't match
the narrow interpretation. Example: If the claim says 'we will not sell your email,'
judges dismiss cookie tracking and non-PII advertising sharing as 'different topic.'

**Affected companies**: NYTimes (4/4 dismissed), SIDEARM Sports (3/3 dismissed),
Barnes & Noble (1/1 dismissed)

**Example — NYTimes** (claim: 'will not sell, rent, swap email'):

#### nytimes.com_044_vs_nytimes.com_027
**Company**: nytimes.com (OPP-115)
**NLI**: CONTRADICTION (score=0.856)
**Judges**: NOT_CONTRADICTION (unanimous)

**Claim** (nytimes.com_044):
> WITH WHOM DO WE SHARE THE INFORMATION THAT WE GATHER- Within The New York Times If you have registered to use the NYT Services, we will not sell, rent, swap or authorize any third party to use your email address without your permission.

**Practice** (nytimes.com_027):
> We may transmit non-personally identifiable website usage information to third parties in order to show you advertising for The New York Times when you visit other sites. For more information about our third-party ad server, or to learn your choices about not having this non-personal information used to target ads to you, please click here.

  - **anthropic/claude-haiku-4.5**: not contradiction — The claim specifically protects email addresses from being sold or shared without permission, while the practice describes sharing non-personally identifiable website usage information for advertising purposes. Since non-personally identifiable information is distinct from personal information like email addresses, the practice does not contradict the claim's commitment to protect email addresses.
  - **openai/gpt-5-mini**: not contradiction — 
  - **google/gemini-3-flash-preview**: not contradiction — The claim specifically promises not to share email addresses with third parties, whereas the practice describes the transmission of non-personally identifiable website usage information for advertising purposes.


The judges correctly note that 'non-PII' is not email — but miss that a company
claiming 'we won't sell your info' while transmitting browsing data to ad networks
is exactly the kind of tension our pipeline should detect.

### Pattern B: Rationalizing Practices as 'Consistent With' Broad Claims

When claims use general language like 'we limit sharing' or 'we protect your data,'
judges rationalize virtually any practice as falling within the claim's scope.

**Affected companies**: Tesla (11/11 dismissed), LinkedIn (1/1 dismissed)

**Example — Tesla** (claim: 'We limit how, and with who, we share your data'):

#### tesla_020_vs_tesla_015
**Company**: tesla (OPPT)
**NLI**: CONTRADICTION (score=0.858)
**Judges**: NOT_CONTRADICTION (unanimous)

**Claim** (tesla_020):
> We may share information with:

- Our service providers, business partners and affiliates
- Third parties you authorize
- Other third parties as required by law

We limit how, and with who, we share your personal data. Examples of when we may share your information include, payment processing, order fulfillment, product installation, customer service, marketing, financing, service or repair, and other similar services.

**We do not sell your personal data to anyone for any purpose, period.** The table below illustrates who Tesla may share your personal data with depending on your interactions ...

**Practice** (tesla_015):
> - To respond to your inquiries and fulfill your requests
- To offer you information on contests, events, and promotions and to administer these activities
- To share administrative information with you, such as changes to our terms, conditions, and policies
- For educational and awareness purposes on topics that interest you
- To advise you of important safety-related information about your vehicle or energy product or to notify first responders in the event of an accident involving your vehicle
- To conduct research, surveys and obtain your feedback

  - **anthropic/claude-haiku-4.5**: not contradiction — The practice describes specific uses of personal data (customer service, safety notifications, research, etc.) that fall within the claim's stated categories of sharing with service providers and for purposes like 'customer service' and 'other similar services.' The practice does not contradict the claim that Tesla does not sell personal data, as these uses represent internal business operations and service delivery rather than data sales.
  - **openai/gpt-5-mini**: not contradiction — Segment B lists purposes for using or sharing data (customer service, marketing/promotions, safety notifications, research) that fall within the categories and examples in Segment A and does not indicate any sale of personal data or sharing that contradicts A's stated limits.
  - **google/gemini-3-flash-preview**: not contradiction — The practice segment outlines specific operational purposes for using and sharing data that align with the service-related examples and legal requirements mentioned in the claim. These activities do not constitute the sale of personal data, which is the primary restriction established in the claim.


The judges note that each individual practice falls within Tesla's listed purposes.
But the aggregate effect — sharing data for customer service, marketing, contests,
events, safety, research, promotions, inquiries, and 'other similar services' — 
contradicts the claim of 'limiting' sharing. The NLI model captures this gestalt tension;
the judges miss it by evaluating each practice in isolation.

### Pattern C: PII vs Non-PII Distinction

Judges dismiss contradictions when the practice involves 'non-personally identifiable'
data, even though the claim makes a broader promise about user information.

**Affected companies**: VoxMedia (2/2 dismissed), TheAtlantic (1 of 2 dismissed)

---

## 5. Judge-Only Contradictions — Are They Genuine?

The judges found 112 contradictions NLI missed. Here we evaluate representative samples.

### united-airlines (8 judge-only contradictions)
*NLI found 0; judges found 8. Children's data protection claim vs general sharing practices.*

#### united-airlines_019_vs_united-airlines_005
**Company**: united-airlines (OPPT)
**NLI**: not flagged (score=0.001)
**Judges**: CONTRADICTION (majority)

**Claim** (united-airlines_019):
> Due to the nature of our services, we collect information about children, including those under the age of 13, when necessary to comply with aviation or security regulations, for safety or security reasons, or as otherwise necessary to provide transportation and other requested services, including the MileagePlus Program. Where required by applicable law, we will obtain consent from a child's parent or guardian to provide a product or service. We will not disclose personal information of a child to third parties unless required by law (such as to comply with a court order or subpoena) or to pr...

**Practice** (united-airlines_005):
> When you enroll and participate in our loyalty program, MileagePlus, we collect information such as your name, contact information, MileagePlus number and security information. We also collect other information that you choose to save in your profile or otherwise provide to us such as payment and purchase information, travel preferences and special requests, marketing preferences, and other loyalty program information.

Personal information collected and processed as part of our MileagePlus program is held by Mileage Plus Intellectual Property Assets, Ltd. ("MIPA"), a member of the United grou...

  - **anthropic/claude-haiku-4.5**: not contradiction — The practice describes how MileagePlus collects and processes personal information, including from children, which aligns with the claim's statement that the company collects information about children 'when necessary to comply with aviation or security regulations' and 'as otherwise necessary to provide transportation and other requested services, including the MileagePlus Program.' The practice does not describe third-party disclosures that would contradict the claim's restriction on such disclosures.
  - **openai/gpt-5-mini**: CONTRADICTION — The claim promises parental consent where required and no disclosure of a child's personal information to third parties except for legal or safety reasons; the practice states MileagePlus data is processed by a separate entity (MIPA) and may be processed on the basis of legitimate interests (e.g., program improvements/marketing) and contractual purposes, which implies sharing/processing without the promised parental-consent/third-party restriction and thus contradicts the claim.
  - **google/gemini-3-flash-preview**: CONTRADICTION — The claim promises that personal information of children will not be disclosed to third parties except for legal or safety reasons, but the practice reveals that MileagePlus data is held and controlled by a separate legal entity in the Cayman Islands (MIPA) for commercial interests.

---

#### united-airlines_019_vs_united-airlines_008
**Company**: united-airlines (OPPT)
**NLI**: not flagged (score=0.000)
**Judges**: CONTRADICTION (unanimous)

**Claim** (united-airlines_019):
> Due to the nature of our services, we collect information about children, including those under the age of 13, when necessary to comply with aviation or security regulations, for safety or security reasons, or as otherwise necessary to provide transportation and other requested services, including the MileagePlus Program. Where required by applicable law, we will obtain consent from a child's parent or guardian to provide a product or service. We will not disclose personal information of a child to third parties unless required by law (such as to comply with a court order or subpoena) or to pr...

**Practice** (united-airlines_008):
> We collect your information to assist you and facilitate your requests regarding United's services, including information you provide to our customer service teams and agents through our call center and chat features. We may use technology, including AI-powered technology for supported chat and call center support to provide, improve, or develop our services, including the chat and call center capabilities and functionalities, so that we can better respond to your and other customers' future interactions. By interacting with United, including our customer service teams and agents, you understa...

  - **anthropic/claude-haiku-4.5**: CONTRADICTION — The claim states that personal information of children will not be disclosed to third parties unless required by law or for safety/security reasons. However, the practice describes sharing information with 'third-party service providers' for recording, monitoring, and training purposes without explicitly limiting this to non-children or obtaining parental consent, which contradicts the claim's strict limitation on third-party disclosure of children's information.
  - **openai/gpt-5-mini**: CONTRADICTION — Segment B states United and third-party service providers will record and use interaction data (including for AI, QA, and training) and treats consent as given by interacting; that constitutes disclosure to third parties and implied consent, which conflicts with Segment A's promise not to disclose a child's personal information to third parties except as required by law or for safety and only with parental consent where required.
  - **google/gemini-3-flash-preview**: CONTRADICTION — The claim promises that United will not disclose a child's personal information to third parties except for legal or safety reasons, but the practice states that all interactions (which would include those involving children's data) are recorded and used by third-party service providers for service enhancement and training.

---

#### united-airlines_019_vs_united-airlines_014
**Company**: united-airlines (OPPT)
**NLI**: not flagged (score=0.001)
**Judges**: CONTRADICTION (unanimous)

**Claim** (united-airlines_019):
> Due to the nature of our services, we collect information about children, including those under the age of 13, when necessary to comply with aviation or security regulations, for safety or security reasons, or as otherwise necessary to provide transportation and other requested services, including the MileagePlus Program. Where required by applicable law, we will obtain consent from a child's parent or guardian to provide a product or service. We will not disclose personal information of a child to third parties unless required by law (such as to comply with a court order or subpoena) or to pr...

**Practice** (united-airlines_014):
> We and our third-party service providers may automatically collect information about you, your device, or your use of our websites and apps through Tracking Technologies. Such information includes, but is not limited to, the following:

- Domain name;
- Browser type and operating system;
- IP address;
- Device ID or alternative ID;
- Geolocation of your device that may be imprecise (i.e., inferred from your device's IP address);
- Precise geolocation location of your device from technologies like GPS, Wi-Fi, or cell tower proximity if enabled by your device settings;
- Motion information from ...

  - **anthropic/claude-haiku-4.5**: CONTRADICTION — The claim states that personal information of children will not be disclosed to third parties unless required by law or for safety/security reasons. However, the practice describes automatic collection and sharing of detailed tracking data (IP address, device ID, geolocation, browsing activity, etc.) with third-party service providers without mentioning parental consent or limiting such disclosure to legal requirements or safety purposes, which directly contradicts the child privacy protection commitment.
  - **openai/gpt-5-mini**: CONTRADICTION — Segment B says the company and its third-party service providers automatically collect and combine extensive tracking data (including precise geolocation), which implies disclosure to third parties; Segment A promises not to disclose a child’s personal information to third parties except in narrow legal or safety circumstances, so the broad third‑party collection in B undermines that commitment.
  - **google/gemini-3-flash-preview**: CONTRADICTION — The claim promises that the company will not disclose a child's personal information to third parties except for legal or safety reasons, but the practice describes the automatic collection and sharing of extensive behavioral and device data with 'third-party service providers' without excluding children's data.

---

*...plus 5 more judge-only contradictions for this company.*

### bumble (4 judge-only contradictions)
*NLI found 0 (previously called 'clean'); judges found 4. Message content non-sharing promise vs third-party service providers.*

#### bumble_017_vs_bumble_026
**Company**: bumble (OPPT)
**NLI**: not flagged (score=0.000)
**Judges**: CONTRADICTION (unanimous)

**Claim** (bumble_017):
> We review the content of messages sent in the App to identify topics, sentiments, and trends across our Users. We will take steps to remove personally identifying information from such messages, prior to reviewing them. We will not share the content of User messages or information we derive from them with any third party.

**Practice** (bumble_026):
> Safety on our App and Sites is very important to us, so we take steps to make sure every person follows our Terms and Conditions of Use while connecting. We use a combination of automated systems and a team of moderators to monitor and review accounts and messages for content that suggests a violation of our Terms and Conditions of Use. This process involves some personal information, such as photos and any other information uploaded to a profile or shared in messages. 
We will issue a warning to the relevant account if any account or message meets the relevant criteria suggesting a likely vio...

  - **anthropic/claude-haiku-4.5**: CONTRADICTION — The claim states that Bumble will 'remove personally identifying information from such messages, prior to reviewing them,' but the practice describes reviewing messages that contain 'personal information, such as photos and any other information uploaded to a profile or shared in messages' without mentioning removal of such identifying information before review. This directly contradicts the commitment to strip personally identifying information before the review process.
  - **openai/gpt-5-mini**: CONTRADICTION — The claim promises personally identifying information will be removed prior to message review, but the practice states moderators and systems review accounts and messages involving personal information such as photos and profile data, which undermines the promise to anonymize before review.
  - **google/gemini-3-flash-preview**: CONTRADICTION — The claim promises that Bumble will remove personally identifying information from messages prior to review, whereas the practice states that the review process for safety violations involves personal information, including photos and message content.

---

#### bumble_017_vs_bumble_034
**Company**: bumble (OPPT)
**NLI**: not flagged (score=0.000)
**Judges**: CONTRADICTION (unanimous)

**Claim** (bumble_017):
> We review the content of messages sent in the App to identify topics, sentiments, and trends across our Users. We will take steps to remove personally identifying information from such messages, prior to reviewing them. We will not share the content of User messages or information we derive from them with any third party.

**Practice** (bumble_034):
> With this in mind and under these restrictions, you should be aware that some of these trusted third parties might also use the personal information they collect for their own purposes. For example, by aggregating your personal information with other data they hold to inform advertising-related services provided to their other clients.

  - **anthropic/claude-haiku-4.5**: CONTRADICTION — The claim explicitly states the company will 'not share the content of User messages or information we derive from them with any third party.' However, the practice describes sharing personal information with trusted third parties who then use it for their own purposes, including aggregating it for advertising services, which directly violates the stated commitment.
  - **openai/gpt-5-mini**: CONTRADICTION — Segment A promises not to share user message content or information derived from them with third parties; Segment B states trusted third parties may use personal information they collect (e.g., aggregating it for advertising), which implies sharing/third‑party use of user data and thus contradicts the promise.
  - **google/gemini-3-flash-preview**: CONTRADICTION — The claim explicitly promises that the company will not share the content of user messages or derived information with any third party, yet the practice admits that trusted third parties collect and use personal information for their own advertising purposes.

---

#### bumble_017_vs_bumble_035
**Company**: bumble (OPPT)
**NLI**: not flagged (score=0.000)
**Judges**: CONTRADICTION (unanimous)

**Claim** (bumble_017):
> We review the content of messages sent in the App to identify topics, sentiments, and trends across our Users. We will take steps to remove personally identifying information from such messages, prior to reviewing them. We will not share the content of User messages or information we derive from them with any third party.

**Practice** (bumble_035):
> We investigate and verify (also known as carrying out due diligence) all of the trusted third parties we work with, or “Service Providers”, to make sure they have adequate data protection and information security measures in place. 

We take steps to make sure the personal information we share is as unidentifiable as possible. 

We hold our Service Providers to extensive contractual requirements, including strict limits on keeping personal information.

  - **anthropic/claude-haiku-4.5**: CONTRADICTION — The claim explicitly states 'We will not share the content of User messages or information we derive from them with any third party,' but the practice describes sharing personal information with Service Providers (third parties), even if de-identified and contractually restricted. The practice of sharing with Service Providers directly contradicts the absolute prohibition on third-party sharing stated in the claim.
  - **openai/gpt-5-mini**: CONTRADICTION — The claim promises they will not share user message content or information derived from messages with any third party; the practice states they share personal information with Service Providers (albeit attempting de-identification) and hold them to contractual limits. That implied sharing of personal/derived data conflicts with the explicit promise not to share such content or information.
  - **google/gemini-3-flash-preview**: CONTRADICTION — The claim explicitly promises that the company will not share the content of user messages or derived information with any third party, but the practice describes sharing personal information with 'Service Providers' (third parties) and merely attempts to make that shared data unidentifiable.

---

*...plus 1 more judge-only contradictions for this company.*

### meta (2 judge-only contradictions)
*NLI found 0 (previously noted Meta 'avoids reassurance language'); judges found 2.*

#### meta_116_vs_meta_095
**Company**: meta (OPPT)
**NLI**: not flagged (score=0.000)
**Judges**: CONTRADICTION (majority)

**Claim** (meta_116):
> We share certain information with: Advertisers who show ads on our Products Businesses we hire to market our Products for us Businesses we hire to do things like offer customer service or conduct surveys Researchers who use it to do things like innovate, advance technology, or improve people’s safety We don’t sell your information, and we never will. We don't sell any of your information to anyone, and we never will. We also require partners [50] and other third parties [51] to follow rules about how they can and cannot use and disclose the information we provide. Here’s more detail about who ...

**Practice** (meta_095):
> We, you and people using our Products can send public content (like your profile photo, or information you share on a Facebook Page or public Instagram account) to anyone on, across or off our Products. For example, users can share it in a public forum, or it can appear in search results on the internet or our research tools Public content can also be seen, accessed, reshared or downloaded through third-party services, like: APIs The media, like TV Other apps and websites connected to our Products Search engines. Learn more [46] Search engines and other third parties use this information accor...

  - **anthropic/claude-haiku-4.5**: not contradiction — The claim describes sharing information with specific partners (advertisers, service providers, researchers) under Meta's rules, while the practice describes how public content can be accessed by third parties through their own terms. These address different scenarios: the claim covers Meta's controlled sharing with partners, while the practice covers user-generated public content that exists outside Meta's direct control, which is a standard distinction in privacy policies.
  - **openai/gpt-5-mini**: CONTRADICTION — Segment A promises Meta requires partners/third parties to follow rules about how information is used and assures it never sells data; Segment B states public content can be accessed and used by search engines and other third parties according to their own terms (not Meta’s), which undermines the claim of enforced use/disclosure restrictions and thus contradicts the stated control/assurance.
  - **google/gemini-3-flash-preview**: CONTRADICTION — The claim promises that Meta requires third parties to follow specific rules on how they use and disclose provided information, but the practice explicitly states that search engines and other third parties use this information according to their own terms and policies, not Meta’s.

---

#### meta_116_vs_meta_103
**Company**: meta (OPPT)
**NLI**: not flagged (score=0.000)
**Judges**: CONTRADICTION (unanimous)

**Claim** (meta_116):
> We share certain information with: Advertisers who show ads on our Products Businesses we hire to market our Products for us Businesses we hire to do things like offer customer service or conduct surveys Researchers who use it to do things like innovate, advance technology, or improve people’s safety We don’t sell your information, and we never will. We don't sell any of your information to anyone, and we never will. We also require partners [50] and other third parties [51] to follow rules about how they can and cannot use and disclose the information we provide. Here’s more detail about who ...

**Practice** (meta_103):
> Integrated partners handle the information you share with them according to their own terms and policies, not Meta’s. You can review their privacy policy on their website or app to learn how they receive and process your information. In some cases, they use a separate service provider to receive and process your information.

  - **anthropic/claude-haiku-4.5**: CONTRADICTION — The claim states Meta requires partners to follow rules about how they can use and disclose information, implying Meta's oversight and control. However, the practice reveals that integrated partners handle information according to their own terms and policies, not Meta's, and may use separate service providers—directly contradicting the claim of enforced partner restrictions.
  - **openai/gpt-5-mini**: CONTRADICTION — The claim promises Meta won’t sell data and requires partners to follow rules about use/disclosure; the practice states integrated partners handle shared data under their own policies (not Meta’s), implying Meta does not control or constrain partners’ use/disclosure and so undermines the commitments.
  - **google/gemini-3-flash-preview**: CONTRADICTION — The claim promises that Meta requires third parties to follow specific rules regarding the use and disclosure of shared information, but the practice states that integrated partners handle information according to their own terms and policies rather than Meta's.

---


### reddit.com (11 judge-only contradictions)
*NLI found 2; judges found 11. 'Private info never for sale' vs broad collection practices.*

#### reddit.com_004_vs_reddit.com_006
**Company**: reddit.com (OPP-115)
**NLI**: not flagged (score=0.000)
**Judges**: CONTRADICTION (majority)

**Claim** (reddit.com_004):
> about this policy reddit is an open platform that allows you to communicate about anything you want on any topic you want. We collect some information in order for you to have an account you can use to participate on the site, and other information that is necessary to make the service work. Our goal in developing our privacy practices is to allow your participation to remain as anonymous as you choose, and we dont sell or profit from the information you share with us.

**Practice** (reddit.com_006):
> what information we collect registration information When you create an account, you are required to provide a username and password, and may opt to provide an email address. We also log, and retain indefinitely, the IP address from which the account is initially created.

  - **anthropic/claude-haiku-4.5**: not contradiction — The practice describes specific registration information collected (username, password, optional email, and IP address), which directly supports the claim that Reddit collects information necessary for account creation and service operation. The practice does not contradict the claim's commitment to anonymity or non-sale of data.
  - **openai/gpt-5-mini**: CONTRADICTION — The claim promises participation can remain as anonymous as you choose, but the practice states the account-creation IP address is logged and retained indefinitely—an immutable identifier that can deanonymize users and thus undermines that anonymity commitment.
  - **google/gemini-3-flash-preview**: CONTRADICTION — The claim promises to allow participation to remain as anonymous as the user chooses, but the practice reveals that Reddit logs and retains the user's IP address indefinitely, which is a persistent identifier that can compromise anonymity regardless of the user's choices.

---

#### reddit.com_004_vs_reddit.com_008
**Company**: reddit.com (OPP-115)
**NLI**: not flagged (score=0.000)
**Judges**: CONTRADICTION (majority)

**Claim** (reddit.com_004):
> about this policy reddit is an open platform that allows you to communicate about anything you want on any topic you want. We collect some information in order for you to have an account you can use to participate on the site, and other information that is necessary to make the service work. Our goal in developing our privacy practices is to allow your participation to remain as anonymous as you choose, and we dont sell or profit from the information you share with us.

**Practice** (reddit.com_008):
> Your messages are generally only viewable by the parties involved, but they may be accessed internally as needed for community support. Moreover, we keep a complete log of all messages sent on our service, even when both parties later delete their accounts.

  - **anthropic/claude-haiku-4.5**: not contradiction — The claim states Reddit collects information necessary to make the service work and doesn't sell or profit from shared information. The practice describes internal message access for community support and message logging, which are operational necessities that support the service functionality and don't contradict the commitment against selling or profiting from user data.
  - **openai/gpt-5-mini**: CONTRADICTION — Segment B's retention of complete message logs and internal access even after account deletion undermines the Claim's reassurance that your participation can remain as anonymous as you choose (and that deletion preserves anonymity), so the practice contradicts the promise.
  - **google/gemini-3-flash-preview**: CONTRADICTION — The claim promises to allow participation to remain as anonymous as the user chooses, but the practice of keeping a complete, permanent log of all messages even after account deletion undermines that control and anonymity.

---

#### reddit.com_004_vs_reddit.com_019
**Company**: reddit.com (OPP-115)
**NLI**: not flagged (score=0.001)
**Judges**: CONTRADICTION (majority)

**Claim** (reddit.com_004):
> about this policy reddit is an open platform that allows you to communicate about anything you want on any topic you want. We collect some information in order for you to have an account you can use to participate on the site, and other information that is necessary to make the service work. Our goal in developing our privacy practices is to allow your participation to remain as anonymous as you choose, and we dont sell or profit from the information you share with us.

**Practice** (reddit.com_019):
> cookie policy technologies we use Cookies are small data files placed on your computer by websites you visit in order to help them remember certain information about you. At reddit, we set only a few cookies for tracking user preferences, authentication, and collecting anonymous analytics data. Additionally, our advertising partners set cookies. We also use pixel trackers, which are images embedded in a webpage, for the purpose of measuring and analyzing usage and activity. Each of these uses is described in greater detail below.

  - **anthropic/claude-haiku-4.5**: not contradiction — The practice describes technical implementations (cookies and pixel trackers) used to support the service functionality and analytics mentioned in the claim. The claim states Reddit collects information 'necessary to make the service work,' and the practice explains how cookies enable authentication, preferences, and analytics—which are standard technical measures that support the claimed service operation without contradicting the commitment about not selling user information.
  - **openai/gpt-5-mini**: CONTRADICTION — The claim promises Reddit does not "sell or profit from the information you share," yet the practice states advertising partners set cookies and pixel trackers collect usage data—indicating third-party advertising tracking and monetization of user information, which undermines that promise.
  - **google/gemini-3-flash-preview**: CONTRADICTION — The claim states that Reddit does not 'profit from the information you share,' but the practice reveals the use of advertising partners and tracking pixels, which are standard tools for generating advertising revenue and profiting from user data.

---

*...plus 8 more judge-only contradictions for this company.*

### archives.gov (6 judge-only contradictions)
*Government site. NLI found 0; judges found 6.*

#### archives.gov_003_vs_archives.gov_008
**Company**: archives.gov (OPP-115)
**NLI**: not flagged (score=0.000)
**Judges**: CONTRADICTION (unanimous)

**Claim** (archives.gov_003):
> If you provide us information about yourself via e-mail or a web form, your information will be used only for the purposes described at the point of collection, such as to send information or products to you, or to respond to your questions or comments. If you provide contact information, National Archives staff or its contractors may contact you to clarify your comment or question, or to learn about your level of customer satisfaction with our services. We do not sell any personal information to third parties. We may transfer personal information to a third party only in the following cases: ...

**Practice** (archives.gov_008):
> We will not use cookies to collect personally identifiable information about visitors. We will not share any information we collect with anyone outside of the National Archives. The usage of cookies in this way is considered a "Tier 2" under the Office of Management and Budget's Memorandum 10-22, Guidance for Online Use of Web Measurement and Customization Technologies. If you wish to disable cookies and opt out of this process, you can find opt-out instructions on usa.gov. Disabling cookies will not restrict your access to the core content of the website.

  - **anthropic/claude-haiku-4.5**: CONTRADICTION — The claim explicitly states that personal information may be transferred to contractors, legal authorities, Congress, courts, and the Foundation for the National Archives. However, the practice states 'We will not share any information we collect with anyone outside of the National Archives,' which directly contradicts the claim's enumerated list of third parties who may receive personal information.
  - **openai/gpt-5-mini**: CONTRADICTION — Segment A explicitly permits transferring personal information to outside parties (banks/treasury, contractors, the Foundation, legal authorities, Congress/courts) while Segment B states a blanket policy of not sharing any information with anyone outside the National Archives, which directly conflicts with those stated exceptions.
  - **google/gemini-3-flash-preview**: CONTRADICTION — Segment A explicitly lists several scenarios where information is shared with third parties (banks, contractors, the Foundation for the National Archives, and legal authorities), whereas Segment B makes an absolute claim that they will not share any collected information with anyone outside of the National Archives.

---

#### archives.gov_003_vs_archives.gov_022
**Company**: archives.gov (OPP-115)
**NLI**: not flagged (score=0.001)
**Judges**: CONTRADICTION (unanimous)

**Claim** (archives.gov_003):
> If you provide us information about yourself via e-mail or a web form, your information will be used only for the purposes described at the point of collection, such as to send information or products to you, or to respond to your questions or comments. If you provide contact information, National Archives staff or its contractors may contact you to clarify your comment or question, or to learn about your level of customer satisfaction with our services. We do not sell any personal information to third parties. We may transfer personal information to a third party only in the following cases: ...

**Practice** (archives.gov_022):
> This information is primarily collected for statistical analysis and technical improvements to the site. The National Archives uses software programs to create summary statistics, which may be used for such purposes as assessing what information is of most and least interest, determining technical design specifications, and identifying system performance or problem areas. In certain circumstances, however, we may take additional steps to identify you based on this information and we may share this information, including your identity, with other government agencies. The information we collect ...

  - **anthropic/claude-haiku-4.5**: CONTRADICTION — The claim states personal information will be used only for purposes described at collection and may be transferred to third parties only in specific enumerated cases, but the practice discloses that the National Archives may share information, including identity, with other government agencies in certain circumstances without mentioning this as one of the permitted transfer cases in the claim.
  - **openai/gpt-5-mini**: CONTRADICTION — Segment A limits use to purposes described at point of collection and lists specific, narrow transfer cases; Segment B states data may be used for statistical/technical purposes, could be used to identify you and shared with other government agencies and retained indefinitely—uses/transfers not covered by A, undermining the promised restrictions.
  - **google/gemini-3-flash-preview**: CONTRADICTION — The claim promises that information will be used 'only for the purposes described at the point of collection,' yet the practice reveals that the agency may take additional steps to identify individuals and share their identity with other government agencies for broader purposes like statistical analysis or permanent retention.

---

#### archives.gov_008_vs_archives.gov_003
**Company**: archives.gov (OPP-115)
**NLI**: not flagged (score=0.000)
**Judges**: CONTRADICTION (unanimous)

**Claim** (archives.gov_008):
> We will not use cookies to collect personally identifiable information about visitors. We will not share any information we collect with anyone outside of the National Archives. The usage of cookies in this way is considered a "Tier 2" under the Office of Management and Budget's Memorandum 10-22, Guidance for Online Use of Web Measurement and Customization Technologies. If you wish to disable cookies and opt out of this process, you can find opt-out instructions on usa.gov. Disabling cookies will not restrict your access to the core content of the website.

**Practice** (archives.gov_003):
> If you provide us information about yourself via e-mail or a web form, your information will be used only for the purposes described at the point of collection, such as to send information or products to you, or to respond to your questions or comments. If you provide contact information, National Archives staff or its contractors may contact you to clarify your comment or question, or to learn about your level of customer satisfaction with our services. We do not sell any personal information to third parties. We may transfer personal information to a third party only in the following cases: ...

  - **anthropic/claude-haiku-4.5**: CONTRADICTION — The claim states 'We will not share any information we collect with anyone outside of the National Archives,' but the practice describes multiple instances of sharing personal information outside the National Archives, including to contractors, the Treasury Department, the Foundation for the National Archives, Congress, and courts. These external disclosures directly contradict the absolute promise of no outside sharing.
  - **openai/gpt-5-mini**: CONTRADICTION — Segment A promises no sharing of collected information with anyone outside the National Archives, but Segment B explicitly allows transfers to external parties (banks/Treasury, contractors, the Foundation, legal authorities, Congress/courts), which contradicts that commitment.
  - **google/gemini-3-flash-preview**: CONTRADICTION — The claim explicitly states the agency will not share any collected information with anyone outside of the National Archives, but the practice lists several third parties—including contractors, the Department of the Treasury, and a non-governmental foundation—with whom they may share personal information.

---

*...plus 3 more judge-only contradictions for this company.*

### kraftrecipes.com (6 judge-only contradictions)
*NLI found 1 (FP); judges found 6 new ones.*

#### kraftrecipes.com_019_vs_kraftrecipes.com_015
**Company**: kraftrecipes.com (OPP-115)
**NLI**: not flagged (score=0.000)
**Judges**: CONTRADICTION (unanimous)

**Claim** (kraftrecipes.com_019):
> How We Share Your Information We do not sell or otherwise disclose personally identifiable information about our website visitors, except as described here. We do not share your personally identifiable information with unaffiliated third parties for their own marketing purposes without your consent. For California residents, please see "Your California Privacy Rights" below.

**Practice** (kraftrecipes.com_015):
> | We also may use third party advertisements placed by ad networks to support our site. Some of these advertisers and ad networks may use technology such as cookies and web beacons/pixel tags when they advertise on our site, which will also send these advertisers and ad networks information including your IP address, ISP, browser type, and whether you have Flash installed. Some of these advertisers and ad networks also may use anonymous data, such as demographic data, received from third parties to assist in the delivery of advertisements to you. These third-party advertisers and ad networks u...

  - **anthropic/claude-haiku-4.5**: CONTRADICTION — The claim states the company does not share personally identifiable information with unaffiliated third parties for their own marketing purposes without consent. However, the practice describes sharing IP address, ISP, browser type, and behavioral/demographic data with third-party ad networks and advertisers for targeted advertising purposes, with no mention of obtaining prior consent for this sharing.
  - **openai/gpt-5-mini**: CONTRADICTION — The claim promises not to share personally identifiable information with unaffiliated third parties for their own marketing without your consent; the practice states ad networks receive identifying data (e.g., IP address, ISP, browser) and use it to deliver targeted advertisements, which constitutes sharing PII for marketing purposes without indicating consent.
  - **google/gemini-3-flash-preview**: CONTRADICTION — The claim promises not to share personally identifiable information with third parties for their own marketing without consent, but the practice describes allowing ad networks to collect IP addresses and behavioral data to serve targeted advertisements.

---

#### kraftrecipes.com_019_vs_kraftrecipes.com_018
**Company**: kraftrecipes.com (OPP-115)
**NLI**: not flagged (score=0.000)
**Judges**: CONTRADICTION (unanimous)

**Claim** (kraftrecipes.com_019):
> How We Share Your Information We do not sell or otherwise disclose personally identifiable information about our website visitors, except as described here. We do not share your personally identifiable information with unaffiliated third parties for their own marketing purposes without your consent. For California residents, please see "Your California Privacy Rights" below.

**Practice** (kraftrecipes.com_018):
> How We Use Your Information We may use the information we collect from and about you to contact you from time to time. For example, we may send you promotional offers, materials, and other communications and information about Kraft, its portfolio of brands and its partners. You may receive these offers in advertising that is directed to you via third party sites and media platforms, including in social media. We may respond to your comments or questions, or contact you if needed while processing a product or service you requested through our website. We also may use the information you provide...

  - **anthropic/claude-haiku-4.5**: CONTRADICTION — The claim states the company does not share personally identifiable information with unaffiliated third parties for their own marketing purposes without consent. However, the practice describes sending promotional offers and advertising directed to users via third-party sites and media platforms, including social media, which implies sharing user information with these unaffiliated third parties for marketing purposes without explicitly requiring prior consent.
  - **openai/gpt-5-mini**: CONTRADICTION — Segment A promises not to share personally identifiable information with unaffiliated third parties for their own marketing without consent; Segment B states users may receive promotional offers via partners and third-party sites/platforms (and about its partners), implying sharing or use of data by third parties for marketing without an explicit consent requirement, which undermines the claim.
  - **google/gemini-3-flash-preview**: CONTRADICTION — The claim promises not to share personally identifiable information with unaffiliated third parties for their marketing purposes without consent, but the practice describes sending promotional materials from 'partners' and delivering targeted advertising via third-party sites and social media platforms.

---

#### kraftrecipes.com_019_vs_kraftrecipes.com_021
**Company**: kraftrecipes.com (OPP-115)
**NLI**: not flagged (score=0.000)
**Judges**: CONTRADICTION (unanimous)

**Claim** (kraftrecipes.com_019):
> How We Share Your Information We do not sell or otherwise disclose personally identifiable information about our website visitors, except as described here. We do not share your personally identifiable information with unaffiliated third parties for their own marketing purposes without your consent. For California residents, please see "Your California Privacy Rights" below.

**Practice** (kraftrecipes.com_021):
> We may share your email address with a third-party, such as a media agency, to send you interest-based advertising on our behalf. We may also share aggregated or de-identified information about you, including based on your email address, with our advertising and marketing partners, and third-party media platforms, including social media sites, to allow them to send targeted advertising messages and/or conduct analyses on our behalf. If you wish to stop receiving advertising messages from these third parties, please review the "Your Choices" section below. In addition, you may be able to opt ou...

  - **anthropic/claude-haiku-4.5**: CONTRADICTION — The claim states the company does not share personally identifiable information with unaffiliated third parties for their own marketing purposes without consent. However, the practice describes sharing email addresses (personally identifiable information) with media agencies and advertising partners for interest-based advertising and targeted messaging without explicitly requiring prior consent—only offering an opt-out mechanism after the fact.
  - **openai/gpt-5-mini**: CONTRADICTION — The claim promises not to share personally identifiable information with unaffiliated third parties for their own marketing without your consent, yet the practice states they may share email addresses with media agencies and advertising/marketing partners to send targeted, interest-based ads and only provides opt-out mechanisms, implying sharing occurs without prior consent.
  - **google/gemini-3-flash-preview**: CONTRADICTION — The claim promises not to share personally identifiable information with unaffiliated third parties for marketing without consent, but the practice describes sharing email addresses with media agencies and social media platforms for targeted advertising and provides an opt-out mechanism rather than requiring prior consent.

---

*...plus 3 more judge-only contradictions for this company.*

## 6. Both Methods Agree: Contradiction (Highest Confidence)

*14 pairs where both NLI and judges agree.*

#### jasper_034_vs_jasper_037
**Company**: jasper (OPPT)
**NLI**: CONTRADICTION (score=0.930)
**Judges**: CONTRADICTION (unanimous)

**Claim** (jasper_034):
> We do not sell the personal information of Consumers We actually know are less than 16 years of age, unless We receive affirmative authorization (the

**Practice** (jasper_037):
> You have the right to opt-out of the sale of Your personal information. Once We receive and confirm a verifiable consumer request from You, we will stop selling Your personal information. To exercise Your right to opt-out, please contact Us.
The Service Providers we partner with (for example, our analytics or advertising partners) may use technology on the Service that sells personal information as defined by the CCPA law. If you wish to opt out of the use of Your personal information for interest-based advertising purposes and these potential sales as defined under CCPA law, you may do so by ...

  - **anthropic/claude-haiku-4.5**: CONTRADICTION — The claim states the company does not sell personal information of consumers under 16 unless they receive affirmative authorization, implying sales are not the default. However, the practice describes an opt-out mechanism for the sale of personal information and mentions that Service Providers 'may use technology on the Service that sells personal information,' indicating that sales occur by default and require active opt-out rather than affirmative authorization.
  - **openai/gpt-5-mini**: CONTRADICTION — Segment A promises not to sell personal information of consumers known to be under 16 without affirmative authorization; Segment B states the service/providers may sell personal information and offers a broad opt-out mechanism, which implies sales may occur and undermines the categorical no-sale reassurance for minors.
  - **google/gemini-3-flash-preview**: CONTRADICTION — The claim implies that the company generally avoids selling data of minors, but the practice reveals that the company and its partners do engage in the sale of personal information by default, requiring an opt-out mechanism to stop it.

---

#### venmo_037_vs_venmo_039
**Company**: venmo (OPPT)
**NLI**: CONTRADICTION (score=0.693)
**Judges**: CONTRADICTION (majority)

**Claim** (venmo_037):
> 2. The categories of third parties to which we (a) disclose such personal information for a business purpose, (b) "share" personal information for "cross-context behavioral advertising," and/or (c) "sell" such personal information.

Under California law, "sharing" is defined as the targeting of advertising to a consumer based on that consumer's personal information obtained from the consumer's activity across websites, and "selling" is defined as the disclosure of personal information to third parties in exchange for monetary or other valuable consideration.

**We do not sell or share your Per...

**Practice** (venmo_039):
> | Category | Sources | Purposes | Third Parties Disclosed To |
|----------|---------|----------|---------------------------|
| **A. Identifiers** (real name, alias, telephone number, postal address, unique personal identifier, online identifier, IP address, email address, account name, SSN, driver's license number, passport number) | From you when you use our Services; partners and merchants; service providers; financial institutions; social networks (with consent); advertising networks | Provide Services and customer support; process and match transactions; resolve disputes; prevent fraud; cr...

  - **anthropic/claude-haiku-4.5**: CONTRADICTION — The claim explicitly states 'We do not sell or share your Personal Information,' but the practice table discloses personal information to numerous third parties (PayPal affiliates, service providers, financial institutions, partners, merchants, third-party platforms) for purposes including 'customize and improve services' and 'create account connections,' which constitutes sharing under California law's definition of targeting based on personal information obtained from consumer activity.
  - **openai/gpt-5-mini**: CONTRADICTION — Segment B lists broad disclosures of personal information to numerous third parties (service providers, affiliates, advertising networks, partners/merchants, etc.) and even uses data for advertising/offers, which directly contradicts Segment A's categorical statement that "We do not sell or share your Personal Information."
  - **google/gemini-3-flash-preview**: not contradiction — The claim specifically defines 'sell' and 'share' according to California legal standards (monetary exchange or cross-context behavioral advertising), while the practice table describes disclosing data to third parties for 'business purposes' such as fraud prevention and service provision, which is explicitly permitted under those definitions.

---

#### taylorswift.com_023_vs_taylorswift.com_017
**Company**: taylorswift.com (OPP-115)
**NLI**: CONTRADICTION (score=0.997)
**Judges**: CONTRADICTION (unanimous)

**Claim** (taylorswift.com_023):
> We will not share your information with third parties for the purposes of their direct marketing unless you affirmatively agree to such disclosure.

**Practice** (taylorswift.com_017):
> We may disclose your personally-identifiable information with our employees, agents, contractors and sub-contractors, and our related and affiliated entities, including, but not limited to, 13 Management, LLC, Firefly Entertainment, Inc., Swift Merchandising, Inc., and Taylor Swift Productions, Inc., and their respective employees, agents, contractors and sub-contractors, for the limited purpose of enabling them to communicate with you directly about upcoming events and promotions.

  - **anthropic/claude-haiku-4.5**: CONTRADICTION — The claim promises no third-party sharing for direct marketing without affirmative agreement, but the practice discloses that the company may share personally-identifiable information with multiple affiliated entities and their contractors specifically 'for the limited purpose of enabling them to communicate with you directly about upcoming events and promotions'—which is direct marketing—with no mention of requiring prior affirmative consent.
  - **openai/gpt-5-mini**: CONTRADICTION — The claim promises not to share information with third parties for their direct marketing unless the user affirmatively agrees, but the practice states the company may disclose PII to agents, contractors and affiliates so they can contact users about events and promotions, which is third-party direct marketing without stating required affirmative consent.
  - **google/gemini-3-flash-preview**: CONTRADICTION — The claim promises not to share information with third parties for direct marketing without affirmative consent, but the practice describes sharing data with various affiliated entities specifically for the purpose of direct communication about promotions without mentioning a consent requirement.

---

#### taylorswift.com_023_vs_taylorswift.com_018
**Company**: taylorswift.com (OPP-115)
**NLI**: CONTRADICTION (score=0.955)
**Judges**: CONTRADICTION (majority)

**Claim** (taylorswift.com_023):
> We will not share your information with third parties for the purposes of their direct marketing unless you affirmatively agree to such disclosure.

**Practice** (taylorswift.com_018):
> We will share your personally-identifiable information with other parties under the following circumstances:

  - **anthropic/claude-haiku-4.5**: CONTRADICTION — The claim promises no third-party sharing for direct marketing without affirmative agreement, but the practice states information will be shared with other parties under unspecified circumstances, which could include direct marketing purposes without explicit consent requirements being mentioned.
  - **openai/gpt-5-mini**: not contradiction — Segment B only states that personal information may be shared under certain circumstances but does not assert sharing for third‑party direct marketing without consent; it therefore does not directly contradict the commitment not to share for direct marketing absent affirmative agreement.
  - **google/gemini-3-flash-preview**: CONTRADICTION — The claim promises that information will not be shared with third parties for marketing without affirmative consent, but the practice segment introduces broad circumstances for sharing personally-identifiable information without mentioning any consent requirement.

---

#### latinpost.com_057_vs_latinpost.com_003
**Company**: latinpost.com (OPP-115)
**NLI**: CONTRADICTION (score=0.980)
**Judges**: CONTRADICTION (majority)

**Claim** (latinpost.com_057):
> d. Use of Information. Latin Post will not use a wireless telephone number, wireless or conventional Internet email address, or other Information submitted for its wireless marketing services for any other purpose but to provide the service requested, unless we provide advance notice of any other use. We will not share any Personal Information with Advertisers or other third party marketers unless you opt-in to such disclosure. We will share Personal Information with the operational service providers that assist us in delivering these wireless services to you and with the Parent Companies and ...

**Practice** (latinpost.com_003):
> 1. When This Privacy Policy Applies. This Privacy Policy applies whether you are accessing the Site via a personal computer, a mobile device or any other technology or devices now known or hereafter developed or discovered (each, a "Device") and whether you are accessing the Site as a registered user (if offered by the Site) or other user of the Site. This Privacy Policy governs only the Personal Information and Other Information (as those terms are defined below) collected by the Site and does not cover any such information collected in any other manner, the Parent Companies and/or any subsid...

  - **anthropic/claude-haiku-4.5**: CONTRADICTION — The Claim states that Personal Information will not be shared with Advertisers unless the user opts-in, but the Practice describes combining Information with data received from Advertisers and then using that combined Information subject to the privacy policy, which does not explicitly require opt-in consent for such combinations or uses.
  - **openai/gpt-5-mini**: not contradiction — Segment B does not state that the company shares users' Personal Information with Advertisers or third‑party marketers; it only says the Site may combine its own data with information received from sources (including Advertisers). Segment A expressly prohibits sharing with Advertisers without opt‑in and permits sharing with service providers and Affiliates, so B does not contradict A.
  - **google/gemini-3-flash-preview**: CONTRADICTION — The claim promises that personal information will not be shared with advertisers or third-party marketers without an opt-in, but the practice reveals that the company actively receives and combines user data with information from those same marketing companies and advertisers.

---

#### latinpost.com_057_vs_latinpost.com_015
**Company**: latinpost.com (OPP-115)
**NLI**: CONTRADICTION (score=0.975)
**Judges**: CONTRADICTION (majority)

**Claim** (latinpost.com_057):
> d. Use of Information. Latin Post will not use a wireless telephone number, wireless or conventional Internet email address, or other Information submitted for its wireless marketing services for any other purpose but to provide the service requested, unless we provide advance notice of any other use. We will not share any Personal Information with Advertisers or other third party marketers unless you opt-in to such disclosure. We will share Personal Information with the operational service providers that assist us in delivering these wireless services to you and with the Parent Companies and ...

**Practice** (latinpost.com_015):
> These Third Party Advertising Service Providers do not have access to Tracking Technologies set by the Site except to the extent necessary to provide services to the Site. The Third Party Advertising Service Providers, as well as Advertisers, may themselves set and access their own Tracking Technologies on your Device if you choose to have Tracking Technologies enabled in your browser (or, for Flash cookies, if you have not removed them) and/or they may otherwise have access to Other Information about you.

  - **anthropic/claude-haiku-4.5**: CONTRADICTION — The claim states that Personal Information will not be shared with Advertisers unless you opt-in, but the practice describes Third Party Advertising Service Providers and Advertisers setting and accessing Tracking Technologies on your device based on browser settings rather than explicit opt-in consent. This represents a sharing/access mechanism that operates independently of the opt-in requirement promised in the claim.
  - **openai/gpt-5-mini**: not contradiction — Segment B describes third-party advertisers setting and accessing their own tracking technologies (subject to the user enabling tracking) and possibly obtaining other information independently; it does not state that Latin Post shares users' Personal Information with advertisers without opt-in, so it does not contradict the promise in Segment A.
  - **google/gemini-3-flash-preview**: CONTRADICTION — The claim promises that personal information will not be shared with advertisers without an opt-in, but the practice reveals that advertisers may set tracking technologies and access information about the user if browser settings allow it, bypassing the promised opt-in requirement.

---

#### latinpost.com_057_vs_latinpost.com_017
**Company**: latinpost.com (OPP-115)
**NLI**: CONTRADICTION (score=0.967)
**Judges**: CONTRADICTION (majority)

**Claim** (latinpost.com_057):
> d. Use of Information. Latin Post will not use a wireless telephone number, wireless or conventional Internet email address, or other Information submitted for its wireless marketing services for any other purpose but to provide the service requested, unless we provide advance notice of any other use. We will not share any Personal Information with Advertisers or other third party marketers unless you opt-in to such disclosure. We will share Personal Information with the operational service providers that assist us in delivering these wireless services to you and with the Parent Companies and ...

**Practice** (latinpost.com_017):
> i. Personal Information. We, and/or our Parent Companies and Affiliates, use the Personal Information we collect from you in a variety of ways, including:

  - **anthropic/claude-haiku-4.5**: not contradiction — The practice describes how Personal Information is used by the company and its Parent Companies and Affiliates, which is explicitly permitted in the claim. The claim allows sharing with Parent Companies and Affiliates, and the practice's statement that they use collected information is consistent with this authorization.
  - **openai/gpt-5-mini**: CONTRADICTION — The claim limits use of wireless numbers/emails to providing the requested service and forbids sharing with advertisers absent opt-in (only allowing operational providers and affiliates for delivery), while the practice says Parent Companies/Affiliates use personal information 'in a variety of ways,' implying broader uses beyond the promised service and opt-in restrictions, which undermines the commitment.
  - **google/gemini-3-flash-preview**: CONTRADICTION — The claim promises that personal information will not be used for any purpose other than providing the requested service, but the practice states that the information is used in a 'variety of ways' without limiting those uses to the specific service requested.

---

#### latinpost.com_057_vs_latinpost.com_018
**Company**: latinpost.com (OPP-115)
**NLI**: CONTRADICTION (score=0.975)
**Judges**: CONTRADICTION (unanimous)

**Claim** (latinpost.com_057):
> d. Use of Information. Latin Post will not use a wireless telephone number, wireless or conventional Internet email address, or other Information submitted for its wireless marketing services for any other purpose but to provide the service requested, unless we provide advance notice of any other use. We will not share any Personal Information with Advertisers or other third party marketers unless you opt-in to such disclosure. We will share Personal Information with the operational service providers that assist us in delivering these wireless services to you and with the Parent Companies and ...

**Practice** (latinpost.com_018):
> Sending marketing and promotional e-mails or, subject to the "Wireless Marketing Services and Associated Promotional Opportunities" Section below, text messages offering the purchase of goods and/or services that may be of interest to users, whether those goods and/or services are provided by the Site, the Parent Companies, Affiliates or third parties (for example, we may send you an email about a product sold by a third party);

  - **anthropic/claude-haiku-4.5**: CONTRADICTION — The claim states that personal information will not be shared with third-party marketers unless users opt-in, but the practice describes sending marketing emails about products sold by third parties without explicitly requiring prior opt-in consent. This suggests third-party marketing communications occur as a default practice rather than only upon user opt-in.
  - **openai/gpt-5-mini**: CONTRADICTION — Segment A promises not to use wireless numbers/email for purposes other than the requested service (or share with third-party marketers without opt-in), while Segment B states the company will send marketing/promotional emails and texts (including about third-party products) — an additional use/share that contradicts A absent advance notice or opt-in.
  - **google/gemini-3-flash-preview**: CONTRADICTION — The claim promises that information submitted for wireless services will not be used for any purpose other than the requested service, yet the practice describes using that information to send marketing emails and text messages for third-party goods and services.

---

#### latinpost.com_057_vs_latinpost.com_029
**Company**: latinpost.com (OPP-115)
**NLI**: CONTRADICTION (score=0.993)
**Judges**: CONTRADICTION (majority)

**Claim** (latinpost.com_057):
> d. Use of Information. Latin Post will not use a wireless telephone number, wireless or conventional Internet email address, or other Information submitted for its wireless marketing services for any other purpose but to provide the service requested, unless we provide advance notice of any other use. We will not share any Personal Information with Advertisers or other third party marketers unless you opt-in to such disclosure. We will share Personal Information with the operational service providers that assist us in delivering these wireless services to you and with the Parent Companies and ...

**Practice** (latinpost.com_029):
> ii. Other Information Collected by Us. We, and/or our Parent Companies and Affiliates, use the Other Information we collect from you in a variety of ways, including: Keeping count of your return visits to the Site or our Parent Companies', Affiliates', Advertisers' or partners' sites; Accumulating and reporting aggregate, statistical information in connection with the Site and user activity; Determining which features, webpages, products and services users like best to, among other things, help us operate the Site, enhance and improve our services and the Site and display advertising and marke...

  - **anthropic/claude-haiku-4.5**: not contradiction — The claim addresses sharing of Personal Information with Advertisers and third-party marketers (requiring opt-in) and operational service providers/affiliates. The practice describes uses of 'Other Information' (non-personal data like aggregate statistics, visit counts, and usage patterns) for site improvement and analytics, which does not contradict the Personal Information sharing restrictions stated in the claim.
  - **openai/gpt-5-mini**: CONTRADICTION — Segment A promises that information submitted for wireless marketing will only be used to provide the requested service and will not be shared with advertisers without opt-in; Segment B says Other Information is used to display advertising, track visits across advertisers/partners, and tailor marketing — uses beyond the stated service and implying advertiser-facing use, which contradicts the commitment.
  - **google/gemini-3-flash-preview**: CONTRADICTION — The claim promises that information will not be used for any purpose other than the requested service without advance notice, yet the practice describes using collected information for a wide range of secondary purposes including displaying advertising, tailoring user experience, and internal business purposes.

---

#### latinpost.com_057_vs_latinpost.com_036
**Company**: latinpost.com (OPP-115)
**NLI**: CONTRADICTION (score=0.963)
**Judges**: CONTRADICTION (majority)

**Claim** (latinpost.com_057):
> d. Use of Information. Latin Post will not use a wireless telephone number, wireless or conventional Internet email address, or other Information submitted for its wireless marketing services for any other purpose but to provide the service requested, unless we provide advance notice of any other use. We will not share any Personal Information with Advertisers or other third party marketers unless you opt-in to such disclosure. We will share Personal Information with the operational service providers that assist us in delivering these wireless services to you and with the Parent Companies and ...

**Practice** (latinpost.com_036):
> Third Party Advertising Service Providers and Advertisers may collect Other Information about you when you visit this Site to help identify products and services that may interest you and deliver advertising tailored to your interests.

  - **anthropic/claude-haiku-4.5**: CONTRADICTION — The claim states that Personal Information will not be shared with Advertisers unless the user opts-in, but the practice describes Third Party Advertising Service Providers and Advertisers collecting information about users to deliver targeted advertising, which implies data sharing without explicit mention of opt-in consent requirements.
  - **openai/gpt-5-mini**: not contradiction — The claim limits sharing of Personal Information (e.g., wireless numbers, emails) with advertisers absent opt‑in, while the practice states that advertisers may collect Other Information during site visits; since the policy distinguishes Personal Information from Other Information and the practice does not say Personal Information is shared, it does not directly contradict the promise.
  - **google/gemini-3-flash-preview**: CONTRADICTION — The claim promises that personal information will not be shared with advertisers without an opt-in, but the practice reveals that third-party advertisers are permitted to collect information about the user directly on the site for targeted advertising.

---

#### theatlantic.com_016_vs_theatlantic.com_031
**Company**: theatlantic.com (OPP-115)
**NLI**: CONTRADICTION (score=0.971)
**Judges**: CONTRADICTION (majority)

**Claim** (theatlantic.com_016):
> Who Can See Your Information? We will not disclose your personally identifiable information collected from the Sites to any organizations not part of The Atlantic or its subsidiaries or related entities, except as described in this privacy policy.

**Practice** (theatlantic.com_031):
> Contests, Sweepstakes or Games When we run a contest or sweepstakes or game relating to our Sites, it will be accompanied by a set of rules. The rules for each contest, sweepstakes or game will specify how the information gathered from you for entry will be used and disclosed if it is different than as described in this privacy policy. In conjunction with your entry in such contest or sweepstakes, personally identifiable information will be collected only if you voluntarily submit it.

  - **anthropic/claude-haiku-4.5**: CONTRADICTION — The claim promises that personally identifiable information will not be disclosed to organizations outside The Atlantic and its subsidiaries except as described in the privacy policy. However, the practice states that contest/sweepstakes rules may specify different uses and disclosures than described in the privacy policy, which directly contradicts the claim's promise that disclosures only occur 'as described in this privacy policy.'
  - **openai/gpt-5-mini**: CONTRADICTION — The claim promises no disclosure of PII to outside organizations except as described in the privacy policy, but the contest language allows separate rules to specify disclosures that differ from the privacy policy, potentially permitting sharing with non‑affiliated parties and thus undermining the promise.
  - **google/gemini-3-flash-preview**: not contradiction — The claim explicitly includes the caveat 'except as described in this privacy policy,' and the practice describes a specific exception for contests where users voluntarily submit information under disclosed rules.

---

#### ocregister.com_009_vs_ocregister.com_014
**Company**: ocregister.com (OPP-115)
**NLI**: CONTRADICTION (score=1.000)
**Judges**: CONTRADICTION (majority)

**Claim** (ocregister.com_009):
> How Do We Use The Information We Collect? We will not sell, share, or rent personal information to third parties, and we will not otherwise disclose personal information to third parties, without your permission, except as disclosed in this Privacy Policy.

**Practice** (ocregister.com_014):
> We may work with third-party advertising companies which may use information about your visit to the Site in order to provide advertisements about goods and services that may be of interest to you on the Site and on third-party Web sites. From the Site, these companies may place or recognize a unique cookie on your computer or use other technologies such as Web beacons or pixel tags. Our Privacy Policy does not cover any use of information that a third-party advertisement serving company may collect from you. For more information about ad cookies and companies that provide users the ability to...

  - **anthropic/claude-haiku-4.5**: CONTRADICTION — The claim promises not to share personal information with third parties without permission, but the practice describes working with third-party advertising companies that collect information about user visits through cookies, web beacons, and pixel tags. This data sharing with advertisers occurs without explicit mention of user permission, directly contradicting the stated commitment.
  - **openai/gpt-5-mini**: not contradiction — Segment A disallows selling/sharing without permission but qualifies that exception with 'except as disclosed in this Privacy Policy.' Segment B is an explicit disclosure that the company works with third‑party advertisers (with opt‑out info), so it falls within that stated exception and does not contradict the claim.
  - **google/gemini-3-flash-preview**: CONTRADICTION — The claim promises not to share personal information with third parties without permission, but the practice describes allowing third-party advertising companies to collect user information via cookies and trackers for targeted marketing. Furthermore, the practice shifts the responsibility to the user to 'opt-out' rather than obtaining 'permission' as promised in the claim.

---

#### meredith.com_054_vs_meredith.com_053
**Company**: meredith.com (OPP-115)
**NLI**: CONTRADICTION (score=0.995)
**Judges**: CONTRADICTION (unanimous)

**Claim** (meredith.com_054):
> If you use our Services to sign up for special email offers from third-party advertisers, we will also share your email address and any other information you provided with your request with the advertisers you selected. Except as described in this policy, we will not sell or rent your email address to unaffiliated third parties for their email marketing purposes, without your consent.

**Practice** (meredith.com_053):
> Email. We share our users' email addresses with service providers that send email messages and deliver targeted advertising in our emails on our behalf. These service providers may collect data about how you interact with those messages (including information about whether and when you opened a particular message or clicked on a link within a message and the device you used to do so) and analyze it in conjunction with similar information they collect when you respond to emails they send on behalf of their other clients who are not affiliated with us. They use this email response information in...

  - **anthropic/claude-haiku-4.5**: CONTRADICTION — The claim states the company will not sell or rent email addresses to unaffiliated third parties for their email marketing purposes without consent, but the practice describes sharing email addresses (in hashed form) with service providers who use them to recognize users across third-party email services and send them interest-based advertising, which constitutes sharing for third-party marketing purposes beyond the explicit opt-in scenario described in the claim.
  - **openai/gpt-5-mini**: CONTRADICTION — The practice states service providers use your email (and hashed email lists) to recognize you and deliver interest-based advertising for their other clients and analyze data across clients, which effectively shares/uses email data for third-party marketing. That undermines the claim that the company will not sell or rent your email address to unaffiliated third parties for email marketing without your consent.
  - **google/gemini-3-flash-preview**: CONTRADICTION — The claim promises not to sell or rent email addresses to unaffiliated third parties for their own marketing purposes, but the practice describes sharing email data with service providers who use it to target advertising for their other unaffiliated clients.

---

#### lynda.com_029_vs_lynda.com_059
**Company**: lynda.com (OPP-115)
**NLI**: CONTRADICTION (score=0.983)
**Judges**: CONTRADICTION (unanimous)

**Claim** (lynda.com_029):
> DISCLOSURE OF YOUR INFORMATION We will share your Personally Identifiable Information with third parties only in the ways that are described in this Privacy Policy. Parents have the right to allow the collection and use of Personal Information from a Child without also consenting to its disclosure to Third Parties. We do not sell, trade, rent or disclose your information to others, except as provided herein:

**Practice** (lynda.com_059):
> The use of cookies by our partners, affiliates, tracking utility company and service providers, is not covered by our Privacy Policy. We do not have access or control over these cookies. Our partners, affiliates, tracking utility company, and service providers, use session ID cookies to make it easier for you to navigate our site, in order for you to use the shopping cart, etc.

  - **anthropic/claude-haiku-4.5**: CONTRADICTION — The claim states the company will only share PII 'in the ways that are described in this Privacy Policy' and does not disclose information 'except as provided herein,' but the practice reveals that cookies used by partners, affiliates, and service providers are 'not covered by our Privacy Policy' and the company has 'no access or control' over them. This means third parties are collecting data outside the described policy framework, contradicting the promise of controlled, policy-governed sharing.
  - **openai/gpt-5-mini**: CONTRADICTION — Segment A promises that personal information will only be shared as described in the Privacy Policy and not disclosed except as provided, while Segment B states partners/affiliates set cookies and their practices are not covered or controlled by the policy, implying third-party disclosures outside the described limits and thus undermining the commitment.
  - **google/gemini-3-flash-preview**: CONTRADICTION — The claim promises that the company does not disclose information to others except as described in the policy, yet the practice reveals that third-party partners and tracking companies are permitted to collect data via cookies that are explicitly 'not covered' by the policy.

---

## 7. Per-Company Comparison Table

| Company | Corpus | Pairs | NLI | Judge | Both | NLI-only | Judge-only |
|---------|--------|-------|-----|-------|------|----------|------------|
| latinpost.com | OPP-115 | 57 | 15 | 14 | 6 | 9 | 8 |
| reddit.com | OPP-115 | 60 | 2 | 11 | 0 | 2 | 11 |
| tesla | OPPT | 21 | 11 | 0 | 0 | 11 | 0 |
| sidearmsports.com | OPP-115 | 54 | 3 | 7 | 0 | 3 | 7 |
| meredith.com | OPP-115 | 24 | 4 | 6 | 1 | 3 | 5 |
| lynda.com | OPP-115 | 73 | 6 | 4 | 1 | 5 | 3 |
| united-airlines | OPPT | 19 | 0 | 8 | 0 | 0 | 8 |
| motorola-solutions | OPPT | 26 | 1 | 6 | 0 | 1 | 6 |
| taylorswift.com | OPP-115 | 12 | 3 | 4 | 2 | 1 | 2 |
| kraftrecipes.com | OPP-115 | 33 | 1 | 6 | 0 | 1 | 6 |
| venmo | OPPT | 38 | 4 | 2 | 1 | 3 | 1 |
| nytimes.com | OPP-115 | 53 | 4 | 2 | 0 | 4 | 2 |
| voxmedia.com | OPP-115 | 30 | 2 | 4 | 0 | 2 | 4 |
| barnesandnoble.com | OPP-115 | 41 | 1 | 5 | 0 | 1 | 5 |
| archives.gov | OPP-115 | 35 | 0 | 6 | 0 | 0 | 6 |
| bumble | OPPT | 19 | 0 | 4 | 0 | 0 | 4 |
| allstate.com | OPP-115 | 18 | 1 | 3 | 0 | 1 | 3 |
| theatlantic.com | OPP-115 | 17 | 2 | 2 | 1 | 1 | 1 |
| ocregister.com | OPP-115 | 12 | 1 | 3 | 1 | 0 | 2 |
| kaleidahealth.org | OPP-115 | 42 | 0 | 4 | 0 | 0 | 4 |
| pbs.org | OPP-115 | 19 | 1 | 3 | 0 | 1 | 3 |
| jasper | OPPT | 17 | 1 | 2 | 1 | 0 | 1 |
| meta | OPPT | 99 | 0 | 2 | 0 | 0 | 2 |
| xiaomi | OPPT | 17 | 0 | 2 | 0 | 0 | 2 |
| citizen.org | OPP-115 | 10 | 0 | 2 | 0 | 0 | 2 |
| adweek.com | OPP-115 | 10 | 1 | 1 | 0 | 1 | 1 |
| mlb.mlb.com | OPP-115 | 21 | 1 | 1 | 0 | 1 | 1 |
| abcnews.com | OPP-115 | 16 | 1 | 1 | 0 | 1 | 1 |
| tgifridays.com | OPP-115 | 16 | 0 | 2 | 0 | 0 | 2 |
| washingtonian.com | OPP-115 | 10 | 0 | 2 | 0 | 0 | 2 |
| minecraft.gamepedia.com | OPP-115 | 13 | 0 | 2 | 0 | 0 | 2 |
| si.edu | OPP-115 | 8 | 0 | 2 | 0 | 0 | 2 |
| github | OPPT | 6 | 0 | 1 | 0 | 0 | 1 |
| linkedin | OPPT | 13 | 1 | 0 | 0 | 1 | 0 |
| microsoft | OPPT | 1 | 1 | 0 | 0 | 1 | 0 |
| pimeyes | OPPT | 10 | 0 | 1 | 0 | 0 | 1 |
| lids.com | OPP-115 | 10 | 1 | 0 | 0 | 1 | 0 |
| www.loc.gov | OPP-115 | 10 | 0 | 1 | 0 | 0 | 1 |
| sheknows.com | OPP-115 | 4 | 1 | 0 | 0 | 1 | 0 |
| sciencemag.org | OPP-115 | 1 | 1 | 0 | 0 | 1 | 0 |

---

## 8. Conclusions

### What the judges got right

1. **False positive correction**: 6 of 7 known NLI false positives correctly dismissed (86%)
2. **New findings in previously 'clean' companies**: Judges found plausible contradictions in
   Bumble (4), United Airlines (8), and Meta (2) — companies NLI rated as clean
3. **Strong reasoning quality**: Judge reasoning is detailed, specific, and references exact
   text from both segments
4. **High agreement rate**: 82-83% unanimous across both corpora

### What the judges got wrong

1. **Massive false negative rate**: Dismissed 80.3% of NLI-flagged pairs (57 of 71),
   including most known genuine contradictions
2. **Complete Tesla miss**: All 11 NLI-flagged Tesla contradictions dismissed (9 were genuine)
3. **Complete NYTimes miss**: All 4 genuine contradictions dismissed
4. **Complete SIDEARM/VoxMedia/B&N miss**: All genuine contradictions dismissed
5. **LinkedIn miss**: The one genuine enforced-company contradiction dismissed

### Root cause: Judges are too sophisticated

The LLM judges reason like corporate lawyers, finding ways to reconcile claim and practice:

- They interpret claims **narrowly** ("won't sell email" → cookies aren't email)
- They categorize practices as **within scope** ("we limit sharing" → marketing is a listed purpose)
- They distinguish **PII from non-PII** (browsing data shared with advertisers isn't "personal info")

The NLI classifier, by contrast, captures **gestalt tension** — the overall direction of
the claim vs practice, without rationalizing each practice individually. This is closer
to how a user would experience the contradiction: a reassuring claim followed by broad
data practices creates a misleading impression regardless of technical distinctions.

### Recommendation

The NLI pipeline remains the better primary signal for privacy washing detection.
LLM judges are useful for:

- **False positive filtering**: Use judges to dismiss the ~10% FP rate from NLI
- **Supplementary detection**: Judge-only findings in United Airlines, Bumble, etc. may
  capture contradictions NLI misses (particularly children's data protection claims)
- **Reasoning generation**: Judge explanations provide readable justifications for flagged pairs

A **combined approach** — NLI primary detection + judge FP filtering — could improve
precision from 63.4% to ~70%+ while retaining NLI's superior recall on genuine contradictions.
