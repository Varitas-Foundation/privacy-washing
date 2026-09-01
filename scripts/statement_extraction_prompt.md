You are extracting atomic statements from a privacy policy segment.

SEGMENT TEXT:
{segment_text}

COMPANY: {company}
CATEGORY: {category}

{annotation_block}

TASK: Extract each distinct claim or practice as a separate atomic statement.

For each statement, provide:
1. **text**: A self-contained sentence (10-30 words) that captures one specific claim or practice. Include enough context to be understood without the original segment.
2. **type**:
   - COMMITMENT: A promise, reassurance, or limitation the company places on itself ("we do not...", "we limit...", "we protect...")
   - PRACTICE: A description of what the company actually does with data ("we collect...", "we share...", "we use...")
3. **category**: The OPPT category this statement relates to (e.g., FIRST_PARTY, THIRD_PARTY, TRACKING, SALE_SHARING, SECURITY)

RULES:
- Each statement must be self-contained (understandable without the original paragraph)
- Preserve the original meaning — do not soften or strengthen language
- If a sentence contains both a commitment and a practice, split into two statements
- Ignore procedural/navigational text ("click here", "see our policy")
- If the segment is purely informational with no claims or practices, return an empty list

Respond with ONLY this JSON (no other text):
{{"statements": [
    {{"text": "...", "type": "COMMITMENT", "category": "..."}},
    {{"text": "...", "type": "PRACTICE", "category": "..."}}
]}}
