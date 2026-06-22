# ============================================================
# kaggle_train_t5_cot.py
# T5 Chain-of-Thought question generation — Kaggle P100 version
# ============================================================
# HOW TO USE ON KAGGLE:
#
# 1. Go to kaggle.com → New Notebook
# 2. Settings (right panel) → Accelerator → GPU P100
# 3. Settings → Internet → ON
# 4. Copy this entire script into a code cell
# 5. Click Run All  (~7 hours on P100, fits in 12hr session)
# 6. When done → Output tab → Download entire t5_qgen_model/ folder
# 7. Put the folder into ml_models/models/ on your PC
#    (replace the existing t5_qgen_model/ folder)
# ============================================================

# ── CELL 1: Install + Config ──────────────────────────────────
import subprocess
subprocess.run(["pip", "install", "-q", "transformers==4.40.0", "datasets"], check=True)

import os, re, json
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import T5ForConditionalGeneration, AutoTokenizer
from transformers import get_linear_schedule_with_warmup
from torch.optim import AdamW
from datasets import load_dataset
from tqdm import tqdm

MODEL_NAME = "t5-base"
WORK_DIR   = "/kaggle/working"
CKPT_DIR   = os.path.join(WORK_DIR, "t5_checkpoint")   # resume checkpoint
BEST_DIR   = os.path.join(WORK_DIR, "t5_qgen_model")   # final best model — download this
PAIRS_FILE = os.path.join(WORK_DIR, "t5_cot_pairs.json")
STATE_FILE = os.path.join(WORK_DIR, "t5_train_state.json")

os.makedirs(WORK_DIR, exist_ok=True)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Device : {device}")
print(f"Model  : {MODEL_NAME}")
if device.type == "cuda":
    print(f"GPU    : {torch.cuda.get_device_name(0)}")
    print(f"VRAM   : {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")


# ── CELL 2: Symptom group detection ──────────────────────────
def _detect_groups(text):
    t = text.lower()
    return {
        "cardiac":     any(w in t for w in ["chest pain","heart","palpitation","arrhythmia","angina","cardiac"]),
        "respiratory": any(w in t for w in ["breath","cough","wheez","lung","pneumonia","asthma","tuberculosis"]),
        "neuro":       any(w in t for w in ["headache","migraine","seizure","paralysis","stroke","numbness","dizziness","confusion","fainting","vision"]),
        "gastro":      any(w in t for w in ["stomach","abdominal","nausea","vomit","diarrhea","constipation","bloating","heartburn","bowel","liver"]),
        "fever":       any(w in t for w in ["fever","chills","sweating","temperature"]),
        "ortho":       any(w in t for w in ["joint","back pain","knee","bone","fracture","arthritis","muscle","sprain","shoulder"]),
        "skin":        any(w in t for w in ["rash","skin","itch","eczema","psoriasis","hives","acne"]),
        "urinary":     any(w in t for w in ["urin","kidney","bladder","burning urination","frequent urination"]),
        "mental":      any(w in t for w in ["anxiety","depression","panic","stress","mental","mood","sleep","insomnia"]),
        "gynec":       any(w in t for w in ["menstrual","period","vaginal","pregnancy","pelvic","ovary"]),
    }

def build_cot_reasoning(text):
    g   = _detect_groups(text)
    cot = []
    if g["cardiac"]:
        cot.append("chest or cardiac symptoms detected")
        cot.append("need to rule out MI vs angina vs musculoskeletal")
        cot.append("ask about radiation, duration, associated diaphoresis and dyspnea")
    if g["respiratory"]:
        cot.append("respiratory symptoms detected")
        cot.append("need to differentiate infection vs obstruction vs embolism")
        cot.append("ask about sputum, fever, onset, and exertional component")
    if g["neuro"]:
        cot.append("neurological symptoms detected")
        cot.append("need to rule out meningitis, stroke, migraine, raised ICP")
        cot.append("ask about onset speed, neck stiffness, photophobia, focal deficits")
    if g["gastro"] and g["fever"]:
        cot.append("fever with GI symptoms detected")
        cot.append("need to rule out appendicitis, typhoid, cholecystitis, gastroenteritis")
        cot.append("ask about pain location, duration, travel history, bowel changes")
    elif g["gastro"]:
        cot.append("gastrointestinal symptoms detected")
        cot.append("need to differentiate peptic ulcer, GERD, IBD, IBS")
        cot.append("ask about relation to meals, blood in stool, weight loss")
    if g["fever"] and not g["gastro"] and not g["respiratory"]:
        cot.append("isolated fever detected")
        cot.append("need to rule out viral, bacterial, malaria, typhoid")
        cot.append("ask about duration, pattern, travel, contact history")
    if g["ortho"]:
        cot.append("musculoskeletal symptoms detected")
        cot.append("need to differentiate trauma, arthritis, infection, referred pain")
        cot.append("ask about injury history, swelling, morning stiffness, activity limitation")
    if g["mental"]:
        cot.append("mental health symptoms detected")
        cot.append("need to assess severity, triggers, functional impact")
        cot.append("ask about duration, sleep, appetite, suicidal ideation, triggers")
    if g["urinary"]:
        cot.append("urinary symptoms detected")
        cot.append("need to rule out UTI, kidney stones, diabetes, prostate issues")
        cot.append("ask about burning, frequency, blood in urine, flank pain")
    if g["skin"]:
        cot.append("skin symptoms detected")
        cot.append("need to differentiate allergic, infectious, autoimmune")
        cot.append("ask about distribution, triggers, associated fever, new products")
    if g["gynec"]:
        cot.append("gynecological symptoms detected")
        cot.append("need to assess cycle regularity, pregnancy possibility, infection")
        cot.append("ask about last period, discharge, pain character, sexual history")
    if not cot:
        cot = [
            "general symptoms detected",
            "need to assess duration, severity, and associated features",
            "ask about onset, progression, and impact on daily activities"
        ]
    return " | ".join(cot)


# ── CELL 3: Extract questions from doctor response ────────────
SKIP_PHRASES = [
    "how are you", "how do you do", "how can i help", "any other",
    "anything else", "is there anything", "hope i have", "not to worry",
    "consult a doctor", "i would suggest", "i would advise", "dear friend",
    "thanks for", "chat doctor", "i understand", "i studied your"
]

def extract_questions(doctor_text):
    sentences = re.split(r'(?<=[.!?])\s+', doctor_text.strip())
    questions = []
    for s in sentences:
        s = s.strip()
        if not s.endswith("?"):
            continue
        if len(s) < 15 or len(s) > 200:
            continue
        if any(p in s.lower() for p in SKIP_PHRASES):
            continue
        questions.append(s)
    return questions[:5]


# ── CELL 4: Build CoT pairs ───────────────────────────────────
def build_cot_pairs(dataset_split, max_samples=60000):
    pairs = []
    for item in tqdm(dataset_split, desc="Building CoT pairs"):
        patient_text = str(item.get("input",  "")).strip()
        doctor_text  = str(item.get("output", "")).strip()
        if len(patient_text) < 20 or not doctor_text:
            continue
        questions = extract_questions(doctor_text)
        if len(questions) < 2:
            continue
        reasoning   = build_cot_reasoning(patient_text)
        input_text  = f"symptoms: {patient_text[:400]}"
        target_text = f"THINK: {reasoning} QUESTIONS: {' [SEP] '.join(questions)}"
        pairs.append({"input": input_text, "target": target_text})
        if len(pairs) >= max_samples:
            break
    print(f"Built {len(pairs)} CoT pairs")
    return pairs


# ── CELL 5: Load or build pairs ───────────────────────────────
if os.path.exists(PAIRS_FILE):
    print("Loading cached pairs...")
    with open(PAIRS_FILE, "r") as f:
        all_pairs = json.load(f)
    print(f"Loaded {len(all_pairs)} pairs")
else:
    print("Loading HealthCareMagic-100k...")
    ds = load_dataset("lavita/ChatDoctor-HealthCareMagic-100k")["train"]
    print(f"Dataset rows: {len(ds)}")
    all_pairs = build_cot_pairs(ds, max_samples=60000)
    with open(PAIRS_FILE, "w") as f:
        json.dump(all_pairs, f)
    print(f"Saved {len(all_pairs)} pairs")

print(f"\nSample input : {all_pairs[0]['input'][:100]}")
print(f"Sample target: {all_pairs[0]['target'][:150]}")

split       = int(len(all_pairs) * 0.9)
train_pairs = all_pairs[:split]
val_pairs   = all_pairs[split:]
print(f"\nTrain: {len(train_pairs)}  Val: {len(val_pairs)}")


# ── CELL 6: Dataset ───────────────────────────────────────────
class T5CotDataset(Dataset):
    def __init__(self, pairs, tokenizer, max_input=256, max_target=200):
        self.pairs     = pairs
        self.tokenizer = tokenizer
        self.max_input  = max_input
        self.max_target = max_target

    def __len__(self): return len(self.pairs)

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
        labels[labels == self.tokenizer.pad_token_id] = -100
        return {
            "input_ids":      inp["input_ids"].squeeze(0),
            "attention_mask": inp["attention_mask"].squeeze(0),
            "labels":         labels,
        }


# ── CELL 7: Load model ────────────────────────────────────────
if os.path.exists(CKPT_DIR):
    print(f"\nResuming from checkpoint: {CKPT_DIR}")
    tokenizer = AutoTokenizer.from_pretrained(CKPT_DIR)
    model     = T5ForConditionalGeneration.from_pretrained(CKPT_DIR).to(device)
else:
    print(f"\nLoading fresh {MODEL_NAME}...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model     = T5ForConditionalGeneration.from_pretrained(MODEL_NAME).to(device)

print(f"Parameters: {sum(p.numel() for p in model.parameters()):,}")

train_ds     = T5CotDataset(train_pairs, tokenizer)
val_ds       = T5CotDataset(val_pairs,   tokenizer)
# P100 16GB — batch_size=16 for t5-base (vs 8 on T4)
train_loader = DataLoader(train_ds, batch_size=16, shuffle=True,  num_workers=2, pin_memory=True)
val_loader   = DataLoader(val_ds,   batch_size=32, shuffle=False, num_workers=2, pin_memory=True)
print(f"Train batches: {len(train_loader)}  Val batches: {len(val_loader)}")


# ── CELL 8: Training ──────────────────────────────────────────
NUM_EPOCHS = 10
LR         = 3e-4
PATIENCE   = 3

start_epoch    = 0
best_val_loss  = float("inf")
patience_count = 0
history        = []

if os.path.exists(STATE_FILE):
    with open(STATE_FILE, "r") as f:
        state = json.load(f)
    start_epoch    = state["epoch"] + 1
    best_val_loss  = state["best_val_loss"]
    patience_count = state["patience_count"]
    history        = state["history"]
    print(f"Resuming from epoch {start_epoch}, best_val_loss={best_val_loss:.4f}")

total_steps = len(train_loader) * NUM_EPOCHS
optimizer   = AdamW(model.parameters(), lr=LR, weight_decay=0.01)
scheduler   = get_linear_schedule_with_warmup(
    optimizer,
    num_warmup_steps=int(total_steps * 0.05),
    num_training_steps=total_steps
)

for epoch in range(start_epoch, NUM_EPOCHS):
    model.train()
    train_loss = 0
    for b in tqdm(train_loader, desc=f"Train E{epoch+1}/{NUM_EPOCHS}"):
        out = model(
            input_ids=b["input_ids"].to(device),
            attention_mask=b["attention_mask"].to(device),
            labels=b["labels"].to(device)
        )
        optimizer.zero_grad()
        out.loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        scheduler.step()
        train_loss += out.loss.item()
    train_loss /= len(train_loader)

    model.eval()
    val_loss = 0
    with torch.no_grad():
        for b in tqdm(val_loader, desc="Eval", leave=False):
            out = model(
                input_ids=b["input_ids"].to(device),
                attention_mask=b["attention_mask"].to(device),
                labels=b["labels"].to(device)
            )
            val_loss += out.loss.item()
    val_loss /= len(val_loader)

    print(f"Epoch {epoch+1}/{NUM_EPOCHS} | train={train_loss:.4f} | val={val_loss:.4f}")
    history.append({"epoch": epoch+1, "train_loss": train_loss, "val_loss": val_loss})

    if val_loss < best_val_loss:
        best_val_loss  = val_loss
        patience_count = 0
        model.save_pretrained(BEST_DIR)
        tokenizer.save_pretrained(BEST_DIR)
        print(f"  Saved best model (val_loss={best_val_loss:.4f})")
    else:
        patience_count += 1
        if patience_count >= PATIENCE:
            print("Early stopping.")
            break

    # Save checkpoint every epoch
    model.save_pretrained(CKPT_DIR)
    tokenizer.save_pretrained(CKPT_DIR)
    with open(STATE_FILE, "w") as f:
        json.dump({
            "epoch": epoch, "best_val_loss": best_val_loss,
            "patience_count": patience_count, "history": history
        }, f)

with open(os.path.join(WORK_DIR, "t5_history.json"), "w") as f:
    json.dump(history, f, indent=2)
print(f"\nTraining complete. Best val_loss: {best_val_loss:.4f}")


# ── CELL 9: Inference test ────────────────────────────────────
model = T5ForConditionalGeneration.from_pretrained(BEST_DIR).to(device)
model.eval()

def generate_questions(symptom_text, show_reasoning=False):
    ids = tokenizer(
        f"symptoms: {symptom_text}", return_tensors="pt",
        max_length=256, truncation=True
    ).input_ids.to(device)
    with torch.no_grad():
        out = model.generate(ids, max_new_tokens=200, num_beams=4,
                             early_stopping=True, no_repeat_ngram_size=3)
    decoded = tokenizer.decode(out[0], skip_special_tokens=True)
    if show_reasoning and "THINK:" in decoded:
        print(f"  Reasoning: {decoded.split('QUESTIONS:')[0].replace('THINK:','').strip()}")
    q_part    = decoded.split("QUESTIONS:")[-1].strip() if "QUESTIONS:" in decoded else decoded
    questions = [q.strip() for q in q_part.split("[SEP]") if len(q.strip()) > 10]
    questions = [q if q.endswith("?") else q + "?" for q in questions]
    return questions[:5]

tests = [
    "I have chest pain radiating to my left arm and I am sweating a lot",
    "I have had fever for 3 days with stomach pain and vomiting",
    "I have severe headache and neck stiffness since yesterday morning",
    "I have been feeling very anxious and having panic attacks at night",
    "I have knee pain and swelling after a fall yesterday",
]

print("\nInference test:")
print("-" * 65)
for symptom in tests:
    print(f"Symptom: {symptom}")
    questions = generate_questions(symptom, show_reasoning=True)
    for i, q in enumerate(questions, 1):
        print(f"  Q{i}: {q}")
    print()

print(f"\n{'='*60}")
print("TRAINING COMPLETE — Download from Output tab:")
print(f"{'='*60}")
print("  /kaggle/working/t5_qgen_model/  → ml_models/models/t5_qgen_model/")
print("  (download the entire folder, replace existing)")
