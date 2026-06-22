# ============================================================
# kaggle_train_bioclinicalbert.py
# Bio_ClinicalBERT — Kaggle P100 version
# ============================================================
# HOW TO USE ON KAGGLE:
#
# 1. Go to kaggle.com → New Notebook
# 2. Settings (right panel) → Accelerator → GPU P100
# 3. Settings → Internet → ON
# 4. Click "+ Add Data" → no dataset needed (downloads automatically)
# 5. Copy this entire script into a code cell
# 6. Click Run All
# 7. When done → go to Output tab → Download:
#       biobert_clinical_best.pth
#       urgency_encoder.pkl
#       specialist_encoder.pkl
# 8. Put all 3 files into ml_models/models/ on your PC
# ============================================================

# ── CELL 1: Install + Config ──────────────────────────────────
import subprocess
subprocess.run(["pip", "install", "-q", "transformers==4.40.0", "datasets", "scikit-learn"], check=True)

import os, json, pickle, re
import torch
import torch.nn as nn
import pandas as pd
import numpy as np
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModel, get_linear_schedule_with_warmup
from torch.optim import AdamW
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from datasets import load_dataset
from tqdm import tqdm

BASE_MODEL   = "emilyalsentzer/Bio_ClinicalBERT"
WORK_DIR     = "/kaggle/working"          # all outputs saved here — downloadable after run
CKPT_DIR     = os.path.join(WORK_DIR, "checkpoints")
os.makedirs(CKPT_DIR, exist_ok=True)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Device    : {device}")
print(f"Model     : {BASE_MODEL}")
print(f"Output dir: {WORK_DIR}")
if device.type == "cuda":
    print(f"GPU       : {torch.cuda.get_device_name(0)}")
    print(f"VRAM      : {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")


# ── CELL 2: Keyword labelling ─────────────────────────────────
def _detect_groups(text):
    t = text.lower()
    return {
        "cardiac":     any(w in t for w in ["chest pain","heart attack","palpitation","arrhythmia","angina","cardiac","heart racing","irregular heartbeat"]),
        "respiratory": any(w in t for w in ["shortness of breath","difficulty breathing","wheezing","cough","breathless","lung","pneumonia","asthma","tuberculosis"]),
        "neuro":       any(w in t for w in ["headache","migraine","seizure","paralysis","stroke","numbness","blurred vision","dizziness","memory","confusion","fainting"]),
        "gastro":      any(w in t for w in ["stomach","abdominal","nausea","vomiting","diarrhea","constipation","bloating","heartburn","gastric","bowel","liver","indigestion"]),
        "fever":       any(w in t for w in ["fever","chills","sweating","high temperature"]),
        "ortho":       any(w in t for w in ["joint pain","back pain","knee","bone","fracture","arthritis","muscle pain","sprain","neck pain","shoulder pain"]),
        "skin":        any(w in t for w in ["rash","skin","itch","eczema","psoriasis","bruising","hives","acne"]),
        "urinary":     any(w in t for w in ["urination","urine","urinary","kidney","bladder","burning urination","frequent urination","blood in urine"]),
        "mental":      any(w in t for w in ["anxiety","depression","panic","stress","mental","mood","sleep","insomnia","suicidal","hallucination"]),
        "gynec":       any(w in t for w in ["menstrual","period","vaginal","pregnancy","pelvic","ovary","uterus","discharge"]),
        "eye":         any(w in t for w in ["eye pain","vision loss","red eye","blurry vision","eye discharge"]),
        "ent":         any(w in t for w in ["ear pain","throat pain","sore throat","nose bleed","hearing loss","tonsil"]),
        "diabetes":    any(w in t for w in ["thirst","blood sugar","diabetes","glucose","weight loss"]),
    }

def label_specialist(text):
    g = _detect_groups(text)
    if g["cardiac"]:                              return "Cardiologist"
    if g["respiratory"] and g["fever"]:           return "Pulmonologist"
    if g["fever"] and g["gastro"]:                return "Gastroenterologist"
    if g["fever"] and g["urinary"]:               return "Urologist"
    if g["fever"] and g["neuro"]:                 return "Neurologist"
    if g["respiratory"]:                          return "Pulmonologist"
    if g["neuro"]:                                return "Neurologist"
    if g["gastro"]:                               return "Gastroenterologist"
    if g["ortho"]:                                return "Orthopedist"
    if g["skin"]:                                 return "Dermatologist"
    if g["mental"]:                               return "Psychiatrist"
    if g["gynec"]:                                return "Gynecologist"
    if g["urinary"] or g["diabetes"]:             return "Urologist"
    if g["eye"]:                                  return "Ophthalmologist"
    if g["ent"]:                                  return "ENT Specialist"
    if g["fever"]:                                return "General Physician"
    return "General Physician"

def label_urgency(text):
    t = text.lower()
    g = _detect_groups(text)
    if any(w in t for w in ["chest pain","heart attack","stroke","not breathing","unconscious","severe bleeding","anaphylaxis","crushing"]):
        return "immediate"
    if any(w in t for w in ["high fever","difficulty breathing","vomiting blood","blood in stool","severe pain","confusion","seizure","paralysis","fainting"]):
        return "within_24_hours"
    if g["cardiac"]:
        return "within_24_hours"
    if g["fever"] and (g["gastro"] or g["neuro"] or g["urinary"]):
        return "within_24_hours"
    if any(w in t for w in ["fever","pain","swelling","infection","cough","vomiting","diarrhea","persistent","worsening"]):
        return "within_a_week"
    return "routine"

def label_severity(text):
    t = text.lower()
    g = _detect_groups(text)
    base = 4
    if g["cardiac"]:                              base = 8
    elif g["respiratory"] and g["fever"]:         base = 7
    elif g["respiratory"]:                        base = 6
    elif g["neuro"] and g["fever"]:               base = 7
    elif g["neuro"]:                              base = 6
    elif g["gastro"] and g["fever"]:              base = 6
    elif g["fever"] and g["urinary"]:             base = 6
    elif g["fever"]:                              base = 5
    elif g["gastro"]:                             base = 5
    elif g["mental"]:                             base = 5
    elif g["ortho"]:                              base = 4
    elif g["skin"] or g["eye"] or g["ent"]:       base = 3
    if any(w in t for w in ["unbearable","excruciating","worst ever","extreme","crushing"]):
        base = max(base, 9)
    elif any(w in t for w in ["severe","very bad","intense","sharp","high fever","vomiting blood"]):
        base = max(base, 7)
    elif any(w in t for w in ["moderate","significant","persistent","worsening"]):
        base = max(base, 5)
    elif any(w in t for w in ["mild","slight","minor","occasional"]):
        base = min(base, 3)
    if any(w in t for w in ["month","months","chronic","years"]):
        base = min(base + 2, 10)
    elif any(w in t for w in ["week","weeks","few days"]):
        base = min(base + 1, 10)
    return base

def make_record(text):
    text = text.strip()[:512]
    return {
        "symptom_text":   text,
        "specialist":     label_specialist(text),
        "urgency":        label_urgency(text),
        "severity_score": label_severity(text),
    }


# ── CELL 3: Load datasets ─────────────────────────────────────
PROCESSED_CSV  = os.path.join(WORK_DIR, "combined_dataset.csv")
URGENCY_PKL    = os.path.join(WORK_DIR, "urgency_encoder.pkl")
SPECIALIST_PKL = os.path.join(WORK_DIR, "specialist_encoder.pkl")

records = []

print("Loading HealthCareMagic-100k...")
hm = load_dataset("lavita/ChatDoctor-HealthCareMagic-100k")["train"]
print(f"  Rows: {len(hm)}")
for item in tqdm(hm, desc="HealthCareMagic"):
    text = str(item.get("input", "")).strip()
    if len(text) >= 30:
        records.append(make_record(text))

print("\nLoading MedQuAD...")
try:
    mq = load_dataset("lavita/MedQuAD")["train"]
    print(f"  Rows: {len(mq)}")
    for item in tqdm(mq, desc="MedQuAD"):
        text = str(item.get("question", "")).strip()
        if len(text) >= 30:
            records.append(make_record(text))
except Exception as e:
    print(f"  MedQuAD failed: {e} — continuing with HealthCareMagic only")

df = pd.DataFrame(records)
print(f"\nTotal records: {len(df)}")
print(df["specialist"].value_counts().to_string())
print(df["urgency"].value_counts().to_string())

urgency_enc    = LabelEncoder()
specialist_enc = LabelEncoder()
df["urgency_encoded"]    = urgency_enc.fit_transform(df["urgency"])
df["specialist_encoded"] = specialist_enc.fit_transform(df["specialist"])

df.to_csv(PROCESSED_CSV, index=False)
with open(URGENCY_PKL,    "wb") as f: pickle.dump(urgency_enc,    f)
with open(SPECIALIST_PKL, "wb") as f: pickle.dump(specialist_enc, f)
print(f"\nSaved encoders to {WORK_DIR}")
print(f"Urgency classes    : {list(urgency_enc.classes_)}")
print(f"Specialist classes : {list(specialist_enc.classes_)}")

NUM_URGENCY    = len(urgency_enc.classes_)
NUM_SPECIALIST = len(specialist_enc.classes_)

train_df, val_df = train_test_split(
    df, test_size=0.15, random_state=42, stratify=df["specialist"])
print(f"\nTrain: {len(train_df)}  Val: {len(val_df)}")


# ── CELL 4: Dataset ───────────────────────────────────────────
class MedDataset(Dataset):
    def __init__(self, df, tokenizer, max_len=256):
        self.df        = df.reset_index(drop=True)
        self.tokenizer = tokenizer
        self.max_len   = max_len

    def __len__(self): return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        enc = self.tokenizer(
            str(row["symptom_text"]),
            max_length=self.max_len, padding="max_length",
            truncation=True, return_tensors="pt"
        )
        return {
            "input_ids":      enc["input_ids"].squeeze(0),
            "attention_mask": enc["attention_mask"].squeeze(0),
            "severity_cls":   torch.tensor(int(row["severity_score"]) - 1, dtype=torch.long),
            "severity_reg":   torch.tensor(float(row["severity_score"]),   dtype=torch.float),
            "urgency":        torch.tensor(int(row["urgency_encoded"]),     dtype=torch.long),
            "specialist":     torch.tensor(int(row["specialist_encoded"]),  dtype=torch.long),
        }


# ── CELL 5: Model ─────────────────────────────────────────────
class ClinicalBERTModel(nn.Module):
    def __init__(self, num_urgency, num_specialist):
        super().__init__()
        self.bert    = AutoModel.from_pretrained(BASE_MODEL)
        self.dropout = nn.Dropout(0.3)
        self.severity_cls    = nn.Sequential(nn.Linear(768,256), nn.ReLU(), nn.Dropout(0.2), nn.Linear(256,10))
        self.severity_reg    = nn.Sequential(nn.Linear(768,128), nn.ReLU(), nn.Dropout(0.2), nn.Linear(128,1), nn.Sigmoid())
        self.urgency_head    = nn.Sequential(nn.Linear(768,256), nn.ReLU(), nn.Dropout(0.2), nn.Linear(256,num_urgency))
        self.specialist_head = nn.Sequential(
            nn.Linear(768,512), nn.ReLU(), nn.Dropout(0.25),
            nn.Linear(512,256), nn.ReLU(), nn.Dropout(0.2),
            nn.Linear(256,num_specialist)
        )

    def forward(self, input_ids, attention_mask):
        pooled = self.dropout(
            self.bert(input_ids=input_ids, attention_mask=attention_mask).pooler_output)
        return {
            "severity_cls": self.severity_cls(pooled),
            "severity_reg": self.severity_reg(pooled).squeeze(-1) * 9 + 1,
            "urgency":      self.urgency_head(pooled),
            "specialist":   self.specialist_head(pooled),
        }


# ── CELL 6: Helpers ───────────────────────────────────────────
ce_loss  = nn.CrossEntropyLoss()
mse_loss = nn.MSELoss()

def evaluate(model, loader):
    model.eval()
    sp, st, up, ut, srp, srt, reg_err = [], [], [], [], [], [], []
    with torch.no_grad():
        for b in tqdm(loader, desc="Eval", leave=False):
            ids, mask = b["input_ids"].to(device), b["attention_mask"].to(device)
            out = model(ids, mask)
            sp.extend(torch.argmax(out["specialist"],  1).cpu().tolist())
            st.extend(b["specialist"].tolist())
            up.extend(torch.argmax(out["urgency"],     1).cpu().tolist())
            ut.extend(b["urgency"].tolist())
            srp.extend(torch.argmax(out["severity_cls"],1).cpu().tolist())
            srt.extend(b["severity_cls"].tolist())
            reg_err.extend((out["severity_reg"].cpu() - b["severity_reg"]).abs().tolist())
    return {
        "specialist_acc": accuracy_score(st, sp),
        "urgency_acc":    accuracy_score(ut, up),
        "severity_acc":   accuracy_score(srt, srp),
        "severity_mae":   float(np.mean(reg_err)),
    }

def save_checkpoint(stage, epoch, model, optimizer, best_acc, history):
    path = os.path.join(CKPT_DIR, f"ckpt_{stage}.pth")
    torch.save({
        "stage": stage, "epoch": epoch,
        "model": model.state_dict(),
        "optimizer": optimizer.state_dict(),
        "best_acc": best_acc, "history": history,
    }, path)

def load_checkpoint(stage, model, optimizer):
    path = os.path.join(CKPT_DIR, f"ckpt_{stage}.pth")
    if not os.path.exists(path):
        return 0, 0.0, []
    ckpt = torch.load(path, map_location=device)
    model.load_state_dict(ckpt["model"])
    optimizer.load_state_dict(ckpt["optimizer"])
    print(f"  Resumed {stage} from epoch {ckpt['epoch']+1}, best_acc={ckpt['best_acc']:.4f}")
    return ckpt["epoch"] + 1, ckpt["best_acc"], ckpt["history"]


# ── CELL 7: Tokenizer + DataLoaders ──────────────────────────
print(f"\nLoading tokenizer: {BASE_MODEL}")
tokenizer    = AutoTokenizer.from_pretrained(BASE_MODEL)
train_ds     = MedDataset(train_df, tokenizer)
val_ds       = MedDataset(val_df,   tokenizer)
# P100 has 16GB VRAM — batch_size=32 is safe (vs 16 on T4)
train_loader = DataLoader(train_ds, batch_size=32, shuffle=True,  num_workers=2, pin_memory=True)
val_loader   = DataLoader(val_ds,   batch_size=64, shuffle=False, num_workers=2, pin_memory=True)
print(f"Train batches: {len(train_loader)}  Val batches: {len(val_loader)}")


# ── CELL 8: run_stage ─────────────────────────────────────────
def run_stage(stage, epochs, optimizer, scheduler, loss_fn, patience=3):
    start_epoch, best_acc, history = load_checkpoint(stage, model, optimizer)
    no_improve = 0

    for epoch in range(start_epoch, epochs):
        model.train()
        total_loss = 0
        for b in tqdm(train_loader, desc=f"{stage} E{epoch+1}/{epochs}"):
            ids, mask = b["input_ids"].to(device), b["attention_mask"].to(device)
            out  = model(ids, mask)
            loss = loss_fn(out, b)
            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            if scheduler: scheduler.step()
            total_loss += loss.item()

        metrics  = evaluate(model, val_loader)
        avg_loss = total_loss / len(train_loader)
        print(f"[{stage}] E{epoch+1}/{epochs} | loss={avg_loss:.4f} | "
              f"spec={metrics['specialist_acc']:.4f} | urg={metrics['urgency_acc']:.4f} | "
              f"sev_acc={metrics['severity_acc']:.4f} | sev_mae={metrics['severity_mae']:.4f}")

        history.append({"stage": stage, "epoch": epoch+1, "loss": avg_loss, **metrics})

        if metrics["specialist_acc"] > best_acc:
            best_acc   = metrics["specialist_acc"]
            no_improve = 0
            torch.save(model.state_dict(), os.path.join(WORK_DIR, f"best_{stage}.pth"))
            print(f"  Saved best (spec_acc={best_acc:.4f})")
        else:
            no_improve += 1
            if no_improve >= patience:
                print(f"  Early stopping at epoch {epoch+1}")
                break

        save_checkpoint(stage, epoch, model, optimizer, best_acc, history)

    best_path = os.path.join(WORK_DIR, f"best_{stage}.pth")
    if os.path.exists(best_path):
        model.load_state_dict(torch.load(best_path, map_location=device))
    print(f"  [{stage}] Best specialist_acc: {best_acc:.4f}")
    return history


# ── CELL 9: Build model ───────────────────────────────────────
model = ClinicalBERTModel(NUM_URGENCY, NUM_SPECIALIST).to(device)
print(f"Total params: {sum(p.numel() for p in model.parameters()):,}")
all_history = []


# ── CELL 10: Stage 1 — Specialist head only (BERT frozen) ────
print("\n" + "="*60)
print("STAGE 1: specialist_head only — BERT frozen")
print("="*60)
for p in model.bert.parameters(): p.requires_grad = False

opt1 = AdamW(model.specialist_head.parameters(), lr=1e-3, weight_decay=0.01)
sch1 = get_linear_schedule_with_warmup(
    opt1, num_warmup_steps=100, num_training_steps=len(train_loader)*5)

h = run_stage("stage1", epochs=5, optimizer=opt1, scheduler=sch1,
              loss_fn=lambda out,b: ce_loss(out["specialist"], b["specialist"].to(device)))
all_history.extend(h)


# ── CELL 11: Stage 2 — Urgency head only (BERT still frozen) ─
print("\n" + "="*60)
print("STAGE 2: urgency_head only — BERT frozen")
print("="*60)
opt2 = AdamW(model.urgency_head.parameters(), lr=1e-3, weight_decay=0.01)
sch2 = get_linear_schedule_with_warmup(
    opt2, num_warmup_steps=100, num_training_steps=len(train_loader)*5)

h = run_stage("stage2", epochs=5, optimizer=opt2, scheduler=sch2,
              loss_fn=lambda out,b: ce_loss(out["urgency"], b["urgency"].to(device)))
all_history.extend(h)


# ── CELL 12: Stage 3 — Joint fine-tune (all unfrozen, low LR) ─
print("\n" + "="*60)
print("STAGE 3: joint fine-tune — all layers unfrozen")
print("="*60)
for p in model.bert.parameters():            p.requires_grad = True
for p in model.bert.embeddings.parameters(): p.requires_grad = False

opt3 = AdamW([
    {"params": model.bert.parameters(),            "lr": 2e-5},
    {"params": model.specialist_head.parameters(), "lr": 5e-5},
    {"params": model.urgency_head.parameters(),    "lr": 5e-5},
    {"params": model.severity_cls.parameters(),    "lr": 5e-5},
    {"params": model.severity_reg.parameters(),    "lr": 5e-5},
], weight_decay=0.01)

total_steps = len(train_loader) * 10
sch3 = get_linear_schedule_with_warmup(
    opt3, num_warmup_steps=int(total_steps*0.1), num_training_steps=total_steps)

def joint_loss(out, b):
    return (
        1.5 * ce_loss(out["specialist"],   b["specialist"].to(device))  +
        1.2 * ce_loss(out["urgency"],      b["urgency"].to(device))     +
        1.0 * ce_loss(out["severity_cls"], b["severity_cls"].to(device))+
        0.5 * mse_loss(out["severity_reg"],b["severity_reg"].to(device))
    )

h = run_stage("stage3", epochs=10, optimizer=opt3, scheduler=sch3,
              loss_fn=joint_loss, patience=3)
all_history.extend(h)


# ── CELL 13: Save final outputs ───────────────────────────────
FINAL_PTH = os.path.join(WORK_DIR, "biobert_clinical_best.pth")
torch.save(model.state_dict(), FINAL_PTH)
with open(os.path.join(WORK_DIR, "training_history.json"), "w") as f:
    json.dump(all_history, f, indent=2)

print("\nFinal evaluation:")
final = evaluate(model, val_loader)
for k, v in final.items():
    print(f"  {k}: {v:.4f}")

print(f"\n{'='*60}")
print("TRAINING COMPLETE — Download these from Output tab:")
print(f"{'='*60}")
print("  /kaggle/working/biobert_clinical_best.pth  → ml_models/models/")
print("  /kaggle/working/urgency_encoder.pkl        → ml_models/models/")
print("  /kaggle/working/specialist_encoder.pkl     → ml_models/models/")


# ── CELL 14: Inference test ───────────────────────────────────
model.eval()
tests = [
    "45 year old male, chest pain radiating to left arm, sweating, shortness of breath",
    "28 year old female, fever for 3 days, stomach pain, nausea, vomiting",
    "35 year old male, severe headache, neck stiffness, sensitivity to light",
    "22 year old female, mild skin rash on arms, itching for 2 days",
    "60 year old male, shortness of breath, wheezing, cough with mucus",
    "30 year old female, anxiety, panic attacks, difficulty sleeping",
    "50 year old male, frequent urination, excessive thirst, weight loss",
]
print("\nInference test:")
print("-" * 70)
for text in tests:
    enc = tokenizer(text, return_tensors="pt", max_length=256,
                    truncation=True, padding="max_length")
    with torch.no_grad():
        out = model(enc["input_ids"].to(device), enc["attention_mask"].to(device))
    print(f"Input     : {text[:65]}")
    print(f"Specialist: {specialist_enc.classes_[torch.argmax(out['specialist']).item()]}  "
          f"(conf={torch.softmax(out['specialist'],1).max().item():.2f})")
    print(f"Urgency   : {urgency_enc.classes_[torch.argmax(out['urgency']).item()]}")
    print(f"Severity  : {torch.argmax(out['severity_cls']).item()+1}/10  "
          f"(reg={out['severity_reg'].item():.1f})")
    print()
