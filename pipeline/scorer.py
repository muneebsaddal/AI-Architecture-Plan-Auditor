import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Path to the rules markdown file
RULES_MD_PATH = "Mostadam_Commercial_Buildings_DC.md"

def load_rules():
    """Load the sustainability rules from the markdown file."""
    if not os.path.exists(RULES_MD_PATH):
        return "Rules file not found."
    with open(RULES_MD_PATH, "r", encoding="utf-8") as f:
        return f.read()

def score_site_sustainability(features):
    """
    Evaluate floor plan features against the Site Sustainability (SS) rules.
    Specifically targeting: SS-01, SS-02, and SS-05.
    """
    rules_text = load_rules()
    
    # Specific credit summaries as provided by the user
    credit_guidelines = """
    CRITICAL EVALUATION FOCUS:
    
    1. SS-01: Sewage, Flood and Rainwater Management (Keystone) - Total 3 pts
       - Req #1 (Keystone - 1 pt): Sewage network connection or Treatment Plant. Grease traps for food prep.
       - Req #2 (2 pts total with Req 3): Not in legal flood hazard area.
       - Req #3: Rainwater Management Plan (site infiltration or redirection).
    
    2. SS-02: Ecological Assessment and Protection (Keystone) - Total 1 pt
       - Req #1 & #2 (Keystone - 1 pt): Ecological Assessment by pro + mitigation measures identifying natural assets.
    
    3. SS-05: Heat Island Effect (Optional) - Total 2 pts
       - Req #1 (1 pt): Specific SRI values (Hardscape >=45, Shade >=75, Roofs >=75).
       - Req #2 (1 pt): Vegetative covering over >=70% of unused roof/shade.
    """

    prompt = f"""
You are a Site Sustainability auditor for the Mostadam certification system.

### TASK:
Evaluate the provided FLOOR PLAN FEATURES against the following specific Site Sustainability (SS) credits.

### GUIDELINES:
{credit_guidelines}

### RULES SOURCE CONTENT (Reference):
{rules_text[:100000]}  # Context limit check

### FLOOR PLAN FEATURES:
{features}

### INSTRUCTIONS:
1. Calculate a single "Site Sustainability Score" out of 6 points.
2. Provide an "Executive Summary" (concise).
3. Provide a "Detailed Report" explaining the score for each credit (SS-01, SS-02, SS-05).
   - For SS-01 and SS-02 (Keystones), clearly state if the Keystone requirement is met.
   - For signals not visible in a 2D floor plan (like flood zones or SRI values), evaluate based on what is visible (e.g., presence of grease traps, rainwater drainage, roof vegetation) and list assumptions/recommendations for high-fidelity compliance.

Return ONLY a JSON object:
{{
 "score": int,
 "max_score": 6,
 "summary": "string",
 "detailed_report": {{
    "SS-01": "explanation",
    "SS-02": "explanation",
    "SS-05": "explanation"
 }},
 "calculation_logic": "string explaining how the points were tallied"
}}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            response_format={ "type": "json_object" }
        )
        return response.choices[0].message.content
    except Exception as e:
        return json.dumps({"error": str(e)})
