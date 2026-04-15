import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Path to the rules markdown file
RULES_MD_PATH = "Mostadam_Commercial_Buildings_DC.md"

def load_rules():
    """Load the sustainability rules from the markdown file."""
    if not os.path.exists(RULES_MD_PATH):
        return "Rules file not found."
    with open(RULES_MD_PATH, "r", encoding="utf-8") as f:
        return f.read()


def score_site_sustainability(features, api_key: str = None):
    """
    Evaluate floor plan features against the Site Sustainability (SS) rules.
    STRICT AUDIT MODE: Minimal assumptions, focus on clear visual evidence.

    Args:
        features: Extracted feature description string from the vision model.
        api_key:  OpenAI API key. Falls back to the OPENAI_API_KEY env var.
    """
    # Always create the client at call-time so the key is never stale
    key = api_key or os.getenv("OPENAI_API_KEY", "")
    client = OpenAI(api_key=key)

    rules_text = load_rules()

    credit_guidelines = """
    STRICT COMPLIANCE GUIDELINES:

    1. SS-01: Sewage, Flood and Rainwater Management (Keystone) - Total 3 pts
       - Requirement #1 (Keystone - 1 pt): Sewage network connection or Treatment Plant. Grease trap for kitchens.
       - Requirement #2 (2 pts total with Req 3): Not in legal flood hazard area.
       - Requirement #3: Rainwater Management Plan implementation.

    2. SS-02: Ecological Assessment and Protection (Keystone) - Total 1 pt
       - Requirement #1 & #2 (Keystone - 1 pt): Ecological Assessment by pro and Asset Protection measures.

    3. SS-05: Heat Island Effect (Optional) - Total 2 pts
       - Requirement #1 (1 pt): High Solar Reflective Index (SRI) surfaces.
       - Requirement #2 (1 pt): Vegetative covering over >=70% unused roof/shade.
    """

    prompt = f"""
You are a STRICT Site Sustainability auditor for the Mostadam certification system.

### AUDIT PRINCIPLES:
1. **STRICT EVIDENCE**: Only award points if clear visual evidence is present in the "FEATURES" list.
2. **NO ASSUMPTIONS**: If a feature is not clearly drawn/described, AWARD 0 POINTS and mark as "Unverified".
3. **25% ASSUMPTION CAP**: Limit assumed compliance to less than 25% of the total score. Default to "Insufficient Evidence" for ambiguous signals.
4. **SITE CONTEXT**: Since this is a 2D floor plan, signals like "Flood Area" or "SRI values" are impossible to verify visually. Do NOT award points for these; instead, mark them as "Requires External Documentation".

### GUIDELINES:
{credit_guidelines}

### RULES SOURCE CONTENT (Reference):
{rules_text[:100000]}

### FLOOR PLAN FEATURES (The only source of proof):
{features}

### INSTRUCTIONS:
- Break down points for SS-01, SS-02, and SS-05.
- For Keystones, confirm whether the visual proof is present.
- The "summary" field must be 3-5 sentences covering: overall compliance posture, which credits passed/failed, key missing evidence, and the final score.
- The "audit_report" field must be a detailed narrative (minimum 150 words) explaining:
    • What evidence WAS found for each credit and exactly why points were or were not awarded.
    • What documentation or design changes would be needed to earn any missing points.
    • An overall compliance recommendation.

Return ONLY a JSON object with this exact structure:
{{
 "summary": "3-5 sentence executive summary covering overall compliance, credits passed/failed, key missing evidence, and the final score.",
 "credits": {{
    "SS-01": {{
        "points": <int>,
        "max_points": 3,
        "is_keystone": true,
        "keystone_met": <bool>,
        "status": "Verified | Unverified | Requires External Documentation",
        "explanation": "Concise 2-3 sentence reasoning: what WAS or WAS NOT seen and why points were awarded or withheld."
    }},
    "SS-02": {{
        "points": <int>,
        "max_points": 1,
        "is_keystone": true,
        "keystone_met": <bool>,
        "status": "Verified | Unverified | Requires External Documentation",
        "explanation": "Concise 2-3 sentence reasoning: what WAS or WAS NOT seen and why points were awarded or withheld."
    }},
    "SS-05": {{
        "points": <int>,
        "max_points": 2,
        "is_keystone": false,
        "status": "Verified | Unverified | Requires External Documentation",
        "explanation": "Concise 2-3 sentence reasoning: what WAS or WAS NOT seen and why points were awarded or withheld."
    }}
 }},
 "audit_report": "Detailed narrative report (minimum 150 words) covering evidence found per credit, justification for point deductions, missing documentation, and overall compliance recommendation."
}}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            response_format={"type": "json_object"},
        )
        return response.choices[0].message.content
    except Exception as e:
        return json.dumps({"error": str(e)})
