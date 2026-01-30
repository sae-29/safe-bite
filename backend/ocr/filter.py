import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def filter_ingredient_text(raw_ocr_text: str) -> str:
    """
    Uses Gemini AI to intelligently filter OCR text, extracting only ingredient-related information.
    
    Args:
        raw_ocr_text: Complete OCR output from food packaging
        
    Returns:
        Clean text containing only ingredients and consumable information
    """
    
    if not raw_ocr_text or not raw_ocr_text.strip():
        return ""
    
    prompt = f"""You are a strict OCR text filter for food packaging. Extract ONLY ingredients and health-related information.

Raw OCR text:
{raw_ocr_text}

WHAT TO EXTRACT (ONLY these):
1. **Ingredient List**: The actual food ingredients (e.g., "Potatoes, Sunflower Oil, Rapeseed Oil, Salt")
2. **Sub-ingredients**: Items in brackets/parentheses (e.g., "vegetable oil (sunflower, rapeseed)")
3. **Additives**: Preservatives, flavor enhancers, colorings (e.g., "monosodium glutamate", "E621")
4. **Allergen Information**: "Contains milk", "May contain nuts", "SUITABLE FOR VEGETARIANS"
5. **Health Warnings**: If any specific health warnings are present

WHAT TO REMOVE (DO NOT include):
- Nutritional tables (Energy, Fat, Carbohydrate, Protein, Salt percentages/grams)
- Serving size information ("This pack contains 1 serving", "Per 100g")
- Manufacturing information ("Made in a factory that also handles...")
- Storage instructions ("Store in cool dry place", "Packaged in Protective Atmosphere")
- Best before dates, batch codes, barcodes
- Brand names, marketing slogans
- Packaging instructions ("Tear here", "Reseal after opening")
- Any text with percentages, grams, calories, or nutritional values
- Broken/garbled OCR text

EXAMPLE INPUT:
"Energy 2156kJ, Fat 33.1g, Carbohydrate 49.9g, Protein 1.5g, Salt 1.35g
Ready Salted Potato Crisps
Ingredients: Potatoes, Sunflower Oil, Rapeseed Oil, Salt
SUITABLE FOR VEGETARIANS
Made in a factory that also handles milk
Packaged in a Protective Atmosphere"

CORRECT OUTPUT:
"Ingredients: Potatoes, Sunflower Oil, Rapeseed Oil, Salt
SUITABLE FOR VEGETARIANS"

Return ONLY the ingredient list and allergen/health information.
If no ingredients are found, return "No ingredients detected".
Do NOT include nutritional values, manufacturing info, or storage instructions.
"""
    
    try:
        model = genai.GenerativeModel("gemini-2.0-flash-exp")
        
        print(f"DEBUG FILTER: Sending to Gemini for filtering...")
        print(f"DEBUG FILTER: Raw text length: {len(raw_ocr_text)} chars")
        
        result = model.generate_content(prompt)
        
        filtered_text = result.text.strip()
        
        print(f"DEBUG FILTER: Gemini returned: {filtered_text[:200]}...")
        
        # If Gemini returns empty or just says no ingredients
        if not filtered_text or filtered_text.lower() in ["no ingredients detected", "none", ""]:
            print("DEBUG FILTER: No ingredients detected by Gemini")
            return "No clear ingredient information found in the image."
        
        print(f"DEBUG FILTER: Successfully filtered to {len(filtered_text)} chars")
        return filtered_text
        
    except Exception as e:
        print(f"ERROR in filter_ingredient_text: {e}")
        print(f"ERROR FILTER: Falling back to raw text")
        # Fallback: return original text if filtering fails
        return raw_ocr_text

