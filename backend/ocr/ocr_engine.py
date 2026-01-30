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
        
        # Try standard name first
        model_name = "gemini-1.5-flash"
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content([prompt, img])
        except Exception as inner_e:
            if "404" in str(inner_e):
                print(f"DEBUG: {model_name} failed. Checking available models...")
                from ..gemini.explain import list_available_models
                list_available_models()
                # Fallback to pro if flash fails
                model = genai.GenerativeModel("gemini-1.0-pro-vision")
                response = model.generate_content([prompt, img])
            else:
                raise inner_e
        
        if response and response.text:
            return response.text
        return ""
        
    except Exception as e:
        print(f"ERROR: Gemini Vision OCR failed: {e}")
        return ""
    finally:
        # We don't delete the temp file here, main.py handles it
        pass
