"""
Run from project root:
    cd C:\Users\91934\OneDrive\Desktop\Swasthya-Bandhu-main\Swasthya-Bandhu-main
    python test_t5_raw.py
"""
import os, sys, torch
os.environ["TRANSFORMERS_OFFLINE"] = "1"
sys.path.append("ml_models/models")

from transformers import AutoTokenizer, T5ForConditionalGeneration

MODELS_DIR = "ml_models/models"

# Find T5 path
t5_path = None
for entry in os.listdir(MODELS_DIR):
    if entry.startswith("t5_qgen_model") and os.path.isdir(os.path.join(MODELS_DIR, entry)):
        inner = os.path.join(MODELS_DIR, entry, "t5_qgen_model")
        t5_path = inner if os.path.isdir(inner) else os.path.join(MODELS_DIR, entry)
        break

print(f"T5 path: {t5_path}\n")

device = torch.device("cpu")
model = T5ForConditionalGeneration.from_pretrained(t5_path).to(device)
tok   = AutoTokenizer.from_pretrained(t5_path, use_fast=True)
model.eval()

symptom = "I have fever and stomach pain for 3 days"

# Try every likely prefix the model was trained with
prefixes = [
    f"generate questions: {symptom}",
    f"generate medical questions: {symptom}",
    f"ask questions: {symptom}",
    f"question: {symptom}",
    f"generate: {symptom}",
    symptom,
]

for prefix in prefixes:
    ids = tok(prefix, return_tensors="pt", max_length=128, truncation=True).input_ids
    with torch.no_grad():
        out = model.generate(
            ids,
            max_new_tokens=200,
            num_beams=4,
            early_stopping=True,
            no_repeat_ngram_size=2,
        )
    decoded = tok.decode(out[0], skip_special_tokens=True)
    print(f"PREFIX: '{prefix[:50]}'")
    print(f"OUTPUT: {decoded}")
    print("-" * 60)
