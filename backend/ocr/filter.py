from google import genai
import os

# Initialize the new Gemini Client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def get_best_model(client):
    try:
        models = [m.name for m in client.models.list()]
        priorities = ["gemini-1.5-flash", "gemini-1.5-flash-latest", "gemini-2.0-flash-exp"]
        for p in priorities:
            for m in models:
                if p == m or f"models/{p}" == m:
                    return m
        for m in models:
            if "flash" in m.lower():
                return m
        return "gemini-1.5-flash"
    except:
        return "gemini-1.5-flash"

def filter_ingredient_text(raw_ocr_text: str) -> str:
    if not raw_ocr_text or not raw_ocr_text.strip():
        return ""
    
    prompt = f"""You are a strict OCR text filter for food packaging. Extract ONLY ingredients and health-related information.

Raw OCR text:
{raw_ocr_text}

WHAT TO EXTRACT (ONLY these):
1. **Ingredient List**: The actual food ingredients
2. **Sub-ingredients**: Items in brackets/parentheses
3. **Additives**: Preservatives, colorings, MSG
4. **Allergen Information**: "Contains milk", etc.
5. **Health Warnings**

WHAT TO REMOVE:
- Nutritional tables, energy, fat, protein, salt grams
- Serving sizes, manufacturing dates, brand marketing
- Storage instructions, packaging info

Return ONLY clean ingredient text.
"""
    
    try:
        model_name = get_best_model(client)
        
        response = client.models.generate_content(
            model=model_name,
            contents=prompt
        )
        
        filtered_text = response.text.strip()
        
        if not filtered_text or filtered_text.lower() in ["no ingredients detected", "none", ""]:
            return "No clear ingredient information found in the image."
        
        return filtered_text
        
    except Exception as e:
        print(f"ERROR in filter_ingredient_text: {e}")
        return raw_ocr_text
