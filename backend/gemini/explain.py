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

Ingredient analysis data (includes severity: Harmfull, Moderate, Safe):
{structured_input}

CRITICAL INSTRUCTIONS:
1. Generate a JSON response with exactly these 5 keys: "harm_explanation", "risk_factors", "alternatives", "commercial_alternatives", "ingredient_explanations".
2. **Harm Explanation**: Directly explain why this product is risky for {profile}. Use the 'Harmfull' and 'Moderate' tags from the input data to justify your reasoning. Keep it SHORT (1-2 sentences).
3. **Risk Factors**: List exactly 3 specific risk factors found in the data.
4. **Natural Alternatives**: Provide exactly **3** natural/homemade alternatives.
5. **Commercial Alternatives**: Provide exactly **3** specific, healthier brand-name product suggestions available in market.
6. **Ingredient Explanations**: Provide a brief (1-line) explanation for EVERY ingredient marked as 'Harmfull' or 'Moderate' in the input.

RETURN JSON STRUCTURE:
{{
  "harm_explanation": "Summary relative to {profile} and the detected risks.",
  "risk_factors": ["Risk 1", "Risk 2", "Risk 3"],
  "alternatives": [
    {{ "name": "Natural A", "why": "...", "how_to_use": "...", "benefit": "..." }},
    {{ "name": "Natural B", "why": "...", "how_to_use": "...", "benefit": "..." }},
    {{ "name": "Natural C", "why": "...", "how_to_use": "...", "benefit": "..." }}
  ],
  "commercial_alternatives": [
    {{ "product_name": "Healthier Brand X", "why_better": "...", "availability": "..." }},
    {{ "product_name": "Healthier Brand Y", "why_better": "...", "availability": "..." }},
    {{ "product_name": "Healthier Brand Z", "why_better": "...", "availability": "..." }}
  ],
  "ingredient_explanations": {{
    "IngredientName": "Why it matters for {profile}"
  }}
}}

STRICT RULES:
1. NO Markdown (no ```json blocks).
2. NO conversational text.
3. RETURN ONLY JSON.
4. Ensure exactly 3 items in 'alternatives' and 'commercial_alternatives'.
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
