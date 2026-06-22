"""
Data Preprocessing for Medical AI Training
Converts raw medical datasets into training format
"""

import pandas as pd
import json
import numpy as np
from typing import List, Dict

# Specialist mapping based on medical conditions
SPECIALIST_MAPPING = {
    # Cardiovascular
    'Myocardial Infarction': 'Cardiologist',
    'Angina': 'Cardiologist',
    'Heart Failure': 'Cardiologist',
    'Arrhythmia': 'Cardiologist',
    
    # Gastrointestinal
    'Typhoid': 'Gastroenterologist',
    'Appendicitis': 'Gastroenterologist',
    'Cholecystitis': 'Gastroenterologist',
    'Pancreatitis': 'Gastroenterologist',
    'IBD': 'Gastroenterologist',
    'Gastroenteritis': 'General Physician',
    
    # Respiratory
    'Pneumonia': 'Pulmonologist',
    'Asthma': 'Pulmonologist',
    'COPD': 'Pulmonologist',
    'Bronchitis': 'Pulmonologist',
    
    # Neurological
    'Stroke': 'Neurologist',
    'Migraine': 'Neurologist',
    'Seizure': 'Neurologist',
    'Meningitis': 'Neurologist',
    
    # Infectious
    'Malaria': 'Infectious Disease',
    'Tuberculosis': 'Infectious Disease',
    'Sepsis': 'Emergency Medicine',
    
    # Others
    'Diabetes': 'Endocrinologist',
    'Hypertension': 'Cardiologist',
    'Arthritis': 'Rheumatologist',
}

# Test recommendations by condition
TEST_MAPPING = {
    'Typhoid': ['Complete Blood Count', 'Blood culture', 'Widal test', 'Stool culture', 'Liver function tests'],
    'Appendicitis': ['Complete Blood Count', 'Abdominal ultrasound', 'CT scan abdomen', 'Urinalysis', 'CRP'],
    'Myocardial Infarction': ['ECG', 'Cardiac enzymes (Troponin)', 'Chest X-ray', 'Echocardiogram', 'Lipid profile'],
    'Pneumonia': ['Chest X-ray', 'Complete Blood Count', 'Sputum culture', 'Blood culture', 'Oxygen saturation'],
    'Stroke': ['CT scan brain', 'MRI brain', 'ECG', 'Carotid ultrasound', 'Blood glucose'],
    'Cholecystitis': ['Abdominal ultrasound', 'Complete Blood Count', 'Liver function tests', 'Lipase', 'CT scan'],
    'Pancreatitis': ['Serum amylase', 'Serum lipase', 'Complete Blood Count', 'Abdominal CT', 'Liver function tests'],
}

# Risk factors by condition
RISK_FACTORS_MAPPING = {
    'Typhoid': ['Recent travel to endemic areas', 'Contaminated food/water exposure', 'Prolonged fever', 'Dehydration risk'],
    'Appendicitis': ['Acute abdominal pain', 'Risk of perforation', 'Peritonitis risk', 'Requires urgent evaluation'],
    'Myocardial Infarction': ['Chest pain radiating to arm', 'Cardiovascular emergency', 'Age >50 years', 'Smoking history', 'Diabetes/hypertension'],
}

def calculate_severity(row: pd.Series) -> int:
    """Calculate severity score 1-10 based on symptoms"""
    severity = 5  # Default
    
    # Emergency conditions
    if row.get('PATHOLOGY') in ['Myocardial Infarction', 'Stroke', 'Sepsis', 'Pulmonary Embolism']:
        severity = 9
    elif row.get('PATHOLOGY') in ['Appendicitis', 'Cholecystitis', 'Pancreatitis', 'Pneumonia']:
        severity = 7
    elif row.get('PATHOLOGY') in ['Typhoid', 'Meningitis', 'Pyelonephritis']:
        severity = 7
    elif row.get('PATHOLOGY') in ['Gastroenteritis', 'Bronchitis', 'UTI']:
        severity = 5
    elif row.get('PATHOLOGY') in ['Migraine', 'Common Cold', 'Allergic Rhinitis']:
        severity = 3
    
    # Adjust for age
    age = row.get('AGE', 40)
    if age > 65:
        severity = min(severity + 1, 10)
    elif age < 5:
        severity = min(severity + 1, 10)
    
    return severity

def map_urgency(row: pd.Series) -> str:
    """Map condition to urgency level"""
    severity = calculate_severity(row)
    
    if severity >= 9:
        return 'immediate'
    elif severity >= 7:
        return 'within 24 hours'
    elif severity >= 5:
        return 'within a week'
    else:
        return 'routine'

def preprocess_ddxplus(csv_path: str, output_path: str):
    """Preprocess DDXPlus dataset"""
    print("Loading DDXPlus dataset...")
    df = pd.read_csv(csv_path)
    
    training_data = []
    
    for idx, row in df.iterrows():
        # Extract active symptoms
        symptoms = []
        for col in df.columns:
            if col.startswith('SYMPTOM_') and row[col] == 1:
                symptom_name = col.replace('SYMPTOM_', '').replace('_', ' ').lower()
                symptoms.append(symptom_name)
        
        if not symptoms:
            continue
        
        symptom_text = ', '.join(symptoms)
        pathology = row['PATHOLOGY']
        
        # Get mappings
        specialist = SPECIALIST_MAPPING.get(pathology, 'General Physician')
        tests = TEST_MAPPING.get(pathology, ['Complete Blood Count', 'Basic clinical examination'])
        risk_factors = RISK_FACTORS_MAPPING.get(pathology, ['Requires medical evaluation'])
        
        training_data.append({
            'symptom_text': symptom_text,
            'age': row.get('AGE', 40),
            'gender': row.get('SEX', 'M'),
            'diagnosis': pathology,
            'severity_score': calculate_severity(row),
            'urgency': map_urgency(row),
            'specialist': specialist,
            'tests': json.dumps(tests),
            'risk_factors': json.dumps(risk_factors),
            'differential_diagnoses': json.dumps([pathology])  # Can add similar conditions
        })
        
        if idx % 1000 == 0:
            print(f"Processed {idx} rows...")
    
    # Save
    output_df = pd.DataFrame(training_data)
    output_df.to_csv(output_path, index=False)
    print(f"Saved {len(training_data)} training samples to {output_path}")
    
    return output_df

def create_label_encodings(df: pd.DataFrame):
    """Create label encodings for categorical variables"""
    
    # Urgency encoding
    urgency_map = {
        'routine': 0,
        'within a week': 1,
        'within 24 hours': 2,
        'immediate': 3
    }
    
    # Specialist encoding
    specialists = df['specialist'].unique().tolist()
    specialist_map = {s: i for i, s in enumerate(specialists)}
    
    # Diagnosis encoding
    diagnoses = df['diagnosis'].unique().tolist()
    diagnosis_map = {d: i for i, d in enumerate(diagnoses)}
    
    # Save mappings
    mappings = {
        'urgency_map': urgency_map,
        'specialist_map': specialist_map,
        'diagnosis_map': diagnosis_map,
        'num_specialists': len(specialists),
        'num_diagnoses': len(diagnoses)
    }
    
    with open('label_mappings.json', 'w') as f:
        json.dump(mappings, f, indent=2)
    
    print(f"Created mappings: {len(specialists)} specialists, {len(diagnoses)} diagnoses")
    return mappings

def preprocess_meddialog(json_path: str, output_path: str):
    """Preprocess MedDialog for question generation"""
    print("Loading MedDialog dataset...")
    
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    question_data = []
    
    for conversation in data:
        if len(conversation) < 2:
            continue
        
        # First message is patient symptom
        patient_msg = conversation[0]['content']
        
        # Extract doctor's questions
        doctor_questions = []
        for msg in conversation[1:]:
            if msg['role'] == 'doctor' and '?' in msg['content']:
                questions = [q.strip() + '?' for q in msg['content'].split('?') if q.strip()]
                doctor_questions.extend(questions[:3])  # Max 3 questions
        
        if doctor_questions:
            question_data.append({
                'initial_symptom': patient_msg,
                'questions': json.dumps(doctor_questions),
                'num_questions': len(doctor_questions)
            })
    
    output_df = pd.DataFrame(question_data)
    output_df.to_csv(output_path, index=False)
    print(f"Saved {len(question_data)} question samples to {output_path}")
    
    return output_df

if __name__ == "__main__":
    # Example usage
    print("Medical Data Preprocessing")
    print("=" * 50)
    
    # Preprocess DDXPlus
    # df = preprocess_ddxplus('ddxplus.csv', 'processed_training_data.csv')
    # mappings = create_label_encodings(df)
    
    print("\nTo use:")
    print("1. Download DDXPlus: wget https://figshare.com/ndownloader/files/35945800 -O ddxplus.csv")
    print("2. Run: python data_preprocessing.py")
    print("3. Output: processed_training_data.csv with all features")
