import base64
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def extract_features_with_vision(image_input, is_path=True, api_key: str = None):
    """
    Uses GPT-4o Vision to extract architectural and site features specifically
    for Site Sustainability (SS) evaluation.

    Args:
        image_input: Absolute path (str) or raw bytes of the image.
        is_path:     True if image_input is a file path, False if raw bytes.
        api_key:     OpenAI API key. Falls back to OPENAI_API_KEY env var.
    """
    # Always create the client at call-time so the key is never stale
    key = api_key or os.getenv("OPENAI_API_KEY", "")
    client = OpenAI(api_key=key)

    if is_path:
        base64_image = encode_image(image_input)
    else:
        base64_image = base64.b64encode(image_input).decode("utf-8")

    prompt = """
Analyze this floor plan and site layout for Site Sustainability features.

Please return the findings using these EXACT headings and emojis:

🚰 SITE SERVICES: Describe sewage lines, drainage points, or network connections.
🍳 FOOD SERVICE: Describe kitchen/food prep areas and potential grease trap locations.
🌦️ WATER MANAGEMENT: Describe rainwater harvesting, roof drainage, or flood features.
🌳 ECOLOGY: Describe natural assets, vegetation, or protected areas.
🔥 HEAT ISLAND: Describe roof type, shade structures, and hardscape materials.
📐 SPATIAL LAYOUT: Describe general room types and coverage ratios.

Keep descriptions concise and professional.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
            max_tokens=1000,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error during vision processing: {e}"


# Stubs for compatibility
def preprocess_image(path): return None, None
def detect_contours(thresh): return []
def extract_text(path): return ""
def map_rooms(text): return []
def extract_features(contours, rooms): return "Features extracted via Vision API"
