# ============================================================
# train_t5_healthcaremagic.py
# Fine-tune T5 on HealthCareMagic-100k for question generation
# Run in Google Colab with GPU (T4 or better)
# ============================================================
# SETUP IN COLAB:
#   !pip install transformers==4.40.0 datasets torch tqdm
#   Then run this script cell by cell
# ============================================================

# ── CELL 1: Install + Imports ─────────────────────────────────
import torch
import json
import re
from torch.utils.data import Dataset, DataLoader
from transformers import T5ForConditionalGeneration, AutoTokenizer
from transformers import get_linear_schedule_with_warmup
from torch.optim import AdamW
from datasets import load_dataset
from tqdm import tqdm

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Device: {device}")

# ── CELL 2: Load HealthCareMagic-100k ────────────────────────
print("Loading HealthCareMagic-100k from HuggingFace...")
# This is a real doctor-patient conversation dataset
# Each row: input (patient symptoms) + output (doctor response with questions)
dataset = load_dataset("lavita/ChatDoctor-HealthCareMagic-100k")
print(f"Dataset: {dataset}")
print(f"Sample:\n{dataset['train'][0]}")

# ── CELL 3: Extract symptom → questions pairs ─────────────────
def extract_questions_from_doctor_response(doctor_text: str) -> list:
    """
    Extract actual questions from doctor's response text.
    Doctor responses contain questions mixed with advice.
    We only want the diagnostic questions.
    """
    sentences = re.split(r'(?<=[.!?])\s+', doctor_text.strip())
    questions = []
    for s in sentences:
        s = s.strip()
        # Must end with ? and be a real question (not too short/long)
        if s.endswith("?") and 15 < len(s) < 200:
            # Filter out non-diagnostic questions
            skip = ["how are you", "how do you do", "how can i help",
                    "any other", "anything else", "is there anything"]
            if not any(p in s.lower() for p in skip):
                questions.append(s)
    return questions[:5]  # max 5 questions per sample


def build_t5_pairs(dataset_split, max_samples=50000):
    """
    Build (input, target) pairs for T5:
    input:  "generate questions: <patient symptom text>"
    target: "Q1? [SEP] Q2? [SEP] Q3?"
    """
    pairs = []
    for item in tqdm(dataset_split, desc="Building pairs"):
        patient_text  = item.get("input", "").strip()
        doctor_text   = item.get("output", "").strip()

        if not patient_text or not doctor_text:
            continue
        if len(patient_text) < 20:
            continue

        questions = extract_questions_from_doctor_response(doctor_text)
        if len(questions) < 2:  # need at least 2 questions
            continue

        input_text  = f"generate questions: {patient_text[:400]}"
        target_text = " [SEP] ".join(questions)

        pairs.append({"input": input_text, "target": target_text})

        if len(pairs) >= max_samples:
            break

    print(f"Built {len(pairs)} training pairs")
    return pairs


print("\nBuilding training pairs...")
all_pairs = build_t5_pairs(dataset["train"], max_samples=60000)

# Split
split_idx  = int(len(all_pairs) * 0.9)
train_pairs = all_pairs[:split_idx]
val_pairs   = all_pairs[split_idx:]
print(f"Train: {len(train_pairs)}, Val: {len(val_pairs)}")

# Show sample
print(f"\nSample pair:")
print(f"  INPUT : {train_pairs[0]['input'][:100]}")
print(f"  TARGET: {train_pairs[0]['target'][:100]}")

# ── CELL 4: Dataset class ─────────────────────────────────────
class T5MedicalDataset(Dataset):
    def __init__(self, pairs, tokenizer, max_input=256, max_target=128):
        self.pairs      = pairs
        self.tokenizer  = tokenizer
        self.max_input  = max_input
        self.max_target = max_target

    def __len__(self):
        return len(self.pairs)

    def __getitem__(self, idx):
        pair = self.pairs[idx]
        inp  = self.tokenizer(
            pair["input"], max_length=self.max_input,
            padding="max_length", truncation=True, return_tensors="pt"
        )
        tgt  = self.tokenizer(
            pair["target"], max_length=self.max_target,
            padding="max_length", truncation=True, return_tensors="pt"
        )
        labels = tgt["input_ids"].squeeze(0).clone()
        # Replace padding token id with -100 so loss ignores padding
        labels[labels == self.tokenizer.pad_token_id] = -100

        return {
            "input_ids":      inp["input_ids"].squeeze(0),
            "attention_mask": inp["attention_mask"].squeeze(0),
            "labels":         labels,
        }

# ── CELL 5: Load T5 model ─────────────────────────────────────
MODEL_NAME = "t5-small"   # use t5-base if Colab has enough RAM
print(f"\nLoading {MODEL_NAME}...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model     = T5ForConditionalGeneration.from_pretrained(MODEL_NAME).to(device)
print(f"Parameters: {sum(p.numel() for p in model.parameters()):,}")

# ── CELL 6: Training setup ────────────────────────────────────
BATCH_SIZE = 16
NUM_EPOCHS = 10
LR         = 3e-4   # T5 uses higher LR than BERT

train_ds = T5MedicalDataset(train_pairs, tokenizer)
val_ds   = T5MedicalDataset(val_pairs,   tokenizer)

train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True,  num_workers=2)
val_loader   = DataLoader(val_ds,   batch_size=32,         shuffle=False, num_workers=2)

optimizer   = AdamW(model.parameters(), lr=LR, weight_decay=0.01)
total_steps = len(train_loader) * NUM_EPOCHS
scheduler   = get_linear_schedule_with_warmup(
    optimizer,
    num_warmup_steps=int(total_steps * 0.05),
    num_training_steps=total_steps
)

# ── CELL 7: Train ─────────────────────────────────────────────
def train_epoch(model, loader):
    model.train()
    total_loss = 0
    for batch in tqdm(loader, desc="Train"):
        out  = model(
            input_ids=batch["input_ids"].to(device),
            attention_mask=batch["attention_mask"].to(device),
            labels=batch["labels"].to(device)
        )
        loss = out.loss
        optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        scheduler.step()
        total_loss += loss.item()
    return total_loss / len(loader)


def eval_epoch(model, loader):
    model.eval()
    total_loss = 0
    with torch.no_grad():
        for batch in tqdm(loader, desc="Eval"):
            out = model(
                input_ids=batch["input_ids"].to(device),
                attention_mask=batch["attention_mask"].to(device),
                labels=batch["labels"].to(device)
            )
            total_loss += out.loss.item()
    return total_loss / len(loader)


best_val_loss  = float("inf")
patience_count = 0
PATIENCE       = 3
history        = []

for epoch in range(NUM_EPOCHS):
    print(f"\n{'='*50}")
    print(f"Epoch {epoch+1}/{NUM_EPOCHS}")
    train_loss = train_epoch(model, train_loader)
    val_loss   = eval_epoch(model,  val_loader)
    print(f"Train Loss: {train_loss:.4f}  Val Loss: {val_loss:.4f}")
    history.append({"epoch": epoch+1, "train_loss": train_loss, "val_loss": val_loss})

    if val_loss < best_val_loss:
        best_val_loss  = val_loss
        patience_count = 0
        model.save_pretrained("t5_qgen_model")
        tokenizer.save_pretrained("t5_qgen_model")
        print(f"Saved best model (val_loss={best_val_loss:.4f})")
    else:
        patience_count += 1
        if patience_count >= PATIENCE:
            print("Early stopping.")
            break

with open("t5_history.json", "w") as f:
    json.dump(history, f, indent=2)

# ── CELL 8: Test inference ────────────────────────────────────
model = T5ForConditionalGeneration.from_pretrained("t5_qgen_model").to(device)
model.eval()

test_symptoms = [
    "I have chest pain radiating to my left arm and I am sweating",
    "I have fever and stomach pain for 3 days with vomiting",
    "I have severe headache and neck stiffness since yesterday",
    "I have been feeling anxious and having panic attacks",
    "I have knee pain and swelling after a fall",
]

print("\nInference test:")
print("-" * 60)
for symptom in test_symptoms:
    input_text = f"generate questions: {symptom}"
    ids = tokenizer(input_text, return_tensors="pt",
                    max_length=256, truncation=True).input_ids.to(device)
    with torch.no_grad():
        out = model.generate(
            ids,
            max_new_tokens=150,
            num_beams=4,
            early_stopping=True,
            no_repeat_ngram_size=3,
        )
    decoded = tokenizer.decode(out[0], skip_special_tokens=True)
    questions = [q.strip() for q in decoded.split("[SEP]") if q.strip()]

    print(f"Symptom  : {symptom}")
    print(f"Questions:")
    for i, q in enumerate(questions, 1):
        print(f"  {i}. {q}")
    print()

print("\nFiles to download from Colab:")
print("  t5_qgen_model/  (entire folder) -> ml_models/models/t5_qgen_model/")
print("  t5_history.json                 -> ml_models/models/")
