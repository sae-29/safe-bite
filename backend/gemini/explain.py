

import google.generativeai as genai
import os
import json

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def explain_with_gemini(analysis: list, profile: str = "General"):
    """
    analysis: list of ML predictions
    profile: User health profile (e.g., "Diabetic", "Child", "None")
    """

    structured_input = json.dumps(analysis, indent=2)

    prompt = f"""
You are a food safety and nutrition expert providing health analysis for a specific user profile.

User Profile: {profile}

Ingredient analysis data:
{structured_input}

CRITICAL INSTRUCTIONS:
1. Use ONLY the ingredients provided above - do NOT invent or assume other ingredients
2. ALL explanations must be SPECIFIC to the "{profile}" profile
3. Be medically accurate and evidence-based
4. Use simple, human-friendly language (avoid jargon)

PROFILE-SPECIFIC GUIDANCE:
- **Diabetic**: Focus on sugar content, glycemic index, blood sugar impact, insulin response
- **Heart Patient**: Focus on saturated fats, trans fats, sodium, cholesterol, cardiovascular health
- **Child**: Focus on growth, development, additives, artificial ingredients, allergens
- **Pregnant**: Focus on fetal development, nutrients, food safety, harmful additives
- **General**: Focus on overall health, balanced nutrition, moderation

RETURN VALID JSON ONLY (no markdown, no code blocks):
{{
  "harm_explanation": "Clear explanation of why this product is harmful/safe/moderate for a {profile}. Mention specific health impacts relevant to {profile}.",
  "risk_factors": [
    "Specific risk factor 1 for {profile}",
    "Specific risk factor 2 for {profile}",
    "Specific risk factor 3 for {profile}"
  ],
  "alternatives": [
    {{
      "name": "Natural/Homemade Alternative (Indian/Ayurvedic)",
      "why": "Why this is better for {profile} specifically",
      "how_to_use": "Simple preparation or usage tip",
      "benefit": "Specific health benefit for {profile}"
    }}
  ],
  "commercial_alternatives": [
    {{
      "product_name": "Real Brand/Product Name available in India",
      "why_better": "Specific reason why this is healthier for {profile}",
      "availability": "Where to buy (e.g., Amazon India, BigBasket, local supermarkets)"
    }}
  ],
  "ingredient_explanations": {{
    "Ingredient Name": "Why this is Safe/Moderate/Harmful for {profile} in 1-2 sentences. Be specific to {profile}'s health needs."
  }}
}}

REQUIREMENTS:
- Provide 2-3 natural/homemade alternatives (Indian/Ayurvedic preferred)
- Provide 2-3 real commercial products available in Indian market
- EVERY ingredient must have an explanation in 'ingredient_explanations'
- All explanations must clearly state WHY it matters for {profile}
- Use medical accuracy but simple language

Example for Diabetic:
"Monosodium Glutamate": "Can cause blood sugar spikes and insulin resistance in diabetics. Frequent consumption may worsen glucose control."

Example for Child:
"Monosodium Glutamate": "May cause headaches and hyperactivity in children. Not recommended for regular consumption in growing kids."
"""

    model = genai.GenerativeModel("gemini-2.5-flash")
    result = model.generate_content(prompt)
    
    # Clean up response to ensure valid JSON
    text = result.text.strip()
    if text.startswith("```json"):
        text = text[7:-3].strip()
    elif text.startswith("```"):
         text = text[3:-3].strip()
         
    try:
        return json.loads(text)
    except:
        return {
            "harm_explanation": text, 
            "risk_factors": [], 
            "alternatives": []
        }


