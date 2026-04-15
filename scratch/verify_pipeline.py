from pipeline.pdf_parser import extract_pdf_text
from pipeline.scorer import extract_rules
import os
from dotenv import load_dotenv

load_dotenv()

def test_pipeline():
    print("Testing PDF Extraction...")
    pdf_path = "Mostadam for Commercial Buildings (D+C).pdf"
    text = extract_pdf_text(pdf_path, max_pages=3)
    
    if text:
        print(f"✅ Successfully extracted {len(text)} characters from first 3 pages.")
        
        if os.getenv("OPENAI_API_KEY"):
            print("Testing Rule Extraction...")
            rules = extract_rules(text)
            print("✅ Rules Extracted:")
            print(rules[:500] + "...")
        else:
            print("⚠️ Skipping Rule Extraction (No API Key).")
    else:
        print("❌ PDF extraction failed.")

if __name__ == "__main__":
    test_pipeline()
