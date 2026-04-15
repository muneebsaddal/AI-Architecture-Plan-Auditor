import pdfplumber
import os

def extract_pdf_text(pdf_path, max_pages=10):
    """
    Extracts text from a PDF file.
    Limit to first max_pages to prevent token overload.
    """
    full_text = ""
    
    if not os.path.exists(pdf_path):
        print(f"Error: File not found at {pdf_path}")
        return ""

    try:
        with pdfplumber.open(pdf_path) as pdf:
            # Limit pages to prevent token overload
            pages_to_extract = pdf.pages[:max_pages]
            for page in pages_to_extract:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"
    except Exception as e:
        print(f"Error parsing PDF: {e}")
        return ""

    return full_text
