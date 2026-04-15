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
    Returns a granular point breakdown for backend consistency.
    """
    rules_text = load_rules()
    
    # Specific credit summaries
    credit_guidelines = """
    CRITICAL EVALUATION FOCUS & POINT SCORING:
    
    1. SS-01: Sewage, Flood and Rainwater Management (Keystone) - Total 3 pts available
       - Requirement #1 (Keystone - 1 pt): Sewage network connection or Treatment Plant. Grease trap for kitchens.
       - Requirement #2 (2 pts total with Req 3): Not in legal flood hazard area.
       - Requirement #3: Rainwater Management Plan implementation.
    
    2. SS-02: Ecological Assessment and Protection (Keystone) - Total 1 pt available
       - Requirement #1 & #2 (Keystone - 1 pt): Ecological Assessment by pro and Asset Protection measures.
    
    3. SS-05: Heat Island Effect (Optional) - Total 2 pts available
       - Requirement #1 (1 pt): High Solar Reflective Index (SRI) surfaces.
       - Requirement #2 (1 pt): Vegetative covering over >=70% unused roof/shade.
    """

    prompt = f"""
You are a Site Sustainability auditor for the Mostadam certification system.

### TASK:
Evaluate the FLOOR PLAN FEATURES against the provided GUIDELINES and RULES.

### GUIDELINES:
{credit_guidelines}

### RULES SOURCE CONTENT (Reference):
{rules_text[:100000]}

### FLOOR PLAN FEATURES:
{features}

### INSTRUCTIONS:
1. Provide granular point allocations for each credit (SS-01, SS-02, SS-05).
2. For Keystone requirements, specifically confirm if they are met.
3. If information is missing from the 2D plan, use professional architectural judgment to flag likely compliance or gaps.

Return ONLY a JSON object:
{{
 "summary": "Executive summary of compliance",
 "credits": {{
    "SS-01": {{
        "points": int,
        "max_points": 3,
        "is_keystone": true,
        "keystone_met": bool,
        "explanation": "concise reasoning for assigned points"
    }},
    "SS-02": {{
        "points": int,
        "max_points": 1,
        "is_keystone": true,
        "keystone_met": bool,
        "explanation": "concise reasoning for assigned points"
    }},
    "SS-05": {{
        "points": int,
        "max_points": 2,
        "is_keystone": false,
        "explanation": "concise reasoning for assigned points"
    }}
 }},
 "overall_calculation": "Detail how the points were derived from the signals."
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
