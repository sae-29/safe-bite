"""
CORRECT REFINED CONVERSION SCRIPT
--------------------------------
Uses ingredients_text (correct field for 'reduced' config)

Output:
data/processed/ingredient_risk.json

Labels:
0 = Safe
1 = Moderate
2 = Harmful
"""

import json
import os
from datasets import load_dataset
from tqdm import tqdm

# =========================
# CONFIG
# =========================

OUTPUT_PATH = "data/processed/ingredient_risk.json"
MAX_INGREDIENTS = 100000  # demo-safe

os.makedirs("data/processed", exist_ok=True)

# =========================
# RISK RULES
# =========================

HARMFUL_KEYWORDS = [
    "e102", "e110", "e124", "e129", "e133",
    "e211", "e250", "tartrazine",
    "msg", "monosodium glutamate",
    "aspartame", "saccharin"
]

MODERATE_KEYWORDS = [
    "palm oil", "refined sugar", "glucose syrup",
    "sodium benzoate", "preservative",
    "emulsifier", "stabilizer", "flavour"
]

SAFE_KEYWORDS = [
    "rice flour", "wheat flour", "oats",
    "salt", "water", "milk", "jaggery", "honey"
]

# =========================
# HELPERS
# =========================

def split_ingredients(text):
    if not text:
        return []
    text = text.lower().replace("(", "").replace(")", "")
    return [i.strip() for i in text.split(",") if len(i.strip()) > 1]

def assign_label(ingredient):
    for h in HARMFUL_KEYWORDS:
        if h in ingredient:
            return 2
    for m in MODERATE_KEYWORDS:
        if m in ingredient:
            return 1
    for s in SAFE_KEYWORDS:
        if s in ingredient:
            return 0
    return 1  # unknown → moderate

# =========================
# LOAD DATASET (CORRECT)
# =========================

print("Loading Open Food Facts (reduced, streaming)...")

dataset = load_dataset(
    "HC-85/open-food-facts",
    "reduced",
    split="train",
    streaming=True
)

# =========================
# CONVERSION
# =========================

output = []
seen = set()

print("Processing ingredients_text...")

for item in tqdm(dataset):
    if len(output) >= MAX_INGREDIENTS:
        break

    ingredients_text = item.get("ingredients_text")

    for ingredient in split_ingredients(ingredients_text):
        if ingredient in seen:
            continue

        label = assign_label(ingredient)

        output.append({
            "text": ingredient,
            "label": label
        })

        seen.add(ingredient)

        if len(output) >= MAX_INGREDIENTS:
            break

# =========================
# SAVE
# =========================

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2)

print("\n✅ DATASET GENERATION COMPLETE")
print(f"Total unique ingredients labeled: {len(output)}")
print(f"Saved to: {OUTPUT_PATH}")

# =========================
# LABEL DISTRIBUTION
# =========================

counts = {0: 0, 1: 0, 2: 0}
for x in output:
    counts[x["label"]] += 1

print("\nLabel Distribution:")
print(f"Safe (0): {counts[0]}")
print(f"Moderate (1): {counts[1]}")
print(f"Harmful (2): {counts[2]}")
