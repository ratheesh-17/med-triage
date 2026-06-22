"""
DDXPlus → BioBERT Training Data Pipeline
=========================================
Run in Google Colab:

STEP 1: Download DDXPlus dataset
    !wget -q "https://figshare.com/ndownloader/files/35945800" -O train.zip
    !unzip -q train.zip

STEP 2: Upload this file to Colab, then run:
    python ddxplus_preprocessing.py

OUTPUT:
    biobert_training_data.csv   — ready for BioBERT fine-tuning
    urgency_encoder.pkl         — replace your existing one
    specialist_encoder.pkl      — replace your existing one
"""

import pandas as pd
import numpy as np
import json
import pickle
import os
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

# ── Step 1: DDXPlus PATHOLOGY → Specialist mapping ───────────
# DDXPlus has 49 diseases — all mapped here
PATHOLOGY_TO_SPECIALIST = {
    # Cardiac
    "Myocarditis":                          "Cardiologist",
    "Pericarditis":                         "Cardiologist",
    "Unstable angina":                      "Cardiologist",
    "Stable angina":                        "Cardiologist",
    "Acute MI":                             "Cardiologist",
    "SVT":                                  "Cardiologist",
    "Atrial fibrillation":                  "Cardiologist",

    # Pulmonology
    "Pneumonia":                            "Pulmonologist",
    "Bronchitis":                           "Pulmonologist",
    "Bronchospasm / acute asthma exacerbation": "Pulmonologist",
    "Pulmonary embolism":                   "Pulmonologist",
    "Spontaneous pneumothorax":             "Pulmonologist",
    "Pulmonary neoplasm":                   "Pulmonologist",
    "Tuberculosis":                         "Pulmonologist",
    "Pleurisy":                             "Pulmonologist",
    "Acute COPD exacerbation / infection":  "Pulmonologist",
    "Possible NSTEMI / STEMI":              "Cardiologist",

    # Neurology
    "Cluster headache":                     "Neurologist",
    "Migraine":                             "Neurologist",
    "Tension headache":                     "Neurologist",
    "Meningitis":                           "Neurologist",
    "Guillain-Barre syndrome":              "Neurologist",
    "Chagas disease":                       "Neurologist",

    # Gastroenterology
    "Appendicitis":                         "Gastroenterologist",
    "Cholecystitis":                        "Gastroenterologist",
    "Pancreatitis":                         "Gastroenterologist",
    "Gastroenteritis":                      "Gastroenterologist",
    "Bowel obstruction":                    "Gastroenterologist",
    "Hepatitis A":                          "Gastroenterologist",
    "Hepatitis B":                          "Gastroenterologist",
    "Hepatitis C":                          "Gastroenterologist",
    "Hepatitis E":                          "Gastroenterologist",
    "Viral pharyngitis":                    "General Physician",
    "Scombroid food poisoning":             "Gastroenterologist",
    "Boerhaave syndrome":                   "Gastroenterologist",

    # Urology / Nephrology
    "Urinary tract infection":              "Urologist",
    "Pyelonephritis":                       "Urologist",
    "Nephrolithiasis":                      "Urologist",

    # Dermatology
    "Allergic sinusitis":                   "Dermatologist",
    "Anaphylaxis":                          "Dermatologist",
    "Urticaria":                            "Dermatologist",
    "SLE":                                  "Dermatologist",

    # Orthopedics / Rheumatology
    "Localized edema":                      "Orthopedist",
    "Sarcoidosis":                          "General Physician",
    "Anemia":                               "General Physician",
    "HIV (initial infection)":              "General Physician",
    "Influenza":                            "General Physician",
    "Larygospasm":                          "General Physician",
    "Panic attack":                         "Psychiatrist",
    "GERD":                                 "Gastroenterologist",
    "Inguinal hernia":                      "Gastroenterologist",
    "Acute dystonic reactions":             "Neurologist",
    "Epiglottitis":                         "General Physician",
    "Whooping cough":                       "Pulmonologist",
    "Croup":                                "General Physician",
    "PSVT":                                 "Cardiologist",
}

# ── Step 2: PATHOLOGY → Severity (1-10) ──────────────────────
PATHOLOGY_TO_SEVERITY = {
    # Immediate emergencies — 9-10
    "Acute MI":                             10,
    "Possible NSTEMI / STEMI":              10,
    "Pulmonary embolism":                   10,
    "Anaphylaxis":                          10,
    "Boerhaave syndrome":                   10,
    "Meningitis":                           9,
    "Bowel obstruction":                    9,
    "Spontaneous pneumothorax":             9,
    "Epiglottitis":                         9,
    "Larygospasm":                          9,

    # Urgent — 7-8
    "Unstable angina":                      8,
    "Appendicitis":                         8,
    "Cholecystitis":                        8,
    "Pancreatitis":                         8,
    "Pyelonephritis":                       8,
    "Myocarditis":                          8,
    "Pericarditis":                         7,
    "Pneumonia":                            7,
    "Guillain-Barre syndrome":              8,
    "Acute COPD exacerbation / infection":  7,
    "Bronchospasm / acute asthma exacerbation": 7,
    "Hepatitis A":                          7,
    "Hepatitis B":                          7,
    "Hepatitis C":                          7,
    "Hepatitis E":                          7,
    "Nephrolithiasis":                      7,
    "Chagas disease":                       7,
    "SLE":                                  7,
    "Tuberculosis":                         7,
    "HIV (initial infection)":              7,
    "Inguinal hernia":                      7,
    "Acute dystonic reactions":             7,
    "Whooping cough":                       7,
    "Croup":                                7,

    # Moderate — 5-6
    "Stable angina":                        6,
    "Pleurisy":                             6,
    "Urinary tract infection":              5,
    "Gastroenteritis":                      5,
    "Cluster headache":                     6,
    "Migraine":                             6,
    "Bronchitis":                           5,
    "Atrial fibrillation":                  6,
    "SVT":                                  6,
    "PSVT":                                 6,
    "Sarcoidosis":                          6,
    "Anemia":                               5,
    "Scombroid food poisoning":             5,
    "Localized edema":                      5,
    "Pulmonary neoplasm":                   7,
    "GERD":                                 4,
    "Panic attack":                         5,
    "Urticaria":                            4,
    "Allergic sinusitis":                   4,

    # Mild — 2-4
    "Tension headache":                     3,
    "Viral pharyngitis":                    3,
    "Influenza":                            4,
}

# ── Step 3: PATHOLOGY → Urgency ──────────────────────────────
def severity_to_urgency(severity: int) -> str:
    if severity >= 9:   return "immediate"
    elif severity >= 7: return "within_24_hours"
    elif severity >= 5: return "within_a_week"
    else:               return "routine"

# ── Step 4: Decode DDXPlus evidence codes → plain text ───────
def load_evidence_mapping(release_evidences_path: str) -> dict:
    """
    Load release_evidences.json from DDXPlus.
    Returns dict: evidence_code -> plain text description
    """
    with open(release_evidences_path, "r") as f:
        evidences = json.load(f)

    mapping = {}
    for code, info in evidences.items():
        name = info.get("question_en", info.get("name", code))
        # Clean up the question text to symptom description
        name = name.replace("Do you have ", "").replace("Are you ", "")
        name = name.replace("Have you ", "").replace("?", "").strip().lower()
        mapping[code] = name

        # Handle value-coded evidences like E_45_@_2
        if "possible-values" in info:
            for val in info["possible-values"]:
                val_code = f"{code}_@_{val}"
                val_name = info["possible-values"][val] if isinstance(info["possible-values"], dict) else str(val)
                mapping[val_code] = f"{name} ({val_name})"

    return mapping

def decode_evidences(evidence_list: list, mapping: dict) -> str:
    """Convert list of evidence codes to plain English symptom text"""
    symptoms = []
    for code in evidence_list:
        text = mapping.get(code, code.replace("_@_", " level ").replace("_", " ").lower())
        symptoms.append(text)
    return ", ".join(symptoms) if symptoms else ""

# ── Step 5: Age + sex context ────────────────────────────────
def build_symptom_text(evidences_decoded: str, age: int, sex: str) -> str:
    """Add age/sex context to symptom text for richer BioBERT input"""
    sex_str = "male" if str(sex).upper() in ["M", "MALE", "1"] else "female"
    return f"{age} year old {sex_str} patient with: {evidences_decoded}"

# ── Step 6: Severity adjustment for age ──────────────────────
def adjust_severity_for_age(base_severity: int, age: int) -> int:
    if age >= 65 or age <= 5:
        return min(base_severity + 1, 10)
    return base_severity

# ── Main preprocessing function ──────────────────────────────
def preprocess_ddxplus(
    train_csv: str,
    release_evidences_json: str,
    output_csv: str = "biobert_training_data.csv",
    max_rows: int = None
):
    print("Loading DDXPlus dataset...")
    df = pd.read_csv(train_csv)
    if max_rows:
        df = df.head(max_rows)
    print(f"  Rows loaded: {len(df)}")
    print(f"  Columns: {list(df.columns)}")

    # Load evidence mapping
    print("\nLoading evidence mapping...")
    if os.path.exists(release_evidences_json):
        evidence_map = load_evidence_mapping(release_evidences_json)
        print(f"  Loaded {len(evidence_map)} evidence codes")
    else:
        print(f"  WARNING: {release_evidences_json} not found — using raw codes")
        evidence_map = {}

    records = []
    skipped = 0

    for idx, row in df.iterrows():
        pathology = row.get("PATHOLOGY", "")
        if not pathology or pathology not in PATHOLOGY_TO_SPECIALIST:
            skipped += 1
            continue

        # Decode EVIDENCES column — stored as Python list string
        try:
            raw_evidences = row.get("EVIDENCES", "[]")
            if isinstance(raw_evidences, str):
                evidence_list = json.loads(raw_evidences.replace("'", '"'))
            else:
                evidence_list = list(raw_evidences)
        except Exception:
            skipped += 1
            continue

        if not evidence_list:
            skipped += 1
            continue

        age = int(row.get("AGE", 40))
        sex = str(row.get("SEX", "M"))

        # Decode evidence codes to plain text
        evidences_decoded = decode_evidences(evidence_list, evidence_map)
        symptom_text      = build_symptom_text(evidences_decoded, age, sex)

        # Get labels
        specialist = PATHOLOGY_TO_SPECIALIST[pathology]
        base_sev   = PATHOLOGY_TO_SEVERITY.get(pathology, 5)
        severity   = adjust_severity_for_age(base_sev, age)
        urgency    = severity_to_urgency(severity)

        records.append({
            "symptom_text":   symptom_text,
            "age":            age,
            "sex":            sex,
            "pathology":      pathology,
            "specialist":     specialist,
            "severity_score": severity,
            "urgency":        urgency,
        })

        if idx % 10000 == 0:
            print(f"  Processed {idx}/{len(df)} rows...")

    print(f"\nDone. Records: {len(records)}, Skipped: {skipped}")

    out_df = pd.DataFrame(records)

    # Print distribution
    print("\nSpecialist distribution:")
    print(out_df["specialist"].value_counts().to_string())
    print("\nUrgency distribution:")
    print(out_df["urgency"].value_counts().to_string())
    print("\nSeverity distribution:")
    print(out_df["severity_score"].value_counts().sort_index().to_string())

    out_df.to_csv(output_csv, index=False)
    print(f"\nSaved to {output_csv}")
    return out_df


def build_encoders(df: pd.DataFrame):
    """Build and save LabelEncoders matching your existing pkl format"""
    urgency_encoder    = LabelEncoder()
    specialist_encoder = LabelEncoder()

    df["urgency_encoded"]    = urgency_encoder.fit_transform(df["urgency"])
    df["specialist_encoded"] = specialist_encoder.fit_transform(df["specialist"])

    print(f"\nUrgency classes    : {list(urgency_encoder.classes_)}")
    print(f"Specialist classes : {list(specialist_encoder.classes_)}")

    with open("urgency_encoder.pkl",    "wb") as f: pickle.dump(urgency_encoder,    f)
    with open("specialist_encoder.pkl", "wb") as f: pickle.dump(specialist_encoder, f)
    print("\nSaved urgency_encoder.pkl and specialist_encoder.pkl")
    print("Replace the ones in ml_models/models/ with these after training.")

    return df, urgency_encoder, specialist_encoder


def split_and_verify(df: pd.DataFrame):
    """Split and print final stats"""
    train_df, val_df = train_test_split(df, test_size=0.2, random_state=42, stratify=df["specialist"])
    print(f"\nTrain: {len(train_df)}, Val: {len(val_df)}")

    # Verify no specialist is missing from val
    missing = set(train_df["specialist"]) - set(val_df["specialist"])
    if missing:
        print(f"WARNING: These specialists missing from val set: {missing}")
    else:
        print("All specialist classes present in both train and val sets.")

    train_df.to_csv("train_data.csv", index=False)
    val_df.to_csv("val_data.csv",     index=False)
    print("Saved train_data.csv and val_data.csv")
    return train_df, val_df


# ── Run ───────────────────────────────────────────────────────
if __name__ == "__main__":
    # These files come from DDXPlus zip
    TRAIN_CSV              = "train.csv"           # DDXPlus train split
    RELEASE_EVIDENCES_JSON = "release_evidences.json"  # DDXPlus evidence codebook

    if not os.path.exists(TRAIN_CSV):
        print("ERROR: train.csv not found.")
        print("Download DDXPlus first:")
        print("  !wget -q 'https://figshare.com/ndownloader/files/35945800' -O train.zip")
        print("  !unzip -q train.zip")
        exit(1)

    df = preprocess_ddxplus(TRAIN_CSV, RELEASE_EVIDENCES_JSON)
    df, urgency_enc, specialist_enc = build_encoders(df)
    train_df, val_df = split_and_verify(df)

    print("\nPreprocessing complete.")
    print("Next step: run train_biobert_ddxplus.py in Colab with GPU.")
