You are a privacy policy analyst assessing whether two atomic statements from the
same company's privacy policy contradict each other.

STATEMENT A (COMMITMENT): A specific promise, reassurance, or limitation the company
places on itself regarding data handling.

STATEMENT B (PRACTICE): A description of what the company actually does with data.

YOUR TASK: Determine whether Statement B contradicts the commitment made in Statement A.

WHAT IS A CONTRADICTION:
- Statement A makes a specific promise that Statement B violates or undermines
- Example: A: "We do not sell your personal information." /
  B: "We share data with advertising partners for targeted marketing." -> CONTRADICTION
- Example: A: "We limit data sharing to essential service providers." /
  B: "We share user data with affiliates, partners, and advertisers." -> CONTRADICTION

WHAT IS NOT A CONTRADICTION:
- B implements or supports what A promises (e.g., A: "We protect your data" /
  B: "We use industry-standard encryption" -> NOT a contradiction)
- B restates the same commitment in different words
- B describes an unrelated practice with no bearing on A's commitment
- B is about a different data type, user group, or context than A
- A uses hedging language ("may", "might") and B describes that possibility occurring
- A and B are about different products or services within the same company

EXAMPLES:

Example 1 -- CONTRADICTION:
  Commitment: "We do not share personal information with third parties for marketing."
  Practice: "We provide user data to advertising partners to deliver personalized ads."
  Verdict: CONTRADICTION -- The commitment prohibits marketing sharing, but the practice
  describes sharing with advertising partners.

Example 2 -- NOT_CONTRADICTION:
  Commitment: "We implement security measures to protect your personal information."
  Practice: "We collect device identifiers and IP addresses for service improvement."
  Verdict: NOT_CONTRADICTION -- The practice describes data collection, which is unrelated
  to the security commitment. Different topics, no conflict.

Example 3 -- CONTRADICTION:
  Commitment: "We do not sell personal information of consumers under 16."
  Practice: "Service providers acting on our behalf may process and sell user data."
  Verdict: CONTRADICTION -- The commitment claims no selling, but the practice describes
  service providers who may sell data.

Example 4 -- NOT_CONTRADICTION:
  Commitment: "We do not sell your personal data."
  Practice: "We collect browsing history and usage data to improve our services."
  Verdict: NOT_CONTRADICTION -- Collecting data for internal improvement is distinct from
  selling it. No conflict between these specific claims.

Now assess this pair from {company}:

COMMITMENT: {commitment_text}

PRACTICE: {practice_text}

Respond with ONLY this JSON (no other text):
{{"verdict": "CONTRADICTION" or "NOT_CONTRADICTION", "reasoning": "1-2 sentence explanation"}}
