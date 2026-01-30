

import google.generativeai as genai
import os
import json

genai.configure(api_key=os.getenv("GEMINI_API_KEY"), api_version='v1')

def list_available_models():
    """Debug helper to see what models we can actually use"""
    try:
        models = [m.name for m in genai.list_models()]
        print(f"DEBUG: Available Gemini Models: {models}")
        return models
    except Exception as e:
        print(f"DEBUG: Could not list models: {e}")
        return []

def explain_with_gemini(analysis: list, profile: str = "General"):
    """
    analysis: list of ML predictions
    profile: User health profile (e.g., "Diabetic", "Child", "None")
    """

    structured_input = json.dumps(analysis, indent=2)

    prompt = f"""
You are a food safety and nutrition expert. Your goal is to provide a structured, profile-specific analysis.

User Profile: {profile}

Ingredient analysis data:
{structured_input}

CRITICAL INSTRUCTION:
Generate a JSON response with exactly these 3 sections.
Keep explanations SHORT and PUNCHY (1-2 sentences max).

RETURN JSON STRUCTURE:
{{
  "harm_explanation": "Directly explain why this product is risky for {profile}. Focus on the specific ingredients (e.g., 'High sugar affects blood glucose'). Max 2 sentences.",
  "risk_factors": [
    "Factor 1: Brief explanation",
    "Factor 2: Brief explanation",
    "Factor 3: Brief explanation"
  ],
  "alternatives": [
    {{
      "name": "Natural Option 1",
      "why": "Why it's better",
      "how_to_use": "Quick tip",
      "benefit": "Health benefit"
    }},
    {{ "name": "Natural Option 2", "why": "...", "how_to_use": "...", "benefit": "..." }},
    {{ "name": "Natural Option 3", "why": "...", "how_to_use": "...", "benefit": "..." }}
  ],
  "commercial_alternatives": [
    {{
      "product_name": "Brand Name Product 1",
      "why_better": "Why it's healthier",
      "availability": "Where to buy"
    }},
    {{ "product_name": "Brand Name Product 2", "why_better": "...", "availability": "..." }},
    {{ "product_name": "Brand Name Product 3", "why_better": "...", "availability": "..." }}
  ],
  "ingredient_explanations": {{
    "Ingredient": "1-line explanation for {profile}"
  }}
}}

STRICT RULES:
1. NO Markdown (no ```json blocks).
2. NO conversational text.
3. RETURN ONLY JSON.
"""

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        result = model.generate_content(prompt)
    except Exception as e:
        if "404" in str(e):
            print(f"ERROR: gemini-1.5-flash not found. Listing models...")
            list_available_models()
            # Try a fallback if flash is missing (unlikely but safe)
            model = genai.GenerativeModel("gemini-pro")
            result = model.generate_content(prompt)
        else:
            raise e
    
    # Clean up response to ensure valid JSON
    text = result.text.strip()
    if text.startswith("```json"):
        text = text[7:-3].strip()
    elif text.startswith("```"):
         text = text[3:-3].strip()
         
    try:
        # Clean the response text (remove Markdown code blocks)
        cleaned_text = text.strip()
        if cleaned_text.startswith("```json"):
            cleaned_text = cleaned_text[7:]
        if cleaned_text.startswith("```"):
            cleaned_text = cleaned_text[3:]
        if cleaned_text.endswith("```"):
            cleaned_text = cleaned_text[:-3]
        
        cleaned_text = cleaned_text.strip()
        
        return json.loads(cleaned_text)
    except json.JSONDecodeError as e:
        print(f"JSON Parse Error: {e}")
        print(f"Raw Text: {text}")
        # Fallback: return structure with error message but valid format
        return {
            "harm_explanation": "Could not generate analysis. Please try again.",
            "risk_factors": ["Error parsing AI response"],
            "alternatives": [],
            "commercial_alternatives": [],
            "ingredient_explanations": {}
        }
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return {
             "harm_explanation": "An unexpected error occurred.",
             "risk_factors": [],
             "alternatives": [],
             "commercial_alternatives": [],
             "ingredient_explanations": {}
        }


