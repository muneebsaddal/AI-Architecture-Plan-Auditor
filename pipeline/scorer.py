from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Use environment variable or default to a placeholder
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_rules(pdf_text):
    """
    Summarize sustainability rules from PDF text.
    """
    if not pdf_text:
        return "No rules text provided."

    prompt = f"""
Extract key sustainability evaluation rules from this document.

Focus on:
- Daylight
- Ventilation
- Space efficiency
- Any measurable criteria

Return concise bullet points.

Document:
{pdf_text[:12000]}  # Increased context slightly
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error extracting rules: {e}"

def score_plan(features, rules_text):
    """
    Evaluate floor plan features against extracted rules.
    """
    if not features or not rules_text:
        return "Missing features or rules for scoring."

    prompt = f"""
You are an architectural sustainability expert.

SUSTAINABILITY RULES:
{rules_text}

FLOOR PLAN FEATURES:
{features}

Evaluate based ONLY on the provided rules.

Return JSON:
{{
 "daylight": int,
 "ventilation": int,
 "efficiency": int,
 "summary": "clear explanation referencing rules",
 "traceability": "Based on rule: '...'"
}}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            response_format={ "type": "json_object" }
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error during scoring: {e}"
