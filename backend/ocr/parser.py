import re

def parse_ingredients(text):
    """
    Parse ingredient text into a list of individual ingredients.
    Filters out garbage text and non-ingredient items.
    """
    if not text or text.strip() == "":
        return {"ingredients": []}
    
    # Remove common prefixes
    text = text.lower()
    text = text.replace("\n", " ")
    text = re.sub(r"ingredients?:?", "", text, flags=re.IGNORECASE)
    
    # Split by common delimiters
    items = re.split(r",|;|\n", text)
    
    ingredients = []
    for item in items:
        item = item.strip()
        
        # Skip if too short or contains numbers/garbage
        if len(item) < 3:
            continue
        
        # Skip if it's mostly numbers or special characters
        if re.search(r'\d{2,}', item):  # Skip if has 2+ consecutive digits
            continue
        
        # Skip common garbage patterns
        garbage_patterns = [
            r'best before',
            r'batch',
            r'upright',
            r'tear',
            r'store in',
            r'consume',
            r'packaged',
            r'\d+g',  # Weight measurements
            r'\d+%',  # Percentages
            r'calories',
            r'energy',
        ]
        
        is_garbage = False
        for pattern in garbage_patterns:
            if re.search(pattern, item, re.IGNORECASE):
                is_garbage = True
                break
        
        if not is_garbage:
            ingredients.append(item)
    
    return {
        "ingredients": ingredients
    }

