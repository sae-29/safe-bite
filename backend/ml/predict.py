from transformers import DistilBertForSequenceClassification, DistilBertTokenizerFast
import torch

# =========================
# LOAD TRAINED MODEL
# =========================

MODEL_PATH = "D:\\snack-analyzer\\backend\\ml\\models\\final_model"

loaded_tokenizer = DistilBertTokenizerFast.from_pretrained(MODEL_PATH)
loaded_model = DistilBertForSequenceClassification.from_pretrained(MODEL_PATH)

loaded_model.eval()

# Use GPU if available
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
loaded_model.to(DEVICE)

# =========================
# LABEL MAP (MUST MATCH TRAINING)
# =========================

label_map = {
    0: "Safe",
    1: "Moderate",
    2: "Harmfull"
}

# =========================
# PREDICTION FUNCTION
# =========================

def predict_ingredient(ingredient_text: str):
    """
    Predict risk category for a single ingredient
    """

    inputs = loaded_tokenizer(
        ingredient_text,
        return_tensors="pt",
        truncation=True,
        padding=True
    )

    inputs = {k: v.to(DEVICE) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = loaded_model(**inputs)

    logits = outputs.logits
    predicted_class_id = torch.argmax(logits, dim=1).item()
    confidence = torch.softmax(logits, dim=1)[0][predicted_class_id].item()

    return {
        "ingredient": ingredient_text,
        "risk": label_map.get(predicted_class_id, "Unknown"),
        "confidence": round(confidence, 2)
    }
