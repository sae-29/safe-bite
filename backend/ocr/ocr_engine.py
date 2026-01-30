from google import genai
import os
from PIL import Image

# Initialize the new Gemini Client forcing v1 stable API
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options={'api_version': 'v1'}
)

def extract_text(image_path: str) -> str:
    """
    Extracts text from an image using Gemini 1.5 Flash (Vision).
    Replaces local Tesseract OCR for better accuracy and easier deployment.
    """
    try:
        # Load the image
        img = Image.open(image_path)
        
        # Prompt for OCR
        prompt = "Extract all text from this food label, specifically focusing on the ingredients list. Return the raw text."
        
        # Using the new SDK's generate_content with image support
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=[prompt, img]
        )
        
        if response and response.text:
            return response.text
        return ""
        
    except Exception as e:
        print(f"ERROR: Gemini Vision OCR failed: {e}")
        return ""
    finally:
        # We don't delete the temp file here, main.py handles it
        pass
