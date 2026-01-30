import re

def calculate_risk_score(ingredients_text: str, ml_results: list) -> dict:
    """
    Calculates a 0-100 risk score based on:
    - Artificial preservatives (25%)
    - Excess sugar/sodium (20%)
    - Harmful additives (20%)
    - Allergens (15%)
    - Ultra-processing indicators (20%)
    """
    
    score = 0
    breakdown = []
    
    # 1. Artificial Preservatives (25%)
    preservatives = ["benzoate", "sorbate", "nitrate", "nitrite", "bbq", "tbhq", "bha", "bht", "gallate", "metabisulfite"]
    if any(p in ingredients_text.lower() for p in preservatives):
        score += 25
        breakdown.append("Contains Artificial Preservatives (+25)")
        
    # 2. Excess Sugar/Sodium/Fat (20%)
    sugar_salt_fat = ["sugar", "syrup", "dextrose", "fructose", "sucrose", "maltodextrin", "sodium", "salt", "oil", "fat", "glucose", "cane", "corn syrup"]
    # Check for presence and repetition
    matches = [s for s in sugar_salt_fat if s in ingredients_text.lower()]
    if len(matches) >= 2:
        score += 20
        breakdown.append("High Sugar/Sodium/Fat Content (+20)")

    # 3. Harmful Additives (20%) - Based on ML results
    harmful_count = sum(1 for r in ml_results if r["risk"] == "Harmfull")
    if harmful_count > 0:
        score += 20
        breakdown.append(f"Contains {harmful_count} Harmful Additives (+20)")

    # 4. Allergens (15%)
    allergens = ["soy", "peanut", "milk", "gluten", "wheat", "egg", "fish", "shellfish", "nut", "dairy", "lactose", "casein"]
    if any(a in ingredients_text.lower() for a in allergens):
        score += 15
        breakdown.append("Contains Common Allergens (+15)")

    # 5. Ultra-processing indicators (20%)
    processed = ["hydrolyzed", "isolate", "modified starch", "hydrogenated", "flavor", "colour", "color", "acid", "gum", "emulsifier", "stabilizer", "artificial", "extract"]
    if any(p in ingredients_text.lower() for p in processed):
        score += 20
        breakdown.append("Ultra-processed Ingredients (+20)")

    # Cap score at 100
    final_score = min(score, 100)
    
    # Determine Level
    if final_score <= 30:
        level = "Safe"
    elif final_score <= 60:
        level = "Moderate"
    else:
        level = "High Risk"
        
    return {
        "score": final_score,
        "level": level,
        "breakdown": breakdown
    }
