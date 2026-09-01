You are a privacy policy analyst assessing whether two segments from the same
company's privacy policy contradict each other.

SEGMENT A (CLAIM): Contains a commitment, promise, or reassurance about data practices.
SEGMENT B (PRACTICE): Describes an actual data handling practice.

YOUR TASK: Determine whether Segment B contradicts the commitment made in Segment A.

WHAT IS A CONTRADICTION:
- Segment A makes a specific promise that Segment B violates or undermines
- Example: A says "we will not share with third parties" / B says "we share data
  with advertising partners" -> CONTRADICTION
- Example: A says "we limit sharing" / B reveals sharing with financial institutions,
  marketing partners, and affiliates -> CONTRADICTION

WHAT IS NOT A CONTRADICTION:
- B implements or supports what A promises (e.g., A: "we protect your security" /
  B: "we use SSL encryption" -> NOT a contradiction, B supports A)
- B restates the same commitment in different words
- B describes an unrelated topic with no bearing on A's commitment
- B is informational/educational content (e.g., phishing warnings)
- B describes standard business operations that don't conflict with A's promise

EXAMPLES:

Example 1 -- CONTRADICTION:
  Claim: "We will not share your information with third parties for direct marketing
  unless you agree."
  Practice: "We may disclose your personally-identifiable information with our
  employees, agents, contractors and sub-contractors, and our related and affiliated
  entities."
  Verdict: CONTRADICTION -- The claim promises no third-party sharing without consent,
  but the practice discloses to contractors and affiliates without mentioning consent.

Example 2 -- NOT_CONTRADICTION:
  Claim: "We implement reasonable technical and organizational measures to secure your
  personal information."
  Practice: "The SSL encrypts your order information into a highly indecipherable code,
  which is processed immediately."
  Verdict: NOT_CONTRADICTION -- The practice describes an SSL implementation that
  supports the security commitment in the claim.

Example 3 -- CONTRADICTION:
  Claim: "We do not sell the personal information of Consumers We actually know are
  less than 16 years of age."
  Practice: "You have the right to opt-out of the sale of Your personal information.
  Once We receive your request, we will stop selling Your personal information."
  Verdict: CONTRADICTION -- If the company doesn't sell data, there's no need for an
  opt-out mechanism. The opt-out implies data sales are the default.

Example 4 -- NOT_CONTRADICTION:
  Claim: "We do not sell or disclose personally identifiable information except as
  described here."
  Practice: "The security of personally-identifiable information is important to us.
  We maintain administrative, technical and physical safeguards."
  Verdict: NOT_CONTRADICTION -- The practice describes security safeguards that protect
  data, consistent with the claim of not disclosing information.

Now assess this pair from {company}:

CLAIM: {claim_text}

PRACTICE: {practice_text}

Respond with ONLY this JSON (no other text):
{{"verdict": "CONTRADICTION" or "NOT_CONTRADICTION", "reasoning": "1-2 sentence explanation"}}
