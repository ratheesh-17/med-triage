"""
Medical AI Model Architecture
Combines BERT-based text understanding with traditional ML for medical diagnosis
"""

import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModel, AutoConfig
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import json
import os

class MedicalBERTModel(nn.Module):
    """
    BERT-based model for medical text understanding
    """
    def __init__(self, model_name='distilbert-base-uncased', num_conditions=50, num_specialists=20):
        super(MedicalBERTModel, self).__init__()
        
        self.bert = AutoModel.from_pretrained(model_name)
        self.dropout = nn.Dropout(0.3)
        
        # Multiple heads for different predictions
        self.condition_classifier = nn.Linear(self.bert.config.hidden_size, num_conditions)
        self.severity_regressor = nn.Linear(self.bert.config.hidden_size, 1)
        self.specialist_classifier = nn.Linear(self.bert.config.hidden_size, num_specialists)
        self.urgency_classifier = nn.Linear(self.bert.config.hidden_size, 4)  # immediate, 24h, week, routine
        
    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        pooled_output = outputs.pooler_output
        pooled_output = self.dropout(pooled_output)
        
        condition_logits = self.condition_classifier(pooled_output)
        severity_score = torch.sigmoid(self.severity_regressor(pooled_output)) * 10  # Scale to 1-10
        specialist_logits = self.specialist_classifier(pooled_output)
        urgency_logits = self.urgency_classifier(pooled_output)
        
        return {
            'condition_logits': condition_logits,
            'severity_score': severity_score,
            'specialist_logits': specialist_logits,
            'urgency_logits': urgency_logits
        }

class HybridMedicalAI:
    """
    Hybrid model combining BERT with traditional ML for robust medical AI
    """
    def __init__(self, model_name='distilbert-base-uncased'):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.bert_model = None
        self.rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.tfidf = TfidfVectorizer(max_features=5000, stop_words='english')
        
        # Label encoders
        self.condition_encoder = LabelEncoder()
        self.specialist_encoder = LabelEncoder()
        self.urgency_encoder = LabelEncoder()
        
        # Medical knowledge base
        self.medical_kb = self._load_medical_knowledge()
        
    def _load_medical_knowledge(self):
        """
        Load medical knowledge base for rule-based fallbacks
        """
        return {
            'emergency_keywords': [
                'chest pain', 'difficulty breathing', 'severe headache', 'unconscious',
                'bleeding heavily', 'severe abdominal pain', 'stroke symptoms',
                'heart attack', 'seizure', 'severe allergic reaction'
            ],
            'symptom_specialist_mapping': {
                'chest pain': 'Cardiologist',
                'heart': 'Cardiologist',
                'breathing': 'Pulmonologist',
                'cough': 'Pulmonologist',
                'headache': 'Neurologist',
                'seizure': 'Neurologist',
                'stomach': 'Gastroenterologist',
                'abdominal': 'Gastroenterologist',
                'joint': 'Orthopedic Surgeon',
                'skin': 'Dermatologist',
                'eye': 'Ophthalmologist',
                'ear': 'ENT Specialist'
            },
            'severity_indicators': {
                'severe': 8,
                'intense': 7,
                'moderate': 5,
                'mild': 3,
                'slight': 2
            }
        }
    
    def preprocess_text(self, text):
        """
        Preprocess medical text
        """
        text = text.lower().strip()
        # Add medical-specific preprocessing here
        return text
    
    def train(self, df):
        """
        Train the hybrid model
        """
        print("Training Hybrid Medical AI Model...")
        
        # Prepare data
        texts = df['symptom_text'].apply(self.preprocess_text).tolist()
        conditions = df['condition'].tolist()
        specialists = df['recommended_specialist'].tolist()
        severities = df['severity_score'].tolist()
        urgencies = df['urgency'].tolist()
        
        # Encode labels
        self.condition_encoder.fit(conditions)
        self.specialist_encoder.fit(specialists)
        self.urgency_encoder.fit(urgencies)
        
        # Train TF-IDF + Random Forest (fallback model)
        print("Training TF-IDF + Random Forest model...")
        tfidf_features = self.tfidf.fit_transform(texts)
        
        # Create combined target for RF (condition + specialist)
        combined_targets = [f"{cond}_{spec}" for cond, spec in zip(conditions, specialists)]
        self.rf_model.fit(tfidf_features, combined_targets)
        
        print("✓ Hybrid model training completed")
        
        # Save models
        self.save_models()
    
    def predict(self, symptom_text):
        """
        Make prediction using hybrid approach
        """
        processed_text = self.preprocess_text(symptom_text)
        
        # Check for emergency keywords first
        is_emergency = self._check_emergency(processed_text)
        if is_emergency:
            return self._emergency_response(processed_text)
        
        # Use TF-IDF + Random Forest for prediction
        tfidf_features = self.tfidf.transform([processed_text])
        rf_prediction = self.rf_model.predict(tfidf_features)[0]
        rf_proba = self.rf_model.predict_proba(tfidf_features)[0]
        
        # Parse RF prediction
        condition, specialist = rf_prediction.split('_', 1)
        confidence = max(rf_proba)
        
        # Determine severity using rule-based approach
        severity = self._calculate_severity(processed_text)
        
        # Determine urgency
        urgency = self._determine_urgency(severity, processed_text)
        
        # Generate additional medical information
        risk_factors = self._generate_risk_factors(processed_text, condition)
        tests = self._suggest_tests(condition, specialist)
        diagnoses = self._generate_differential_diagnoses(processed_text, condition)
        
        return {
            'severity_score': severity,
            'urgency': urgency,
            'risk_factors': risk_factors,
            'recommended_specialist': specialist,
            'suggested_tests': tests,
            'differential_diagnoses': diagnoses,
            'clinical_summary': f"Based on symptoms analysis, likely condition: {condition}. Recommend consultation with {specialist}.",
            'confidence': float(confidence)
        }
    
    def _check_emergency(self, text):
        """Check if symptoms indicate emergency"""
        return any(keyword in text for keyword in self.medical_kb['emergency_keywords'])
    
    def _emergency_response(self, text):
        """Generate emergency response"""
        return {
            'severity_score': 10,
            'urgency': 'immediate',
            'risk_factors': ['Emergency condition requiring immediate medical attention'],
            'recommended_specialist': 'Emergency Medicine',
            'suggested_tests': ['Immediate clinical assessment', 'Vital signs monitoring'],
            'differential_diagnoses': ['Medical emergency'],
            'clinical_summary': 'Emergency condition detected. Seek immediate medical attention.',
            'confidence': 1.0
        }
    
    def _calculate_severity(self, text):
        """Calculate severity score based on text analysis"""
        base_severity = 5
        
        # Check for severity indicators
        for indicator, score in self.medical_kb['severity_indicators'].items():
            if indicator in text:
                base_severity = max(base_severity, score)
        
        # Check for pain descriptors
        if 'severe pain' in text or 'intense pain' in text:
            base_severity = max(base_severity, 8)
        elif 'moderate pain' in text:
            base_severity = max(base_severity, 6)
        elif 'mild pain' in text:
            base_severity = max(base_severity, 4)
        
        # Check for duration indicators
        if 'weeks' in text or 'months' in text:
            base_severity = max(base_severity, 6)
        
        return min(base_severity, 10)
    
    def _determine_urgency(self, severity, text):
        """Determine urgency based on severity and symptoms"""
        if severity >= 8:
            return 'within 24 hours'
        elif severity >= 6:
            return 'within a week'
        elif severity >= 4:
            return 'within a week'
        else:
            return 'routine'
    
    def _generate_risk_factors(self, text, condition):
        """Generate relevant risk factors"""
        risk_factors = []
        
        if 'fever' in text:
            risk_factors.append('Possible infection')
        if 'chest' in text:
            risk_factors.append('Cardiovascular risk')
        if 'breathing' in text:
            risk_factors.append('Respiratory distress')
        if 'abdominal' in text or 'stomach' in text:
            risk_factors.append('Gastrointestinal involvement')
        
        if not risk_factors:
            risk_factors = ['General health monitoring recommended']
        
        return risk_factors
    
    def _suggest_tests(self, condition, specialist):
        """Suggest relevant medical tests"""
        test_mapping = {
            'Cardiologist': ['ECG', 'Cardiac enzymes', 'Chest X-ray', 'Echocardiogram'],
            'Pulmonologist': ['Chest X-ray', 'Spirometry', 'Oxygen saturation', 'CT chest'],
            'Gastroenterologist': ['Abdominal ultrasound', 'Blood tests', 'Stool analysis', 'CT abdomen'],
            'Neurologist': ['CT scan', 'MRI', 'Neurological examination', 'EEG'],
            'General Physician': ['Complete blood count', 'Basic metabolic panel', 'Urinalysis']
        }
        
        return test_mapping.get(specialist, ['Complete blood count', 'Basic examination'])
    
    def _generate_differential_diagnoses(self, text, primary_condition):
        """Generate differential diagnoses"""
        diagnoses = [primary_condition]
        
        # Add related conditions based on symptoms
        if 'fever' in text and 'abdominal' in text:
            diagnoses.extend(['Appendicitis', 'Gastroenteritis', 'Typhoid fever'])
        elif 'chest pain' in text:
            diagnoses.extend(['Angina', 'Myocardial infarction', 'Pulmonary embolism'])
        elif 'headache' in text:
            diagnoses.extend(['Migraine', 'Tension headache', 'Sinusitis'])
        
        return list(set(diagnoses))  # Remove duplicates
    
    def save_models(self):
        """Save trained models"""
        os.makedirs('models', exist_ok=True)
        
        # Save traditional ML components
        joblib.dump(self.rf_model, 'models/rf_model.pkl')
        joblib.dump(self.tfidf, 'models/tfidf_vectorizer.pkl')
        joblib.dump(self.condition_encoder, 'models/condition_encoder.pkl')
        joblib.dump(self.specialist_encoder, 'models/specialist_encoder.pkl')
        joblib.dump(self.urgency_encoder, 'models/urgency_encoder.pkl')
        
        # Save medical knowledge base
        with open('models/medical_kb.json', 'w') as f:
            json.dump(self.medical_kb, f)
        
        print("✓ Models saved successfully")
    
    def load_models(self):
        """Load trained models"""
        try:
            self.rf_model = joblib.load('models/rf_model.pkl')
            self.tfidf = joblib.load('models/tfidf_vectorizer.pkl')
            self.condition_encoder = joblib.load('models/condition_encoder.pkl')
            self.specialist_encoder = joblib.load('models/specialist_encoder.pkl')
            self.urgency_encoder = joblib.load('models/urgency_encoder.pkl')
            
            with open('models/medical_kb.json', 'r') as f:
                self.medical_kb = json.load(f)
            
            print("✓ Models loaded successfully")
            return True
        except Exception as e:
            print(f"✗ Error loading models: {e}")
            return False

# Question generation model
class MedicalQuestionGenerator:
    """
    Generate follow-up questions for medical triage
    """
    def __init__(self):
        self.question_templates = {
            'severity': {
                'question': 'On a scale of 1-10, how severe is your {symptom}?',
                'type': 'scale',
                'options': list(range(1, 11))
            },
            'duration': {
                'question': 'How long have you been experiencing {symptom}?',
                'type': 'choice',
                'options': ['Less than 24 hours', '1-3 days', '3-7 days', 'More than a week']
            },
            'progression': {
                'question': 'Are your symptoms getting better, worse, or staying the same?',
                'type': 'choice',
                'options': ['Getting better', 'Getting worse', 'Staying the same']
            },
            'associated_symptoms': {
                'question': 'Are you experiencing any other symptoms along with {symptom}?',
                'type': 'text'
            }
        }
    
    def generate_questions(self, symptom_text):
        """Generate relevant follow-up questions"""
        # Extract main symptom
        main_symptom = self._extract_main_symptom(symptom_text)
        
        questions = []
        for q_type, template in self.question_templates.items():
            question = {
                'id': q_type,
                'question': template['question'].format(symptom=main_symptom),
                'type': template['type']
            }
            if 'options' in template:
                question['options'] = template['options']
            questions.append(question)
        
        return {
            'questions': questions,
            'reasoning': f'These questions help assess the severity and nature of {main_symptom}'
        }
    
    def _extract_main_symptom(self, text):
        """Extract the main symptom from text"""
        common_symptoms = ['pain', 'fever', 'headache', 'nausea', 'cough', 'fatigue']
        text_lower = text.lower()
        
        for symptom in common_symptoms:
            if symptom in text_lower:
                return symptom
        
        return 'your symptoms'