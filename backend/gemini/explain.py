from google import genai
import os
import json

# Initialize the new Gemini Client forcing v1 stable API
# Removing forced api_version to let SDK decide best default
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def get_best_model(client):
    """
    Intelligently finds an available model for the user's key.
    Solves 404 errors by picking what is actually enabled.
    """
    try:
        models = [m.name for m in client.models.list()]
        print(f"DEBUG: Available models for this key: {models}")
        
        # Priority list
        priorities = [
            "gemini-1.5-flash",
            "gemini-1.5-flash-latest",
            "gemini-2.0-flash-exp",
            "gemini-1.5-pro",
            "gemini-1.0-pro"
        ]
        
        for p in priorities:
            for m in models:
                if p == m or f"models/{p}" == m:
                    return m
        
        # Fallback to first compatible model
        for m in models:
            if "flash" in m.lower() or "pro" in m.lower():
                return m
                
        return "gemini-1.5-flash" # Absolute fallback
    except Exception as e:
        print(f"DEBUG: Model auto-discovery failed: {e}")
        return "gemini-1.5-flash"

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
    }}
  ],
  "commercial_alternatives": [
    {{
      "product_name": "Healthier Brand 1",
      "why_better": "Specific health benefit",
      "availability": "Online/Stores"
    }}
  ],
  "ingredient_explanations": {{
    "IngredientName": "Why it matters for {profile}"
  }}
}}

STRICT RULES:
1. NO Markdown (no ```json blocks).
2. NO conversational text.
3. RETURN ONLY JSON.
"""

    try:
        model_name = get_best_model(client)
        print(f"DEBUG: Using model '{model_name}' for explanation.")
        
        response = client.models.generate_content(
            model=model_name,
            contents=prompt
        )
        
        text = response.text.strip()
        
        if text.startswith("```json"):
            text = text[7:-3].strip()
        elif text.startswith("```"):
            text = text[3:-3].strip()
            
        return json.loads(text)

    except Exception as e:
        print(f"ERROR: explain_with_gemini failed: {e}")
        return {
            "harm_explanation": f"Analysis failed: {str(e)}",
            "risk_factors": [],
            "alternatives": [],
            "commercial_alternatives": [],
            "ingredient_explanations": {}
        }
