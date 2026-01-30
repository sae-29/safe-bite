import google.generativeai as genai
import os
from PIL import Image

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def extract_text(image_path: str) -> str:
    """
    Extracts text from an image using Gemini 1.5 Flash (Vision).
    Replaces local Tesseract OCR for better accuracy and easier deployment.
    """
    try:
        # Load the image
        img = Image.open(image_path)
        
        # Initialize model
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Prompt for OCR
        prompt = "Extract all text from this food label, specifically focusing on the ingredients list. Return the raw text."
        
        # Generate content
        response = model.generate_content([prompt, img])
        
        if response and response.text:
            return response.text
        return ""
        
    except Exception as e:
        print(f"ERROR: Gemini Vision OCR failed: {e}")
        return ""
    finally:
        # We don't delete the temp file here, main.py handles it
        pass
