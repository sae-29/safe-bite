from google import genai
import os
import json

# Initialize the new Gemini Client forcing v1 stable API
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options={'api_version': 'v1'}
)

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
        # Using the new SDK's generate_content
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )
        
        text = response.text.strip()
        
        # Robust JSON cleaning
        if text.startswith("```json"):
            text = text[7:-3].strip()
        elif text.startswith("```"):
            text = text[3:-3].strip()
            
        return json.loads(text)

    except Exception as e:
        print(f"ERROR: explain_with_gemini failed: {e}")
        # Return valid empty structure on failure
        return {
            "harm_explanation": f"Analysis failed: {str(e)}",
            "risk_factors": [],
            "alternatives": [],
            "commercial_alternatives": [],
            "ingredient_explanations": {}
        }
