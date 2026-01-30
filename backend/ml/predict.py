import re

# =========================
# KEYWORD-BASED CLASSIFIER (Lightweight for Deployment)
# =========================

# Lists of concern
HARMFUL_KEYWORDS = [
    # Artificial Preservatives
    "benzoate", "sorbate", "nitrate", "nitrite", "bbq", "tbhq", "bha", "bht", "gallate", "metabisulfite",
    # Artificial Sweeteners
    "aspartame", "sucralose", "saccharin", "acesulfame", "neotame",
    # Flavor Enhancers
    "monosodium glutamate", "msg", "glutamate", "disodium",
    # Artificial Colors
    "red 40", "yellow 5", "yellow 6", "blue 1", "blue 2", "artificial color", "caramel color",
    # Unhealthy Fats
    "hydrogenated", "trans fat", "corn oil", "soybean oil", "palm oil", "margarine",
    # Other
    "high fructose corn syrup", "corn syrup"
]

MODERATE_KEYWORDS = [
    # Refined Sugars
    "sugar", "syrup", "dextrose", "fructose", "sucrose", "maltodextrin", "glucose", "cane",
    # Additives
    "gum", "emulsifier", "stabilizer", "lecithin", "modified starch", "flavor", "extract",
    # Salts
    "sodium", "salt"
]

def predict_ingredient(ingredient_text: str):
    """
    Predict risk category for a single ingredient using keyword matching.
    Replaces heavy ML model for lightweight deployment.
    """
    text_lower = ingredient_text.lower()
    
    # Check Harmful
    if any(k in text_lower for k in HARMFUL_KEYWORDS):
        return {
            "ingredient": ingredient_text,
            "risk": "Harmfull",  # Kept spelling to match frontend
            "confidence": 0.95
        }
        
    # Check Moderate
    if any(k in text_lower for k in MODERATE_KEYWORDS):
        return {
            "ingredient": ingredient_text,
            "risk": "Moderate",
            "confidence": 0.90
        }
        
    # Default to Safe
    return {
        "ingredient": ingredient_text,
        "risk": "Safe",
        "confidence": 0.85
    }
