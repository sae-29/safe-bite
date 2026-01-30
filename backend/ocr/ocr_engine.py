from google import genai
import os
from PIL import Image

# Initialize the new Gemini Client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def get_best_model(client):
    try:
        models = [m.name for m in client.models.list()]
        priorities = ["gemini-1.5-flash", "gemini-1.5-flash-latest", "gemini-2.0-flash-exp", "gemini-1.5-pro"]
        for p in priorities:
            for m in models:
                if p == m or f"models/{p}" == m:
                    return m
        for m in models:
            if "flash" in m.lower() or "pro" in m.lower():
                return m
        return "gemini-1.5-flash"
    except:
        return "gemini-1.5-flash"

def extract_text(image_path: str) -> str:
    """
    Extracts text from an image using Gemini (Vision).
    """
    try:
        img = Image.open(image_path)
        prompt = "Extract all text from this food label, specifically focusing on the ingredients list. Return the raw text."
        
        # Auto-discover working model
        model_name = get_best_model(client)
        print(f"DEBUG OCR: Using model '{model_name}'")
        
        response = client.models.generate_content(
            model=model_name,
            contents=[prompt, img]
        )
        
        if response and response.text:
            return response.text
        return ""
        
    except Exception as e:
        print(f"ERROR: Gemini Vision OCR failed: {e}")
        return ""
    finally:
        pass
