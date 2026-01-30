from datasets import load_dataset
from .model import tokenizer

dataset = load_dataset(
    "json",
    data_files={
        "train": "D:\\snack-analyzer\\data\\processed\\ingredient_risk.json"
    }
)

def tokenize(batch):
    return tokenizer(
        batch["text"],
        padding=True,
        truncation=True
    )

dataset = dataset.map(tokenize, batched=True)
