import re

def parse_ingredients(text):
    """
    Parse ingredient text into a list of individual ingredients.
    Filters out garbage text and non-ingredient items.
    """
    if not text or text.strip() == "":
        return {"ingredients": []}
    
    # Remove common prefixes more robustly
    text = text.lower().strip()
    text = text.replace("\n", " ")
    # Strip everything up to the first 'ingredients:' if present
    marker = "ingredients:"
    if marker in text:
        text = text.split(marker, 1)[1]
    
    # Split by common delimiters: comma, semicolon, period, or newline
    # Using regex to handle "item. next" but not "E331" if possible
    items = re.split(r",|;|\.|\n", text)
    
    ingredients = []
    for item in items:
        item = item.strip()
        
        # Skip if too short
        if len(item) < 3:
            continue
        
        # Skip if it's mostly random numbers, but KEEP E-numbers (e.g., e331)
        # Modified regex: skip if has 2+ consecutive digits NOT preceded by 'e'
        if re.search(r'(?<!e)\d{2,}', item, re.IGNORECASE):
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

