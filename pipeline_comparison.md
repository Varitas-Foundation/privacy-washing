# Pipeline Comparison: Statement-Level vs Segment-Level

*Generated: 2026-01-27 05:10 UTC*

## 1. Pipeline Summary Statistics

| Metric | Segment-Level | Statement-Level |
|--------|---------------|-----------------|
| Total pairs evaluated | 318 | 23395 |
| Contradictions detected | 19 | 4032 |
| Contradiction rate | 0.0597 | 0.1723 |
| Companies with contradictions | 6 | 5 |
| Unique segment pairs with contradictions | 19 | 1268 |

## 2. Segment-Pair Level Comparison

- **Both pipelines flag**: 11 segment pairs
- **Segment-level only**: 8 segment pairs (statement-level did NOT flag)
- **Statement-level only**: 1257 segment pairs (NEW contradictions)
- **Total unique flagged**: 1276

## 3. Assessment Against Judge Ground Truth

| Metric | Segment-Level | Statement-Level |
|--------|---------------|-----------------|
| Flagged pairs | 19 | 1268 |
| Judge confirmed (CONTRADICTION) | 2 | 1 |
| Judge dismissed (NOT_CONTRADICTION) | 17 | 34 |
| No judge data | 0 | 1233 |
| Judge-based precision | 10.5% | 2.9% |

> **Note:** Judge verdicts are an imperfect ground truth. Judges systematically
> dismiss genuine contradictions via narrow literal interpretation (see judge_vs_nli_experiment).
> The manual assessment found 45 genuine, 19 borderline, and 7 FP among 71 NLI-flagged pairs.

## 4. Known False Positive Patterns

The segment-level pipeline produced 7 known false positives with 3 systematic patterns:

- **security_implementation**: Practice describes implementation (e.g., SSL, BitLocker) that supports the security commitment
- **restated_commitment**: Practice restates the same non-sharing commitment in different words
- **informational_content**: Practice is informational/educational content, not a data practice

### FP Elimination Check

| FP | Company | Pattern | Seg-Level | Stmt-Level | Eliminated? |
|----|---------|---------|-----------|------------|-------------|
| OPPT | microsoft | security_implementation | FLAGGED | clear | YES |
| OPP-115 | sciencemag.org | security_implementation | clear | clear | — |
| OPP-115 | kraftrecipes.com | security_implementation | clear | clear | — |
| OPP-115 | adweek.com | restated_commitment | clear | clear | — |
| OPP-115 | latinpost.com | restated_commitment | clear | clear | — |
| OPP-115 | allstate.com | informational_content | clear | clear | — |
| OPP-115 | latinpost.com | informational_content | clear | clear | — |

## 5. Detailed Pair Comparison

### 5a. Segment-Level Flagged Pairs — Statement-Level Status

| Company | Pair ID | Seg NLI | Stmt Status | Stmt NLI (max) | Judge |
|---------|---------|---------|-------------|----------------|-------|
| jasper | `jasper_034_vs_jasper_037` | 0.930 | clear | 0.000 | CONTRADICTION |
| linkedin | `linkedin_034_vs_linkedin_009` | 0.999 | FLAGGED | 0.999 | NOT_CONTRADICTION |
| microsoft | `microsoft_014_vs_microsoft_053` | 0.997 | clear | 0.000 | NOT_CONTRADICTION |
| motorola-solutions | `motorola-solutions_018_vs_motorola-solutions_002` | 0.560 | clear | 0.000 | NOT_CONTRADICTION |
| tesla | `tesla_020_vs_tesla_004` | 0.862 | FLAGGED | 0.996 | NOT_CONTRADICTION |
| tesla | `tesla_020_vs_tesla_007` | 0.998 | FLAGGED | 0.996 | NOT_CONTRADICTION |
| tesla | `tesla_020_vs_tesla_008` | 0.986 | clear | 0.000 | NOT_CONTRADICTION |
| tesla | `tesla_020_vs_tesla_009` | 0.842 | clear | 0.000 | NOT_CONTRADICTION |
| tesla | `tesla_020_vs_tesla_011` | 0.584 | clear | 0.000 | NOT_CONTRADICTION |
| tesla | `tesla_020_vs_tesla_015` | 0.858 | FLAGGED | 0.989 | NOT_CONTRADICTION |
| tesla | `tesla_020_vs_tesla_016` | 0.964 | FLAGGED | 0.997 | NOT_CONTRADICTION |
| tesla | `tesla_020_vs_tesla_017` | 0.956 | FLAGGED | 0.987 | NOT_CONTRADICTION |
| tesla | `tesla_020_vs_tesla_019` | 0.958 | FLAGGED | 0.979 | NOT_CONTRADICTION |
| tesla | `tesla_020_vs_tesla_021` | 0.991 | FLAGGED | 0.996 | NOT_CONTRADICTION |
| tesla | `tesla_020_vs_tesla_022` | 0.998 | FLAGGED | 0.998 | NOT_CONTRADICTION |
| venmo | `venmo_037_vs_venmo_005` | 0.989 | FLAGGED | 0.998 | NOT_CONTRADICTION |
| venmo | `venmo_037_vs_venmo_011` | 0.989 | clear | 0.000 | NOT_CONTRADICTION |
| venmo | `venmo_037_vs_venmo_026` | 0.970 | clear | 0.000 | NOT_CONTRADICTION |
| venmo | `venmo_037_vs_venmo_039` | 0.693 | FLAGGED | 0.999 | CONTRADICTION |

### 5b. New Statement-Level Contradictions (Not in Segment-Level)

| Company | Segment Pair | # Stmt Contradictions | Max NLI | Top Commitment | Top Practice |
|---------|-------------|----------------------|---------|----------------|--------------|
| ? | `jasper_006_vs_jasper_003` | 2 | 0.993 | Jasper conducts collection and use of third-party data consi... | Jasper collects personally identifiable information includin... |
| ? | `jasper_006_vs_jasper_005` | 1 | 0.986 | Jasper conducts collection and use of third-party data consi... | Jasper allows users to create accounts and log in through th... |
| ? | `jasper_006_vs_jasper_022` | 1 | 0.999 | Jasper conducts collection and use of third-party data consi... | Third-party payment processors' use of personal information ... |
| ? | `jasper_006_vs_jasper_029` | 1 | 0.986 | Jasper conducts collection and use of third-party data consi... | Jasper collects personal information directly from users thr... |
| ? | `jasper_006_vs_jasper_030` | 1 | 0.998 | Jasper conducts collection and use of third-party data consi... | Jasper uses personal information for internal administrative... |
| ? | `jasper_007_vs_jasper_009` | 1 | 0.992 | Users may instruct their browser to refuse all cookies or in... | Jasper uses persistent cookies administered by itself to ide... |
| ? | `jasper_007_vs_jasper_029` | 1 | 0.583 | Users may instruct their browser to refuse all cookies or in... | Jasper automatically collects personal information through c... |
| ? | `jasper_007_vs_jasper_037` | 1 | 0.998 | Users may not be able to use some parts of our service if th... | The company's service does not respond to Do Not Track signa... |
| ? | `jasper_008_vs_jasper_007` | 2 | 1.000 | We only use session cookies to provide requested services to... | We use both session and persistent cookies for purposes incl... |
| ? | `jasper_008_vs_jasper_009` | 1 | 1.000 | We only use session cookies to provide requested services to... | Jasper uses persistent cookies administered by itself to ide... |
| ? | `jasper_008_vs_jasper_010` | 3 | 1.000 | We only use session cookies to provide requested services to... | Jasper uses persistent cookies to remember user choices like... |
| ? | `jasper_008_vs_jasper_011` | 1 | 1.000 | We only use session cookies to provide requested services to... | Persistent cookies are used to test new pages, features, or ... |
| ? | `jasper_008_vs_jasper_012` | 1 | 0.859 | We only use session cookies to provide requested services to... | Persistent cookies administered by third parties track user ... |
| ? | `jasper_008_vs_jasper_020` | 1 | 0.993 | We only use session cookies to provide requested services to... | Google uses cookies as a third party vendor to serve ads on ... |
| ? | `jasper_008_vs_jasper_029` | 1 | 0.872 | We only use session cookies to provide requested services to... | Jasper automatically collects personal information through c... |
| ? | `jasper_016_vs_jasper_005` | 1 | 0.998 | The company will provide notice before personal data is tran... | Jasper uses, shares, and stores personal data from third-par... |
| ? | `jasper_018_vs_jasper_013` | 6 | 0.999 | Third-party vendors handle user data in accordance with thei... | The Company shares or transfers Personal Data in connection ... |
| ? | `jasper_018_vs_jasper_029` | 1 | 0.997 | Third-party vendors handle user data in accordance with thei... | Jasper receives de-anonymized visitor data and buyer intent ... |
| ? | `jasper_018_vs_jasper_031` | 1 | 0.925 | Third-party vendors handle user data in accordance with thei... | Jasper may use or disclose identifiers, personal information... |
| ? | `jasper_021_vs_jasper_030` | 3 | 0.999 | Users may opt-out of receiving marketing communications from... | Jasper discloses personal information as required by applica... |
| ? | `jasper_022_vs_jasper_021` | 1 | 0.999 | Jasper does not store or collect payment card details from u... | Jasper uses personal data to contact users with newsletters,... |
| ? | `jasper_022_vs_jasper_029` | 1 | 0.999 | Jasper does not store or collect payment card details from u... | Jasper collects personal information directly from users thr... |
| ? | `jasper_022_vs_jasper_030` | 10 | 1.000 | Jasper does not store or collect payment card details from u... | Jasper uses personal information to prosecute those responsi... |
| ? | `jasper_022_vs_jasper_031` | 1 | 0.756 | Jasper does not store or collect payment card details from u... | Jasper may use or disclose identifiers, personal information... |
| ? | `jasper_022_vs_jasper_033` | 1 | 1.000 | Jasper does not store or collect payment card details from u... | Jasper shares personal information with payment processors.... |
| ? | `jasper_030_vs_jasper_013` | 2 | 0.993 | Jasper commits to updating its Privacy Policy if it uses per... | Personal information shared in public areas may be viewed by... |
| ? | `jasper_031_vs_jasper_003` | 4 | 0.986 | When Jasper discloses personal information for business purp... | Jasper collects personally identifiable information includin... |
| ? | `jasper_031_vs_jasper_005` | 2 | 0.990 | When Jasper discloses personal information for business purp... | Jasper collects personal data already associated with a user... |
| ? | `jasper_031_vs_jasper_006` | 1 | 0.985 | When Jasper discloses personal information for business purp... | Jasper receives de-anonymized website traffic data from thir... |
| ? | `jasper_031_vs_jasper_013` | 2 | 0.996 | When Jasper discloses personal information for business purp... | The Company shares Personal Data with user consent for purpo... |
| ? | `jasper_031_vs_jasper_016` | 1 | 0.536 | When Jasper discloses personal information for business purp... | Personal data may be transferred if the company is involved ... |
| ? | `jasper_031_vs_jasper_029` | 2 | 0.990 | When Jasper discloses personal information for business purp... | Jasper receives de-anonymized visitor data and buyer intent ... |
| ? | `jasper_031_vs_jasper_030` | 6 | 0.997 | When Jasper discloses personal information for business purp... | Jasper uses personal information to prosecute those responsi... |
| ? | `jasper_031_vs_jasper_035` | 1 | 0.993 | When Jasper discloses personal information for business purp... | We disclose whether we sold or disclosed personal informatio... |
| jasper | `jasper_034_vs_jasper_031` | 1 | 0.998 | Jasper does not sell personal information of consumers known... | Jasper may use or disclose identifiers, personal information... |
| jasper | `jasper_034_vs_jasper_032` | 1 | 0.843 | Jasper does not sell personal information of consumers known... | Jasper may share personal information in these categories fo... |
| ? | `jasper_035_vs_jasper_016` | 1 | 0.695 | California residents have the right to direct us not to sell... | The company may disclose personal data to protect against le... |
| ? | `jasper_037_vs_jasper_013` | 2 | 0.999 | Users have the right to opt-out of the sale of their persona... | The Company shares Personal Data with affiliates and require... |
| ? | `jasper_037_vs_jasper_016` | 2 | 0.918 | The company will stop selling personal information once a ve... | The company may disclose personal data to prevent or investi... |
| ? | `jasper_037_vs_jasper_032` | 2 | 0.904 | Users have the right to opt-out of the sale of their persona... | Jasper may share personal information in these categories fo... |
| ? | `linkedin_008_vs_linkedin_017` | 3 | 0.987 | Users have choices about what profile information to provide... | LinkedIn uses automated systems to suggest possible response... |
| ? | `linkedin_008_vs_linkedin_025` | 1 | 0.998 | Users have choices about what profile information to provide... | LinkedIn uses automated systems to provide content and recom... |
| ? | `linkedin_008_vs_linkedin_031` | 1 | 0.996 | Users have choices about what profile information to provide... | LinkedIn shares user profile data with third parties when al... |
| ? | `linkedin_008_vs_linkedin_040` | 1 | 0.998 | Users can choose whether to include sensitive information on... | User profiles are fully visible to all Members and customers... |
| ? | `linkedin_008_vs_linkedin_041` | 2 | 0.999 | Users can choose whether to include sensitive information on... | User group membership is public and part of their profile by... |
| ? | `linkedin_008_vs_linkedin_045` | 1 | 0.988 | Users have choices about what profile information to provide... | LinkedIn combines information internally across different Se... |
| ? | `linkedin_008_vs_linkedin_047` | 2 | 0.999 | Users have choices about what profile information to provide... | LinkedIn shares user data with third parties when required b... |
| ? | `linkedin_008_vs_linkedin_048` | 1 | 0.988 | Users have choices about what profile information to provide... | Any entity acquiring LinkedIn or part of its business has th... |
| ? | `linkedin_009_vs_linkedin_007` | 1 | 0.997 | Users are not required to post or upload personal data to Li... | LinkedIn collects name, email address, and mobile number to ... |
| ? | `linkedin_009_vs_linkedin_022` | 1 | 0.996 | Users are not required to post or upload personal data to Li... | LinkedIn uses your data to authorize access to its Services ... |
| ? | `linkedin_009_vs_linkedin_029` | 1 | 0.998 | Users are not required to post or upload personal data to Li... | LinkedIn associates user social actions on ads with their na... |
| ? | `linkedin_009_vs_linkedin_040` | 1 | 0.999 | Users are not required to post or upload personal data to Li... | User profiles are fully visible to all Members and customers... |
| ? | `linkedin_009_vs_linkedin_047` | 1 | 0.994 | Users are not required to post or upload personal data to Li... | LinkedIn shares data to enforce agreements with users.... |
| ? | `linkedin_009_vs_linkedin_048` | 1 | 0.992 | Not posting or uploading personal data may limit users' abil... | LinkedIn shares personal data when its business is sold to a... |
| ? | `linkedin_016_vs_linkedin_009` | 1 | 0.818 | LinkedIn requires opt-in consent before using GPS or other t... | LinkedIn collects personal data when users provide, post, or... |
| ? | `linkedin_016_vs_linkedin_010` | 2 | 0.955 | LinkedIn requires opt-in consent before using GPS or other t... | LinkedIn makes collected public information about users avai... |
| ? | `linkedin_016_vs_linkedin_021` | 1 | 0.784 | LinkedIn requires opt-in consent before using GPS or other t... | LinkedIn uses personal data to personalize Services with hel... |
| ? | `linkedin_016_vs_linkedin_031` | 1 | 0.871 | LinkedIn requires opt-in consent before using GPS or other t... | LinkedIn shares user profile data with third parties when al... |
| ? | `linkedin_016_vs_linkedin_047` | 1 | 0.996 | LinkedIn requires opt-in consent before using GPS or other t... | LinkedIn shares user data with third parties when required b... |
| ? | `linkedin_016_vs_linkedin_048` | 2 | 0.997 | LinkedIn requires opt-in consent before using GPS or other t... | Any entity acquiring LinkedIn or part of its business has th... |
| ? | `linkedin_020_vs_linkedin_031` | 2 | 0.999 | LinkedIn notifies users when it collects materially differen... | LinkedIn shares user profile data with third parties when al... |
| ? | `linkedin_020_vs_linkedin_037` | 1 | 0.995 | LinkedIn notifies users when it collects materially differen... | LinkedIn shares ad impression reports with advertisers to in... |
| ? | `linkedin_020_vs_linkedin_048` | 2 | 0.993 | LinkedIn notifies users when it materially changes how it co... | Any entity acquiring LinkedIn or part of its business has th... |
| ? | `linkedin_021_vs_linkedin_010` | 1 | 0.917 | How LinkedIn uses personal data depends on which Services us... | LinkedIn makes collected public information about users avai... |
| ? | `linkedin_021_vs_linkedin_031` | 1 | 0.595 | How LinkedIn uses personal data depends on which Services us... | LinkedIn shares user profile data with third parties when al... |
| ? | `linkedin_021_vs_linkedin_034` | 1 | 0.997 | How LinkedIn uses personal data depends on which Services us... | LinkedIn publishes or allows others to publish economic insi... |
| ? | `linkedin_021_vs_linkedin_040` | 1 | 0.993 | How LinkedIn uses personal data depends on which Services us... | User profiles are fully visible to all Members and customers... |
| ? | `linkedin_021_vs_linkedin_041` | 1 | 0.999 | How LinkedIn uses personal data depends on which Services us... | User group membership is public and part of their profile by... |
| ? | `linkedin_021_vs_linkedin_048` | 1 | 0.997 | How LinkedIn uses personal data depends on which Services us... | LinkedIn shares personal data when its business is sold to a... |
| ? | `linkedin_023_vs_linkedin_007` | 7 | 0.999 | Users can opt-in to allow LinkedIn to use precise location d... | LinkedIn collects name, email address, and mobile number to ... |
| ? | `linkedin_023_vs_linkedin_008` | 1 | 0.523 | Users can opt-in to allow LinkedIn to use proximity data to ... | LinkedIn uses profile information to help recruiters and bus... |
| ? | `linkedin_023_vs_linkedin_009` | 4 | 0.999 | Users can opt-in to allow LinkedIn to use precise location d... | LinkedIn uses calendar meeting information to suggest connec... |
| ? | `linkedin_023_vs_linkedin_011` | 1 | 0.713 | Users can opt-in to allow LinkedIn to use precise location d... | LinkedIn collects email header information when users opt-in... |
| ? | `linkedin_023_vs_linkedin_013` | 1 | 0.905 | Users can opt-in to allow LinkedIn to use proximity data to ... | LinkedIn uses contact and engagement data received from user... |
| ? | `linkedin_023_vs_linkedin_014` | 3 | 0.997 | Users can opt-in to allow LinkedIn to use proximity data to ... | LinkedIn collects IP addresses to identify users and log the... |
| ? | `linkedin_023_vs_linkedin_017` | 4 | 0.999 | Users can opt-in to allow LinkedIn to use proximity data to ... | LinkedIn uses automated systems to manage or block content t... |
| ? | `linkedin_023_vs_linkedin_021` | 2 | 0.947 | Users can opt-in to allow LinkedIn to use proximity data to ... | LinkedIn uses personal data to develop and train artificial ... |
| ? | `linkedin_023_vs_linkedin_022` | 2 | 0.990 | Users can opt-in to allow LinkedIn to use proximity data to ... | LinkedIn uses your data to authorize access to its Services ... |
| ? | `linkedin_023_vs_linkedin_024` | 6 | 0.999 | Users can opt-in to allow LinkedIn to use precise location d... | LinkedIn uses user content, activity, name and photo to prov... |
| ? | `linkedin_023_vs_linkedin_025` | 2 | 0.980 | Users can opt-in to allow LinkedIn to use proximity data to ... | LinkedIn uses user data to recommend jobs to members based o... |
| ? | `linkedin_023_vs_linkedin_029` | 5 | 0.998 | Users can opt-in to allow LinkedIn to use precise location d... | LinkedIn uses member-provided profile and contact informatio... |
| ? | `linkedin_023_vs_linkedin_031` | 4 | 0.997 | Visitors have choices about how LinkedIn uses their data.... | LinkedIn shares user profile data with third parties when al... |
| ? | `linkedin_023_vs_linkedin_032` | 1 | 0.720 | Users can opt-in to allow LinkedIn to use proximity data to ... | LinkedIn uses members' data and content for invitations and ... |
| ? | `linkedin_023_vs_linkedin_034` | 3 | 0.998 | Users can opt-in to allow LinkedIn to use proximity data to ... | LinkedIn uses personal data to research social, economic and... |
| ? | `linkedin_023_vs_linkedin_036` | 2 | 0.764 | Users can opt-in to allow LinkedIn to use proximity data to ... | LinkedIn uses data to resolve service issues such as bugs.... |
| ? | `linkedin_023_vs_linkedin_037` | 7 | 1.000 | Users can opt-in to allow LinkedIn to use proximity data to ... | LinkedIn uses data to calculate ad impressions served or cli... |
| ? | `linkedin_023_vs_linkedin_038` | 2 | 0.996 | Users can opt-in to allow LinkedIn to use proximity data to ... | LinkedIn uses data to investigate attempts to harm members, ... |
| ? | `linkedin_023_vs_linkedin_039` | 2 | 0.999 | Users can opt-in to allow LinkedIn to use precise location d... | LinkedIn uses user online activities such as likes, follows,... |
| ? | `linkedin_023_vs_linkedin_040` | 2 | 0.985 | Users can choose whether to share their list of connections ... | User profiles are fully visible to all Members and customers... |
| ? | `linkedin_023_vs_linkedin_041` | 1 | 0.999 | Users can choose whether to share their list of connections ... | User group membership is public and part of their profile by... |
| ? | `linkedin_023_vs_linkedin_043` | 5 | 0.974 | Users can opt-in to allow LinkedIn to use proximity data to ... | LinkedIn enables archiving of messages by and to regulated M... |
| ? | `linkedin_023_vs_linkedin_045` | 1 | 0.681 | Users can opt-in to allow LinkedIn to use proximity data to ... | LinkedIn personalizes user feeds and job recommendations bas... |
| ? | `linkedin_023_vs_linkedin_047` | 8 | 0.999 | Users can opt-in to allow LinkedIn to use precise location d... | LinkedIn shares user data with third parties when required b... |
| ? | `linkedin_023_vs_linkedin_048` | 5 | 0.993 | Users can opt-in to allow LinkedIn to use precise location d... | LinkedIn shares personal data when its business is sold to a... |
| ? | `linkedin_024_vs_linkedin_007` | 1 | 0.821 | LinkedIn notifies others about user activities subject to us... | LinkedIn collects name, email address, and mobile number to ... |
| ? | `linkedin_024_vs_linkedin_031` | 1 | 0.973 | LinkedIn notifies others about user activities subject to us... | LinkedIn shares user profile data with third parties when al... |
| ? | `linkedin_024_vs_linkedin_040` | 1 | 0.988 | LinkedIn notifies others about user activities subject to us... | User profiles are fully visible to all Members and customers... |
| ? | `linkedin_024_vs_linkedin_041` | 1 | 0.997 | LinkedIn notifies others about user activities subject to us... | User group membership is public and part of their profile by... |
| ? | `linkedin_024_vs_linkedin_047` | 1 | 0.701 | LinkedIn notifies others about user activities subject to us... | LinkedIn shares user data with third parties when required b... |
| ? | `linkedin_024_vs_linkedin_048` | 1 | 0.892 | LinkedIn notifies others about user activities subject to us... | LinkedIn shares personal data when its business is sold to a... |
| ? | `linkedin_027_vs_linkedin_015` | 2 | 0.999 | Data stored by premium Services customers about users is sub... | We rely on third parties including Microsoft to collect devi... |
| ? | `linkedin_027_vs_linkedin_018` | 3 | 0.999 | Data stored by premium Services customers about users is sub... | Organizations share personal data and user profile informati... |
| ? | `linkedin_027_vs_linkedin_029` | 1 | 0.995 | Data stored by premium Services customers about users is sub... | LinkedIn shares user data with advertising partners, vendors... |
| ? | `linkedin_027_vs_linkedin_031` | 1 | 1.000 | Data stored by premium Services customers about users is sub... | LinkedIn shares user profile data with third parties when al... |
| ? | `linkedin_027_vs_linkedin_041` | 2 | 0.997 | Data stored by premium Services customers about users is sub... | Information shared through company or organization pages is ... |
| ? | `linkedin_027_vs_linkedin_043` | 2 | 0.993 | Data stored by premium Services customers about users is sub... | LinkedIn shares contents of communications with third-party ... |
| ? | `linkedin_027_vs_linkedin_045` | 1 | 0.961 | Data stored by premium Services customers about users is sub... | LinkedIn shares personal data with Affiliates including Micr... |
| ? | `linkedin_027_vs_linkedin_047` | 4 | 0.997 | Data stored by premium Services customers about users is sub... | LinkedIn shares data to assist government enforcement agenci... |
| ? | `linkedin_027_vs_linkedin_048` | 2 | 0.996 | Data stored by premium Services customers about users is sub... | Any entity acquiring LinkedIn or part of its business has th... |
| ? | `linkedin_028_vs_linkedin_010` | 1 | 0.967 | Members cannot opt out of receiving service messages includi... | LinkedIn includes public information about users in notifica... |
| ? | `linkedin_028_vs_linkedin_029` | 1 | 0.998 | Members cannot opt out of receiving service messages includi... | LinkedIn may mention user social actions with related ads su... |
| ? | `linkedin_028_vs_linkedin_041` | 1 | 0.999 | Members may change their communication preferences at any ti... | User group membership is public and part of their profile by... |
| ? | `linkedin_028_vs_linkedin_042` | 1 | 0.509 | Members cannot opt out of receiving service messages includi... | LinkedIn requests permission to share relevant profile data ... |
| ? | `linkedin_028_vs_linkedin_043` | 1 | 0.809 | Members cannot opt out of receiving service messages includi... | LinkedIn enables archiving of messages by and to regulated M... |
| ? | `linkedin_028_vs_linkedin_046` | 1 | 0.613 | Members cannot opt out of receiving service messages includi... | LinkedIn may use payment service providers who separately co... |
| ? | `linkedin_031_vs_linkedin_009` | 1 | 0.831 | LinkedIn takes steps to verify that user consent has been pr... | LinkedIn collects personal data when users provide, post, or... |
| ? | `linkedin_031_vs_linkedin_010` | 9 | 0.999 | LinkedIn does not share personal data with non-affiliated th... | LinkedIn makes collected public information about users avai... |
| ? | `linkedin_031_vs_linkedin_011` | 4 | 0.995 | LinkedIn does not share personal data with non-affiliated th... | LinkedIn receives contact information when others associate ... |
| ? | `linkedin_031_vs_linkedin_012` | 2 | 0.997 | LinkedIn does not share personal data with non-affiliated th... | LinkedIn receives personal data about users when they use se... |
| ? | `linkedin_031_vs_linkedin_013` | 3 | 0.992 | LinkedIn does not share personal data with non-affiliated th... | LinkedIn receives data about users when they use services pr... |
| ? | `linkedin_031_vs_linkedin_015` | 1 | 0.934 | LinkedIn contractually requires advertising partners to obta... | We allow others to use cookies as described in our Cookie Po... |
| ? | `linkedin_031_vs_linkedin_016` | 1 | 0.833 | LinkedIn does not share personal data with non-affiliated th... | LinkedIn collects device identifiers, features, cookie IDs, ... |
| ? | `linkedin_031_vs_linkedin_018` | 3 | 0.997 | LinkedIn does not share personal data with non-affiliated th... | LinkedIn receives contact information and user eligibility d... |
| ? | `linkedin_031_vs_linkedin_019` | 3 | 0.999 | LinkedIn does not share personal data with non-affiliated th... | LinkedIn uses collected data for advertising purposes.... |
| ? | `linkedin_031_vs_linkedin_021` | 2 | 0.992 | LinkedIn takes steps to verify that user consent has been pr... | LinkedIn makes inferences about user characteristics includi... |
| ? | `linkedin_031_vs_linkedin_023` | 1 | 0.936 | LinkedIn does not share personal data with non-affiliated th... | LinkedIn uses data from address book uploads and partner int... |
| ? | `linkedin_031_vs_linkedin_024` | 1 | 0.985 | LinkedIn does not share personal data with non-affiliated th... | LinkedIn uses data about users to personalize Services by re... |
| ? | `linkedin_031_vs_linkedin_025` | 2 | 0.985 | LinkedIn does not share personal data with non-affiliated th... | LinkedIn uses user data to recommend jobs to members based o... |
| ? | `linkedin_031_vs_linkedin_029` | 5 | 0.999 | LinkedIn does not share personal data with non-affiliated th... | LinkedIn associates user social actions on ads with their na... |
| ? | `linkedin_031_vs_linkedin_030` | 1 | 0.532 | LinkedIn does not share personal data with non-affiliated th... | LinkedIn uses cookies and tracking elements to show users mo... |
| ? | `linkedin_031_vs_linkedin_032` | 3 | 0.997 | LinkedIn does not share personal data with non-affiliated th... | LinkedIn uses members' data and content for communications p... |
| ? | `linkedin_031_vs_linkedin_034` | 3 | 0.998 | LinkedIn does not share personal data with non-affiliated th... | LinkedIn makes public data available to researchers to asses... |
| ? | `linkedin_031_vs_linkedin_038` | 1 | 0.507 | LinkedIn does not share personal data with non-affiliated th... | LinkedIn Affiliates may see member data to prevent or invest... |
| ? | `linkedin_031_vs_linkedin_039` | 2 | 0.998 | LinkedIn does not share personal data with non-affiliated th... | LinkedIn uses user profile data and content posted on the se... |
| ? | `linkedin_031_vs_linkedin_043` | 1 | 0.990 | LinkedIn does not share personal data with non-affiliated th... | LinkedIn enables archiving of messages by and to regulated M... |
| ? | `linkedin_031_vs_linkedin_044` | 4 | 0.999 | LinkedIn does not share personal data with non-affiliated th... | When users link their account with other services, personal ... |
| ? | `linkedin_031_vs_linkedin_045` | 2 | 0.995 | LinkedIn does not share personal data with non-affiliated th... | LinkedIn shares user data across different Services and Link... |
| ? | `linkedin_031_vs_linkedin_046` | 2 | 0.996 | LinkedIn contractually requires advertising partners to obta... | Third parties receive access to user information as reasonab... |
| ? | `linkedin_031_vs_linkedin_047` | 4 | 0.999 | LinkedIn takes steps to verify that user consent has been pr... | LinkedIn shares user data with third parties when required b... |
| ? | `linkedin_031_vs_linkedin_048` | 4 | 0.997 | LinkedIn takes steps to verify that user consent has been pr... | Any entity acquiring LinkedIn or part of its business has th... |
| ? | `linkedin_034_vs_linkedin_007` | 4 | 0.992 | LinkedIn implements controls designed to protect privacy whe... | LinkedIn uses collected data for account management and basi... |
| ? | `linkedin_034_vs_linkedin_010` | 4 | 1.000 | LinkedIn implements controls designed to protect privacy whe... | LinkedIn makes collected public information about users avai... |
| ? | `linkedin_034_vs_linkedin_011` | 1 | 0.722 | LinkedIn implements controls designed to protect privacy whe... | LinkedIn receives contact information when others send messa... |
| ? | `linkedin_034_vs_linkedin_012` | 1 | 0.977 | LinkedIn implements controls designed to protect privacy whe... | LinkedIn receives personal data about users when they use se... |
| ? | `linkedin_034_vs_linkedin_016` | 3 | 0.999 | LinkedIn implements controls designed to protect privacy whe... | LinkedIn collects device identifiers, features, cookie IDs, ... |
| linkedin | `linkedin_034_vs_linkedin_017` | 1 | 0.984 | LinkedIn implements controls designed to protect privacy whe... | LinkedIn collects information about communications between u... |
| ? | `linkedin_034_vs_linkedin_018` | 1 | 0.992 | LinkedIn implements controls designed to protect privacy whe... | Organizations share personal data and user profile informati... |
| ? | `linkedin_034_vs_linkedin_019` | 2 | 0.994 | LinkedIn implements controls designed to protect privacy whe... | LinkedIn collects data when users log in to other services w... |
| linkedin | `linkedin_034_vs_linkedin_021` | 3 | 0.996 | LinkedIn implements controls designed to protect privacy whe... | LinkedIn makes inferences about user characteristics includi... |
| linkedin | `linkedin_034_vs_linkedin_022` | 1 | 0.998 | LinkedIn implements controls designed to protect privacy whe... | LinkedIn uses your data for account management and basic ser... |
| ? | `linkedin_034_vs_linkedin_023` | 1 | 0.564 | LinkedIn implements controls designed to protect privacy whe... | LinkedIn uses user profile data to help others find your pro... |
| linkedin | `linkedin_034_vs_linkedin_024` | 1 | 0.785 | LinkedIn implements controls designed to protect privacy whe... | LinkedIn uses user content, activity, name and photo to prov... |
| linkedin | `linkedin_034_vs_linkedin_025` | 1 | 0.948 | LinkedIn implements controls designed to protect privacy whe... | LinkedIn uses automated systems to provide content and recom... |
| ? | `linkedin_034_vs_linkedin_026` | 1 | 0.946 | LinkedIn implements controls designed to protect privacy whe... | LinkedIn Services allow users to communicate with other Memb... |
| ? | `linkedin_034_vs_linkedin_028` | 3 | 0.994 | LinkedIn implements controls designed to protect privacy whe... | LinkedIn contacts members and enables communications between... |
| ? | `linkedin_034_vs_linkedin_029` | 4 | 0.999 | LinkedIn implements controls designed to protect privacy whe... | LinkedIn associates user social actions on ads with their na... |
| ? | `linkedin_034_vs_linkedin_030` | 1 | 0.966 | LinkedIn implements controls designed to protect privacy whe... | LinkedIn uses cookies and tracking elements to show users mo... |
| ? | `linkedin_034_vs_linkedin_031` | 3 | 1.000 | LinkedIn implements controls designed to protect privacy whe... | LinkedIn shares user profile data with third parties when al... |
| linkedin | `linkedin_034_vs_linkedin_032` | 4 | 0.997 | LinkedIn implements controls designed to protect privacy whe... | LinkedIn uses members' data and content for invitations and ... |
| linkedin | `linkedin_034_vs_linkedin_033` | 1 | 0.698 | LinkedIn implements controls designed to protect privacy whe... | LinkedIn uses data to provide users with a better, more intu... |
| linkedin | `linkedin_034_vs_linkedin_036` | 1 | 0.994 | LinkedIn implements controls designed to protect privacy whe... | LinkedIn uses data to resolve service issues such as bugs.... |
| linkedin | `linkedin_034_vs_linkedin_037` | 3 | 0.996 | LinkedIn implements controls designed to protect privacy whe... | LinkedIn uses data to calculate ad impressions served or cli... |
| ? | `linkedin_034_vs_linkedin_038` | 2 | 0.998 | LinkedIn implements controls designed to protect privacy whe... | LinkedIn uses data to investigate attempts to harm members, ... |
| ? | `linkedin_034_vs_linkedin_039` | 3 | 0.999 | LinkedIn implements controls designed to protect privacy whe... | LinkedIn uses user online activities such as likes, follows,... |
| ? | `linkedin_034_vs_linkedin_040` | 1 | 0.828 | LinkedIn implements controls designed to protect privacy whe... | User profiles can be visible to Visitors and third-party sea... |
| ? | `linkedin_034_vs_linkedin_041` | 4 | 1.000 | LinkedIn implements controls designed to protect privacy whe... | Publicly shared articles or posts can be viewed by everyone ... |
| ? | `linkedin_034_vs_linkedin_042` | 2 | 1.000 | LinkedIn implements controls designed to protect privacy whe... | Sales Navigator users are asked to share their social sellin... |
| ? | `linkedin_034_vs_linkedin_043` | 3 | 0.999 | LinkedIn implements controls designed to protect privacy whe... | LinkedIn shares contents of communications with third-party ... |
| ? | `linkedin_034_vs_linkedin_044` | 4 | 1.000 | LinkedIn implements controls designed to protect privacy whe... | When users link their account with other services, personal ... |
| ? | `linkedin_034_vs_linkedin_045` | 5 | 0.999 | LinkedIn implements controls designed to protect privacy whe... | LinkedIn shares publicly-shared content with Affiliates incl... |
| ? | `linkedin_034_vs_linkedin_046` | 1 | 0.899 | LinkedIn implements controls designed to protect privacy whe... | Third parties receive access to user information as reasonab... |
| ? | `linkedin_034_vs_linkedin_047` | 5 | 0.999 | LinkedIn implements controls designed to protect privacy whe... | LinkedIn shares user data with third parties when required b... |
| ? | `linkedin_034_vs_linkedin_048` | 3 | 0.999 | LinkedIn implements controls designed to protect privacy whe... | LinkedIn shares personal data when its business is sold to a... |
| ? | `linkedin_037_vs_linkedin_009` | 2 | 0.994 | LinkedIn generates insights from user data that do not ident... | LinkedIn collects personal data when users provide, post, or... |
| ? | `linkedin_037_vs_linkedin_011` | 1 | 0.990 | LinkedIn generates insights from user data that do not ident... | LinkedIn receives contact information when others associate ... |
| ? | `linkedin_037_vs_linkedin_012` | 2 | 0.995 | LinkedIn generates insights from user data that do not ident... | LinkedIn receives personal data about users when they use se... |
| ? | `linkedin_037_vs_linkedin_014` | 1 | 0.997 | LinkedIn generates insights from user data that do not ident... | LinkedIn collects log-ins, cookies, and device information t... |
| ? | `linkedin_037_vs_linkedin_021` | 1 | 0.996 | LinkedIn generates insights from user data that do not ident... | LinkedIn makes inferences about user characteristics includi... |
| ? | `linkedin_037_vs_linkedin_029` | 1 | 0.998 | LinkedIn generates insights from user data that do not ident... | LinkedIn associates user social actions on ads with their na... |
| ? | `linkedin_037_vs_linkedin_031` | 1 | 0.993 | LinkedIn generates insights from user data that do not ident... | LinkedIn shares user profile data with third parties when al... |
| ? | `linkedin_037_vs_linkedin_034` | 1 | 0.983 | LinkedIn generates insights from user data that do not ident... | LinkedIn uses personal data to research social, economic and... |
| ? | `linkedin_037_vs_linkedin_038` | 1 | 0.527 | LinkedIn generates insights from user data that do not ident... | LinkedIn uses data to investigate attempts to harm members, ... |
| ? | `linkedin_037_vs_linkedin_040` | 1 | 0.999 | LinkedIn generates insights from user data that do not ident... | User profiles are fully visible to all Members and customers... |
| ? | `linkedin_037_vs_linkedin_047` | 1 | 0.974 | LinkedIn generates insights from user data that do not ident... | LinkedIn shares data to enforce agreements with users.... |
| ? | `linkedin_037_vs_linkedin_048` | 2 | 0.998 | LinkedIn generates insights from user data that do not ident... | LinkedIn shares personal data when its business is sold to a... |
| ? | `linkedin_041_vs_linkedin_042` | 1 | 0.977 | The platform does not show employers user job searches or pe... | Employers can review and manage employee use of enterprise S... |
| ? | `linkedin_042_vs_linkedin_009` | 5 | 0.993 | LinkedIn does not share job hunting activities with employer... | LinkedIn collects personal data when users respond to survey... |
| ? | `linkedin_042_vs_linkedin_010` | 3 | 0.997 | LinkedIn does not share job hunting activities with employer... | LinkedIn makes collected public information about users avai... |
| ? | `linkedin_042_vs_linkedin_011` | 5 | 0.994 | LinkedIn does not share job hunting activities with employer... | LinkedIn receives contact information when others send messa... |
| ? | `linkedin_042_vs_linkedin_012` | 5 | 0.999 | LinkedIn does not share job hunting activities with employer... | LinkedIn receives job application data from employers, prosp... |
| ? | `linkedin_042_vs_linkedin_018` | 3 | 0.997 | LinkedIn does not share personal messages with employers unl... | LinkedIn receives personal data about users from their emplo... |
| ? | `linkedin_042_vs_linkedin_021` | 3 | 0.990 | LinkedIn does not share personal messages with employers unl... | LinkedIn uses personal data to personalize Services with hel... |
| ? | `linkedin_042_vs_linkedin_025` | 1 | 0.974 | LinkedIn does not share job hunting activities with employer... | LinkedIn uses user data to recommend jobs to members based o... |
| ? | `linkedin_042_vs_linkedin_028` | 1 | 0.992 | LinkedIn does not share job hunting activities with employer... | LinkedIn sends network updates, reminders, job suggestions, ... |
| ? | `linkedin_042_vs_linkedin_029` | 6 | 1.000 | LinkedIn does not share job hunting activities with employer... | LinkedIn infers user attributes like industry, seniority, ag... |
| ? | `linkedin_042_vs_linkedin_031` | 3 | 1.000 | LinkedIn does not share job hunting activities with employer... | LinkedIn shares user profile data with third parties when al... |
| ? | `linkedin_042_vs_linkedin_032` | 3 | 0.990 | LinkedIn does not share personal messages with employers unl... | LinkedIn uses members' data and content for invitations and ... |
| ? | `linkedin_042_vs_linkedin_038` | 1 | 0.859 | LinkedIn does not share job hunting activities with employer... | LinkedIn uses data to investigate attempts to harm members, ... |
| ? | `linkedin_042_vs_linkedin_039` | 1 | 0.894 | LinkedIn does not share job hunting activities with employer... | LinkedIn uses user profile data and content posted on the se... |
| ? | `linkedin_042_vs_linkedin_041` | 1 | 0.995 | LinkedIn does not share job hunting activities with employer... | Employers can see how users utilize work-provided services a... |
| ? | `linkedin_042_vs_linkedin_043` | 1 | 0.966 | LinkedIn does not share personal messages with employers unl... | LinkedIn enables archiving of messages by and to regulated M... |
| ? | `linkedin_042_vs_linkedin_044` | 2 | 0.982 | LinkedIn does not share personal messages with employers unl... | Excerpts from user profiles appear on the services of others... |
| ? | `linkedin_042_vs_linkedin_045` | 6 | 0.995 | LinkedIn does not share job hunting activities with employer... | LinkedIn shares user data across different Services and Link... |
| ? | `linkedin_042_vs_linkedin_047` | 4 | 0.998 | LinkedIn does not share job hunting activities with employer... | LinkedIn shares user data with third parties when required b... |
| ? | `linkedin_042_vs_linkedin_048` | 4 | 0.997 | LinkedIn does not share job hunting activities with employer... | LinkedIn shares personal data when its business is sold to a... |
| ? | `linkedin_044_vs_linkedin_010` | 4 | 0.995 | Third-party services have their own privacy policies and may... | LinkedIn includes public information about users in notifica... |
| ? | `linkedin_044_vs_linkedin_011` | 1 | 0.844 | Information retained on third-party services may not reflect... | LinkedIn receives contact information when others associate ... |
| ? | `linkedin_044_vs_linkedin_018` | 1 | 0.855 | Users may revoke the link with third-party accounts.... | Organizations share personal data and user profile informati... |
| ? | `linkedin_044_vs_linkedin_022` | 2 | 0.981 | Third-party services have their own privacy policies and may... | LinkedIn uses your data to authorize access to its Services ... |
| ? | `linkedin_044_vs_linkedin_029` | 2 | 0.999 | Information retained on third-party services may not reflect... | LinkedIn associates user social actions on ads with their na... |
| ? | `linkedin_044_vs_linkedin_031` | 2 | 0.991 | Information retained on third-party services may not reflect... | LinkedIn shares user profile data with third parties when al... |
| ? | `linkedin_044_vs_linkedin_039` | 2 | 0.997 | Information retained on third-party services may not reflect... | Other users can see user profile data and content posted on ... |
| ? | `linkedin_044_vs_linkedin_041` | 1 | 0.993 | Users may revoke the link with third-party accounts.... | When users like, re-share or comment on content, others can ... |
| ? | `linkedin_044_vs_linkedin_047` | 1 | 0.981 | Users may revoke the link with third-party accounts.... | LinkedIn shares user data with third parties when required b... |
| ? | `linkedin_044_vs_linkedin_048` | 3 | 0.997 | Users may revoke the link with third-party accounts.... | Any entity acquiring LinkedIn or part of its business has th... |
| ? | `linkedin_045_vs_linkedin_010` | 1 | 0.883 | LinkedIn's data sharing with Affiliates is subject to the Eu... | Users and others may post content including information abou... |
| ? | `linkedin_045_vs_linkedin_041` | 1 | 0.982 | LinkedIn's data sharing with Affiliates is subject to the Eu... | Publicly shared articles or posts can be viewed by everyone ... |
| ? | `linkedin_045_vs_linkedin_048` | 1 | 0.993 | LinkedIn's data sharing with Affiliates is subject to the Eu... | Any entity acquiring LinkedIn or part of its business has th... |
| ? | `linkedin_046_vs_linkedin_010` | 1 | 0.997 | Third parties are obligated not to disclose or use user info... | Users and others may post content including information abou... |
| ? | `linkedin_046_vs_linkedin_012` | 1 | 0.612 | Third parties are obligated not to disclose or use user info... | LinkedIn receives personal data about users when they use se... |
| ? | `linkedin_046_vs_linkedin_029` | 2 | 0.999 | Third parties are obligated not to disclose or use user info... | LinkedIn shares user data with advertising partners, vendors... |
| ? | `linkedin_046_vs_linkedin_031` | 1 | 0.983 | Third parties are obligated not to disclose or use user info... | LinkedIn shares hashed IDs or device identifiers with advert... |
| ? | `linkedin_046_vs_linkedin_038` | 1 | 0.891 | Third parties are obligated not to disclose or use user info... | LinkedIn uses data to investigate attempts to harm members, ... |
| ? | `linkedin_046_vs_linkedin_039` | 1 | 0.991 | Third parties are obligated not to disclose or use user info... | Other users can see user profile data and content posted on ... |
| ? | `linkedin_046_vs_linkedin_040` | 1 | 0.594 | Third parties are obligated not to disclose or use user info... | User profiles can be visible to Visitors and third-party sea... |
| ? | `linkedin_046_vs_linkedin_041` | 2 | 0.999 | Third parties are obligated not to disclose or use user info... | Members, Visitors and others can find and see publicly-share... |
| ? | `linkedin_046_vs_linkedin_043` | 3 | 0.966 | Third parties are obligated not to disclose or use user info... | LinkedIn enables archiving of messages by and to regulated M... |
| ? | `linkedin_046_vs_linkedin_044` | 4 | 0.995 | Third parties are obligated not to disclose or use user info... | When users link their account with other services, personal ... |
| ? | `linkedin_046_vs_linkedin_045` | 3 | 0.996 | Third parties are obligated not to disclose or use user info... | LinkedIn shares personal data with Affiliates including Micr... |
| ? | `linkedin_046_vs_linkedin_047` | 1 | 0.896 | Third parties are obligated not to disclose or use user info... | LinkedIn shares data to exercise or protect the rights and s... |
| ? | `linkedin_046_vs_linkedin_048` | 2 | 1.000 | Third parties are obligated not to disclose or use user info... | Any entity acquiring LinkedIn or part of its business has th... |
| ? | `linkedin_047_vs_linkedin_007` | 1 | 0.964 | LinkedIn attempts to notify members about legal demands for ... | LinkedIn encourages users to create complete profiles to max... |
| ? | `linkedin_047_vs_linkedin_031` | 2 | 0.999 | LinkedIn attempts to notify members about legal demands for ... | LinkedIn shares user profile data with third parties when al... |
| ? | `linkedin_047_vs_linkedin_039` | 1 | 0.663 | LinkedIn attempts to notify members about legal demands for ... | LinkedIn uses user profile data and content posted on the se... |
| ? | `linkedin_047_vs_linkedin_042` | 1 | 0.998 | LinkedIn attempts to notify members about legal demands for ... | Sales Navigator users are asked to share their social sellin... |
| ? | `linkedin_047_vs_linkedin_048` | 2 | 0.993 | LinkedIn attempts to notify members about legal demands for ... | Any entity acquiring LinkedIn or part of its business has th... |
| ? | `linkedin_048_vs_linkedin_047` | 1 | 0.830 | An acquiring entity may only use shared data in the manner s... | LinkedIn shares user data with third parties when required b... |
| ? | `linkedin_055_vs_linkedin_010` | 2 | 0.996 | LinkedIn does not share personal data with third parties for... | LinkedIn makes collected public information about users avai... |
| ? | `linkedin_055_vs_linkedin_011` | 1 | 0.504 | LinkedIn does not share personal data with third parties for... | LinkedIn receives contact information when others send messa... |
| ? | `linkedin_055_vs_linkedin_012` | 1 | 0.977 | LinkedIn does not share personal data with third parties for... | LinkedIn receives personal data about users when they use se... |
| ? | `linkedin_055_vs_linkedin_019` | 1 | 0.996 | LinkedIn does not share personal data with third parties for... | LinkedIn uses collected data for advertising purposes.... |
| ? | `linkedin_055_vs_linkedin_021` | 1 | 0.703 | LinkedIn does not share personal data with third parties for... | LinkedIn makes inferences about user characteristics includi... |
| ? | `linkedin_055_vs_linkedin_029` | 4 | 0.998 | LinkedIn does not share personal data with third parties for... | LinkedIn associates user social actions on ads with their na... |
| ? | `linkedin_055_vs_linkedin_030` | 1 | 0.776 | LinkedIn does not share personal data with third parties for... | LinkedIn uses cookies and tracking elements to show users mo... |
| ? | `linkedin_055_vs_linkedin_031` | 2 | 0.982 | LinkedIn does not share personal data with third parties for... | Advertising partners can associate personal data collected d... |
| ? | `linkedin_055_vs_linkedin_032` | 3 | 0.997 | LinkedIn does not share personal data with third parties for... | LinkedIn uses members' data and content for communications p... |
| ? | `linkedin_055_vs_linkedin_038` | 1 | 0.961 | LinkedIn does not share personal data with third parties for... | LinkedIn uses data to investigate attempts to harm members, ... |
| ? | `linkedin_055_vs_linkedin_043` | 1 | 0.804 | LinkedIn does not share personal data with third parties for... | LinkedIn enables archiving of messages by and to regulated M... |
| ? | `linkedin_055_vs_linkedin_044` | 1 | 0.998 | LinkedIn does not share personal data with third parties for... | When users link their account with other services, personal ... |
| ? | `linkedin_055_vs_linkedin_045` | 1 | 0.995 | LinkedIn does not share personal data with third parties for... | LinkedIn shares user data across different Services and Link... |
| ? | `linkedin_055_vs_linkedin_047` | 1 | 0.996 | LinkedIn does not share personal data with third parties for... | LinkedIn shares user data with third parties when required b... |
| ? | `linkedin_055_vs_linkedin_048` | 1 | 0.996 | LinkedIn does not share personal data with third parties for... | Any entity acquiring LinkedIn or part of its business has th... |
| ? | `microsoft_007_vs_microsoft_011` | 5 | 1.000 | Vendors and agents receiving personal data from Microsoft mu... | Third parties can use or share data received from Microsoft ... |
| ? | `microsoft_007_vs_microsoft_012` | 1 | 0.904 | Microsoft may refer matters involving stolen property to law... | Game and app publishers receive data about a child's in-game... |
| ? | `microsoft_007_vs_microsoft_018` | 2 | 0.998 | Vendors and agents are not allowed to use personal data rece... | Third parties can access and use the advertising ID in Windo... |
| ? | `microsoft_007_vs_microsoft_019` | 1 | 0.994 | Vendors and agents are not allowed to use personal data rece... | Microsoft employees and vendors review voice data snippets t... |
| ? | `microsoft_007_vs_microsoft_022` | 1 | 0.909 | Vendors and agents are not allowed to use personal data rece... | Microsoft Copilot appears as an assistant in third-party pro... |
| ? | `microsoft_007_vs_microsoft_023` | 3 | 0.999 | Microsoft may refer matters involving stolen property to law... | Microsoft uses customer-provided information to perform requ... |
| ? | `microsoft_007_vs_microsoft_030` | 1 | 0.877 | Microsoft may refer matters involving stolen property to law... | Microsoft shares user information with Enterprise customers ... |
| ? | `microsoft_007_vs_microsoft_033` | 3 | 0.997 | Vendors and agents receiving personal data from Microsoft mu... | Microsoft may access, transfer, disclose, and preserve user ... |
| ? | `microsoft_007_vs_microsoft_036` | 1 | 0.734 | Vendors and agents receiving personal data from Microsoft mu... | Bing receives search queries and related data from third-par... |
| ? | `microsoft_007_vs_microsoft_046` | 1 | 0.565 | Vendors and agents are not allowed to use personal data rece... | Microsoft shares feedback and collected data with partners l... |
| ? | `microsoft_007_vs_microsoft_049` | 1 | 0.987 | Vendors and agents are not allowed to use personal data rece... | Third-party apps may use alternative technologies to determi... |
| ? | `microsoft_007_vs_microsoft_062` | 3 | 0.997 | Vendors and agents are not allowed to use personal data rece... | Game and app publishers receive access to your Xbox user ide... |
| ? | `microsoft_008_vs_microsoft_007` | 5 | 0.976 | Users can control third-party data collection using Tracking... | Microsoft shares content with third parties when users send ... |
| ? | `microsoft_008_vs_microsoft_018` | 2 | 0.804 | Users can control third-party data collection using Tracking... | Third parties can access and use the advertising ID in Windo... |
| ? | `microsoft_008_vs_microsoft_042` | 1 | 0.863 | Users can control data stored by cookies using browser-based... | Windows generates a unique advertising ID for each person us... |
| ? | `microsoft_008_vs_microsoft_062` | 1 | 0.989 | Users can control third-party data collection using Tracking... | Your gamertag, game statistics, achievements, and activity a... |
| ? | `microsoft_009_vs_microsoft_002` | 3 | 0.996 | Microsoft prohibits analytics providers from using web beaco... | Microsoft uses cookies to analyze site operations.... |
| ? | `microsoft_009_vs_microsoft_007` | 5 | 0.999 | Microsoft prohibits analytics providers from using web beaco... | Microsoft discloses personal data to prevent spam, fraud, an... |
| ? | `microsoft_009_vs_microsoft_018` | 3 | 1.000 | Microsoft prohibits analytics providers from using web beaco... | Microsoft combines cookies on devices with IP address and br... |
| ? | `microsoft_009_vs_microsoft_028` | 1 | 1.000 | Microsoft prohibits analytics providers from using web beaco... | Microsoft collects location data when Location Sharing, Driv... |
| ? | `microsoft_009_vs_microsoft_033` | 1 | 0.998 | Microsoft prohibits analytics providers from using web beaco... | Microsoft may access, transfer, disclose, and preserve user ... |
| ? | `microsoft_009_vs_microsoft_040` | 1 | 0.754 | Microsoft prohibits analytics providers from using web beaco... | Microsoft uses device identifiers and location data for frau... |
| ? | `microsoft_009_vs_microsoft_041` | 2 | 0.999 | Microsoft prohibits analytics providers from using web beaco... | Microsoft collects activity history tracking apps, services,... |
| ? | `microsoft_009_vs_microsoft_042` | 1 | 0.999 | Microsoft prohibits analytics providers from using web beaco... | Windows generates a unique advertising ID for each person us... |
| ? | `microsoft_009_vs_microsoft_044` | 1 | 0.999 | Microsoft prohibits analytics providers from using web beaco... | Microsoft collects optional diagnostic data including browsi... |
| ? | `microsoft_009_vs_microsoft_045` | 3 | 0.999 | Microsoft prohibits analytics providers from using web beaco... | Microsoft uses device information and Windows diagnostic dat... |
| ? | `microsoft_009_vs_microsoft_057` | 1 | 0.999 | Microsoft prohibits analytics providers from using web beaco... | Microsoft Edge sends information typed into the address bar ... |
| ? | `microsoft_011_vs_microsoft_007` | 7 | 0.999 | Microsoft is not responsible for the privacy or security pra... | Microsoft discloses personal data to operate and maintain se... |
| ? | `microsoft_011_vs_microsoft_023` | 1 | 0.808 | Microsoft recommends users carefully review privacy statemen... | Microsoft collects customer name and contact data when engag... |
| ? | `microsoft_011_vs_microsoft_024` | 1 | 0.837 | Microsoft is not responsible for the privacy or security pra... | Microsoft acts as a data controller for Personal Data proces... |
| ? | `microsoft_011_vs_microsoft_036` | 1 | 0.997 | Microsoft allows users to sign in to some products without p... | Microsoft collects website addresses visited by users partic... |
| ? | `microsoft_011_vs_microsoft_038` | 2 | 0.998 | Microsoft recommends users carefully review privacy statemen... | Microsoft deletes identifiers and certain text like email ad... |
| ? | `microsoft_011_vs_microsoft_045` | 1 | 0.999 | Microsoft allows users to sign in to some products without p... | Microsoft uses contextual device data and basic account data... |
| ? | `microsoft_011_vs_microsoft_049` | 2 | 0.999 | Microsoft recommends users carefully review privacy statemen... | Microsoft removes identifying data from location information... |
| ? | `microsoft_011_vs_microsoft_051` | 2 | 0.883 | Microsoft is not responsible for the privacy or security pra... | Android contacts are synced to Microsoft cloud and stored on... |
| ? | `microsoft_011_vs_microsoft_054` | 1 | 0.636 | Microsoft allows users to sign in to some products without p... | Microsoft collects voice recordings to provide speech recogn... |
| ? | `microsoft_011_vs_microsoft_062` | 1 | 0.927 | Microsoft is not responsible for the privacy or security pra... | Microsoft collects and reviews voice, text, images, videos, ... |
| ? | `microsoft_011_vs_microsoft_063` | 1 | 0.908 | Microsoft allows users to sign in to some products without p... | Your name and picture from your Microsoft account are publis... |
| ? | `microsoft_012_vs_microsoft_007` | 5 | 0.996 | Microsoft will not knowingly ask children under 13 to provid... | Microsoft discloses personal data to prevent spam, fraud, an... |
| ? | `microsoft_012_vs_microsoft_011` | 1 | 0.952 | Microsoft will not knowingly ask children under 13 to provid... | Organization domain owners may control, administer, and acce... |
| ? | `microsoft_012_vs_microsoft_023` | 2 | 0.981 | Microsoft will not knowingly ask children under 13 to provid... | Microsoft collects customer name and contact data when engag... |
| ? | `microsoft_012_vs_microsoft_024` | 1 | 0.997 | Kinect facial recognition data stays on the console, is not ... | Bing Search Services use search query data as described in t... |
| ? | `microsoft_012_vs_microsoft_028` | 2 | 1.000 | Kinect facial recognition data stays on the console, is not ... | Microsoft uploads location data to the cloud and shares it w... |
| ? | `microsoft_012_vs_microsoft_029` | 1 | 0.997 | Kinect facial recognition data stays on the console, is not ... | Microsoft Launcher syncs Glance data across devices signed i... |
| ? | `microsoft_012_vs_microsoft_036` | 1 | 0.994 | Kinect facial recognition data stays on the console, is not ... | Microsoft collects images provided by users when they use Bi... |
| ? | `microsoft_012_vs_microsoft_037` | 2 | 0.998 | Kinect facial recognition data stays on the console, is not ... | Microsoft Edge de-identifies collected search data by removi... |
| ? | `microsoft_012_vs_microsoft_038` | 2 | 0.988 | Xbox's AI-enhanced features do not use children's data for m... | Microsoft uses submitted data to personalize user experience... |
| ? | `microsoft_012_vs_microsoft_039` | 1 | 0.999 | Kinect facial recognition data stays on the console, is not ... | SwiftKey collects de-identified device and usage data to hel... |
| ? | `microsoft_012_vs_microsoft_045` | 2 | 0.996 | Xbox's AI-enhanced features do not use children's data for m... | Microsoft uses optional diagnostic data about app usage and ... |
| ? | `microsoft_012_vs_microsoft_049` | 1 | 1.000 | Kinect facial recognition data stays on the console, is not ... | Microsoft removes identifying data from location information... |
| ? | `microsoft_012_vs_microsoft_051` | 1 | 0.845 | Kinect facial recognition data stays on the console, is not ... | Photos are temporarily stored on Windows device and removed ... |
| ? | `microsoft_012_vs_microsoft_058` | 1 | 1.000 | Kinect facial recognition data stays on the console, is not ... | Click to Do captures and analyzes screenshots to identify te... |
| ? | `microsoft_012_vs_microsoft_062` | 3 | 0.995 | Kinect facial recognition data stays on the console, is not ... | Microsoft collects content you add, upload, or share through... |
| ? | `microsoft_015_vs_microsoft_011` | 1 | 0.994 | Microsoft processes collected data according to privacy stat... | Service providers have control over third-party Microsoft ac... |
| ? | `microsoft_015_vs_microsoft_040` | 1 | 0.998 | Microsoft processes collected data according to privacy stat... | Microsoft collects product keys when Windows is activated on... |
| ? | `microsoft_015_vs_microsoft_044` | 1 | 0.512 | Microsoft processes collected data according to privacy stat... | Microsoft collects optional diagnostic data including browsi... |
| ? | `microsoft_015_vs_microsoft_045` | 1 | 0.766 | Microsoft processes collected data according to privacy stat... | Microsoft uses contextual device data and basic account data... |
| ? | `microsoft_015_vs_microsoft_062` | 1 | 0.994 | Microsoft processes collected data according to privacy stat... | Microsoft collects content you add, upload, or share through... |
| ? | `microsoft_015_vs_microsoft_065` | 1 | 0.912 | Microsoft processes collected data according to privacy stat... | Silverlight requests media usage rights from a rights server... |
| ? | `microsoft_018_vs_microsoft_007` | 10 | 1.000 | Microsoft does not use email, chat, video calls, voicemail, ... | Microsoft discloses personal data to prevent spam, fraud, an... |
| ? | `microsoft_018_vs_microsoft_008` | 1 | 0.992 | Microsoft retains personalized advertising data for no more ... | Opt-out cookie for personalized advertising has expiration d... |
| ? | `microsoft_018_vs_microsoft_009` | 2 | 0.989 | Microsoft Advertising does not collect sensitive data under ... | Microsoft records user decisions not to receive interest-bas... |
| ? | `microsoft_018_vs_microsoft_011` | 10 | 0.995 | Microsoft does not deliver personalized advertising to child... | Microsoft displays user name, username, and profile photo in... |
| ? | `microsoft_018_vs_microsoft_012` | 3 | 0.998 | Microsoft does not use email, chat, video calls, voicemail, ... | Microsoft collects content a child adds, uploads, or shares ... |
| ? | `microsoft_018_vs_microsoft_015` | 1 | 0.899 | Microsoft Advertising does not collect sensitive data under ... | Microsoft stores and processes personal data in customer's r... |
| ? | `microsoft_018_vs_microsoft_019` | 1 | 0.590 | Microsoft does not use email, chat, video calls, voicemail, ... | Microsoft integrates speech recognition technologies into ma... |
| ? | `microsoft_018_vs_microsoft_022` | 2 | 0.998 | Microsoft does not use email, chat, video calls, voicemail, ... | Microsoft Copilot uses prior conversation history to persona... |
| ? | `microsoft_018_vs_microsoft_023` | 5 | 0.999 | Microsoft does not use email, chat, video calls, voicemail, ... | Microsoft uses customer data to personalize communication co... |
| ? | `microsoft_018_vs_microsoft_024` | 8 | 0.999 | Microsoft retains personalized advertising data for no more ... | Microsoft uses Payment Data to complete transactions and det... |
| ? | `microsoft_018_vs_microsoft_027` | 2 | 0.979 | Microsoft retains personalized advertising data for no more ... | Essential services like the licensing service cannot be disa... |
| ? | `microsoft_018_vs_microsoft_028` | 1 | 0.980 | Microsoft does not use email, chat, video calls, voicemail, ... | Microsoft collects details about how children use their devi... |
| ? | `microsoft_018_vs_microsoft_029` | 6 | 0.999 | Microsoft does not use email, chat, video calls, voicemail, ... | Microsoft Launcher uses account information to provide perso... |
| ? | `microsoft_018_vs_microsoft_030` | 2 | 0.927 | Microsoft does not use email, chat, video calls, voicemail, ... | Microsoft can send SMS or email invitations on behalf of use... |
| ? | `microsoft_018_vs_microsoft_032` | 2 | 0.785 | Microsoft does not use email, chat, video calls, voicemail, ... | Outlook.com email accounts end in outlook.com, live.com, hot... |
| ? | `microsoft_018_vs_microsoft_033` | 3 | 0.998 | Microsoft retains personalized advertising data for no more ... | Required diagnostic data is always sent to Microsoft for all... |
| ? | `microsoft_018_vs_microsoft_036` | 3 | 0.997 | Microsoft does not use email, chat, video calls, voicemail, ... | Microsoft collects words, phrases, and surrounding content w... |
| ? | `microsoft_018_vs_microsoft_037` | 1 | 0.986 | Microsoft retains personalized advertising data for no more ... | Microsoft Edge de-identifies collected search data by removi... |
| ? | `microsoft_018_vs_microsoft_038` | 5 | 0.996 | Microsoft Advertising does not collect sensitive data under ... | Microsoft uses submitted data to personalize user experience... |
| ? | `microsoft_018_vs_microsoft_039` | 3 | 0.999 | Microsoft does not use email, chat, video calls, voicemail, ... | Windows collects data about you, your device, and how you us... |
| ? | `microsoft_018_vs_microsoft_040` | 7 | 0.986 | Microsoft retains personalized advertising data for no more ... | Microsoft uses device identifiers and location data for stoc... |
| ? | `microsoft_018_vs_microsoft_044` | 2 | 0.999 | Microsoft retains personalized advertising data for no more ... | Microsoft collects basic error reporting data about operatin... |
| ? | `microsoft_018_vs_microsoft_045` | 20 | 1.000 | Microsoft does not deliver personalized advertising to child... | Microsoft uses Windows diagnostic data to offer personalized... |
| ? | `microsoft_018_vs_microsoft_049` | 4 | 1.000 | Microsoft retains personalized advertising data for no more ... | Microsoft removes identifying data from location information... |
| ? | `microsoft_018_vs_microsoft_051` | 1 | 0.722 | Microsoft does not use email, chat, video calls, voicemail, ... | Phone Link accesses content of text messages and contact inf... |
| ? | `microsoft_018_vs_microsoft_053` | 4 | 0.997 | Microsoft Advertising does not collect sensitive data under ... | When Microsoft Defender SmartScreen checks web and app conte... |
| ? | `microsoft_018_vs_microsoft_054` | 1 | 0.998 | Microsoft does not use email, chat, video calls, voicemail, ... | Windows actively listens to the microphone for app-specific ... |
| ? | `microsoft_018_vs_microsoft_055` | 1 | 0.997 | Microsoft does not use email, chat, video calls, voicemail, ... | Microsoft uses stored settings, files, and device configurat... |
| ? | `microsoft_018_vs_microsoft_058` | 1 | 0.999 | Microsoft does not use email, chat, video calls, voicemail, ... | Click to Do captures and analyzes screenshots to identify te... |
| ? | `microsoft_018_vs_microsoft_062` | 6 | 0.999 | Microsoft does not use email, chat, video calls, voicemail, ... | Microsoft collects content you add, upload, or share through... |
| ? | `microsoft_018_vs_microsoft_063` | 7 | 0.999 | Microsoft does not deliver personalized advertising to child... | Your name and picture from your Microsoft account are publis... |
| ? | `microsoft_018_vs_microsoft_064` | 4 | 0.998 | Microsoft does not use email, chat, video calls, voicemail, ... | Microsoft uses collected data to provide personalized and re... |
| ? | `microsoft_022_vs_microsoft_007` | 4 | 0.999 | Microsoft 365 Copilot for enterprise provides enterprise-gra... | Microsoft discloses personal data to protect its rights and ... |
| ? | `microsoft_022_vs_microsoft_012` | 6 | 1.000 | Microsoft 365 Copilot for enterprise provides enterprise-gra... | Microsoft uses voice-to-text data from Xbox party chat to pr... |
| ? | `microsoft_022_vs_microsoft_018` | 1 | 0.801 | Microsoft 365 Copilot for enterprise provides enterprise-gra... | Microsoft selects ads based on interests, location, transact... |
| ? | `microsoft_022_vs_microsoft_019` | 1 | 0.994 | Microsoft 365 Copilot for enterprise provides enterprise-gra... | Microsoft uses voice data to build and improve speech recogn... |
| ? | `microsoft_022_vs_microsoft_023` | 2 | 0.998 | Microsoft's collection and use of personal data in developin... | Microsoft collects organization information during customer ... |
| ? | `microsoft_022_vs_microsoft_024` | 8 | 0.998 | Microsoft 365 Copilot for enterprise provides enterprise-gra... | Microsoft uses Administrator Data to contact customers about... |
| ? | `microsoft_022_vs_microsoft_027` | 1 | 0.789 | Microsoft 365 Copilot for enterprise provides enterprise-gra... | Microsoft 365 apps and To Do and Whiteboard access user cont... |
| ? | `microsoft_022_vs_microsoft_028` | 1 | 0.977 | Microsoft 365 Copilot for enterprise provides enterprise-gra... | Microsoft collects details about how children use their devi... |
| ? | `microsoft_022_vs_microsoft_029` | 3 | 0.999 | Microsoft 365 Copilot for enterprise provides enterprise-gra... | Microsoft Launcher collects location data or zip code to pro... |
| ? | `microsoft_022_vs_microsoft_030` | 2 | 0.710 | Microsoft's collection and use of personal data in developin... | Microsoft processes non-user contact data to determine Teams... |
| ? | `microsoft_022_vs_microsoft_031` | 2 | 0.992 | Microsoft 365 Copilot for enterprise provides enterprise-gra... | OneDrive for Business collects and transmits personal data i... |
| ? | `microsoft_022_vs_microsoft_032` | 2 | 0.993 | Microsoft 365 Copilot for enterprise provides enterprise-gra... | Outlook uses device location information to provide weather ... |
| ? | `microsoft_022_vs_microsoft_034` | 2 | 1.000 | Microsoft 365 Copilot for enterprise provides enterprise-gra... | Surface Duo collects required diagnostic data representing t... |
| ? | `microsoft_022_vs_microsoft_036` | 2 | 0.967 | Microsoft 365 Copilot for enterprise provides enterprise-gra... | Microsoft collects website addresses visited by users partic... |
| ? | `microsoft_022_vs_microsoft_037` | 11 | 0.999 | Microsoft 365 Copilot for enterprise provides enterprise-gra... | Microsoft Edge de-identifies collected search data by removi... |
| ? | `microsoft_022_vs_microsoft_038` | 4 | 1.000 | Microsoft 365 Copilot for enterprise provides enterprise-gra... | Microsoft Translator processes device and usage data from us... |
| ? | `microsoft_022_vs_microsoft_040` | 4 | 1.000 | Microsoft 365 Copilot for enterprise provides enterprise-gra... | Microsoft uses device identifiers and location data for stoc... |
| ? | `microsoft_022_vs_microsoft_044` | 3 | 0.998 | Microsoft 365 Copilot for enterprise provides enterprise-gra... | Microsoft collects basic error reporting data about operatin... |
| ? | `microsoft_022_vs_microsoft_045` | 2 | 0.896 | Microsoft 365 Copilot for enterprise provides enterprise-gra... | Microsoft uses contextual device data and basic account data... |
| ? | `microsoft_022_vs_microsoft_049` | 2 | 0.999 | Microsoft 365 Copilot for enterprise provides enterprise-gra... | Microsoft removes identifying data from location information... |
| ? | `microsoft_022_vs_microsoft_051` | 1 | 0.964 | Microsoft 365 Copilot for enterprise provides enterprise-gra... | Microsoft uses cloud service to relay files for inserting ph... |
| ? | `microsoft_022_vs_microsoft_054` | 1 | 0.974 | Microsoft 365 Copilot for enterprise provides enterprise-gra... | Microsoft collects voice recordings to provide speech recogn... |
| ? | `microsoft_022_vs_microsoft_057` | 3 | 0.999 | Microsoft 365 Copilot for enterprise provides enterprise-gra... | Microsoft Edge syncs favorites, reading lists, autofill form... |
| ? | `microsoft_022_vs_microsoft_061` | 2 | 0.999 | Microsoft 365 Copilot for enterprise provides enterprise-gra... | Microsoft uses collected data from Windows Search to provide... |
| ? | `microsoft_022_vs_microsoft_062` | 5 | 0.965 | Microsoft's AI deployment and use is subject to Microsoft's ... | Microsoft offers optional AI-enhanced features including Sup... |
| ? | `microsoft_022_vs_microsoft_064` | 2 | 0.992 | Microsoft 365 Copilot for enterprise provides enterprise-gra... | Microsoft uses location data to provide relevant local weath... |
| ? | `microsoft_023_vs_microsoft_011` | 1 | 0.997 | In conflicts between privacy statement and customer agreemen... | Service providers have control over third-party Microsoft ac... |
| ? | `microsoft_024_vs_microsoft_007` | 9 | 0.999 | Microsoft will not share confidential or contact information... | Microsoft sends data to third-party notification providers t... |
| ? | `microsoft_024_vs_microsoft_011` | 5 | 0.999 | Microsoft will not share confidential or contact information... | Microsoft passes payment information to third parties or ven... |
| ? | `microsoft_024_vs_microsoft_012` | 2 | 0.945 | Microsoft uses Personal Data in the least identifiable form ... | Microsoft assigns a unique identifier to a child's device wh... |
| ? | `microsoft_024_vs_microsoft_018` | 2 | 0.997 | Microsoft will not share confidential or contact information... | Microsoft shares reports with advertisers about data collect... |
| ? | `microsoft_024_vs_microsoft_022` | 1 | 0.788 | Microsoft uses Personal Data in the least identifiable form ... | Microsoft Copilot uses prompts, location, language, and user... |
| ? | `microsoft_024_vs_microsoft_029` | 1 | 0.984 | Microsoft uses Personal Data in the least identifiable form ... | Microsoft Launcher collects location data or zip code to pro... |
| ? | `microsoft_024_vs_microsoft_030` | 3 | 0.999 | Microsoft uses Personal Data in the least identifiable form ... | Microsoft processes non-user contact data to determine Teams... |
| ? | `microsoft_024_vs_microsoft_033` | 1 | 0.985 | Microsoft will not share confidential or contact information... | Microsoft may access, transfer, disclose, and preserve user ... |
| ? | `microsoft_024_vs_microsoft_034` | 1 | 0.998 | Microsoft will not share confidential or contact information... | Microsoft shares location data with Google to enable locatio... |
| ? | `microsoft_024_vs_microsoft_039` | 1 | 0.978 | Microsoft uses Personal Data in the least identifiable form ... | Windows uses physical MAC address, IMEI and mobile number fo... |
| ? | `microsoft_024_vs_microsoft_040` | 3 | 0.986 | Microsoft uses Personal Data in the least identifiable form ... | Microsoft uses device identifiers and location data for stoc... |
| ? | `microsoft_024_vs_microsoft_044` | 2 | 0.998 | Microsoft uses Personal Data in the least identifiable form ... | Microsoft collects network data including IP address, mobile... |
| ? | `microsoft_024_vs_microsoft_045` | 1 | 0.991 | Microsoft uses Personal Data in the least identifiable form ... | Microsoft transmits Tailored experiences data to Microsoft s... |
| ? | `microsoft_024_vs_microsoft_046` | 1 | 0.994 | Microsoft will not share confidential or contact information... | Microsoft shares feedback and collected data with partners l... |
| ? | `microsoft_024_vs_microsoft_049` | 2 | 1.000 | Customer is the controller of Personal Data and Microsoft is... | Microsoft retains only the last known location, with each ne... |
| ? | `microsoft_024_vs_microsoft_054` | 1 | 0.746 | Microsoft uses Personal Data in the least identifiable form ... | Microsoft collects voice recordings to provide speech recogn... |
| ? | `microsoft_024_vs_microsoft_062` | 2 | 0.984 | Microsoft uses Personal Data in the least identifiable form ... | Microsoft collects social activity data including chat, inte... |
| ? | `microsoft_024_vs_microsoft_063` | 1 | 0.994 | Microsoft uses Personal Data in the least identifiable form ... | Your name and picture from your Microsoft account are publis... |
| ? | `microsoft_024_vs_microsoft_064` | 2 | 0.996 | Microsoft uses Personal Data in the least identifiable form ... | Microsoft uses location data to provide relevant local weath... |
| ? | `microsoft_025_vs_microsoft_011` | 4 | 1.000 | HoloLens iris authentication data stays on the device and is... | Microsoft makes account information available across product... |
| ? | `microsoft_025_vs_microsoft_012` | 2 | 1.000 | HoloLens hand gesture data is processed on the device and is... | Kinect sensor maps body joint distances to create a stick fi... |
| ? | `microsoft_025_vs_microsoft_019` | 1 | 0.974 | HoloLens hand gesture data is processed on the device and is... | Microsoft collects voice data through device-based and cloud... |
| ? | `microsoft_025_vs_microsoft_023` | 1 | 0.551 | HoloLens hand gesture data is processed on the device and is... | Microsoft collects device and usage data from customers inte... |
| ? | `microsoft_025_vs_microsoft_024` | 2 | 1.000 | HoloLens environmental tracking data contains no images and ... | Bing Search Services use search query data as described in t... |
| ? | `microsoft_025_vs_microsoft_027` | 2 | 1.000 | HoloLens iris authentication data stays on the device and is... | Office Roaming Service removes settings from a device when u... |
| ? | `microsoft_025_vs_microsoft_028` | 4 | 1.000 | HoloLens iris authentication data stays on the device and is... | Microsoft uploads location data to the cloud and shares it w... |
| ? | `microsoft_025_vs_microsoft_029` | 5 | 1.000 | HoloLens iris authentication data stays on the device and is... | Microsoft Launcher syncs Glance data across devices signed i... |
| ? | `microsoft_025_vs_microsoft_030` | 3 | 0.965 | HoloLens iris authentication data stays on the device and is... | Microsoft stores non-user contact information on servers whi... |
| ? | `microsoft_025_vs_microsoft_031` | 1 | 0.998 | HoloLens environmental tracking data contains no images and ... | OneDrive uses location information to enable users to search... |
| ? | `microsoft_025_vs_microsoft_032` | 2 | 0.997 | HoloLens environmental tracking data contains no images and ... | Outlook uses device location information to provide weather ... |
| ? | `microsoft_025_vs_microsoft_033` | 4 | 1.000 | HoloLens hand gesture data is processed on the device and is... | Microsoft collects usage data about Skype communications inc... |
| ? | `microsoft_025_vs_microsoft_034` | 3 | 1.000 | HoloLens hand gesture data is processed on the device and is... | Surface Duo uses Google location services to determine devic... |
| ? | `microsoft_025_vs_microsoft_036` | 3 | 1.000 | HoloLens hand gesture data is processed on the device and is... | Microsoft collects voice input and performance data when use... |
| ? | `microsoft_025_vs_microsoft_037` | 11 | 1.000 | HoloLens iris authentication data stays on the device and is... | Microsoft Edge syncs browser data across signed-in devices w... |
| ? | `microsoft_025_vs_microsoft_038` | 1 | 0.999 | HoloLens iris authentication data stays on the device and is... | Microsoft Translator processes device and usage data from us... |
| ? | `microsoft_025_vs_microsoft_039` | 7 | 1.000 | HoloLens iris authentication data stays on the device and is... | SwiftKey collects de-identified device and usage data to hel... |
| ? | `microsoft_025_vs_microsoft_040` | 4 | 1.000 | HoloLens hand gesture data is processed on the device and is... | Microsoft collects device location from Windows phones at fi... |
| ? | `microsoft_025_vs_microsoft_044` | 2 | 0.999 | HoloLens hand gesture data is processed on the device and is... | Microsoft collects device information including processor ty... |
| ? | `microsoft_025_vs_microsoft_045` | 3 | 0.999 | Customers have choices about the data they provide to enterp... | Microsoft uses contextual device data and basic account data... |
| ? | `microsoft_025_vs_microsoft_046` | 3 | 1.000 | HoloLens environmental tracking data contains no images and ... | For HoloLens, Feedback Hub uses your camera and microphone w... |
| ? | `microsoft_025_vs_microsoft_049` | 3 | 0.999 | HoloLens environmental tracking data contains no images and ... | Microsoft uploads device location to the cloud when signed i... |
| ? | `microsoft_025_vs_microsoft_051` | 1 | 0.999 | HoloLens hand gesture data is processed on the device and is... | Microsoft collects performance, usage, and device data inclu... |
| ? | `microsoft_025_vs_microsoft_052` | 1 | 0.638 | HoloLens hand gesture data is processed on the device and is... | Microsoft collects performance usage and device data, includ... |
| ? | `microsoft_025_vs_microsoft_053` | 2 | 0.943 | HoloLens iris authentication data stays on the device and is... | When Family activity reporting is turned on for a child, Mic... |
| ? | `microsoft_025_vs_microsoft_055` | 3 | 1.000 | HoloLens environmental tracking data contains no images and ... | Windows stores settings, files, and device configuration dat... |
| ? | `microsoft_025_vs_microsoft_057` | 5 | 1.000 | HoloLens iris authentication data stays on the device and is... | Microsoft Edge syncs favorites, reading lists, autofill form... |
| ? | `microsoft_025_vs_microsoft_058` | 2 | 1.000 | HoloLens hand gesture data is processed on the device and is... | Click to Do captures and analyzes screenshots to identify te... |
| ? | `microsoft_025_vs_microsoft_060` | 4 | 1.000 | HoloLens environmental tracking data contains no images and ... | Windows Hello extracts unique points or features from biomet... |
| ? | `microsoft_025_vs_microsoft_062` | 7 | 1.000 | HoloLens hand gesture data is processed on the device and is... | Microsoft stores offline Xbox usage data on device storage a... |
| ? | `microsoft_025_vs_microsoft_066` | 1 | 0.994 | HoloLens hand gesture data is processed on the device and is... | Microsoft collects numeric body joint mapping values from in... |
| ? | `microsoft_027_vs_microsoft_007` | 2 | 0.995 | Users can configure connected experiences through privacy co... | Microsoft shares personal data with third parties when users... |
| ? | `microsoft_027_vs_microsoft_011` | 9 | 1.000 | Diagnostic data does not include user names, email addresses... | Microsoft collects credentials, name, contact data, payment ... |
| ? | `microsoft_027_vs_microsoft_012` | 12 | 0.999 | Text and translations from connected experiences are not sto... | Microsoft collects content a child adds, uploads, or shares ... |
| ? | `microsoft_027_vs_microsoft_015` | 1 | 0.996 | Text and translations from connected experiences are not sto... | Microsoft stores and processes personal data in customer's r... |
| ? | `microsoft_027_vs_microsoft_018` | 1 | 0.648 | Text and translations from connected experiences are not sto... | Microsoft serves personalized ads based on online activity w... |
| ? | `microsoft_027_vs_microsoft_019` | 2 | 0.996 | Text and translations from connected experiences are not sto... | Microsoft transcribes voice data into text using speech reco... |
| ? | `microsoft_027_vs_microsoft_022` | 2 | 0.993 | Text and translations from connected experiences are not sto... | Microsoft uses conversation data to train generative AI mode... |
| ? | `microsoft_027_vs_microsoft_023` | 8 | 1.000 | Diagnostic data does not include user names, email addresses... | Microsoft collects customer name and contact data when engag... |
| ? | `microsoft_027_vs_microsoft_024` | 10 | 0.998 | Users can configure connected experiences through privacy co... | Microsoft relies on statistical and aggregate pseudonymized ... |
| ? | `microsoft_027_vs_microsoft_028` | 4 | 0.998 | Copilot in Microsoft 365 uses file content only when users a... | Microsoft uses location data to record drive habits includin... |
| ? | `microsoft_027_vs_microsoft_029` | 5 | 0.998 | Copilot in Microsoft 365 uses file content only when users a... | Microsoft Launcher collects location data or zip code to pro... |
| ? | `microsoft_027_vs_microsoft_030` | 2 | 0.992 | Text and translations from connected experiences are not sto... | Microsoft collects data about Teams feature usage and commun... |
| ? | `microsoft_027_vs_microsoft_031` | 2 | 0.999 | Diagnostic data does not include user names, email addresses... | OneDrive for Business collects and transmits personal data i... |
| ? | `microsoft_027_vs_microsoft_032` | 2 | 0.998 | Applications do not access device capabilities until users b... | Mail, calendar items, files, contacts, and settings automati... |
| ? | `microsoft_027_vs_microsoft_033` | 5 | 0.998 | Diagnostic data does not include user names, email addresses... | Required diagnostic data is always sent to Microsoft for all... |
| ? | `microsoft_027_vs_microsoft_036` | 7 | 1.000 | Text and translations from connected experiences are not sto... | Microsoft collects words, phrases, and surrounding content w... |
| ? | `microsoft_027_vs_microsoft_037` | 11 | 1.000 | Text and translations from connected experiences are not sto... | Microsoft Edge caches content collected into collections on ... |
| ? | `microsoft_027_vs_microsoft_038` | 5 | 0.968 | Users can configure connected experiences through privacy co... | Microsoft Translator processes device and usage data from us... |
| ? | `microsoft_027_vs_microsoft_039` | 2 | 1.000 | Text and translations from connected experiences are not sto... | SwiftKey draws language model data from all scenarios where ... |
| ? | `microsoft_027_vs_microsoft_040` | 7 | 1.000 | Users can configure connected experiences through privacy co... | Microsoft collects device and network identifiers from Windo... |
| ? | `microsoft_027_vs_microsoft_043` | 1 | 0.996 | Users can configure connected experiences through privacy co... | Microsoft collects device and SIM card identifiers when user... |
| ? | `microsoft_027_vs_microsoft_044` | 1 | 1.000 | Diagnostic data does not include user names, email addresses... | Microsoft collects data about installed applications includi... |
| ? | `microsoft_027_vs_microsoft_045` | 15 | 1.000 | Copilot in Microsoft 365 uses file content only when users a... | Microsoft uses contextual device data and basic account data... |
| ? | `microsoft_027_vs_microsoft_046` | 2 | 1.000 | Users can configure connected experiences through privacy co... | Feedback Hub determines installed apps through public APIs o... |
| ? | `microsoft_027_vs_microsoft_049` | 9 | 1.000 | Copilot in Microsoft 365 uses file content only when users a... | Microsoft removes identifying data from location information... |
| ? | `microsoft_027_vs_microsoft_051` | 3 | 0.998 | Text and translations from connected experiences are not sto... | Phone Link accesses content of text messages and contact inf... |
| ? | `microsoft_027_vs_microsoft_053` | 1 | 0.699 | Diagnostic data does not include user names, email addresses... | When Microsoft Defender SmartScreen checks web and app conte... |
| ? | `microsoft_027_vs_microsoft_054` | 3 | 0.999 | Text and translations from connected experiences are not sto... | Microsoft collects voice recordings to provide speech recogn... |
| ? | `microsoft_027_vs_microsoft_055` | 3 | 0.999 | Diagnostic data does not include user names, email addresses... | Microsoft uses stored settings, files, and device configurat... |
| ? | `microsoft_027_vs_microsoft_057` | 6 | 0.999 | Copilot in Microsoft 365 uses file content only when users a... | Microsoft Edge syncs favorites, reading lists, autofill form... |
| ? | `microsoft_027_vs_microsoft_058` | 3 | 0.997 | Text and translations from connected experiences are not sto... | Click to Do sends selected text to Microsoft Azure AI cloud ... |
| ? | `microsoft_027_vs_microsoft_061` | 2 | 0.994 | Users can configure connected experiences through privacy co... | Microsoft collects user online activities through Windows Se... |
| ? | `microsoft_027_vs_microsoft_062` | 10 | 1.000 | Text and translations from connected experiences are not sto... | Microsoft collects content you add, upload, or share through... |
| ? | `microsoft_027_vs_microsoft_063` | 4 | 0.998 | Applications do not access device capabilities until users b... | Microsoft Store automatically checks for, downloads, and ins... |
| ? | `microsoft_027_vs_microsoft_064` | 2 | 0.991 | Copilot in Microsoft 365 uses file content only when users a... | Microsoft uses location data to provide relevant local weath... |
| ? | `microsoft_027_vs_microsoft_065` | 2 | 0.994 | Users can configure connected experiences through privacy co... | Silverlight connects to Microsoft or third-party servers to ... |
| ? | `microsoft_028_vs_microsoft_011` | 5 | 1.000 | Activity reports are routinely deleted from Microsoft server... | Microsoft makes account information available across product... |
| ? | `microsoft_028_vs_microsoft_012` | 2 | 0.891 | Activity reports are routinely deleted from Microsoft server... | Microsoft uses collected Xbox data to improve gaming product... |
| ? | `microsoft_028_vs_microsoft_015` | 1 | 0.965 | Microsoft retains only the last known location as part of th... | Microsoft maintains major data centers across Australia, Aus... |
| ? | `microsoft_028_vs_microsoft_018` | 3 | 0.999 | Activity reports are routinely deleted from Microsoft server... | Microsoft shares reports with advertisers about data collect... |
| ? | `microsoft_028_vs_microsoft_022` | 2 | 0.996 | Activity reports are routinely deleted from Microsoft server... | Microsoft uses Copilot conversations to monitor performance,... |
| ? | `microsoft_028_vs_microsoft_023` | 2 | 0.839 | Activity reports are routinely deleted from Microsoft server... | Microsoft collects error reports to diagnose and resolve cus... |
| ? | `microsoft_028_vs_microsoft_024` | 2 | 0.998 | Activity reports are routinely deleted from Microsoft server... | Microsoft uses Administrator Data to contact customers about... |
| ? | `microsoft_028_vs_microsoft_025` | 2 | 0.811 | Activity reports are routinely deleted from Microsoft server... | Microsoft uses collected data from enterprise software to pr... |
| ? | `microsoft_028_vs_microsoft_027` | 5 | 0.999 | Users can turn off location features at any time in the Fami... | Office Roaming Service removes settings from a device when u... |
| ? | `microsoft_028_vs_microsoft_029` | 4 | 1.000 | Activity reports are routinely deleted from Microsoft server... | Microsoft Launcher syncs Glance data across devices signed i... |
| ? | `microsoft_028_vs_microsoft_030` | 1 | 0.963 | Activity reports are routinely deleted from Microsoft server... | Microsoft processes non-user contact data to determine Teams... |
| ? | `microsoft_028_vs_microsoft_032` | 1 | 0.997 | Microsoft retains only the last known location as part of th... | Outlook.com email accounts end in outlook.com, live.com, hot... |
| ? | `microsoft_028_vs_microsoft_033` | 1 | 1.000 | Activity reports are routinely deleted from Microsoft server... | Required diagnostic data is always sent to Microsoft for all... |
| ? | `microsoft_028_vs_microsoft_034` | 1 | 0.984 | Microsoft retains only the last known location as part of th... | Surface Duo uses Google location services to determine devic... |
| ? | `microsoft_028_vs_microsoft_036` | 4 | 0.999 | Activity reports are routinely deleted from Microsoft server... | Microsoft syncs search history across devices when users sig... |
| ? | `microsoft_028_vs_microsoft_037` | 5 | 1.000 | Activity reports are routinely deleted from Microsoft server... | Microsoft Edge hashes, encrypts, and sends saved credentials... |
| ? | `microsoft_028_vs_microsoft_038` | 2 | 0.999 | Activity reports are routinely deleted from Microsoft server... | Microsoft Translator processes device and usage data from us... |
| ? | `microsoft_028_vs_microsoft_041` | 1 | 0.973 | Activity reports are routinely deleted from Microsoft server... | Microsoft collects activity history tracking apps, services,... |
| ? | `microsoft_028_vs_microsoft_044` | 1 | 0.999 | Activity reports are routinely deleted from Microsoft server... | Microsoft collects diagnostic data periodically and transmit... |
| ? | `microsoft_028_vs_microsoft_045` | 8 | 1.000 | Activity reports are routinely deleted from Microsoft server... | Microsoft combines data from third-party websites shared wit... |
| ? | `microsoft_028_vs_microsoft_046` | 3 | 0.985 | Activity reports are routinely deleted from Microsoft server... | Feedback Hub determines installed apps through public APIs o... |
| ? | `microsoft_028_vs_microsoft_049` | 7 | 1.000 | Users can turn off location features at any time in the Fami... | Microsoft retains only the last known location, with each ne... |
| ? | `microsoft_028_vs_microsoft_050` | 3 | 0.999 | Activity reports are routinely deleted from Microsoft server... | When users request popular links summaries, the visited URL ... |
| ? | `microsoft_028_vs_microsoft_053` | 6 | 1.000 | Activity reports are routinely deleted from Microsoft server... | When Microsoft Defender SmartScreen checks web and app conte... |
| ? | `microsoft_028_vs_microsoft_057` | 2 | 0.999 | Activity reports are routinely deleted from Microsoft server... | Microsoft Edge stores data about device and browser usage in... |
| ? | `microsoft_028_vs_microsoft_062` | 1 | 0.975 | Activity reports are routinely deleted from Microsoft server... | Microsoft sends required diagnostic data to keep Xbox safe, ... |
| ? | `microsoft_028_vs_microsoft_063` | 3 | 1.000 | Activity reports are routinely deleted from Microsoft server... | Microsoft collects ratings, reviews, and problem reports you... |
| ? | `microsoft_028_vs_microsoft_064` | 2 | 0.981 | Activity reports are routinely deleted from Microsoft server... | Microsoft uses collected data to provide personalized and re... |
| ? | `microsoft_028_vs_microsoft_065` | 2 | 0.998 | Activity reports are routinely deleted from Microsoft server... | Silverlight periodically checks a Microsoft server for updat... |
| ? | `microsoft_029_vs_microsoft_002` | 1 | 0.985 | Microsoft Launcher supports Android work profile features to... | Microsoft uses cookies to provide personalized ads to users.... |
| ? | `microsoft_029_vs_microsoft_011` | 5 | 0.995 | Microsoft Launcher can be used without any account, though s... | Microsoft makes account information available across product... |
| ? | `microsoft_029_vs_microsoft_012` | 2 | 0.933 | Microsoft Launcher supports Android work profile features to... | Microsoft collects social activity data including chat data ... |
| ? | `microsoft_029_vs_microsoft_018` | 2 | 0.997 | Microsoft Launcher supports Android work profile features to... | Microsoft selects ads using demographic data, location data,... |
| ? | `microsoft_029_vs_microsoft_019` | 1 | 0.990 | Microsoft Launcher supports Android work profile features to... | Microsoft uses voice data to build and improve speech recogn... |
| ? | `microsoft_029_vs_microsoft_022` | 3 | 1.000 | Microsoft Launcher supports Android work profile features to... | Microsoft Copilot uses prior conversation history to persona... |
| ? | `microsoft_029_vs_microsoft_023` | 4 | 0.993 | Users can manage ad preferences through the Microsoft privac... | Microsoft collects customer name and contact data when engag... |
| ? | `microsoft_029_vs_microsoft_024` | 5 | 0.999 | Users can manage ad preferences through the Microsoft privac... | Microsoft uses Administrator Data to contact customers about... |
| ? | `microsoft_029_vs_microsoft_025` | 1 | 0.917 | Users can manage ad preferences through the Microsoft privac... | Microsoft collects diagnostic data from HoloLens to solve pr... |
| ? | `microsoft_029_vs_microsoft_027` | 5 | 1.000 | Microsoft Launcher supports Android work profile features to... | Office Roaming Service removes settings from a device when u... |
| ? | `microsoft_029_vs_microsoft_028` | 2 | 0.988 | Microsoft Launcher supports Android work profile features to... | Microsoft collects details about how children use their devi... |
| ? | `microsoft_029_vs_microsoft_030` | 1 | 0.949 | Users can manage ad preferences through the Microsoft privac... | Microsoft stores non-user contact information on servers whi... |
| ? | `microsoft_029_vs_microsoft_031` | 2 | 1.000 | Microsoft Launcher supports Android work profile features to... | OneDrive collects device information to deliver personalized... |
| ? | `microsoft_029_vs_microsoft_032` | 2 | 0.999 | Microsoft Launcher supports Android work profile features to... | Outlook uses device location information to provide weather ... |
| ? | `microsoft_029_vs_microsoft_035` | 1 | 0.951 | Users can manage ad preferences through the Microsoft privac... | Search and browse products connect users with information an... |
| ? | `microsoft_029_vs_microsoft_036` | 2 | 0.995 | Microsoft Launcher supports Android work profile features to... | Microsoft syncs search history across devices when users sig... |
| ? | `microsoft_029_vs_microsoft_037` | 17 | 1.000 | Microsoft Launcher supports Android work profile features to... | Microsoft Edge hashes, encrypts, and sends saved credentials... |
| ? | `microsoft_029_vs_microsoft_038` | 3 | 0.999 | Microsoft Launcher supports Android work profile features to... | Microsoft Translator processes device and usage data from us... |
| ? | `microsoft_029_vs_microsoft_039` | 1 | 0.937 | Microsoft Launcher supports Android work profile features to... | Windows collects data about you, your device, and how you us... |
| ? | `microsoft_029_vs_microsoft_040` | 9 | 0.999 | Microsoft Launcher supports Android work profile features to... | Microsoft collects device location from Windows phones at fi... |
| ? | `microsoft_029_vs_microsoft_043` | 2 | 1.000 | Microsoft Launcher supports Android work profile features to... | Microsoft collects device and SIM card identifiers when user... |
| ? | `microsoft_029_vs_microsoft_044` | 1 | 0.549 | Microsoft Launcher supports Android work profile features to... | Microsoft collects basic error reporting data about operatin... |
| ? | `microsoft_029_vs_microsoft_045` | 7 | 1.000 | Microsoft Launcher supports Android work profile features to... | Microsoft combines subscription and purchase history data wi... |
| ? | `microsoft_029_vs_microsoft_047` | 1 | 0.996 | Users can manage ad preferences through the Microsoft privac... | Users can sign into Get Help with their Microsoft account to... |
| ? | `microsoft_029_vs_microsoft_049` | 5 | 0.999 | Microsoft Launcher supports Android work profile features to... | Microsoft collects data about cell towers and Wi-Fi access p... |
| ? | `microsoft_029_vs_microsoft_051` | 1 | 0.984 | Users can manage ad preferences through the Microsoft privac... | Microsoft collects list of installed Android apps and recent... |
| ? | `microsoft_029_vs_microsoft_053` | 3 | 0.994 | Microsoft Launcher supports Android work profile features to... | When Microsoft Defender SmartScreen checks web and app conte... |
| ? | `microsoft_029_vs_microsoft_055` | 1 | 0.679 | Microsoft Launcher supports Android work profile features to... | Windows stores settings, files, and device configuration dat... |
| ? | `microsoft_029_vs_microsoft_057` | 9 | 1.000 | Microsoft Launcher supports Android work profile features to... | Microsoft Edge allows users to pin favorite websites to the ... |
| ? | `microsoft_029_vs_microsoft_058` | 1 | 0.999 | Microsoft Launcher supports Android work profile features to... | Click to Do captures and analyzes screenshots to identify te... |
| ? | `microsoft_029_vs_microsoft_060` | 2 | 1.000 | Microsoft Launcher supports Android work profile features to... | Windows Hello extracts unique points or features from biomet... |
| ? | `microsoft_029_vs_microsoft_061` | 2 | 1.000 | Microsoft Launcher supports Android work profile features to... | Microsoft collects user online activities through Windows Se... |
| ? | `microsoft_029_vs_microsoft_062` | 3 | 0.997 | Microsoft Launcher supports Android work profile features to... | Microsoft collects social activity data including chat, inte... |
| ? | `microsoft_029_vs_microsoft_063` | 2 | 0.997 | Microsoft Launcher supports Android work profile features to... | Microsoft Store uses your device's region configuration to s... |
| ? | `microsoft_029_vs_microsoft_064` | 1 | 0.938 | Microsoft Launcher supports Android work profile features to... | Microsoft uses location data to provide relevant weather con... |
| ? | `microsoft_030_vs_microsoft_007` | 4 | 0.998 | Microsoft is not responsible for privacy or security practic... | Microsoft discloses personal data to operate and maintain se... |
| ? | `microsoft_030_vs_microsoft_011` | 7 | 0.993 | Users can block other users and report concerns to Microsoft... | Service providers have control over third-party Microsoft ac... |
| ? | `microsoft_030_vs_microsoft_012` | 2 | 0.999 | Location sharing for children is permitted with parental con... | Microsoft blocks users under 13 or asks for parental consent... |
| ? | `microsoft_030_vs_microsoft_023` | 1 | 0.572 | Users can sync contacts from third-party providers and unsyn... | Microsoft collects customer name and contact data when engag... |
| ? | `microsoft_030_vs_microsoft_024` | 2 | 0.967 | Microsoft is not responsible for data collected by third-par... | Microsoft collects Customer Data, Personal Data, Administrat... |
| ? | `microsoft_030_vs_microsoft_027` | 8 | 1.000 | Users can block other users and report concerns to Microsoft... | Office Roaming Service removes settings from a device when u... |
| ? | `microsoft_030_vs_microsoft_037` | 1 | 0.797 | Removing third-party accounts from Teams may impact user exp... | Microsoft Edge uses stored privacy preferences to migrate ac... |
| ? | `microsoft_030_vs_microsoft_045` | 3 | 0.999 | Users can disable notification services for Teams calls and ... | Microsoft uses contextual device data and basic account data... |
| ? | `microsoft_030_vs_microsoft_046` | 1 | 0.997 | Users can disable notification services for Teams calls and ... | Feedback Hub determines installed apps through public APIs o... |
| ? | `microsoft_030_vs_microsoft_049` | 5 | 0.999 | Users can disable notification services for Teams calls and ... | Windows shares precise location during emergency calls regar... |
| ? | `microsoft_030_vs_microsoft_050` | 1 | 0.999 | Users can disable notification services for Teams calls and ... | When users enable 'Help Make Narrator Better' and submit ver... |
| ? | `microsoft_030_vs_microsoft_054` | 1 | 0.733 | Users can disable notification services for Teams calls and ... | Windows actively listens to the microphone for app-specific ... |
| ? | `microsoft_030_vs_microsoft_057` | 1 | 0.877 | Users can sync Teams calendar with third-party provider cale... | Microsoft syncs browser information across devices when user... |
| ? | `microsoft_030_vs_microsoft_063` | 1 | 0.662 | Users can block other users and report concerns to Microsoft... | Microsoft Store automatically checks for, downloads, and ins... |
| ? | `microsoft_032_vs_microsoft_002` | 1 | 0.971 | Desktop Outlook application allows users to choose whether d... | Microsoft uses cookies to provide personalized ads to users.... |
| ? | `microsoft_032_vs_microsoft_011` | 1 | 0.999 | Users can remove an account or change synced data from their... | Service providers have control over third-party Microsoft ac... |
| ? | `microsoft_032_vs_microsoft_012` | 2 | 1.000 | Users can remove an account or change synced data from their... | Microsoft blocks users under 13 or asks for parental consent... |
| ? | `microsoft_032_vs_microsoft_018` | 1 | 0.527 | Desktop Outlook application allows users to choose whether d... | Microsoft selects ads based on interests, location, transact... |
| ? | `microsoft_032_vs_microsoft_022` | 3 | 0.997 | Desktop Outlook application allows users to choose whether d... | Microsoft Copilot uses prior conversation history to persona... |
| ? | `microsoft_032_vs_microsoft_024` | 1 | 0.990 | Users can remove an account or change synced data from their... | Microsoft uses Administrator Data to contact customers about... |
| ? | `microsoft_032_vs_microsoft_025` | 1 | 0.999 | Desktop Outlook application allows users to choose whether d... | Microsoft collects diagnostic data from HoloLens to solve pr... |
| ? | `microsoft_032_vs_microsoft_027` | 3 | 1.000 | Desktop Outlook application allows users to choose whether d... | Office Roaming Service removes settings from a device when u... |
| ? | `microsoft_032_vs_microsoft_029` | 7 | 0.998 | Desktop Outlook application allows users to choose whether d... | Microsoft Launcher collects device photos, files, and app us... |
| ? | `microsoft_032_vs_microsoft_031` | 1 | 0.819 | Desktop Outlook application allows users to choose whether d... | OneDrive for Business collects and transmits personal data i... |
| ? | `microsoft_032_vs_microsoft_034` | 1 | 0.999 | Desktop Outlook application allows users to choose whether d... | Surface Duo collects diagnostic data to solve problems and k... |
| ? | `microsoft_032_vs_microsoft_037` | 12 | 1.000 | Desktop Outlook application allows users to choose whether d... | Microsoft Edge caches content collected into collections on ... |
| ? | `microsoft_032_vs_microsoft_038` | 3 | 0.999 | Desktop Outlook application allows users to choose whether d... | Microsoft Translator processes device and usage data from us... |
| ? | `microsoft_032_vs_microsoft_040` | 3 | 1.000 | Desktop Outlook application allows users to choose whether d... | Microsoft collects device and network identifiers from Windo... |
| ? | `microsoft_032_vs_microsoft_045` | 2 | 1.000 | Desktop Outlook application allows users to choose whether d... | Microsoft uses contextual device data and basic account data... |
| ? | `microsoft_032_vs_microsoft_049` | 5 | 1.000 | Deleted emails remain in Deleted Items folder for approximat... | Microsoft retains only the last known location, with each ne... |
| ? | `microsoft_032_vs_microsoft_051` | 1 | 0.998 | Desktop Outlook application allows users to choose whether d... | Microsoft collects list of installed Android apps and recent... |
| ? | `microsoft_032_vs_microsoft_053` | 4 | 1.000 | Desktop Outlook application allows users to choose whether d... | Microsoft Defender Antivirus automatically sends reports to ... |
| ? | `microsoft_032_vs_microsoft_056` | 3 | 0.999 | Desktop Outlook application allows users to choose whether d... | Windows Update automatically downloads Windows software upda... |
| ? | `microsoft_032_vs_microsoft_057` | 5 | 0.999 | Desktop Outlook application allows users to choose whether d... | Microsoft Edge allows users to pin favorite websites to the ... |
| ? | `microsoft_032_vs_microsoft_061` | 1 | 1.000 | Desktop Outlook application allows users to choose whether d... | Microsoft collects user online activities through Windows Se... |
| ? | `microsoft_032_vs_microsoft_062` | 1 | 1.000 | Desktop Outlook application allows users to choose whether d... | Microsoft stores offline Xbox usage data on device storage a... |
| ? | `microsoft_032_vs_microsoft_063` | 3 | 0.959 | Desktop Outlook application allows users to choose whether d... | Microsoft Store uses your device's region configuration to s... |
| ? | `microsoft_032_vs_microsoft_064` | 1 | 0.931 | Desktop Outlook application allows users to choose whether d... | Microsoft collects data on app installation, version, device... |
| ? | `microsoft_032_vs_microsoft_065` | 4 | 0.999 | Desktop Outlook application allows users to choose whether d... | Silverlight sends a request to a Microsoft server containing... |
| ? | `microsoft_033_vs_microsoft_015` | 1 | 0.911 | Location information is only shared with emergency services ... | Microsoft stores and processes personal data in customer's r... |
| ? | `microsoft_033_vs_microsoft_028` | 2 | 0.993 | Location information is only shared with emergency services ... | Drive safety reports are uploaded to the cloud and can be sh... |
| ? | `microsoft_033_vs_microsoft_030` | 1 | 0.580 | When using Skype through a partner company, that company's p... | Microsoft shares user information with Enterprise customers ... |
| ? | `microsoft_033_vs_microsoft_036` | 1 | 0.949 | When using Skype through a partner company, that company's p... | Bing receives search queries and related data from third-par... |
| ? | `microsoft_033_vs_microsoft_040` | 1 | 1.000 | Location information is only shared with emergency services ... | Microsoft collects device location from Windows phones at fi... |
| ? | `microsoft_033_vs_microsoft_045` | 1 | 0.980 | Location information is only shared with emergency services ... | Microsoft uses device information and activity data locally ... |
| ? | `microsoft_033_vs_microsoft_049` | 6 | 1.000 | Location information is only shared with emergency services ... | Windows shares precise location during emergency calls regar... |
| ? | `microsoft_033_vs_microsoft_057` | 1 | 0.999 | Location information is only shared with emergency services ... | Microsoft Edge sends search queries, device information, and... |
| ? | `microsoft_033_vs_microsoft_062` | 2 | 0.994 | When using Skype through a partner company, that company's p... | Your gamertag, game statistics, achievements, and activity a... |
| ? | `microsoft_034_vs_microsoft_031` | 1 | 1.000 | Diagnostic data collected does not include user name, email ... | OneDrive for Business collects and transmits personal data i... |
| ? | `microsoft_034_vs_microsoft_033` | 1 | 0.999 | Diagnostic data collected does not include user name, email ... | Required diagnostic data is always sent to Microsoft for all... |
| ? | `microsoft_034_vs_microsoft_045` | 3 | 1.000 | Diagnostic data collected does not include user name, email ... | Microsoft uses contextual device data and basic account data... |
| ? | `microsoft_034_vs_microsoft_062` | 1 | 0.994 | Diagnostic data collected does not include user name, email ... | Microsoft sends required diagnostic data to keep Xbox safe, ... |
| ? | `microsoft_036_vs_microsoft_011` | 3 | 0.983 | Microsoft requires third parties receiving Bing data to keep... | Third parties can use or share data received from Microsoft ... |
| ? | `microsoft_036_vs_microsoft_012` | 1 | 0.983 | Microsoft does not use Bing Experience Improvement Program d... | Microsoft uses collected Xbox data to improve gaming product... |
| ? | `microsoft_036_vs_microsoft_018` | 3 | 0.998 | Microsoft does not use Bing Experience Improvement Program d... | Microsoft serves personalized ads based on online activity w... |
| ? | `microsoft_036_vs_microsoft_022` | 1 | 0.998 | Microsoft does not use Bing Experience Improvement Program d... | Microsoft Copilot uses prompts and related information to pr... |
| ? | `microsoft_036_vs_microsoft_023` | 2 | 1.000 | Microsoft does not use Bing Experience Improvement Program d... | Microsoft uses customer data to personalize communication co... |
| ? | `microsoft_036_vs_microsoft_025` | 3 | 0.998 | Microsoft does not use Bing Experience Improvement Program d... | Microsoft collects diagnostic data from HoloLens to improve ... |
| ? | `microsoft_036_vs_microsoft_030` | 1 | 0.997 | Microsoft does not use Bing Experience Improvement Program d... | Microsoft collects data about Teams feature usage and commun... |
| ? | `microsoft_036_vs_microsoft_033` | 2 | 1.000 | Microsoft does not use Bing Experience Improvement Program d... | Required diagnostic data is always sent to Microsoft for all... |
| ? | `microsoft_036_vs_microsoft_034` | 1 | 0.791 | Microsoft requires third parties receiving Bing data to keep... | Microsoft shares location data with Google to enable locatio... |
| ? | `microsoft_036_vs_microsoft_037` | 1 | 0.968 | Microsoft does not use Bing Experience Improvement Program d... | Microsoft Edge collects search activity data across the web ... |
| ? | `microsoft_036_vs_microsoft_038` | 2 | 0.999 | Microsoft does not use Bing Experience Improvement Program d... | Microsoft uses submitted data to personalize user experience... |
| ? | `microsoft_036_vs_microsoft_045` | 14 | 1.000 | Microsoft does not use Bing Experience Improvement Program d... | Microsoft uses device information and Windows diagnostic dat... |
| ? | `microsoft_036_vs_microsoft_050` | 1 | 0.998 | Microsoft does not use Bing Experience Improvement Program d... | Collected device and usage data from Narrator feedback is us... |
| ? | `microsoft_036_vs_microsoft_051` | 2 | 0.839 | Microsoft does not use Bing Experience Improvement Program d... | Android contacts are synced to Microsoft cloud and stored on... |
| ? | `microsoft_036_vs_microsoft_057` | 1 | 0.987 | Microsoft does not use Bing Experience Improvement Program d... | Microsoft Edge sends information typed into the address bar ... |
| ? | `microsoft_036_vs_microsoft_061` | 1 | 0.998 | Microsoft requires third parties receiving Bing data to keep... | Microsoft uses collected data from Windows Search to provide... |
| ? | `microsoft_036_vs_microsoft_062` | 1 | 0.775 | Microsoft does not use Bing Experience Improvement Program d... | Microsoft uses collected data to provide services, curated e... |
| ? | `microsoft_036_vs_microsoft_064` | 2 | 0.999 | Microsoft does not use Bing Experience Improvement Program d... | Microsoft uses collected data to provide personalized and re... |
| ? | `microsoft_037_vs_microsoft_002` | 1 | 0.916 | Microsoft does not use collected search data to personalize ... | Microsoft uses cookies to provide personalized ads to users.... |
| ? | `microsoft_037_vs_microsoft_007` | 2 | 1.000 | Microsoft does not use collected search data to personalize ... | Microsoft discloses personal data to prevent spam, fraud, an... |
| ? | `microsoft_037_vs_microsoft_009` | 1 | 0.893 | Users can control use of browsing activity for personalized ... | Microsoft uses cookies to manage child account information w... |
| ? | `microsoft_037_vs_microsoft_011` | 16 | 1.000 | Microsoft does not retain credential data after Password Mon... | Microsoft collects credentials, name, contact data, payment ... |
| ? | `microsoft_037_vs_microsoft_012` | 21 | 1.000 | Users can send optional diagnostic data about how they use M... | Microsoft collects required minimum data necessary to keep X... |
| ? | `microsoft_037_vs_microsoft_018` | 8 | 0.999 | Microsoft does not use collected search data to personalize ... | Microsoft selects ads based on interests, location, transact... |
| ? | `microsoft_037_vs_microsoft_022` | 3 | 0.998 | Users can delete browsing data from their device using Clear... | Microsoft Copilot uses prior conversation history to persona... |
| ? | `microsoft_037_vs_microsoft_023` | 8 | 0.999 | Microsoft does not use collected search data to personalize ... | Microsoft uses customer data to personalize communication co... |
| ? | `microsoft_037_vs_microsoft_024` | 20 | 0.999 | Users can choose which browser data to sync, including favor... | Microsoft uses Administrator Data to contact customers about... |
| ? | `microsoft_037_vs_microsoft_025` | 6 | 1.000 | Users can turn off search and site suggestions features in b... | HoloLens microphones enable voice commands for navigation, c... |
| ? | `microsoft_037_vs_microsoft_027` | 12 | 1.000 | Users can choose to share Microsoft Edge browsing activity t... | Office Roaming Service removes settings from a device when u... |
| ? | `microsoft_037_vs_microsoft_028` | 5 | 1.000 | Users can delete browsing data from their device using Clear... | Microsoft uploads location data to the cloud and shares it w... |
| ? | `microsoft_037_vs_microsoft_029` | 26 | 1.000 | Microsoft does not use collected search data to personalize ... | Microsoft Launcher uses account information to provide perso... |
| ? | `microsoft_037_vs_microsoft_030` | 11 | 0.999 | Microsoft does not retain credential data after Password Mon... | Microsoft collects data about Teams feature usage and commun... |
| ? | `microsoft_037_vs_microsoft_031` | 6 | 0.998 | Users can control use of browsing activity for personalized ... | OneDrive for Business collects and transmits personal data i... |
| ? | `microsoft_037_vs_microsoft_032` | 5 | 0.999 | Users can choose which browser data to sync, including favor... | Mail, calendar items, files, contacts, and settings automati... |
| ? | `microsoft_037_vs_microsoft_033` | 6 | 1.000 | Users can send optional diagnostic data about how they use M... | Required diagnostic data is always sent to Microsoft for all... |
| ? | `microsoft_037_vs_microsoft_034` | 9 | 1.000 | Users can choose to share Microsoft Edge browsing activity t... | Surface Duo uses Google location services to determine devic... |
| ? | `microsoft_037_vs_microsoft_035` | 3 | 0.953 | Users can delete browsing data from their device using Clear... | Search and browse products learn and adapt over time based o... |
| ? | `microsoft_037_vs_microsoft_036` | 14 | 0.998 | Microsoft does not retain credential data after Password Mon... | Microsoft syncs search history across devices when users sig... |
| ? | `microsoft_037_vs_microsoft_038` | 6 | 1.000 | Users can send optional diagnostic data about how they use M... | Microsoft deletes identifiers and certain text like email ad... |
| ? | `microsoft_037_vs_microsoft_039` | 2 | 0.999 | Microsoft does not retain credential data after Password Mon... | Windows collects data about you, your device, and how you us... |
| ? | `microsoft_037_vs_microsoft_040` | 21 | 1.000 | Microsoft does not retain credential data after Password Mon... | Microsoft collects device and network identifiers from Windo... |
| ? | `microsoft_037_vs_microsoft_043` | 3 | 0.998 | Users can control use of browsing activity for personalized ... | Microsoft collects device and SIM card identifiers when user... |
| ? | `microsoft_037_vs_microsoft_045` | 24 | 1.000 | Microsoft does not retain credential data after Password Mon... | Microsoft uses contextual device data and basic account data... |
| ? | `microsoft_037_vs_microsoft_047` | 2 | 0.991 | Users can control use of browsing activity for personalized ... | Users can sign into Get Help with their Microsoft account to... |
| ? | `microsoft_037_vs_microsoft_049` | 11 | 1.000 | Users can disable or configure syncing in Microsoft Edge set... | Microsoft retains only the last known location, with each ne... |
| ? | `microsoft_037_vs_microsoft_050` | 1 | 0.987 | Users can send optional diagnostic data about how they use M... | When users request image descriptions, images are sent to Mi... |
| ? | `microsoft_037_vs_microsoft_051` | 4 | 0.998 | Users can send optional diagnostic data about how they use M... | Microsoft collects list of installed Android apps and recent... |
| ? | `microsoft_037_vs_microsoft_053` | 9 | 1.000 | Users can send optional diagnostic data about how they use M... | Microsoft Defender Antivirus automatically sends reports to ... |
| ? | `microsoft_037_vs_microsoft_054` | 2 | 0.995 | Users can send optional diagnostic data about how they use M... | Microsoft collects voice recordings to provide speech recogn... |
| ? | `microsoft_037_vs_microsoft_055` | 2 | 0.999 | Microsoft does not retain credential data after Password Mon... | Windows stores settings, files, and device configuration dat... |
| ? | `microsoft_037_vs_microsoft_056` | 1 | 0.997 | Users can disable or configure syncing in Microsoft Edge set... | Users can configure Windows Update to automatically install ... |
| ? | `microsoft_037_vs_microsoft_057` | 6 | 0.996 | Users can delete browsing data from their device using Clear... | Microsoft Edge syncs favorites, reading lists, autofill form... |
| ? | `microsoft_037_vs_microsoft_058` | 5 | 0.999 | Users can choose which browser data to sync, including favor... | Click to Do captures and analyzes screenshots to identify te... |
| ? | `microsoft_037_vs_microsoft_060` | 3 | 1.000 | Users can send optional diagnostic data about how they use M... | Windows Hello extracts unique points or features from biomet... |
| ? | `microsoft_037_vs_microsoft_061` | 7 | 0.999 | Users can send optional diagnostic data about how they use M... | Microsoft collects user online activities through Windows Se... |
| ? | `microsoft_037_vs_microsoft_062` | 15 | 1.000 | Users can share optional diagnostic data about Microsoft Edg... | Microsoft stores offline Xbox usage data on device storage a... |
| ? | `microsoft_037_vs_microsoft_063` | 9 | 0.999 | Microsoft does not retain credential data after Password Mon... | Your Microsoft account is associated with your ratings and r... |
| ? | `microsoft_037_vs_microsoft_064` | 2 | 1.000 | Microsoft does not use collected search data to personalize ... | Microsoft uses collected data to provide personalized and re... |
| ? | `microsoft_037_vs_microsoft_065` | 23 | 1.000 | Users can send optional diagnostic data about how they use M... | Silverlight provides the rights server with content file ID ... |
| ? | `microsoft_038_vs_microsoft_002` | 1 | 0.997 | Microsoft has implemented measures designed to help de-ident... | Microsoft uses cookies to provide personalized ads to users.... |
| ? | `microsoft_038_vs_microsoft_011` | 3 | 0.999 | Microsoft has implemented measures designed to help de-ident... | Microsoft displays user name, username, and profile photo in... |
| ? | `microsoft_038_vs_microsoft_012` | 2 | 1.000 | Microsoft has implemented measures designed to help de-ident... | Microsoft assigns a unique identifier to a child's device wh... |
| ? | `microsoft_038_vs_microsoft_018` | 1 | 0.992 | Microsoft has implemented measures designed to help de-ident... | Microsoft serves personalized ads based on online activity w... |
| ? | `microsoft_038_vs_microsoft_019` | 1 | 0.866 | Microsoft has implemented measures designed to help de-ident... | Microsoft uses voice data to build and improve speech recogn... |
| ? | `microsoft_038_vs_microsoft_022` | 1 | 0.996 | Microsoft has implemented measures designed to help de-ident... | Microsoft Copilot uses prior conversation history to persona... |
| ? | `microsoft_038_vs_microsoft_023` | 1 | 0.982 | Microsoft has implemented measures designed to help de-ident... | Microsoft collects customer name and contact data when engag... |
| ? | `microsoft_038_vs_microsoft_024` | 1 | 0.988 | Microsoft has implemented measures designed to help de-ident... | Microsoft uses Administrator Data to contact customers about... |
| ? | `microsoft_038_vs_microsoft_028` | 2 | 0.967 | Microsoft has implemented measures designed to help de-ident... | Microsoft uses location data to record drive habits includin... |
| ? | `microsoft_038_vs_microsoft_029` | 7 | 0.999 | Microsoft has implemented measures designed to help de-ident... | Microsoft Launcher syncs Glance data across devices signed i... |
| ? | `microsoft_038_vs_microsoft_031` | 1 | 0.988 | Microsoft has implemented measures designed to help de-ident... | OneDrive collects device information to deliver personalized... |
| ? | `microsoft_038_vs_microsoft_032` | 3 | 0.996 | Microsoft has implemented measures designed to help de-ident... | Mobile Outlook application syncs data to Microsoft servers t... |
| ? | `microsoft_038_vs_microsoft_036` | 2 | 0.710 | Microsoft has implemented measures designed to help de-ident... | Copilot Search collects personal data consistent with Bing's... |
| ? | `microsoft_038_vs_microsoft_037` | 7 | 0.999 | Microsoft has implemented measures designed to help de-ident... | Microsoft Edge hashes, encrypts, and sends saved credentials... |
| ? | `microsoft_038_vs_microsoft_039` | 1 | 0.710 | Microsoft has implemented measures designed to help de-ident... | SwiftKey draws language model data from all scenarios where ... |
| ? | `microsoft_038_vs_microsoft_040` | 3 | 0.998 | Microsoft has implemented measures designed to help de-ident... | Microsoft uses device identifiers and location data for stoc... |
| ? | `microsoft_038_vs_microsoft_043` | 1 | 0.574 | Microsoft has implemented measures designed to help de-ident... | Microsoft collects device and SIM card identifiers when user... |
| ? | `microsoft_038_vs_microsoft_044` | 1 | 0.999 | Microsoft has implemented measures designed to help de-ident... | Microsoft collects diagnostic data periodically and transmit... |
| ? | `microsoft_038_vs_microsoft_045` | 5 | 0.999 | Microsoft has implemented measures designed to help de-ident... | Microsoft transmits Tailored experiences data to Microsoft s... |
| ? | `microsoft_038_vs_microsoft_048` | 1 | 0.947 | Microsoft has implemented measures designed to help de-ident... | Live captions transcribe audio to help with comprehension of... |
| ? | `microsoft_038_vs_microsoft_049` | 1 | 0.679 | Microsoft has implemented measures designed to help de-ident... | Microsoft uploads device location to the cloud when signed i... |
| ? | `microsoft_038_vs_microsoft_057` | 2 | 0.989 | Microsoft has implemented measures designed to help de-ident... | Microsoft Edge allows users to create and save ink and text ... |
| ? | `microsoft_038_vs_microsoft_058` | 1 | 0.950 | Microsoft has implemented measures designed to help de-ident... | Click to Do captures and analyzes screenshots to identify te... |
| ? | `microsoft_038_vs_microsoft_060` | 2 | 1.000 | Microsoft has implemented measures designed to help de-ident... | Biometric verification data remains on your device until you... |
| ? | `microsoft_038_vs_microsoft_061` | 1 | 0.992 | Microsoft has implemented measures designed to help de-ident... | Microsoft collects user online activities through Windows Se... |
| ? | `microsoft_038_vs_microsoft_062` | 2 | 0.997 | Microsoft has implemented measures designed to help de-ident... | Microsoft stores offline Xbox usage data on device storage a... |
| ? | `microsoft_038_vs_microsoft_063` | 4 | 0.999 | Microsoft has implemented measures designed to help de-ident... | Microsoft Store uses your device identifier to manage produc... |
| ? | `microsoft_039_vs_microsoft_007` | 3 | 0.951 | Windows provides privacy settings pages for each device capa... | Microsoft discloses personal data to operate and maintain se... |
| ? | `microsoft_039_vs_microsoft_009` | 1 | 0.998 | Windows provides choices about personal data collection and ... | Microsoft uses Silverlight Application Storage to store data... |
| ? | `microsoft_039_vs_microsoft_011` | 5 | 0.992 | SwiftKey does not link de-identified text snippets to Micros... | Microsoft displays user name, username, and profile photo in... |
| ? | `microsoft_039_vs_microsoft_012` | 14 | 1.000 | Windows provides choices about personal data collection and ... | Microsoft collects required minimum data necessary to keep X... |
| ? | `microsoft_039_vs_microsoft_018` | 2 | 0.633 | Windows provides privacy settings pages for each device capa... | Microsoft serves personalized ads based on online activity w... |
| ? | `microsoft_039_vs_microsoft_019` | 2 | 0.999 | Windows provides choices about personal data collection and ... | Microsoft transcribes voice data into text using speech reco... |
| ? | `microsoft_039_vs_microsoft_022` | 6 | 1.000 | SwiftKey de-identifies text snippets shared for product impr... | Microsoft Copilot uses prior conversation history to persona... |
| ? | `microsoft_039_vs_microsoft_023` | 4 | 0.999 | Windows provides privacy settings pages for each device capa... | Microsoft collects customer name and contact data when engag... |
| ? | `microsoft_039_vs_microsoft_024` | 7 | 0.999 | Windows provides choices about personal data collection and ... | Microsoft relies on statistical and aggregate pseudonymized ... |
| ? | `microsoft_039_vs_microsoft_025` | 1 | 0.777 | Windows provides choices about personal data collection and ... | Microsoft collects diagnostic data from HoloLens to improve ... |
| ? | `microsoft_039_vs_microsoft_027` | 10 | 0.999 | SwiftKey de-identifies text snippets shared for product impr... | Copilot in Microsoft 365 uses large language model processin... |
| ? | `microsoft_039_vs_microsoft_028` | 3 | 0.999 | OneDrive backup data is protected by encryption in transit a... | Microsoft uploads location data to the cloud and shares it w... |
| ? | `microsoft_039_vs_microsoft_029` | 15 | 1.000 | Windows provides privacy settings pages for each device capa... | Microsoft Launcher syncs Glance data across devices signed i... |
| ? | `microsoft_039_vs_microsoft_030` | 6 | 0.999 | Windows provides privacy settings pages for each device capa... | Microsoft stores non-user contact information on servers whi... |
| ? | `microsoft_039_vs_microsoft_031` | 2 | 0.999 | OneDrive backup data is protected by encryption in transit a... | Sharing OneDrive content via link makes the content accessib... |
| ? | `microsoft_039_vs_microsoft_033` | 2 | 0.998 | Extracted face and hand data is used solely to apply AR effe... | Required diagnostic data is always sent to Microsoft for all... |
| ? | `microsoft_039_vs_microsoft_034` | 4 | 1.000 | Windows provides privacy settings pages for each device capa... | Surface Duo uses Google location services to determine devic... |
| ? | `microsoft_039_vs_microsoft_036` | 14 | 1.000 | SwiftKey de-identifies text snippets shared for product impr... | Copilot Search collects personal data consistent with Bing's... |
| ? | `microsoft_039_vs_microsoft_037` | 35 | 1.000 | Windows provides privacy settings pages for each device capa... | Microsoft Edge sends information typed into the browser addr... |
| ? | `microsoft_039_vs_microsoft_038` | 4 | 1.000 | Windows provides choices about personal data collection and ... | Microsoft Translator processes text, image, and voice data s... |
| ? | `microsoft_039_vs_microsoft_040` | 11 | 1.000 | SwiftKey de-identifies text snippets shared for product impr... | Microsoft uses device identifiers and location data for stoc... |
| ? | `microsoft_039_vs_microsoft_044` | 1 | 0.911 | Windows provides choices about personal data collection and ... | Microsoft collects network data including IP address, mobile... |
| ? | `microsoft_039_vs_microsoft_045` | 4 | 0.999 | Windows provides choices about personal data collection and ... | Microsoft uses contextual device data and basic account data... |
| ? | `microsoft_039_vs_microsoft_046` | 1 | 0.992 | Windows provides privacy settings pages for each device capa... | Feedback Hub determines installed apps through public APIs o... |
| ? | `microsoft_039_vs_microsoft_049` | 6 | 1.000 | Windows provides privacy settings pages for each device capa... | Microsoft removes identifying data from location information... |
| ? | `microsoft_039_vs_microsoft_051` | 4 | 0.996 | Windows provides privacy settings pages for each device capa... | Microsoft collects list of installed Android apps and recent... |
| ? | `microsoft_039_vs_microsoft_053` | 3 | 0.998 | Windows provides choices about personal data collection and ... | Microsoft Defender SmartScreen sends the full web address of... |
| ? | `microsoft_039_vs_microsoft_054` | 1 | 0.997 | Windows provides choices about personal data collection and ... | Microsoft collects voice recordings to provide speech recogn... |
| ? | `microsoft_039_vs_microsoft_057` | 12 | 1.000 | OneDrive backup data is protected by encryption in transit a... | Microsoft Edge syncs favorites, reading lists, autofill form... |
| ? | `microsoft_039_vs_microsoft_058` | 4 | 0.999 | SwiftKey de-identifies text snippets shared for product impr... | Click to Do captures and analyzes screenshots to identify te... |
| ? | `microsoft_039_vs_microsoft_060` | 4 | 1.000 | Extracted face and hand data is used solely to apply AR effe... | Biometric verification data remains on your device until you... |
| ? | `microsoft_039_vs_microsoft_061` | 1 | 0.934 | Windows provides privacy settings pages for each device capa... | Microsoft collects user online activities through Windows Se... |
| ? | `microsoft_039_vs_microsoft_062` | 13 | 1.000 | Windows provides choices about personal data collection and ... | Microsoft sends required diagnostic data to keep Xbox safe, ... |
| ? | `microsoft_039_vs_microsoft_063` | 3 | 0.907 | SwiftKey does not link de-identified text snippets to Micros... | Your name and picture from your Microsoft account are publis... |
| ? | `microsoft_039_vs_microsoft_065` | 6 | 1.000 | Windows provides privacy settings pages for each device capa... | Silverlight provides the rights server with content file ID ... |
| ? | `microsoft_041_vs_microsoft_009` | 2 | 0.998 | Activity history is stored locally on the user's device rath... | Microsoft uses session cookies for load balancing to ensure ... |
| ? | `microsoft_041_vs_microsoft_036` | 1 | 0.997 | Activity history is stored locally on the user's device rath... | Microsoft syncs search history across devices when users sig... |
| ? | `microsoft_042_vs_microsoft_007` | 8 | 0.996 | Third-party apps' use of the advertising ID is subject to th... | Microsoft discloses personal data to prevent spam, fraud, an... |
| ? | `microsoft_042_vs_microsoft_009` | 4 | 0.999 | Microsoft collects the advertising ID only when users choose... | Microsoft uses cookies to authenticate users and enable sign... |
| ? | `microsoft_042_vs_microsoft_011` | 2 | 0.999 | Microsoft collects the advertising ID only when users choose... | Microsoft assigns a unique ID number to identify each accoun... |
| ? | `microsoft_042_vs_microsoft_018` | 5 | 0.962 | Microsoft collects the advertising ID only when users choose... | Microsoft selects ads based on interests, location, transact... |
| ? | `microsoft_042_vs_microsoft_023` | 1 | 0.996 | Microsoft collects the advertising ID only when users choose... | Microsoft collects customer name and contact data when engag... |
| ? | `microsoft_042_vs_microsoft_034` | 1 | 0.994 | Third-party apps' use of the advertising ID is subject to th... | Microsoft shares location data with Google to enable locatio... |
| ? | `microsoft_042_vs_microsoft_036` | 1 | 0.995 | Third-party apps' use of the advertising ID is subject to th... | Microsoft shares de-identified data from Bing with selected ... |
| ? | `microsoft_042_vs_microsoft_043` | 1 | 0.986 | Microsoft collects the advertising ID only when users choose... | Microsoft collects device and SIM card identifiers when user... |
| ? | `microsoft_042_vs_microsoft_045` | 2 | 1.000 | Microsoft collects the advertising ID only when users choose... | Microsoft uses contextual device data and basic account data... |
| ? | `microsoft_042_vs_microsoft_062` | 2 | 0.997 | Microsoft collects the advertising ID only when users choose... | Microsoft assigns a unique identifier to your Xbox device wh... |
| ? | `microsoft_042_vs_microsoft_063` | 1 | 0.984 | Microsoft collects the advertising ID only when users choose... | Microsoft Store uses your device identifier to manage produc... |
| ? | `microsoft_044_vs_microsoft_002` | 1 | 0.993 | Microsoft processes inking and typing data to remove unique ... | Microsoft uses cookies to provide personalized ads to users.... |
| ? | `microsoft_044_vs_microsoft_009` | 1 | 0.957 | Microsoft processes inking and typing data to remove unique ... | Microsoft uses ANID cookie containing unique identifier from... |
| ? | `microsoft_044_vs_microsoft_011` | 7 | 1.000 | Microsoft processes inking and typing data to remove unique ... | Microsoft makes account information available across product... |
| ? | `microsoft_044_vs_microsoft_012` | 6 | 1.000 | Microsoft processes inking and typing data to remove unique ... | Microsoft uses voice-to-text data from Xbox party chat to pr... |
| ? | `microsoft_044_vs_microsoft_018` | 1 | 0.945 | Microsoft processes inking and typing data to remove unique ... | Microsoft serves personalized ads based on online activity w... |
| ? | `microsoft_044_vs_microsoft_019` | 4 | 1.000 | Microsoft processes inking and typing data to remove unique ... | Microsoft uses voice data to build and improve speech recogn... |
| ? | `microsoft_044_vs_microsoft_022` | 2 | 0.993 | Microsoft minimizes optional diagnostic data collection by s... | Microsoft uses Copilot conversations to monitor performance,... |
| ? | `microsoft_044_vs_microsoft_023` | 3 | 0.997 | Microsoft processes inking and typing data to remove unique ... | Microsoft collects name and contact data of customer designa... |
| ? | `microsoft_044_vs_microsoft_024` | 4 | 0.998 | Microsoft minimizes optional diagnostic data collection by s... | Microsoft relies on statistical and aggregate pseudonymized ... |
| ? | `microsoft_044_vs_microsoft_025` | 2 | 0.999 | Microsoft processes inking and typing data to remove unique ... | Microsoft collects diagnostic data from HoloLens to solve pr... |
| ? | `microsoft_044_vs_microsoft_027` | 1 | 0.982 | Microsoft processes inking and typing data to remove unique ... | Microsoft automatically detects, downloads, and installs sec... |
| ? | `microsoft_044_vs_microsoft_028` | 3 | 0.999 | Microsoft processes inking and typing data to remove unique ... | Microsoft uses location data to record drive habits includin... |
| ? | `microsoft_044_vs_microsoft_029` | 4 | 0.998 | Microsoft processes inking and typing data to remove unique ... | Microsoft Launcher collects access to photos and videos to e... |
| ? | `microsoft_044_vs_microsoft_030` | 3 | 0.992 | Microsoft processes inking and typing data to remove unique ... | With permission, Teams syncs device and Outlook contacts per... |
| ? | `microsoft_044_vs_microsoft_031` | 1 | 0.996 | Microsoft processes inking and typing data to remove unique ... | OneDrive for Business collects and transmits personal data i... |
| ? | `microsoft_044_vs_microsoft_033` | 2 | 1.000 | Microsoft minimizes optional diagnostic data collection by s... | Required diagnostic data is always sent to Microsoft for all... |
| ? | `microsoft_044_vs_microsoft_036` | 6 | 0.998 | Microsoft processes inking and typing data to remove unique ... | Microsoft collects voice input and performance data when use... |
| ? | `microsoft_044_vs_microsoft_037` | 3 | 0.998 | Microsoft processes inking and typing data to remove unique ... | Microsoft Edge stores data about how you use your browser, i... |
| ? | `microsoft_044_vs_microsoft_038` | 3 | 1.000 | Microsoft processes inking and typing data to remove unique ... | Microsoft randomly samples text and audio to improve Microso... |
| ? | `microsoft_044_vs_microsoft_039` | 1 | 0.655 | Microsoft processes inking and typing data to remove unique ... | Windows collects data about you, your device, and how you us... |
| ? | `microsoft_044_vs_microsoft_040` | 6 | 1.000 | Microsoft processes inking and typing data to remove unique ... | Microsoft collects device and network identifiers from Windo... |
| ? | `microsoft_044_vs_microsoft_042` | 1 | 0.986 | Microsoft processes inking and typing data to remove unique ... | Windows generates a unique advertising ID for each person us... |
| ? | `microsoft_044_vs_microsoft_043` | 1 | 0.998 | Microsoft processes inking and typing data to remove unique ... | Microsoft collects device and SIM card identifiers when user... |
| ? | `microsoft_044_vs_microsoft_045` | 7 | 0.999 | Microsoft minimizes optional diagnostic data collection by s... | Microsoft uses contextual device data and basic account data... |
| ? | `microsoft_044_vs_microsoft_051` | 1 | 0.940 | Microsoft processes inking and typing data to remove unique ... | Microsoft collects performance, usage, and device data inclu... |
| ? | `microsoft_044_vs_microsoft_052` | 1 | 0.995 | Microsoft processes inking and typing data to remove unique ... | Microsoft collects performance usage and device data, includ... |
| ? | `microsoft_044_vs_microsoft_053` | 1 | 0.618 | Microsoft processes inking and typing data to remove unique ... | Microsoft Defender Antivirus automatically sends reports to ... |
| ? | `microsoft_044_vs_microsoft_054` | 2 | 1.000 | Microsoft processes inking and typing data to remove unique ... | Microsoft collects voice recordings to provide speech recogn... |
| ? | `microsoft_044_vs_microsoft_057` | 3 | 0.999 | Microsoft processes inking and typing data to remove unique ... | Microsoft Edge stores data about device and browser usage in... |
| ? | `microsoft_044_vs_microsoft_058` | 1 | 1.000 | Microsoft processes inking and typing data to remove unique ... | Click to Do captures and analyzes screenshots to identify te... |
| ? | `microsoft_044_vs_microsoft_060` | 3 | 0.996 | Microsoft processes inking and typing data to remove unique ... | Biometric verification data remains on your device until you... |
| ? | `microsoft_044_vs_microsoft_061` | 1 | 0.671 | Microsoft processes inking and typing data to remove unique ... | Microsoft collects user online activities through Windows Se... |
| ? | `microsoft_044_vs_microsoft_062` | 6 | 0.999 | Microsoft processes inking and typing data to remove unique ... | Microsoft uses voice-to-text chat data to provide captioning... |
| ? | `microsoft_044_vs_microsoft_063` | 5 | 0.997 | Microsoft processes inking and typing data to remove unique ... | Your name and picture from your Microsoft account are publis... |
| ? | `microsoft_044_vs_microsoft_064` | 2 | 0.939 | Microsoft processes inking and typing data to remove unique ... | Microsoft uses location data to provide relevant local weath... |
| ? | `microsoft_044_vs_microsoft_066` | 2 | 0.966 | Microsoft processes inking and typing data to remove unique ... | Microsoft collects numeric body joint mapping values from in... |
| ? | `microsoft_045_vs_microsoft_007` | 6 | 1.000 | Microsoft does not use website browsing information, crash d... | Microsoft discloses personal data to prevent spam, fraud, an... |
| ? | `microsoft_045_vs_microsoft_009` | 2 | 0.999 | Microsoft does not use website browsing information, crash d... | Microsoft uses required cookies to perform essential website... |
| ? | `microsoft_045_vs_microsoft_011` | 5 | 0.994 | Microsoft does not use website browsing information, crash d... | Microsoft collects credentials, name, contact data, payment ... |
| ? | `microsoft_045_vs_microsoft_012` | 11 | 0.999 | Microsoft does not use content of crash dumps, speech, typin... | Microsoft collects content a child adds, uploads, or shares ... |
| ? | `microsoft_045_vs_microsoft_018` | 7 | 0.999 | Microsoft does not use website browsing information, crash d... | Microsoft selects ads using demographic data, location data,... |
| ? | `microsoft_045_vs_microsoft_019` | 5 | 0.999 | Microsoft does not use website browsing information, crash d... | Microsoft integrates speech recognition technologies into ma... |
| ? | `microsoft_045_vs_microsoft_022` | 8 | 0.999 | Microsoft does not use website browsing information, crash d... | Microsoft Copilot uses prompts, location, language, and user... |
| ? | `microsoft_045_vs_microsoft_023` | 2 | 0.999 | Microsoft does not use website browsing information, crash d... | Microsoft uses customer data to personalize communication co... |
| ? | `microsoft_045_vs_microsoft_024` | 2 | 0.998 | Microsoft does not use website browsing information, crash d... | Microsoft collects Customer Data, Personal Data, Administrat... |
| ? | `microsoft_045_vs_microsoft_025` | 6 | 0.996 | Microsoft does not use website browsing information, crash d... | Microsoft collects diagnostic data from HoloLens to improve ... |
| ? | `microsoft_045_vs_microsoft_027` | 3 | 0.947 | Microsoft does not use website browsing information, crash d... | Copilot in Microsoft 365 uses large language model processin... |
| ? | `microsoft_045_vs_microsoft_028` | 2 | 0.813 | Microsoft does not use content of crash dumps, speech, typin... | Microsoft collects details about how children use their devi... |
| ? | `microsoft_045_vs_microsoft_029` | 8 | 0.998 | Microsoft does not use website browsing information, crash d... | Microsoft Launcher collects device camera and microphone acc... |
| ? | `microsoft_045_vs_microsoft_030` | 2 | 0.997 | Microsoft does not use website browsing information, crash d... | Microsoft collects data about Teams feature usage and commun... |
| ? | `microsoft_045_vs_microsoft_033` | 3 | 1.000 | Microsoft does not use website browsing information, crash d... | Required diagnostic data is always sent to Microsoft for all... |
| ? | `microsoft_045_vs_microsoft_035` | 1 | 0.977 | Microsoft does not use website browsing information, crash d... | Search and browse products connect users with information an... |
| ? | `microsoft_045_vs_microsoft_036` | 6 | 0.998 | Microsoft does not use content of crash dumps, speech, typin... | Microsoft collects words, phrases, and surrounding content w... |
| ? | `microsoft_045_vs_microsoft_037` | 11 | 0.999 | Microsoft does not use website browsing information, crash d... | Microsoft Edge downloads content from Microsoft services to ... |
| ? | `microsoft_045_vs_microsoft_038` | 10 | 0.999 | Microsoft does not use content of crash dumps, speech, typin... | Microsoft uses submitted data to personalize user experience... |
| ? | `microsoft_045_vs_microsoft_039` | 3 | 0.991 | Microsoft does not use content of crash dumps, speech, typin... | Windows collects data about you, your device, and how you us... |
| ? | `microsoft_045_vs_microsoft_040` | 1 | 0.547 | In the European Economic Area, turning off Personalized offe... | Microsoft uses device identifiers and location data for stoc... |
| ? | `microsoft_045_vs_microsoft_044` | 1 | 0.999 | Microsoft does not use website browsing information, crash d... | Microsoft collects optional diagnostic data including browsi... |
| ? | `microsoft_045_vs_microsoft_046` | 1 | 0.529 | Microsoft does not use website browsing information, crash d... | Feedback Hub sends diagnostic data automatically or offers t... |
| ? | `microsoft_045_vs_microsoft_049` | 1 | 0.993 | In the European Economic Area, turning off Personalized offe... | Microsoft removes identifying data from location information... |
| ? | `microsoft_045_vs_microsoft_050` | 4 | 0.997 | Microsoft does not use content of crash dumps, speech, typin... | When users enable 'Help Make Narrator Better' and submit ver... |
| ? | `microsoft_045_vs_microsoft_053` | 4 | 0.989 | Microsoft does not use website browsing information, crash d... | When Microsoft Defender SmartScreen checks web and app conte... |
| ? | `microsoft_045_vs_microsoft_054` | 8 | 0.999 | Microsoft does not use website browsing information, crash d... | Microsoft collects voice recordings to provide speech recogn... |
| ? | `microsoft_045_vs_microsoft_055` | 1 | 0.999 | Microsoft does not use website browsing information, crash d... | Microsoft uses stored settings, files, and device configurat... |
| ? | `microsoft_045_vs_microsoft_057` | 6 | 0.994 | Microsoft does not use website browsing information, crash d... | Microsoft Edge syncs favorites, reading lists, autofill form... |
| ? | `microsoft_045_vs_microsoft_058` | 2 | 0.993 | Microsoft does not use content of crash dumps, speech, typin... | Click to Do captures and analyzes screenshots to identify te... |
| ? | `microsoft_045_vs_microsoft_060` | 2 | 0.998 | Microsoft does not use website browsing information, crash d... | Windows Hello extracts unique points or features from biomet... |
| ? | `microsoft_045_vs_microsoft_061` | 1 | 0.976 | Microsoft does not use website browsing information, crash d... | Microsoft collects user online activities through Windows Se... |
| ? | `microsoft_045_vs_microsoft_062` | 16 | 0.999 | Microsoft does not use website browsing information, crash d... | Microsoft sends required diagnostic data to keep Xbox safe, ... |
| ? | `microsoft_045_vs_microsoft_063` | 2 | 0.971 | Microsoft does not use website browsing information, crash d... | Your name and picture from your Microsoft account are publis... |
| ? | `microsoft_045_vs_microsoft_064` | 4 | 1.000 | Microsoft does not use website browsing information, crash d... | Microsoft uses collected data to provide personalized and re... |
| ? | `microsoft_045_vs_microsoft_066` | 2 | 0.896 | Microsoft does not use content of crash dumps, speech, typin... | Microsoft uses diagnostic data to improve Mixed Reality and ... |
| ? | `microsoft_047_vs_microsoft_015` | 1 | 0.979 | Get Help does not use location data as part of its services.... | Microsoft stores and processes personal data in customer's r... |
| ? | `microsoft_047_vs_microsoft_028` | 1 | 0.970 | Get Help does not use location data as part of its services.... | Microsoft uploads location data to the cloud and shares it w... |
| ? | `microsoft_047_vs_microsoft_029` | 2 | 0.772 | Get Help does not use location data as part of its services.... | Microsoft Launcher collects location information to deliver ... |
| ? | `microsoft_047_vs_microsoft_034` | 1 | 0.996 | Get Help does not use location data as part of its services.... | Surface Duo uses Google location services to determine devic... |
| ? | `microsoft_047_vs_microsoft_045` | 1 | 0.995 | Get Help does not use location data as part of its services.... | Microsoft uses device information and activity data locally ... |
| ? | `microsoft_047_vs_microsoft_049` | 5 | 1.000 | Get Help does not use location data as part of its services.... | Microsoft retains only the last known location, with each ne... |
| ? | `microsoft_047_vs_microsoft_057` | 1 | 0.994 | Get Help does not use location data as part of its services.... | Microsoft Edge sends search queries, device information, and... |
| ? | `microsoft_048_vs_microsoft_012` | 1 | 0.971 | Transcribing microphone audio is disabled by default in live... | Kinect microphone enables voice chat between players and voi... |
| ? | `microsoft_048_vs_microsoft_019` | 2 | 0.998 | Transcribing microphone audio is disabled by default in live... | Microsoft transcribes voice data into text using speech reco... |
| ? | `microsoft_048_vs_microsoft_024` | 1 | 0.998 | Voice data that is captioned is only processed on the user's... | Microsoft uses Payment Data to complete transactions and det... |
| ? | `microsoft_048_vs_microsoft_025` | 2 | 0.994 | Transcribing microphone audio is disabled by default in live... | HoloLens microphones enable voice commands for navigation, c... |
| ? | `microsoft_048_vs_microsoft_027` | 3 | 1.000 | Transcribing microphone audio is disabled by default in live... | Speaker Coach accesses device microphone and provides on-scr... |
| ? | `microsoft_048_vs_microsoft_029` | 3 | 0.994 | Voice data that is captioned is only processed on the user's... | Microsoft Launcher syncs Glance data across devices signed i... |
| ? | `microsoft_048_vs_microsoft_032` | 1 | 0.987 | Transcribing microphone audio is disabled by default in live... | Outlook Dictate feature uses device microphone or connected ... |
| ? | `microsoft_048_vs_microsoft_033` | 1 | 1.000 | Voice data that is captioned is only processed on the user's... | Required diagnostic data is always sent to Microsoft for all... |
| ? | `microsoft_048_vs_microsoft_036` | 2 | 0.925 | Transcribing microphone audio is disabled by default in live... | Microsoft collects voice input and performance data when use... |
| ? | `microsoft_048_vs_microsoft_038` | 2 | 0.999 | Voice data that is captioned is only processed on the user's... | Microsoft randomly samples text and audio to improve Microso... |
| ? | `microsoft_048_vs_microsoft_039` | 1 | 0.995 | Transcribing microphone audio is disabled by default in live... | Windows Settings uses your microphone when controlling volum... |
| ? | `microsoft_048_vs_microsoft_040` | 2 | 0.909 | Voice data that is captioned is only processed on the user's... | Microsoft collects device location from Windows phones at fi... |
| ? | `microsoft_048_vs_microsoft_045` | 1 | 0.999 | Voice data that is captioned is only processed on the user's... | Microsoft uses contextual device data and basic account data... |
| ? | `microsoft_048_vs_microsoft_046` | 2 | 0.998 | Voice data that is captioned is only processed on the user's... | Diagnostic data is sent to Microsoft when you submit feedbac... |
| ? | `microsoft_048_vs_microsoft_049` | 2 | 1.000 | Voice data that is captioned is only processed on the user's... | Microsoft removes identifying data from location information... |
| ? | `microsoft_048_vs_microsoft_050` | 1 | 0.981 | Voice data that is captioned is only processed on the user's... | When users enable 'Help Make Narrator Better' and submit ver... |
| ? | `microsoft_048_vs_microsoft_051` | 3 | 0.999 | Voice data that is captioned is only processed on the user's... | Phone Link accesses content of text messages and contact inf... |
| ? | `microsoft_048_vs_microsoft_054` | 3 | 0.998 | Transcribing microphone audio is disabled by default in live... | Windows actively listens to the microphone for app-specific ... |
| ? | `microsoft_048_vs_microsoft_057` | 3 | 0.989 | Voice data that is captioned is only processed on the user's... | Microsoft Edge sends search queries, device information, and... |
| ? | `microsoft_048_vs_microsoft_058` | 3 | 0.999 | Voice data that is captioned is only processed on the user's... | Click to Do captures and analyzes screenshots to identify te... |
| ? | `microsoft_048_vs_microsoft_062` | 2 | 0.971 | Transcribing microphone audio is disabled by default in live... | Kinect microphone enables voice chat between players and voi... |
| ? | `microsoft_049_vs_microsoft_007` | 1 | 0.980 | Microsoft is not responsible for how users use recording fea... | Microsoft discloses personal data to prevent spam, fraud, an... |
| ? | `microsoft_049_vs_microsoft_009` | 1 | 0.991 | Microsoft is not responsible for how users use recording fea... | Microsoft records user decisions not to receive interest-bas... |
| ? | `microsoft_049_vs_microsoft_011` | 3 | 0.993 | Users can view or delete location data from their Microsoft ... | Service providers have control over third-party Microsoft ac... |
| ? | `microsoft_049_vs_microsoft_012` | 3 | 0.998 | Users can view or delete location data from their Microsoft ... | Microsoft uses voice-to-text data from Xbox party chat to pr... |
| ? | `microsoft_049_vs_microsoft_019` | 1 | 0.803 | Users can view or delete location data from their Microsoft ... | Microsoft uses voice data to build and improve speech recogn... |
| ? | `microsoft_049_vs_microsoft_023` | 2 | 0.987 | Users can view or delete location data from their Microsoft ... | Microsoft collects customer name and contact data when engag... |
| ? | `microsoft_049_vs_microsoft_024` | 3 | 0.980 | Users can view or delete location data from their Microsoft ... | Microsoft uses Administrator Data to contact customers about... |
| ? | `microsoft_049_vs_microsoft_027` | 3 | 0.999 | Users can control which apps have access to device precise l... | Microsoft automatically detects, downloads, and installs sec... |
| ? | `microsoft_049_vs_microsoft_028` | 1 | 0.999 | Users can view or delete location data from their Microsoft ... | Microsoft uploads location data to the cloud and shares it w... |
| ? | `microsoft_049_vs_microsoft_029` | 4 | 0.994 | Users can view or delete location data from their Microsoft ... | Microsoft Launcher collects device camera and microphone acc... |
| ? | `microsoft_049_vs_microsoft_030` | 2 | 0.949 | Users can view or delete location data from their Microsoft ... | Microsoft processes non-user contact data to determine Teams... |
| ? | `microsoft_049_vs_microsoft_034` | 1 | 0.998 | Users can view or delete location data from their Microsoft ... | Surface Duo uses Google location services to determine devic... |
| ? | `microsoft_049_vs_microsoft_036` | 2 | 0.964 | Users can view or delete location data from their Microsoft ... | Microsoft collects words, phrases, and surrounding content w... |
| ? | `microsoft_049_vs_microsoft_037` | 1 | 0.918 | Users can view or delete location data from their Microsoft ... | Microsoft Edge hashes, encrypts, and sends saved credentials... |
| ? | `microsoft_049_vs_microsoft_038` | 2 | 0.654 | Users can view or delete location data from their Microsoft ... | Microsoft Translator processes device and usage data from us... |
| ? | `microsoft_049_vs_microsoft_039` | 2 | 0.811 | Microsoft is not responsible for how users use recording fea... | Windows Settings uses your camera when using integrated came... |
| ? | `microsoft_049_vs_microsoft_040` | 3 | 0.999 | Users can control which apps have access to device precise l... | Microsoft collects device location from Windows phones at fi... |
| ? | `microsoft_049_vs_microsoft_043` | 1 | 0.977 | Users can view or delete location data from their Microsoft ... | Microsoft collects device and SIM card identifiers when user... |
| ? | `microsoft_049_vs_microsoft_045` | 2 | 0.999 | Users can control which apps have access to device precise l... | Microsoft uses contextual device data and basic account data... |
| ? | `microsoft_049_vs_microsoft_046` | 1 | 0.508 | Users can view or delete location data from their Microsoft ... | Additional personal data may be collected based on feedback ... |
| ? | `microsoft_049_vs_microsoft_053` | 1 | 0.996 | Users can view or delete location data from their Microsoft ... | Microsoft Defender SmartScreen sends the full web address of... |
| ? | `microsoft_049_vs_microsoft_056` | 2 | 0.999 | Users can control which apps have access to device precise l... | Windows Update automatically downloads Windows software upda... |
| ? | `microsoft_049_vs_microsoft_057` | 3 | 0.971 | Users can view or delete location data from their Microsoft ... | Microsoft Edge allows users to create, manage, and save read... |
| ? | `microsoft_049_vs_microsoft_058` | 1 | 0.999 | Users can control which apps have access to device precise l... | Click to Do captures and analyzes screenshots to identify te... |
| ? | `microsoft_049_vs_microsoft_060` | 3 | 0.996 | Users can view or delete location data from their Microsoft ... | Windows Hello extracts unique points or features from biomet... |
| ? | `microsoft_049_vs_microsoft_062` | 1 | 0.794 | Users can view or delete location data from their Microsoft ... | Microsoft collects content you add, upload, or share through... |
| ? | `microsoft_049_vs_microsoft_063` | 2 | 0.998 | Users can control which apps have access to device precise l... | Microsoft Store automatically checks for, downloads, and ins... |
| ? | `microsoft_050_vs_microsoft_011` | 1 | 0.777 | Microsoft does not store images used for generating Narrator... | Microsoft displays user name, username, and profile photo in... |
| ? | `microsoft_050_vs_microsoft_012` | 1 | 0.998 | Microsoft does not store images used for generating Narrator... | Microsoft collects content a child adds, uploads, or shares ... |
| ? | `microsoft_050_vs_microsoft_027` | 2 | 0.976 | Microsoft does not store images used for generating Narrator... | When using connected experiences like Translate, the text se... |
| ? | `microsoft_050_vs_microsoft_029` | 4 | 0.999 | Microsoft does not store images used for generating Narrator... | Microsoft Launcher collects access to photos and videos to e... |
| ? | `microsoft_050_vs_microsoft_036` | 1 | 0.999 | Microsoft does not store images used for generating Narrator... | Microsoft collects images provided by users when they use Bi... |
| ? | `microsoft_050_vs_microsoft_045` | 3 | 1.000 | Users can disable Narrator image descriptions, page titles, ... | Microsoft uses contextual device data and basic account data... |
| ? | `microsoft_050_vs_microsoft_054` | 1 | 0.994 | Microsoft does not store images used for generating Narrator... | Turning off inking and typing personalization deletes the cu... |
| ? | `microsoft_050_vs_microsoft_055` | 1 | 0.998 | Microsoft does not store images used for generating Narrator... | Microsoft uses stored settings, files, and device configurat... |
| ? | `microsoft_050_vs_microsoft_058` | 2 | 0.999 | Microsoft does not store images used for generating Narrator... | Click to Do captures and analyzes screenshots to identify te... |
| ? | `microsoft_050_vs_microsoft_062` | 2 | 0.994 | Microsoft does not store images used for generating Narrator... | Microsoft collects content you add, upload, or share through... |
| ? | `microsoft_050_vs_microsoft_063` | 1 | 0.739 | Microsoft does not store images used for generating Narrator... | Your name and picture from your Microsoft account are publis... |
| ? | `microsoft_051_vs_microsoft_002` | 1 | 0.604 | Microsoft does not store what apps are installed or informat... | Microsoft uses cookies to provide personalized ads to users.... |
| ? | `microsoft_051_vs_microsoft_011` | 8 | 1.000 | Microsoft does not store what apps are installed or informat... | Microsoft creates a sign-in record including date, time, pro... |
| ? | `microsoft_051_vs_microsoft_012` | 9 | 1.000 | Microsoft does not store what apps are installed or informat... | Microsoft collects data about which games a child plays, the... |
| ? | `microsoft_051_vs_microsoft_015` | 1 | 0.999 | Microsoft does not store what apps are installed or informat... | Microsoft stores and processes personal data in customer's r... |
| ? | `microsoft_051_vs_microsoft_018` | 3 | 0.998 | Microsoft does not store what apps are installed or informat... | Microsoft uses data to select and deliver ads on Microsoft p... |
| ? | `microsoft_051_vs_microsoft_023` | 4 | 0.999 | Microsoft does not store what apps are installed or informat... | Microsoft uses customer data to personalize communication co... |
| ? | `microsoft_051_vs_microsoft_024` | 8 | 1.000 | Link to Windows does not collect work or school account info... | Microsoft uses Administrator Data to contact customers about... |
| ? | `microsoft_051_vs_microsoft_025` | 3 | 0.998 | Link to Windows does not collect work or school account info... | Microsoft uses collected data from enterprise software to co... |
| ? | `microsoft_051_vs_microsoft_027` | 4 | 0.969 | Microsoft never changes or deletes text messages on Android ... | Office Roaming Service removes settings from a device when u... |
| ? | `microsoft_051_vs_microsoft_028` | 5 | 1.000 | Microsoft does not store what apps are installed or informat... | Microsoft collects details about how children use their devi... |
| ? | `microsoft_051_vs_microsoft_029` | 6 | 1.000 | Microsoft does not store what apps are installed or informat... | Microsoft Launcher uses account information to provide perso... |
| ? | `microsoft_051_vs_microsoft_030` | 1 | 1.000 | Microsoft does not store what apps are installed or informat... | Microsoft collects data about Teams feature usage and commun... |
| ? | `microsoft_051_vs_microsoft_032` | 2 | 0.998 | Microsoft never stores photos on servers or changes or delet... | Mobile Outlook application syncs data to Microsoft servers t... |
| ? | `microsoft_051_vs_microsoft_033` | 3 | 0.999 | Microsoft does not store what apps are installed or informat... | Required diagnostic data is always sent to Microsoft for all... |
| ? | `microsoft_051_vs_microsoft_036` | 5 | 0.998 | Microsoft does not store what apps are installed or informat... | Microsoft collects words, phrases, and surrounding content w... |
| ? | `microsoft_051_vs_microsoft_037` | 11 | 1.000 | Microsoft does not store what apps are installed or informat... | Microsoft Edge diagnostic data is transmitted to Microsoft a... |
| ? | `microsoft_051_vs_microsoft_038` | 1 | 0.996 | Microsoft does not store what apps are installed or informat... | Microsoft uses submitted data to personalize user experience... |
| ? | `microsoft_051_vs_microsoft_039` | 3 | 0.999 | Microsoft does not store what apps are installed or informat... | Windows collects data about you, your device, and how you us... |
| ? | `microsoft_051_vs_microsoft_040` | 7 | 0.999 | Microsoft does not store what apps are installed or informat... | Microsoft collects device and network identifiers from Windo... |
| ? | `microsoft_051_vs_microsoft_041` | 1 | 1.000 | Microsoft does not store what apps are installed or informat... | Microsoft collects activity history tracking apps, services,... |
| ? | `microsoft_051_vs_microsoft_044` | 8 | 1.000 | Microsoft does not store what apps are installed or informat... | Microsoft collects data about installed applications includi... |
| ? | `microsoft_051_vs_microsoft_045` | 18 | 1.000 | Microsoft does not store what apps are installed or informat... | Microsoft uses device information and activity data locally ... |
| ? | `microsoft_051_vs_microsoft_046` | 2 | 0.998 | Microsoft does not store what apps are installed or informat... | Feedback Hub periodically reads the installed app list to de... |
| ? | `microsoft_051_vs_microsoft_047` | 1 | 0.996 | Microsoft does not store what apps are installed or informat... | Get Help accesses the Application List to aid in opening the... |
| ? | `microsoft_051_vs_microsoft_049` | 7 | 0.999 | Microsoft never changes or deletes text messages on Android ... | Microsoft retains only the last known location, with each ne... |
| ? | `microsoft_051_vs_microsoft_050` | 3 | 0.993 | Microsoft does not store what apps are installed or informat... | When users request popular links summaries, the visited URL ... |
| ? | `microsoft_051_vs_microsoft_053` | 8 | 1.000 | Microsoft does not store what apps are installed or informat... | When Microsoft Defender SmartScreen or Smart App Control che... |
| ? | `microsoft_051_vs_microsoft_054` | 2 | 0.665 | Microsoft never changes or deletes text messages on Android ... | Turning off inking and typing personalization deletes the cu... |
| ? | `microsoft_051_vs_microsoft_055` | 5 | 1.000 | Microsoft does not store what apps are installed or informat... | Microsoft uses stored settings, files, and device configurat... |
| ? | `microsoft_051_vs_microsoft_057` | 3 | 0.998 | Microsoft does not store what apps are installed or informat... | Microsoft Edge stores data about device and browser usage in... |
| ? | `microsoft_051_vs_microsoft_058` | 1 | 0.998 | Microsoft never stores photos on servers or changes or delet... | Click to Do captures and analyzes screenshots to identify te... |
| ? | `microsoft_051_vs_microsoft_062` | 7 | 1.000 | Microsoft does not store what apps are installed or informat... | Microsoft collects data about games played, apps used, game ... |
| ? | `microsoft_051_vs_microsoft_063` | 5 | 0.999 | Microsoft does not store what apps are installed or informat... | Your Microsoft account is associated with your ratings and r... |
| ? | `microsoft_051_vs_microsoft_064` | 6 | 1.000 | Microsoft does not store what apps are installed or informat... | Microsoft collects data on app installation, version, device... |
| ? | `microsoft_051_vs_microsoft_065` | 2 | 0.987 | Microsoft never stores photos on servers or changes or delet... | Silverlight sends a request to a Microsoft server containing... |
| ? | `microsoft_052_vs_microsoft_011` | 4 | 1.000 | Microsoft does not record or store camera sessions or inform... | Microsoft creates a sign-in record including date, time, pro... |
| ? | `microsoft_052_vs_microsoft_012` | 8 | 1.000 | Microsoft does not record or store camera sessions or inform... | Microsoft collects information about a child's Xbox sign-in ... |
| ? | `microsoft_052_vs_microsoft_015` | 2 | 0.998 | Microsoft does not record or store camera sessions or inform... | Microsoft stores and processes personal data in customer's r... |
| ? | `microsoft_052_vs_microsoft_018` | 1 | 0.994 | Microsoft does not record or store camera sessions or inform... | Microsoft serves personalized ads based on online activity w... |
| ? | `microsoft_052_vs_microsoft_022` | 1 | 0.763 | Microsoft does not record or store camera sessions or inform... | Microsoft uses Copilot conversations to monitor performance,... |
| ? | `microsoft_052_vs_microsoft_023` | 2 | 0.997 | Microsoft does not record or store camera sessions or inform... | Microsoft uses customer data to personalize communication co... |
| ? | `microsoft_052_vs_microsoft_024` | 8 | 1.000 | Microsoft does not record or store camera sessions or inform... | Microsoft collects Customer Data, Personal Data, Administrat... |
| ? | `microsoft_052_vs_microsoft_025` | 2 | 0.993 | Microsoft does not record or store camera sessions or inform... | Microsoft uses collected data from enterprise software to co... |
| ? | `microsoft_052_vs_microsoft_027` | 4 | 0.998 | Microsoft does not record or store camera sessions or inform... | OneNote can insert photos or record video using device camer... |
| ? | `microsoft_052_vs_microsoft_028` | 7 | 1.000 | Microsoft does not record or store camera sessions or inform... | Microsoft collects details about how children use their devi... |
| ? | `microsoft_052_vs_microsoft_029` | 10 | 1.000 | Microsoft does not record or store camera sessions or inform... | Microsoft Launcher collects device photos, files, and app us... |
| ? | `microsoft_052_vs_microsoft_030` | 1 | 1.000 | Microsoft does not record or store camera sessions or inform... | Microsoft collects data about Teams feature usage and commun... |
| ? | `microsoft_052_vs_microsoft_031` | 2 | 0.999 | Microsoft will not store file contents from mobile devices a... | OneDrive collects device information to deliver personalized... |
| ? | `microsoft_052_vs_microsoft_032` | 2 | 0.996 | Microsoft never stores photos on its servers or modifies pho... | Mobile Outlook application syncs data to Microsoft servers t... |
| ? | `microsoft_052_vs_microsoft_033` | 6 | 0.999 | Microsoft does not record or store camera sessions or inform... | Microsoft collects diagnostic data from Surface devices and ... |
| ? | `microsoft_052_vs_microsoft_036` | 3 | 0.999 | Microsoft does not record or store camera sessions or inform... | Microsoft collects images provided by users when they use Bi... |
| ? | `microsoft_052_vs_microsoft_037` | 13 | 0.999 | Microsoft does not record or store camera sessions or inform... | Microsoft Edge uses stored privacy preferences to migrate ac... |
| ? | `microsoft_052_vs_microsoft_038` | 3 | 0.988 | Microsoft does not record or store camera sessions or inform... | Microsoft uses submitted data to personalize user experience... |
| ? | `microsoft_052_vs_microsoft_039` | 5 | 0.999 | Microsoft does not record or store camera sessions or inform... | Windows collects data about you, your device, and how you us... |
| ? | `microsoft_052_vs_microsoft_040` | 10 | 1.000 | Microsoft will not store file contents from mobile devices a... | Microsoft collects device location from Windows phones at fi... |
| ? | `microsoft_052_vs_microsoft_044` | 7 | 0.999 | Microsoft does not record or store camera sessions or inform... | Microsoft collects device information including processor ty... |
| ? | `microsoft_052_vs_microsoft_045` | 18 | 1.000 | Microsoft does not record or store camera sessions or inform... | Microsoft uses device information and Windows diagnostic dat... |
| ? | `microsoft_052_vs_microsoft_046` | 1 | 0.991 | Microsoft does not record or store camera sessions or inform... | Diagnostic data is sent to Microsoft when you submit feedbac... |
| ? | `microsoft_052_vs_microsoft_049` | 9 | 0.999 | Microsoft never stores photos on its servers or modifies pho... | Microsoft retains only the last known location, with each ne... |
| ? | `microsoft_052_vs_microsoft_050` | 1 | 0.999 | Microsoft never stores photos on its servers or modifies pho... | When users request image descriptions, images are sent to Mi... |
| ? | `microsoft_052_vs_microsoft_051` | 5 | 1.000 | Microsoft does not record or store camera sessions or inform... | Microsoft collects performance, usage, and device data inclu... |
| ? | `microsoft_052_vs_microsoft_053` | 8 | 0.999 | Microsoft does not record or store camera sessions or inform... | When Microsoft Defender SmartScreen checks web and app conte... |
| ? | `microsoft_052_vs_microsoft_054` | 1 | 0.999 | Microsoft does not record or store camera sessions or inform... | Windows actively listens to the microphone for app-specific ... |
| ? | `microsoft_052_vs_microsoft_055` | 5 | 1.000 | Microsoft does not record or store camera sessions or inform... | Microsoft uses stored settings, files, and device configurat... |
| ? | `microsoft_052_vs_microsoft_057` | 4 | 1.000 | Microsoft does not record or store camera sessions or inform... | Microsoft Edge stores data about device and browser usage in... |
| ? | `microsoft_052_vs_microsoft_058` | 4 | 1.000 | Microsoft does not record or store camera sessions or inform... | Click to Do captures and analyzes screenshots to identify te... |
| ? | `microsoft_052_vs_microsoft_060` | 2 | 1.000 | Microsoft does not record or store camera sessions or inform... | Windows Hello extracts unique points or features from biomet... |
| ? | `microsoft_052_vs_microsoft_061` | 1 | 0.969 | Microsoft does not record or store camera sessions or inform... | Microsoft uses collected data from Windows Search to provide... |
| ? | `microsoft_052_vs_microsoft_062` | 14 | 1.000 | Microsoft does not record or store camera sessions or inform... | Microsoft collects data about Xbox sign-in/sign-out, purchas... |
| ? | `microsoft_052_vs_microsoft_063` | 2 | 0.963 | Microsoft does not record or store camera sessions or inform... | Microsoft collects data about how you access and use Microso... |
| ? | `microsoft_052_vs_microsoft_064` | 4 | 0.998 | Microsoft does not record or store camera sessions or inform... | Microsoft collects data about user interactions with Microso... |
| ? | `microsoft_052_vs_microsoft_065` | 3 | 0.993 | Microsoft never stores photos on its servers or modifies pho... | Silverlight sends a request to a Microsoft server containing... |
| ? | `microsoft_052_vs_microsoft_066` | 2 | 0.997 | Microsoft does not record or store camera sessions or inform... | Microsoft uses diagnostic data to improve Mixed Reality and ... |
| ? | `microsoft_054_vs_microsoft_012` | 2 | 0.995 | Microsoft will not store, sample, or listen to voice typing ... | Microsoft collects content a child adds, uploads, or shares ... |
| ? | `microsoft_054_vs_microsoft_019` | 2 | 0.783 | When online speech recognition is turned off, Microsoft will... | Microsoft transcribes voice data into text using speech reco... |
| ? | `microsoft_054_vs_microsoft_022` | 1 | 0.712 | Microsoft will not store, sample, or listen to voice typing ... | Microsoft Copilot uses prior conversation history to persona... |
| ? | `microsoft_054_vs_microsoft_024` | 4 | 0.999 | When online speech recognition is turned off, Microsoft will... | Microsoft uses Payment Data to complete transactions and det... |
| ? | `microsoft_054_vs_microsoft_027` | 5 | 0.993 | Microsoft will not store, sample, or listen to voice typing ... | Speaker Coach accesses device microphone and provides on-scr... |
| ? | `microsoft_054_vs_microsoft_028` | 3 | 0.996 | Microsoft will not store, sample, or listen to voice typing ... | Microsoft uploads location data to the cloud and shares it w... |
| ? | `microsoft_054_vs_microsoft_029` | 3 | 0.997 | Microsoft will not store, sample, or listen to voice typing ... | Microsoft Launcher syncs Glance data across devices signed i... |
| ? | `microsoft_054_vs_microsoft_030` | 2 | 0.939 | Microsoft will not store, sample, or listen to voice typing ... | Microsoft collects data about Teams feature usage and commun... |
| ? | `microsoft_054_vs_microsoft_033` | 4 | 0.999 | When online speech recognition is turned off, Microsoft will... | Required diagnostic data is always sent to Microsoft for all... |
| ? | `microsoft_054_vs_microsoft_036` | 5 | 0.997 | Microsoft will not store, sample, or listen to voice recordi... | Microsoft collects voice input and performance data when use... |
| ? | `microsoft_054_vs_microsoft_037` | 2 | 0.991 | Microsoft will not store, sample, or listen to voice typing ... | Microsoft Edge caches content collected into collections on ... |
| ? | `microsoft_054_vs_microsoft_038` | 3 | 0.999 | Microsoft will not store, sample, or listen to voice typing ... | Microsoft randomly samples text and audio to improve Microso... |
| ? | `microsoft_054_vs_microsoft_039` | 1 | 0.685 | When online speech recognition is turned off, Microsoft will... | Windows Settings uses your microphone when controlling volum... |
| ? | `microsoft_054_vs_microsoft_040` | 2 | 0.993 | Microsoft will not store, sample, or listen to voice typing ... | Microsoft collects device location from Windows phones at fi... |
| ? | `microsoft_054_vs_microsoft_044` | 1 | 0.914 | Microsoft will not store, sample, or listen to voice typing ... | Microsoft collects optional diagnostic data including browsi... |
| ? | `microsoft_054_vs_microsoft_045` | 5 | 0.999 | When online speech recognition is turned off, Microsoft will... | Microsoft uses contextual device data and basic account data... |
| ? | `microsoft_054_vs_microsoft_046` | 1 | 0.717 | Microsoft will not store, sample, or listen to voice typing ... | Diagnostic data is sent to Microsoft when you submit feedbac... |
| ? | `microsoft_054_vs_microsoft_049` | 8 | 1.000 | Microsoft will not store, sample, or listen to voice recordi... | Recordings are saved locally on the device by default.... |
| ? | `microsoft_054_vs_microsoft_055` | 2 | 0.897 | Microsoft will not store, sample, or listen to voice typing ... | Microsoft uses stored settings, files, and device configurat... |
| ? | `microsoft_054_vs_microsoft_056` | 2 | 0.993 | Microsoft will not store, sample, or listen to voice typing ... | Apps from the Microsoft Store are automatically updated thro... |
| ? | `microsoft_054_vs_microsoft_057` | 2 | 0.956 | Microsoft will not store, sample, or listen to voice typing ... | Microsoft Edge syncs favorites, reading lists, autofill form... |
| ? | `microsoft_054_vs_microsoft_062` | 3 | 0.991 | Microsoft will not store, sample, or listen to voice recordi... | Xbox games can use device microphone, camera, and screen rec... |
| ? | `microsoft_054_vs_microsoft_063` | 2 | 0.985 | Microsoft will not store, sample, or listen to voice typing ... | Microsoft Store automatically checks for, downloads, and ins... |
| ? | `microsoft_055_vs_microsoft_011` | 4 | 0.999 | Users can delete previously backed up data from their Micros... | Microsoft creates a sign-in record including date, time, pro... |
| ? | `microsoft_055_vs_microsoft_012` | 5 | 0.998 | Users can delete previously backed up data from their Micros... | Microsoft assigns a unique identifier to a child's device wh... |
| ? | `microsoft_055_vs_microsoft_018` | 2 | 0.996 | Users can delete previously backed up data from their Micros... | Microsoft serves personalized ads based on online activity w... |
| ? | `microsoft_055_vs_microsoft_019` | 2 | 0.984 | Users can delete previously backed up data from their Micros... | Microsoft uses voice data to build and improve speech recogn... |
| ? | `microsoft_055_vs_microsoft_022` | 1 | 0.999 | Users can delete previously backed up data from their Micros... | Microsoft Copilot uses prior conversation history to persona... |
| ? | `microsoft_055_vs_microsoft_023` | 3 | 0.976 | Users can delete previously backed up data from their Micros... | Microsoft collects customer name and contact data when engag... |
| ? | `microsoft_055_vs_microsoft_024` | 1 | 0.990 | Users can delete previously backed up data from their Micros... | Microsoft uses Administrator Data to contact customers about... |
| ? | `microsoft_055_vs_microsoft_025` | 1 | 0.923 | Users can turn off the feature that stores settings, files, ... | Microsoft collects diagnostic data from HoloLens to solve pr... |
| ? | `microsoft_055_vs_microsoft_027` | 2 | 0.984 | Users can delete previously backed up data from their Micros... | Essential services like the licensing service cannot be disa... |
| ? | `microsoft_055_vs_microsoft_028` | 3 | 1.000 | Users can delete previously backed up data from their Micros... | Microsoft uploads location data to the cloud and shares it w... |
| ? | `microsoft_055_vs_microsoft_029` | 6 | 0.998 | Users can delete previously backed up data from their Micros... | Microsoft Launcher syncs Glance data across devices signed i... |
| ? | `microsoft_055_vs_microsoft_030` | 1 | 0.825 | Users can delete previously backed up data from their Micros... | Microsoft processes non-user contact data to determine Teams... |
| ? | `microsoft_055_vs_microsoft_031` | 1 | 0.717 | Users can delete previously backed up data from their Micros... | OneDrive for Business collects and transmits personal data i... |
| ? | `microsoft_055_vs_microsoft_032` | 3 | 0.992 | Users can delete previously backed up data from their Micros... | Mail, calendar items, files, contacts, and settings automati... |
| ? | `microsoft_055_vs_microsoft_033` | 1 | 0.974 | Users can delete previously backed up data from their Micros... | Required diagnostic data is always sent to Microsoft for all... |
| ? | `microsoft_055_vs_microsoft_036` | 1 | 0.995 | Users can delete previously backed up data from their Micros... | Microsoft syncs search history across devices when users sig... |
| ? | `microsoft_055_vs_microsoft_037` | 4 | 0.996 | Users can delete previously backed up data from their Micros... | Microsoft Edge hashes, encrypts, and sends saved credentials... |
| ? | `microsoft_055_vs_microsoft_038` | 2 | 0.993 | Users can turn off the feature that stores settings, files, ... | Microsoft Translator processes device and usage data from us... |
| ? | `microsoft_055_vs_microsoft_039` | 2 | 0.990 | Users can turn off the feature that stores settings, files, ... | Windows Settings uses location to change brightness at night... |
| ? | `microsoft_055_vs_microsoft_040` | 4 | 0.999 | Users can delete previously backed up data from their Micros... | Microsoft collects device and network identifiers from Windo... |
| ? | `microsoft_055_vs_microsoft_043` | 2 | 0.998 | Users can delete previously backed up data from their Micros... | Microsoft collects device and SIM card identifiers when user... |
| ? | `microsoft_055_vs_microsoft_045` | 5 | 0.999 | Users can turn off the feature that stores settings, files, ... | Microsoft uses contextual device data and basic account data... |
| ? | `microsoft_055_vs_microsoft_047` | 1 | 0.894 | Users can delete previously backed up data from their Micros... | Users can sign into Get Help with their Microsoft account to... |
| ? | `microsoft_055_vs_microsoft_049` | 6 | 1.000 | Users can turn off the feature that stores settings, files, ... | Microsoft retains only the last known location, with each ne... |
| ? | `microsoft_055_vs_microsoft_053` | 3 | 0.993 | Users can delete previously backed up data from their Micros... | Microsoft Defender SmartScreen sends the full web address of... |
| ? | `microsoft_055_vs_microsoft_054` | 1 | 0.957 | Users can delete previously backed up data from their Micros... | Microsoft collects voice recordings to provide speech recogn... |
| ? | `microsoft_055_vs_microsoft_057` | 3 | 0.998 | Users can delete previously backed up data from their Micros... | Microsoft Edge syncs favorites, reading lists, autofill form... |
| ? | `microsoft_055_vs_microsoft_060` | 2 | 0.999 | Users can delete previously backed up data from their Micros... | Windows Hello extracts unique points or features from biomet... |
| ? | `microsoft_055_vs_microsoft_061` | 2 | 0.936 | Users can delete previously backed up data from their Micros... | Microsoft collects user online activities through Windows Se... |
| ? | `microsoft_055_vs_microsoft_062` | 3 | 0.948 | Users can delete previously backed up data from their Micros... | Microsoft stores offline Xbox usage data on device storage a... |
| ? | `microsoft_055_vs_microsoft_063` | 1 | 0.985 | Users can delete previously backed up data from their Micros... | Microsoft Store uses your device's region configuration to s... |
| ? | `microsoft_058_vs_microsoft_012` | 2 | 0.996 | Recall microphone audio is not transmitted off the user's de... | Kinect microphone enables voice chat between players and voi... |
| ? | `microsoft_058_vs_microsoft_019` | 2 | 0.998 | Recall microphone audio is not transmitted off the user's de... | Microsoft transcribes voice data into text using speech reco... |
| ? | `microsoft_058_vs_microsoft_023` | 1 | 0.981 | Recall analysis of snapshots is always performed locally on ... | Microsoft collects device and usage data from customers inte... |
| ? | `microsoft_058_vs_microsoft_025` | 2 | 0.999 | Recall microphone audio is not transmitted off the user's de... | HoloLens microphones enable voice commands for navigation, c... |
| ? | `microsoft_058_vs_microsoft_027` | 7 | 0.999 | Recall data remains local to device and is not transmitted u... | Office Roaming Service removes settings from a device when u... |
| ? | `microsoft_058_vs_microsoft_028` | 4 | 1.000 | Recall data remains local to device and is not transmitted u... | Microsoft uploads location data to the cloud and shares it w... |
| ? | `microsoft_058_vs_microsoft_029` | 5 | 0.999 | Recall data remains local to device and is not transmitted u... | Microsoft Launcher syncs Glance data across devices signed i... |
| ? | `microsoft_058_vs_microsoft_030` | 3 | 1.000 | Click to Do data remains on local device unless user explici... | Microsoft stores non-user contact information on servers whi... |
| ? | `microsoft_058_vs_microsoft_031` | 3 | 0.999 | Recall data remains local to device and is not transmitted u... | OneDrive for Business collects and transmits personal data i... |
| ? | `microsoft_058_vs_microsoft_032` | 3 | 0.743 | Recall microphone audio is not transmitted off the user's de... | Outlook Dictate feature uses device microphone or connected ... |
| ? | `microsoft_058_vs_microsoft_033` | 2 | 0.998 | Click to Do data remains on local device unless user explici... | Required diagnostic data is always sent to Microsoft for all... |
| ? | `microsoft_058_vs_microsoft_036` | 2 | 0.989 | Recall analysis of snapshots is always performed locally on ... | Microsoft syncs search history across devices when users sig... |
| ? | `microsoft_058_vs_microsoft_037` | 5 | 0.998 | Click to Do data remains on local device unless user explici... | Microsoft Edge sends search queries, device information, and... |
| ? | `microsoft_058_vs_microsoft_038` | 2 | 0.933 | Click to Do data remains on local device unless user explici... | Microsoft deletes identifiers and certain text like email ad... |
| ? | `microsoft_058_vs_microsoft_039` | 5 | 0.998 | Recall analysis of snapshots is always performed locally on ... | SwiftKey collects de-identified device and usage data to ana... |
| ? | `microsoft_058_vs_microsoft_040` | 2 | 0.997 | Click to Do data remains on local device unless user explici... | Microsoft collects device location from Windows phones at fi... |
| ? | `microsoft_058_vs_microsoft_045` | 3 | 1.000 | Recall data remains local to device and is not transmitted u... | Microsoft transmits Tailored experiences data to Microsoft s... |
| ? | `microsoft_058_vs_microsoft_046` | 3 | 1.000 | Recall analysis of snapshots is always performed locally on ... | Feedback Hub determines installed apps through public APIs o... |
| ? | `microsoft_058_vs_microsoft_049` | 12 | 1.000 | Recall analysis of snapshots is always performed locally on ... | Microsoft retains only the last known location, with each ne... |
| ? | `microsoft_058_vs_microsoft_050` | 1 | 0.597 | Recall microphone audio is not transmitted off the user's de... | When users enable 'Help Make Narrator Better' and submit ver... |
| ? | `microsoft_058_vs_microsoft_051` | 4 | 0.999 | Recall data remains local to device and is not transmitted u... | Phone Link accesses content of text messages and contact inf... |
| ? | `microsoft_058_vs_microsoft_053` | 4 | 1.000 | Recall analysis of snapshots is always performed locally on ... | When Microsoft Defender SmartScreen or Smart App Control che... |
| ? | `microsoft_058_vs_microsoft_054` | 5 | 0.998 | Click to Do microphone audio is not transmitted off the user... | Windows actively listens to the microphone for app-specific ... |
| ? | `microsoft_058_vs_microsoft_055` | 4 | 1.000 | Recall analysis of snapshots is always performed locally on ... | Windows stores settings, files, and device configuration dat... |
| ? | `microsoft_058_vs_microsoft_057` | 7 | 1.000 | Recall data remains local to device and is not transmitted u... | Microsoft Edge sends search queries, device information, and... |
| ? | `microsoft_058_vs_microsoft_062` | 3 | 0.996 | Recall microphone audio is not transmitted off the user's de... | Kinect microphone enables voice chat between players and voi... |
| ? | `microsoft_062_vs_microsoft_007` | 2 | 0.946 | Third-party publishers have independent relationships with u... | Microsoft shares personal data among its controlled affiliat... |
| ? | `microsoft_062_vs_microsoft_018` | 1 | 0.985 | Third-party publishers have independent relationships with u... | Microsoft shares reports with advertisers about data collect... |
| ? | `microsoft_062_vs_microsoft_024` | 1 | 0.989 | Game leaderboard scores and gamertags are considered public ... | Microsoft relies on statistical and aggregate pseudonymized ... |
| ? | `microsoft_062_vs_microsoft_030` | 1 | 0.928 | Third-party publishers have independent relationships with u... | Microsoft shares user information with Enterprise customers ... |
| ? | `microsoft_063_vs_microsoft_007` | 2 | 0.994 | App developers are required to provide privacy policies for ... | Microsoft shares personal data with third parties when users... |
| ? | `microsoft_063_vs_microsoft_011` | 1 | 0.999 | App developers are required to provide privacy policies for ... | Third parties can use or share data received from Microsoft ... |
| ? | `microsoft_063_vs_microsoft_018` | 1 | 0.540 | App developers are required to provide privacy policies for ... | Third parties can access and use the advertising ID in Windo... |
| ? | `microsoft_063_vs_microsoft_033` | 1 | 0.998 | App developers are required to provide privacy policies for ... | Microsoft may access, transfer, disclose, and preserve user ... |
| ? | `microsoft_063_vs_microsoft_043` | 1 | 0.983 | App developers are required to provide privacy policies for ... | Microsoft shares device and SIM card identifiers with third-... |
| ? | `microsoft_064_vs_microsoft_007` | 5 | 0.999 | User sign-in credentials for third-party financial access ar... | Microsoft discloses personal data to prevent spam, fraud, an... |
| ? | `microsoft_064_vs_microsoft_011` | 9 | 0.999 | User sign-in credentials for third-party financial access ar... | Microsoft collects credentials, name, contact data, payment ... |
| ? | `microsoft_064_vs_microsoft_012` | 2 | 0.988 | Users can opt out of interest-based advertising through Micr... | Microsoft blocks users under 13 or asks for parental consent... |
| ? | `microsoft_064_vs_microsoft_018` | 1 | 0.999 | User sign-in credentials for third-party financial access ar... | Third parties can access and use the advertising ID in Windo... |
| ? | `microsoft_064_vs_microsoft_023` | 3 | 0.996 | Users can opt out of interest-based advertising through Micr... | Microsoft collects customer name and contact data when engag... |
| ? | `microsoft_064_vs_microsoft_024` | 2 | 0.999 | Users can opt out of interest-based advertising through Micr... | Microsoft uses Payment Data to complete transactions and det... |
| ? | `microsoft_064_vs_microsoft_027` | 2 | 1.000 | Users can opt out of interest-based advertising through Micr... | Office Roaming Service removes settings from a device when u... |
| ? | `microsoft_064_vs_microsoft_028` | 1 | 0.825 | Users can opt out of interest-based advertising through Micr... | Microsoft collects details about how children use their devi... |
| ? | `microsoft_064_vs_microsoft_029` | 1 | 0.918 | Users can opt out of interest-based advertising through Micr... | Microsoft Launcher uses account information to provide perso... |
| ? | `microsoft_064_vs_microsoft_030` | 1 | 0.993 | User sign-in credentials for third-party financial access ar... | Microsoft shares user information with Enterprise customers ... |
| ? | `microsoft_064_vs_microsoft_031` | 1 | 0.999 | User sign-in credentials for third-party financial access ar... | OneDrive for Business transmits authentication data to Micro... |
| ? | `microsoft_064_vs_microsoft_036` | 2 | 0.998 | Users can opt out of interest-based advertising through Micr... | Microsoft collects words, phrases, and surrounding content w... |
| ? | `microsoft_064_vs_microsoft_037` | 1 | 0.998 | Users can opt out of interest-based advertising through Micr... | Microsoft Edge sends information typed into the browser addr... |
| ? | `microsoft_064_vs_microsoft_038` | 1 | 0.996 | Users can opt out of interest-based advertising through Micr... | Microsoft deletes identifiers and certain text like email ad... |
| ? | `microsoft_064_vs_microsoft_040` | 1 | 0.821 | User sign-in credentials for third-party financial access ar... | Microsoft collects product keys when Windows is activated on... |
| ? | `microsoft_064_vs_microsoft_043` | 1 | 0.927 | User sign-in credentials for third-party financial access ar... | Microsoft shares device and SIM card identifiers with third-... |
| ? | `microsoft_064_vs_microsoft_045` | 4 | 1.000 | Users can opt out of interest-based advertising through Micr... | Microsoft uses contextual device data and basic account data... |
| ? | `microsoft_064_vs_microsoft_049` | 2 | 1.000 | Users can opt out of interest-based advertising through Micr... | Microsoft removes identifying data from location information... |
| ? | `microsoft_064_vs_microsoft_053` | 1 | 0.505 | Users can opt out of interest-based advertising through Micr... | Microsoft Defender Antivirus automatically sends reports to ... |
| ? | `microsoft_064_vs_microsoft_057` | 1 | 0.998 | User sign-in credentials for third-party financial access ar... | Microsoft syncs browser information across devices when user... |
| ? | `microsoft_064_vs_microsoft_062` | 5 | 0.999 | User sign-in credentials for third-party financial access ar... | Game and app publishers receive access to your Xbox user ide... |
| ? | `microsoft_064_vs_microsoft_063` | 2 | 0.997 | Users can opt out of interest-based advertising through Micr... | Microsoft Store automatically checks for, downloads, and ins... |
| ? | `microsoft_066_vs_microsoft_011` | 3 | 1.000 | Hand gesture data is processed on the PC and is not stored.... | Microsoft creates a sign-in record including date, time, pro... |
| ? | `microsoft_066_vs_microsoft_012` | 5 | 1.000 | Hand gesture data is processed on the PC and is not stored.... | Microsoft uses voice-to-text data from Xbox party chat to pr... |
| ? | `microsoft_066_vs_microsoft_015` | 1 | 0.999 | Hand gesture data is processed on the PC and is not stored.... | Microsoft stores and processes personal data in customer's r... |
| ? | `microsoft_066_vs_microsoft_019` | 1 | 1.000 | Hand gesture data is processed on the PC and is not stored.... | Microsoft uses voice data to build and improve speech recogn... |
| ? | `microsoft_066_vs_microsoft_023` | 1 | 0.998 | Hand gesture data is processed on the PC and is not stored.... | Microsoft collects contact and payment data when customers p... |
| ? | `microsoft_066_vs_microsoft_025` | 2 | 1.000 | Hand gesture data is processed on the PC and is not stored.... | HoloLens collects data from cameras, microphones, and infrar... |
| ? | `microsoft_066_vs_microsoft_027` | 4 | 1.000 | Hand gesture data is processed on the PC and is not stored.... | PowerPoint presentation recording feature accesses device mi... |
| ? | `microsoft_066_vs_microsoft_028` | 3 | 0.999 | Hand gesture data is processed on the PC and is not stored.... | Microsoft uses location data to record drive habits includin... |
| ? | `microsoft_066_vs_microsoft_029` | 4 | 0.999 | Hand gesture data is processed on the PC and is not stored.... | Microsoft Launcher collects device camera and microphone acc... |
| ? | `microsoft_066_vs_microsoft_032` | 2 | 1.000 | Hand gesture data is processed on the PC and is not stored.... | Outlook Dictate feature uses device microphone or connected ... |
| ? | `microsoft_066_vs_microsoft_033` | 3 | 0.998 | Hand gesture data is processed on the PC and is not stored.... | Required diagnostic data is always sent to Microsoft for all... |
| ? | `microsoft_066_vs_microsoft_036` | 2 | 0.998 | Hand gesture data is processed on the PC and is not stored.... | Microsoft collects voice input and performance data when use... |
| ? | `microsoft_066_vs_microsoft_037` | 1 | 0.996 | Hand gesture data is processed on the PC and is not stored.... | Microsoft Edge stores data about how you use your browser, i... |
| ? | `microsoft_066_vs_microsoft_039` | 3 | 1.000 | Hand gesture data is processed on the PC and is not stored.... | Windows Settings uses your microphone when controlling volum... |
| ? | `microsoft_066_vs_microsoft_040` | 6 | 1.000 | Hand gesture data is processed on the PC and is not stored.... | Microsoft collects device and network identifiers from Windo... |
| ? | `microsoft_066_vs_microsoft_044` | 4 | 0.999 | Hand gesture data is processed on the PC and is not stored.... | Microsoft collects device information including processor ty... |
| ? | `microsoft_066_vs_microsoft_046` | 2 | 0.994 | Hand gesture data is processed on the PC and is not stored.... | Feedback Hub uses picture and document library to access scr... |
| ? | `microsoft_066_vs_microsoft_049` | 4 | 0.999 | Hand gesture data is processed on the PC and is not stored.... | Microsoft retains only the last known location, with each ne... |
| ? | `microsoft_066_vs_microsoft_051` | 2 | 1.000 | Hand gesture data is processed on the PC and is not stored.... | Microsoft collects performance, usage, and device data inclu... |
| ? | `microsoft_066_vs_microsoft_052` | 1 | 0.981 | Hand gesture data is processed on the PC and is not stored.... | Microsoft collects performance usage and device data, includ... |
| ? | `microsoft_066_vs_microsoft_053` | 2 | 0.999 | Hand gesture data is processed on the PC and is not stored.... | When Microsoft Defender SmartScreen or Smart App Control che... |
| ? | `microsoft_066_vs_microsoft_054` | 4 | 1.000 | Hand gesture data is processed on the PC and is not stored.... | Microsoft collects voice recordings to provide speech recogn... |
| ? | `microsoft_066_vs_microsoft_055` | 2 | 1.000 | Hand gesture data is processed on the PC and is not stored.... | Microsoft uses stored settings, files, and device configurat... |
| ? | `microsoft_066_vs_microsoft_057` | 2 | 1.000 | Hand gesture data is processed on the PC and is not stored.... | Microsoft Edge stores data about device and browser usage in... |
| ? | `microsoft_066_vs_microsoft_058` | 1 | 1.000 | Hand gesture data is processed on the PC and is not stored.... | Click to Do captures and analyzes screenshots to identify te... |
| ? | `microsoft_066_vs_microsoft_060` | 2 | 0.999 | Hand gesture data is processed on the PC and is not stored.... | Windows Hello extracts unique points or features from biomet... |
| ? | `microsoft_066_vs_microsoft_062` | 6 | 1.000 | Hand gesture data is processed on the PC and is not stored.... | Microsoft stores offline Xbox usage data on device storage a... |
| ? | `microsoft_066_vs_microsoft_063` | 3 | 0.997 | Hand gesture data is processed on the PC and is not stored.... | Microsoft Store uses your device identifier to manage produc... |
| ? | `microsoft_066_vs_microsoft_064` | 1 | 0.746 | Hand gesture data is processed on the PC and is not stored.... | Microsoft collects data on app installation, version, device... |
| ? | `tesla_002_vs_tesla_004` | 8 | 0.999 | Tesla keeps camera recordings anonymous and unlinked to user... | Tesla collects information when users visit websites, stores... |
| ? | `tesla_002_vs_tesla_005` | 5 | 1.000 | Tesla keeps camera recordings anonymous and unlinked to user... | Tesla collects contact information including name, address, ... |
| ? | `tesla_002_vs_tesla_006` | 4 | 0.999 | Tesla keeps camera recordings anonymous and unlinked to user... | Tesla collects information from or about Tesla product owner... |
| ? | `tesla_002_vs_tesla_007` | 8 | 1.000 | Tesla keeps camera recordings anonymous and unlinked to user... | Tesla collects purchase details, order agreements, trade-in ... |
| ? | `tesla_002_vs_tesla_008` | 10 | 1.000 | Tesla keeps camera recordings anonymous and unlinked to user... | Tesla collects diagnostic logs to identify and troubleshoot ... |
| ? | `tesla_002_vs_tesla_009` | 8 | 1.000 | Tesla keeps camera recordings anonymous and unlinked to user... | Tesla collects energy diagnostic logs for identifying and tr... |
| ? | `tesla_002_vs_tesla_010` | 4 | 1.000 | Tesla keeps camera recordings anonymous and unlinked to user... | Tesla collects service history data including repair history... |
| ? | `tesla_002_vs_tesla_011` | 5 | 0.999 | Tesla keeps camera recordings anonymous and unlinked to user... | Tesla collects diagnostic logs from vehicles and energy prod... |
| ? | `tesla_002_vs_tesla_012` | 13 | 1.000 | Tesla requires user consent for Data Sharing before sharing ... | Tesla collects usage analytics from vehicle touchscreen, sto... |
| ? | `tesla_002_vs_tesla_013` | 2 | 0.891 | Tesla requires user consent for Data Sharing before sharing ... | Tesla collects Safety Event camera recordings automatically ... |
| ? | `tesla_002_vs_tesla_014` | 3 | 0.980 | Tesla keeps camera recordings anonymous and unlinked to user... | Tesla uses collected information to communicate with users a... |
| ? | `tesla_002_vs_tesla_015` | 11 | 1.000 | Tesla keeps camera recordings anonymous and unlinked to user... | Tesla uses personal information to offer information on cont... |
| ? | `tesla_002_vs_tesla_016` | 7 | 1.000 | Tesla keeps camera recordings anonymous and unlinked to user... | Tesla uses customer data to complete purchases, process prod... |
| ? | `tesla_002_vs_tesla_017` | 10 | 0.999 | Tesla keeps camera recordings anonymous and unlinked to user... | Tesla uses user online activities and generic personal infor... |
| ? | `tesla_002_vs_tesla_018` | 13 | 1.000 | Tesla keeps camera recordings anonymous and unlinked to user... | Tesla uses personal data to analyze, reconstruct, investigat... |
| ? | `tesla_002_vs_tesla_019` | 10 | 1.000 | Tesla only shares personal data when needed to operate or se... | Tesla uses non-personally identifying information for operat... |
| ? | `tesla_002_vs_tesla_020` | 7 | 1.000 | Tesla keeps camera recordings anonymous and unlinked to user... | Tesla shares personal data with third parties as required by... |
| ? | `tesla_002_vs_tesla_022` | 2 | 0.969 | Tesla only shares personal data when needed to operate or se... | Tesla shares connected product data with third-party app dev... |
| ? | `tesla_002_vs_tesla_023` | 8 | 1.000 | Tesla keeps camera recordings anonymous and unlinked to user... | Tesla shares personal data with law enforcement and governme... |
| ? | `tesla_002_vs_tesla_028` | 1 | 0.990 | Tesla keeps camera recordings anonymous and unlinked to user... | Tesla collects and processes personal data based on consent,... |
| ? | `tesla_006_vs_tesla_002` | 4 | 0.985 | Customers can access and update their Tesla Account informat... | Tesla collects minimal personal data necessary for in-app en... |
| ? | `tesla_006_vs_tesla_010` | 1 | 0.897 | Customers can access and update their Tesla Account informat... | Tesla shares road segment data with partners in anonymized f... |
| ? | `tesla_006_vs_tesla_012` | 1 | 0.999 | Customers can access and update their Tesla Account informat... | Tesla collects usage analytics from vehicle touchscreen, sto... |
| ? | `tesla_006_vs_tesla_016` | 1 | 0.982 | Not all types of information collected may be applicable dep... | Tesla uses customer data to understand, triage, and fix issu... |
| ? | `tesla_006_vs_tesla_018` | 2 | 0.987 | Not all types of information collected may be applicable dep... | Tesla uses personal data to analyze, reconstruct, investigat... |
| ? | `tesla_006_vs_tesla_020` | 1 | 0.994 | Customers can access and update their Tesla Account informat... | Tesla shares personal data with third parties as required by... |
| ? | `tesla_006_vs_tesla_023` | 2 | 0.995 | Not all types of information collected may be applicable dep... | Tesla shares personal data with law enforcement and governme... |
| ? | `tesla_010_vs_tesla_002` | 2 | 0.999 | Tesla does not link location data with account or identity, ... | Tesla collects vehicle, diagnostic, infotainment system, and... |
| ? | `tesla_010_vs_tesla_006` | 1 | 0.973 | Tesla does not link location data with account or identity, ... | Tesla collects information from or about Tesla product owner... |
| ? | `tesla_010_vs_tesla_007` | 1 | 0.999 | Tesla does not link location data with account or identity, ... | Tesla collects purchase details, order agreements, trade-in ... |
| ? | `tesla_010_vs_tesla_008` | 5 | 1.000 | Tesla does not link location data with account or identity, ... | Tesla collects service and repair history including facility... |
| ? | `tesla_010_vs_tesla_009` | 2 | 0.898 | Tesla does not link location data with account or identity, ... | Tesla collects home details including roof dimensions, elect... |
| ? | `tesla_010_vs_tesla_011` | 2 | 0.946 | Tesla does not link location data with account or identity, ... | Tesla uses diagnostic logs to make continuous improvements t... |
| ? | `tesla_010_vs_tesla_012` | 1 | 0.999 | Tesla does not link location data with account or identity, ... | Calendar, Phone, Messages, Contacts, Browser, Dashcam, and S... |
| ? | `tesla_010_vs_tesla_014` | 1 | 0.722 | Tesla does not link location data with account or identity, ... | Tesla uses collected information to communicate with users a... |
| ? | `tesla_010_vs_tesla_015` | 2 | 0.996 | Tesla does not link location data with account or identity, ... | Tesla uses personal information to offer information on cont... |
| ? | `tesla_010_vs_tesla_016` | 3 | 0.999 | Tesla does not link location data with account or identity, ... | Tesla uses customer data to complete purchases, process prod... |
| ? | `tesla_010_vs_tesla_018` | 4 | 1.000 | Tesla does not link location data with account or identity, ... | Tesla uses personal data to analyze, reconstruct, investigat... |
| ? | `tesla_010_vs_tesla_020` | 3 | 0.999 | Tesla does not link location data with account or identity, ... | Tesla shares personal data for customer service, marketing, ... |
| ? | `tesla_010_vs_tesla_023` | 2 | 0.999 | Tesla does not link location data with account or identity, ... | Tesla shares personal data with law enforcement and governme... |
| ? | `tesla_011_vs_tesla_007` | 4 | 0.998 | Tesla aims to collect the minimum level of diagnostic data n... | Tesla uses customer support activity data to provide custome... |
| ? | `tesla_011_vs_tesla_015` | 5 | 1.000 | Tesla aims to collect the minimum level of diagnostic data n... | Tesla uses personal information for educational and awarenes... |
| ? | `tesla_011_vs_tesla_016` | 1 | 0.997 | Tesla aims to collect the minimum level of diagnostic data n... | Tesla uses financial data to process payments for products o... |
| ? | `tesla_011_vs_tesla_020` | 2 | 0.996 | Tesla aims to collect the minimum level of diagnostic data n... | Tesla shares personal data for payment processing, order ful... |
| ? | `tesla_011_vs_tesla_021` | 1 | 0.959 | Tesla aims to collect the minimum level of diagnostic data n... | Tesla shares financial data with payment processors to enabl... |
| ? | `tesla_012_vs_tesla_002` | 3 | 0.999 | Tesla does not capture audio voice recordings, only command ... | Tesla processes Autopilot camera data directly on the vehicl... |
| ? | `tesla_012_vs_tesla_004` | 4 | 0.999 | Tesla does not share in-vehicle browser history and sign-in ... | Tesla collects computer information, contact information, an... |
| ? | `tesla_012_vs_tesla_005` | 4 | 0.985 | Tesla does not share in-vehicle browser history and sign-in ... | Tesla uses essential cookies to provide requested services a... |
| ? | `tesla_012_vs_tesla_006` | 2 | 0.998 | Tesla does not share in-vehicle browser history and sign-in ... | Tesla collects information from or about Tesla product owner... |
| ? | `tesla_012_vs_tesla_007` | 6 | 1.000 | Tesla does not capture audio voice recordings, only command ... | Tesla collects payment methods, bank account numbers, credit... |
| ? | `tesla_012_vs_tesla_008` | 11 | 1.000 | Tesla does not share in-vehicle browser history and sign-in ... | Tesla collects service and repair history including facility... |
| ? | `tesla_012_vs_tesla_009` | 3 | 0.998 | Tesla does not capture audio voice recordings, only command ... | Tesla collects home details including roof dimensions, elect... |
| ? | `tesla_012_vs_tesla_010` | 6 | 1.000 | Tesla does not capture audio voice recordings, only command ... | Tesla collects camera images including SRS systems, braking,... |
| ? | `tesla_012_vs_tesla_011` | 1 | 0.842 | Tesla does not capture audio voice recordings, only command ... | Tesla collects diagnostic data including vehicle configurati... |
| ? | `tesla_012_vs_tesla_013` | 1 | 0.999 | Tesla does not capture audio voice recordings, only command ... | Tesla collects Fleet Learning camera recordings to recognize... |
| ? | `tesla_012_vs_tesla_014` | 6 | 0.999 | Tesla does not share in-vehicle browser history and sign-in ... | Tesla uses collected information to communicate with users a... |
| ? | `tesla_012_vs_tesla_015` | 8 | 1.000 | Tesla does not share in-vehicle browser history and sign-in ... | Tesla uses personal information to offer information on cont... |
| ? | `tesla_012_vs_tesla_016` | 8 | 1.000 | Tesla does not share in-vehicle browser history and sign-in ... | Tesla uses customer data to complete purchases, process prod... |
| ? | `tesla_012_vs_tesla_017` | 5 | 0.997 | Tesla does not share in-vehicle browser history and sign-in ... | Tesla uses computer information and generic personal informa... |
| ? | `tesla_012_vs_tesla_018` | 9 | 1.000 | Tesla does not share in-vehicle browser history and sign-in ... | Tesla uses personal data to analyze, reconstruct, investigat... |
| ? | `tesla_012_vs_tesla_020` | 2 | 0.999 | Tesla does not share in-vehicle browser history and sign-in ... | Tesla shares personal data with third parties as required by... |
| ? | `tesla_012_vs_tesla_023` | 2 | 1.000 | Tesla does not share in-vehicle browser history and sign-in ... | Tesla shares information with your social media provider if ... |
| ? | `tesla_012_vs_tesla_025` | 1 | 1.000 | Tesla does not collect information when using voice-to-text;... | Tesla contacts users by email, call, text, or app about prom... |
| ? | `tesla_013_vs_tesla_002` | 13 | 1.000 | Dashcam video is stored locally on USB drive and not transmi... | Tesla processes Autopilot camera data directly on the vehicl... |
| ? | `tesla_013_vs_tesla_006` | 1 | 0.995 | Sentry Mode Live Camera Access cannot be accessed by Tesla d... | Tesla collects information through remote access or in perso... |
| ? | `tesla_013_vs_tesla_007` | 1 | 0.583 | Dashcam video is stored locally on USB drive and not transmi... | Tesla uses customer support activity data to provide custome... |
| ? | `tesla_013_vs_tesla_008` | 10 | 0.999 | Tesla does not capture continuous recordings or provide live... | Tesla collects vehicle telemetry data regarding performance,... |
| ? | `tesla_013_vs_tesla_009` | 2 | 0.943 | Cabin Camera Analytics shared with Tesla are not associated ... | Tesla collects energy diagnostic logs for identifying and tr... |
| ? | `tesla_013_vs_tesla_010` | 6 | 0.999 | Tesla does not capture continuous recordings or provide live... | Tesla collects camera images including SRS systems, braking,... |
| ? | `tesla_013_vs_tesla_011` | 2 | 0.999 | Tesla does not capture continuous recordings or provide live... | Tesla collects diagnostic logs from vehicles and energy prod... |
| ? | `tesla_013_vs_tesla_012` | 14 | 1.000 | Fleet Learning camera recordings require explicit user conse... | Tesla collects usage analytics from vehicle touchscreen, sto... |
| ? | `tesla_013_vs_tesla_015` | 7 | 0.997 | Dashcam video is stored locally on USB drive and not transmi... | Tesla notifies first responders in the event of an accident ... |
| ? | `tesla_013_vs_tesla_016` | 4 | 0.995 | Tesla does not capture continuous recordings or provide live... | Tesla monitors Tesla product performance and uses collected ... |
| ? | `tesla_013_vs_tesla_018` | 4 | 0.998 | Cabin Camera Analytics shared with Tesla are not associated ... | Tesla uses personal data to analyze, reconstruct, investigat... |
| ? | `tesla_013_vs_tesla_023` | 1 | 0.999 | Cabin Camera Analytics shared with Tesla are not associated ... | Tesla shares personal data with law enforcement and governme... |
| ? | `tesla_018_vs_tesla_004` | 1 | 0.997 | Tesla does not share personally identifying information with... | Tesla receives information from third parties about users an... |
| ? | `tesla_018_vs_tesla_006` | 1 | 0.997 | Tesla does not share personally identifying information with... | Tesla collects information from or about Tesla product owner... |
| ? | `tesla_018_vs_tesla_008` | 1 | 0.952 | Tesla retains personal data only as long as necessary to ful... | Tesla collects diagnostic logs to identify and troubleshoot ... |
| ? | `tesla_018_vs_tesla_009` | 2 | 0.911 | Tesla retains personal data only as long as necessary to ful... | Tesla uses diagnostic logs to triage and fix software or pro... |
| ? | `tesla_018_vs_tesla_010` | 2 | 0.997 | Tesla retains personal data only as long as necessary to ful... | Tesla shares road segment data with partners in anonymized f... |
| ? | `tesla_018_vs_tesla_011` | 2 | 0.972 | Tesla retains personal data only as long as necessary to ful... | Tesla collects diagnostic logs from vehicles and energy prod... |
| ? | `tesla_018_vs_tesla_012` | 2 | 1.000 | Tesla does not share personally identifying information with... | Tesla collects usage analytics from vehicle touchscreen, sto... |
| ? | `tesla_018_vs_tesla_013` | 1 | 0.990 | Tesla retains personal data only as long as necessary to ful... | Tesla collects Fleet Learning camera recordings to recognize... |
| ? | `tesla_018_vs_tesla_014` | 2 | 0.997 | Tesla does not share personally identifying information with... | Tesla uses collected information to present products and off... |
| ? | `tesla_018_vs_tesla_015` | 5 | 1.000 | Tesla retains personal data only as long as necessary to ful... | Tesla uses personal information for educational and awarenes... |
| ? | `tesla_018_vs_tesla_016` | 5 | 0.997 | Tesla does not share personally identifying information with... | Tesla uses customer data to complete purchases, process prod... |
| ? | `tesla_018_vs_tesla_019` | 4 | 0.999 | Tesla retains personal data only as long as necessary to ful... | Tesla uses non-personally identifying information for operat... |
| ? | `tesla_018_vs_tesla_020` | 7 | 1.000 | Tesla does not share personally identifying information with... | Tesla shares personal data with third parties as required by... |
| ? | `tesla_018_vs_tesla_021` | 3 | 0.999 | Tesla does not share personally identifying information with... | Tesla shares contact and financial data with service provide... |
| ? | `tesla_018_vs_tesla_022` | 6 | 0.999 | Tesla retains personal data only as long as necessary to ful... | Tesla shares data with energy utilities based on customer co... |
| ? | `tesla_018_vs_tesla_023` | 8 | 1.000 | Tesla does not share personally identifying information with... | Tesla shares personal data with law enforcement and governme... |
| ? | `tesla_018_vs_tesla_028` | 1 | 0.676 | Tesla retains personal data only as long as necessary to ful... | Tesla collects and processes personal data based on consent,... |
| tesla | `tesla_020_vs_tesla_006` | 2 | 0.815 | Tesla limits how and with whom personal data is shared.... | Tesla collects information from or about Tesla product owner... |
| tesla | `tesla_020_vs_tesla_012` | 1 | 0.996 | Tesla limits how and with whom personal data is shared.... | Tesla collects usage analytics from vehicle touchscreen, sto... |
| tesla | `tesla_020_vs_tesla_014` | 1 | 0.831 | Tesla does not sell personal data to anyone for any purpose.... | Tesla uses collected information to present products and off... |
| tesla | `tesla_020_vs_tesla_018` | 1 | 0.999 | Tesla does not sell personal data to anyone for any purpose.... | Tesla uses personal data to establish, exercise, or defend l... |
| tesla | `tesla_020_vs_tesla_023` | 5 | 0.997 | Tesla does not sell personal data to anyone for any purpose.... | Tesla shares personal data with law enforcement and governme... |
| ? | `tesla_023_vs_tesla_004` | 1 | 0.976 | Third-party service providers must abide by Tesla's privacy ... | Tesla receives information from third parties about users an... |
| ? | `tesla_023_vs_tesla_005` | 1 | 0.989 | Third-party service providers must abide by Tesla's privacy ... | Tesla shares website analytics data with affiliates and mark... |
| ? | `tesla_023_vs_tesla_007` | 1 | 0.889 | Third-party service providers must abide by Tesla's privacy ... | Tesla uses customer support activity data to provide custome... |
| ? | `tesla_023_vs_tesla_010` | 1 | 0.994 | Third-party service providers must abide by Tesla's privacy ... | Tesla shares road segment data with partners in anonymized f... |
| ? | `tesla_023_vs_tesla_012` | 1 | 1.000 | Tesla allows you to manage or revoke consent for data sharin... | Tesla collects usage analytics from vehicle touchscreen, sto... |
| ? | `tesla_023_vs_tesla_016` | 2 | 0.997 | Third-party service providers must abide by Tesla's privacy ... | Tesla uses customer data to understand, triage, and fix issu... |
| ? | `tesla_023_vs_tesla_017` | 2 | 0.997 | Third-party service providers must abide by Tesla's privacy ... | Tesla uses user online activities and generic personal infor... |
| ? | `tesla_023_vs_tesla_018` | 5 | 0.998 | Third-party service providers must abide by Tesla's privacy ... | Tesla uses personal data to establish, exercise, or defend l... |
| ? | `tesla_023_vs_tesla_019` | 1 | 0.992 | Third-party service providers must abide by Tesla's privacy ... | Tesla uses non-personally identifying information to improve... |
| ? | `tesla_023_vs_tesla_020` | 4 | 1.000 | Third-party service providers must abide by Tesla's privacy ... | Tesla shares personal data for customer service, marketing, ... |
| ? | `tesla_023_vs_tesla_021` | 2 | 0.992 | Third-party service providers must abide by Tesla's privacy ... | Tesla shares contact and financial data with service provide... |
| ? | `tesla_023_vs_tesla_022` | 3 | 0.999 | Third-party service providers must abide by Tesla's privacy ... | Tesla shares customer data with third-party service and repa... |
| ? | `tesla_023_vs_tesla_025` | 1 | 0.959 | Third-party service providers must abide by Tesla's privacy ... | When data sharing is enabled, Tesla collects vehicle data an... |
| ? | `tesla_025_vs_tesla_002` | 1 | 0.993 | Tesla may still send administrative or important messages li... | Tesla processes Autopilot camera data directly on the vehicl... |
| ? | `tesla_025_vs_tesla_007` | 1 | 0.538 | Tesla may still send administrative or important messages li... | Tesla collects customer support interactions, dates, resolut... |
| ? | `tesla_025_vs_tesla_009` | 1 | 0.734 | Tesla may still send administrative or important messages li... | Tesla collects energy diagnostic logs for identifying and tr... |
| ? | `tesla_025_vs_tesla_010` | 1 | 0.984 | Tesla may still send administrative or important messages li... | Tesla collects camera images including SRS systems, braking,... |
| ? | `tesla_025_vs_tesla_012` | 1 | 0.995 | Tesla may still send administrative or important messages li... | Tesla collects usage analytics from vehicle touchscreen, sto... |
| ? | `tesla_025_vs_tesla_028` | 1 | 0.759 | Tesla may still send administrative or important messages li... | Tesla collects and processes personal data based on consent,... |
| ? | `tesla_027_vs_tesla_018` | 2 | 0.777 | Tesla is not responsible for data security practices of app ... | Tesla uses personal data to establish, exercise, or defend l... |
| ? | `tesla_028_vs_tesla_004` | 1 | 0.905 | Tesla informs users whether and why certain personal informa... | Tesla receives information from third parties about users an... |
| ? | `tesla_028_vs_tesla_009` | 1 | 0.993 | Tesla informs users whether and why certain personal informa... | Tesla collects energy diagnostic logs for identifying and tr... |
| ? | `tesla_028_vs_tesla_010` | 1 | 0.763 | Tesla informs users whether and why certain personal informa... | Tesla collects camera images including SRS systems, braking,... |
| ? | `tesla_028_vs_tesla_015` | 1 | 0.992 | Tesla informs users whether and why certain personal informa... | Tesla notifies first responders in the event of an accident ... |
| ? | `tesla_028_vs_tesla_019` | 6 | 0.998 | Tesla informs users whether and why certain personal informa... | Tesla uses non-personally identifying information for operat... |
| ? | `tesla_028_vs_tesla_020` | 1 | 0.564 | Tesla informs users whether and why certain personal informa... | Tesla shares personal data with third parties as required by... |
| ? | `tesla_028_vs_tesla_023` | 1 | 0.940 | Tesla informs users whether and why certain personal informa... | Tesla shares information with third-party utilities or energ... |
| ? | `venmo_003_vs_venmo_004` | 2 | 1.000 | Users who do not agree to Venmo's collection of IP address a... | Venmo uses collected telephone numbers and device IDs for ac... |
| ? | `venmo_003_vs_venmo_007` | 1 | 0.551 | Users who do not agree to Venmo's collection of IP address a... | Venmo collects geolocation data using GPS, Wi-Fi, or cell si... |
| ? | `venmo_003_vs_venmo_008` | 1 | 0.964 | Users who do not agree to Venmo's collection of IP address a... | Venmo collects email address, Facebook friends list, and pub... |
| ? | `venmo_003_vs_venmo_010` | 3 | 1.000 | Users who do not agree to Venmo's collection of IP address a... | Venmo uses face scans to manage fraud and risk.... |
| ? | `venmo_003_vs_venmo_011` | 1 | 0.996 | Users who do not agree to Venmo's collection of IP address a... | Venmo collects call recordings when customers talk to custom... |
| ? | `venmo_003_vs_venmo_012` | 1 | 0.686 | Users who do not agree to Venmo's collection of IP address a... | Venmo collects information about others if users choose to s... |
| ? | `venmo_003_vs_venmo_019` | 1 | 0.988 | Users who do not agree to Venmo's collection of IP address a... | Information disclosed to third parties through account conne... |
| ? | `venmo_003_vs_venmo_026` | 2 | 0.999 | Users who do not agree to Venmo's collection of IP address a... | Venmo collects username and password created by users for on... |
| ? | `venmo_003_vs_venmo_039` | 4 | 0.999 | Users who do not agree to Venmo's collection of IP address a... | Venmo uses biometric information to provide services and pre... |
| ? | `venmo_007_vs_venmo_010` | 1 | 0.983 | Venmo Services may not function properly if users do not agr... | Venmo collects face scans from users who consent in the user... |
| ? | `venmo_007_vs_venmo_026` | 2 | 0.978 | Venmo Services may not function properly if users do not agr... | Venmo collects email address when users sign up for app acce... |
| ? | `venmo_007_vs_venmo_039` | 1 | 0.794 | Venmo Services may not function properly if users do not agr... | Venmo discloses biometric information only to service provid... |
| ? | `venmo_009_vs_venmo_008` | 4 | 0.997 | Venmo does not disclose financial information with third par... | When mentioned in a visible transaction, a link to your Venm... |
| ? | `venmo_009_vs_venmo_017` | 3 | 0.998 | Venmo does not disclose financial information with third par... | Venmo associates information about PayPal and PayPal Honey t... |
| ? | `venmo_009_vs_venmo_018` | 3 | 0.961 | Venmo does not disclose financial information with third par... | Venmo shares contact information, sign-up date, payment coun... |
| ? | `venmo_009_vs_venmo_019` | 12 | 1.000 | Venmo does not disclose financial information with third par... | Venmo reports personal information about business owners to ... |
| ? | `venmo_009_vs_venmo_020` | 2 | 0.999 | Venmo does not disclose financial information with third par... | Venmo shares friends list, transaction history, and transact... |
| ? | `venmo_009_vs_venmo_028` | 4 | 0.997 | Venmo does not disclose financial information with third par... | Venmo shares data with The Bancorp Bank, N.A. and Mastercard... |
| ? | `venmo_009_vs_venmo_038` | 1 | 0.947 | Venmo does not disclose financial information with third par... | Venmo collects, uses and discloses personal information rega... |
| ? | `venmo_009_vs_venmo_039` | 3 | 0.999 | Venmo does not disclose financial information with third par... | Venmo collects sensitive personal information including SSN,... |
| ? | `venmo_012_vs_venmo_017` | 2 | 0.995 | Venmo is committed to providing a safe, secure, and high-qua... | Venmo uses risk and fraud tools to enforce its User Agreemen... |
| ? | `venmo_012_vs_venmo_018` | 2 | 0.999 | Venmo is committed to providing a safe, secure, and high-qua... | Venmo discloses personal information with payment recipients... |
| ? | `venmo_012_vs_venmo_019` | 8 | 0.999 | Venmo is committed to providing a safe, secure, and high-qua... | Venmo discloses personal information to other users based on... |
| ? | `venmo_012_vs_venmo_028` | 3 | 0.998 | Venmo is committed to providing a safe, secure, and high-qua... | Venmo discloses user data to third parties when legally obli... |
| ? | `venmo_012_vs_venmo_038` | 1 | 0.984 | Venmo is committed to providing a safe, secure, and high-qua... | Venmo collects, uses and discloses personal information rega... |
| ? | `venmo_012_vs_venmo_039` | 7 | 0.999 | Venmo is committed to providing a safe, secure, and high-qua... | Venmo discloses identifiers to other Venmo users and interne... |
| ? | `venmo_013_vs_venmo_027` | 1 | 0.974 | Venmo's Services are not directed to children under the age ... | Venmo collects data to conduct customer analysis and provide... |
| ? | `venmo_018_vs_venmo_009` | 1 | 0.998 | Venmo will not disclose credit card or bank account numbers ... | Venmo collects bank account login information, account and r... |
| ? | `venmo_018_vs_venmo_017` | 1 | 0.987 | Venmo will not disclose credit card or bank account numbers ... | Venmo creates account connections between Venmo accounts and... |
| ? | `venmo_018_vs_venmo_019` | 10 | 0.999 | Venmo will not disclose credit card or bank account numbers ... | Venmo shares personal information with financial institution... |
| ? | `venmo_018_vs_venmo_028` | 4 | 0.998 | Venmo will not disclose credit card or bank account numbers ... | Venmo discloses data with merchants when users make purchase... |
| ? | `venmo_018_vs_venmo_039` | 3 | 0.955 | Venmo will not disclose credit card or bank account numbers ... | Venmo collects sensitive personal information including SSN,... |
| ? | `venmo_019_vs_venmo_005` | 1 | 0.994 | Venmo does not disclose personal information with third part... | Venmo collects name, street address, email address, date of ... |
| ? | `venmo_019_vs_venmo_006` | 1 | 0.838 | Venmo does not disclose personal information with third part... | Venmo collects device type, machine identification number, g... |
| ? | `venmo_019_vs_venmo_008` | 4 | 0.999 | Venmo does not disclose personal information with third part... | Venmo collects email address, Facebook friends list, and pub... |
| ? | `venmo_019_vs_venmo_012` | 3 | 0.991 | Venmo does not disclose personal information with third part... | Venmo receives recipient name and payment information from V... |
| ? | `venmo_019_vs_venmo_017` | 4 | 0.999 | Venmo does not disclose personal information with third part... | Venmo associates information about PayPal and PayPal Honey t... |
| ? | `venmo_019_vs_venmo_018` | 3 | 0.999 | Venmo does not disclose personal information with third part... | Venmo shares contact information, sign-up date, payment coun... |
| ? | `venmo_019_vs_venmo_020` | 1 | 0.999 | Venmo does not disclose personal information with third part... | Venmo shares friends list, transaction history, and transact... |
| ? | `venmo_019_vs_venmo_026` | 1 | 0.989 | Venmo does not disclose personal information with third part... | Venmo collects username and password created by users for on... |
| ? | `venmo_019_vs_venmo_028` | 5 | 0.998 | Venmo does not disclose personal information with third part... | Venmo discloses display names to other users when payments a... |
| ? | `venmo_019_vs_venmo_038` | 1 | 0.981 | Venmo does not disclose personal information with third part... | Venmo collects, uses and discloses personal information rega... |
| ? | `venmo_019_vs_venmo_039` | 16 | 0.999 | Venmo does not disclose personal information with third part... | Venmo collects identifiers including real name, telephone nu... |
| ? | `venmo_020_vs_venmo_006` | 1 | 1.000 | Data disclosed to Apple is used pursuant to Apple's then-cur... | Venmo shares computer information, IP address, and location ... |
| ? | `venmo_020_vs_venmo_018` | 2 | 1.000 | Data disclosed to Apple is used pursuant to Apple's then-cur... | Venmo discloses personal information with payment recipients... |
| ? | `venmo_020_vs_venmo_019` | 13 | 1.000 | Data disclosed to Apple is used pursuant to Apple's then-cur... | Venmo discloses personal information to other users based on... |
| ? | `venmo_020_vs_venmo_021` | 1 | 0.995 | Data disclosed to Apple is used pursuant to Apple's then-cur... | Information broadcast to third-party social networks becomes... |
| ? | `venmo_020_vs_venmo_028` | 3 | 1.000 | Data disclosed to Apple is used pursuant to Apple's then-cur... | Venmo shares data with service providers for payment process... |
| ? | `venmo_020_vs_venmo_039` | 11 | 1.000 | Data disclosed to Apple is used pursuant to Apple's then-cur... | Venmo discloses protected classifications to PayPal affiliat... |
| ? | `venmo_021_vs_venmo_008` | 2 | 0.998 | Venmo does not send personal information to third-party soci... | When mentioned in a visible transaction, a link to your Venm... |
| ? | `venmo_021_vs_venmo_012` | 2 | 0.987 | Venmo does not send personal information to third-party soci... | Venmo collects information about others if users choose to s... |
| ? | `venmo_021_vs_venmo_017` | 1 | 0.993 | Venmo does not send personal information to third-party soci... | Venmo creates account connections between Venmo accounts and... |
| ? | `venmo_021_vs_venmo_018` | 4 | 0.995 | Venmo does not send personal information to third-party soci... | Vendors may disclose user mobile phone numbers or Venmo user... |
| ? | `venmo_021_vs_venmo_019` | 8 | 0.999 | Venmo does not send personal information to third-party soci... | Venmo username, profile photo, first and last name, account ... |
| ? | `venmo_021_vs_venmo_020` | 2 | 0.999 | Venmo does not send personal information to third-party soci... | Venmo shares friends list, transaction history, and transact... |
| ? | `venmo_021_vs_venmo_028` | 3 | 1.000 | Venmo does not send personal information to third-party soci... | Venmo discloses user data to third parties when legally obli... |
| ? | `venmo_021_vs_venmo_039` | 13 | 0.998 | Venmo does not send personal information to third-party soci... | Venmo discloses identifiers to other Venmo users and interne... |
| ? | `venmo_025_vs_venmo_005` | 1 | 0.564 | Venmo will not collect more information than what is require... | Venmo collects sensitive personal data including governmenta... |
| ? | `venmo_025_vs_venmo_018` | 1 | 0.995 | Venmo will not collect more information than what is require... | Venmo discloses personal information with payment recipients... |
| ? | `venmo_025_vs_venmo_019` | 5 | 0.993 | Venmo will not collect more information than what is require... | Venmo discloses personal information to other users based on... |
| ? | `venmo_025_vs_venmo_039` | 1 | 0.994 | Venmo will not collect more information than what is require... | Venmo discloses sensitive personal information to PayPal aff... |
| venmo | `venmo_037_vs_venmo_008` | 2 | 0.998 | Venmo does not share personal information for cross-context ... | Venmo collects email address, Facebook friends list, and pub... |
| venmo | `venmo_037_vs_venmo_012` | 2 | 0.633 | Venmo does not sell or share sensitive personal information,... | Venmo collects information about others if users choose to s... |
| ? | `venmo_037_vs_venmo_013` | 1 | 0.941 | Venmo does not sell or share sensitive personal information,... | Venmo collects personal information from users, including po... |
| venmo | `venmo_037_vs_venmo_017` | 3 | 0.999 | Venmo does not share personal information for cross-context ... | Venmo customizes, personalizes, measures, and improves servi... |
| venmo | `venmo_037_vs_venmo_018` | 4 | 0.999 | Venmo does not sell or share sensitive personal information,... | Venmo discloses personal information with payment recipients... |
| venmo | `venmo_037_vs_venmo_019` | 20 | 0.999 | Venmo does not sell or share sensitive personal information,... | Venmo shares personal information with third parties when us... |
| venmo | `venmo_037_vs_venmo_020` | 1 | 0.570 | Venmo does not sell or share sensitive personal information,... | Venmo shares friends list, transaction history, and transact... |
| venmo | `venmo_037_vs_venmo_028` | 7 | 0.998 | Venmo does not sell or share sensitive personal information,... | Venmo discloses data with merchants when users make purchase... |
| venmo | `venmo_037_vs_venmo_038` | 1 | 0.998 | Venmo does not sell or share sensitive personal information,... | Venmo collects, uses and discloses personal information rega... |
| ? | `venmo_038_vs_venmo_012` | 1 | 0.835 | Venmo did not sell or share any consumers' personal informat... | Venmo collects information about others if users choose to s... |
| ? | `venmo_038_vs_venmo_018` | 1 | 0.999 | Venmo did not sell or share any consumers' personal informat... | Venmo discloses personal information with payment recipients... |
| ? | `venmo_038_vs_venmo_019` | 10 | 0.999 | Venmo did not sell or share any consumers' personal informat... | Venmo discloses personal information to partners, merchants,... |
| ? | `venmo_038_vs_venmo_020` | 1 | 0.733 | Venmo did not sell or share any consumers' personal informat... | Venmo discloses some account data to Apple to facilitate tra... |
| ? | `venmo_038_vs_venmo_028` | 3 | 0.999 | Venmo did not sell or share any consumers' personal informat... | Venmo discloses data with merchants when users make purchase... |
| ? | `venmo_038_vs_venmo_039` | 13 | 0.999 | Venmo did not sell or share any consumers' personal informat... | Venmo discloses personal information to PayPal affiliates, s... |

## 6. Per-Company Summary

| Company | Seg Pairs | Seg Contradictions | Stmt Contradictions (seg-mapped) | Change |
|---------|-----------|-------------------|--------------------------------|--------|
| jasper | 17 | 1 | 2 | +1 |
| linkedin | 13 | 1 | 10 | +9 |
| microsoft | 1 | 1 | 0 | -1 |
| motorola-solutions | 26 | 1 | 0 | -1 |
| tesla | 21 | 11 | 13 | +2 |
| venmo | 38 | 4 | 10 | +6 |

## 7. Summary

- Segment-level pipeline: 19 contradictions
- Statement-level pipeline: 1268 unique segment pairs with contradictions
- Overlap: 11 pairs flagged by both
- Segment-only (potential FPs eliminated): 8
- Statement-only (new finds): 1257

- Preservation rate: 57.9% of segment-level contradictions retained
- Elimination rate: 8 segment-level contradictions not reproduced at statement level
