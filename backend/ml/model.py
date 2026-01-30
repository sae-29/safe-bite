
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification
import torch

MODEL_PATH = "D:\\snack-analyzer\\backend\\ml\\models\\final_model"

tokenizer = DistilBertTokenizerFast.from_pretrained(MODEL_PATH)

model = DistilBertForSequenceClassification.from_pretrained(
    MODEL_PATH
)

model.eval()

# Move to GPU if available
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(DEVICE)
