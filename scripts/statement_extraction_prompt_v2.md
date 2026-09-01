You are extracting atomic statements from a privacy policy segment.

SEGMENT TEXT:
{segment_text}

COMPANY: {company}
CATEGORY: {category}

{annotation_block}

TASK: Extract each distinct claim or practice as a separate atomic statement with enhanced metadata.

For each statement, provide:

1. **text**: A self-contained sentence (10-30 words) that captures one specific claim or practice. Include enough context to be understood without the original segment.

2. **type**:
   - COMMITMENT: A promise, reassurance, or limitation the company places on itself ("we do not...", "we limit...", "we protect...")
   - PRACTICE: A description of what the company actually does with data ("we collect...", "we share...", "we use...")

3. **subject**: WHO performs the action
   - COMPANY: The company itself ("we collect", "we share")
   - SERVICE_PROVIDER: Third parties acting on company's behalf ("our processors", "service providers")
   - THIRD_PARTY: Independent third parties ("advertisers may", "partners collect")
   - AFFILIATES: Related corporate entities ("our subsidiaries", "affiliated companies")
   - USER: User actions ("you can opt out", "users may request")

4. **aspect**: WHAT data lifecycle stage
   - COLLECTION: Gathering data from users
   - USE: Internal processing/analysis
   - SHARING: Providing to third parties (general)
   - SALE: Selling for monetary value (CCPA-specific)
   - RETENTION: How long data is kept
   - DELETION: Data removal practices
   - ACCESS_CONTROL: User access/correction rights
   - SECURITY: Protection measures

5. **scope**: Under WHAT conditions
   - UNIVERSAL: Always applies, no conditions
   - CONDITIONAL: Depends on specific context
   - CONSENT_BASED: Requires user consent
   - LEGAL_REQUIREMENT: Required by law (M&A, subpoenas, law enforcement)
   - GEOGRAPHIC_LIMITED: Jurisdiction-specific (California, EU residents, etc.)

6. **qualifiers**: Array of key limiting phrases verbatim from source text
   - Examples: ["except as required by law", "only for service delivery", "in certain jurisdictions"]
   - If no qualifiers present, use empty array []

7. **category**: The OPPT category this statement relates to (e.g., FIRST_PARTY, THIRD_PARTY, TRACKING, SALE_SHARING, SECURITY)

RULES:
- Each statement must be self-contained (understandable without the original paragraph)
- Preserve the original meaning — do not soften or strengthen language
- If a sentence contains both a commitment and a practice, split into two statements
- Preserve qualifiers exactly as written in the source text
- Ignore procedural/navigational text ("click here", "see our policy")
- If the segment is purely informational with no claims or practices, return an empty list

EXAMPLES:

Input: "We do not sell your personal information, except as required by law or in connection with a merger or acquisition."
Output:
{{"statements": [
    {{"text": "The company does not sell personal information.", "type": "COMMITMENT", "subject": "COMPANY", "aspect": "SALE", "scope": "UNIVERSAL", "qualifiers": ["except as required by law", "in connection with a merger or acquisition"], "category": "SALE_SHARING"}}
]}}

Input: "Third-party advertisers may collect information about your browsing activity across websites."
Output:
{{"statements": [
    {{"text": "Third-party advertisers collect information about user browsing activity across websites.", "type": "PRACTICE", "subject": "THIRD_PARTY", "aspect": "COLLECTION", "scope": "UNIVERSAL", "qualifiers": [], "category": "TRACKING"}}
]}}

Input: "With your consent, we share your location data with our advertising partners."
Output:
{{"statements": [
    {{"text": "The company shares user location data with advertising partners when the user provides consent.", "type": "PRACTICE", "subject": "COMPANY", "aspect": "SHARING", "scope": "CONSENT_BASED", "qualifiers": ["with your consent"], "category": "THIRD_PARTY"}}
]}}

Respond with ONLY this JSON (no other text):
{{"statements": [
    {{"text": "...", "type": "COMMITMENT", "subject": "COMPANY", "aspect": "...", "scope": "...", "qualifiers": [...], "category": "..."}},
    {{"text": "...", "type": "PRACTICE", "subject": "...", "aspect": "...", "scope": "...", "qualifiers": [...], "category": "..."}}
]}}
