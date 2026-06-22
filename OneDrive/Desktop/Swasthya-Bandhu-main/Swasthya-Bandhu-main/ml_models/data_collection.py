"""
Medical Dataset Collection and Preparation
This script helps collect and prepare medical datasets for training our custom model
"""

import pandas as pd
import requests
import json
import os
from typing import List, Dict
import numpy as np

class MedicalDataCollector:
    def __init__(self):
        self.data_sources = {
            'symptom_disease': [],
            'medical_qa': [],
            'clinical_notes': []
        }
    
    def collect_public_datasets(self):
        """
        Collect data from public medical datasets
        """
        datasets = {
            # Symptom-Disease datasets
            'symptom_disease_dataset': 'https://raw.githubusercontent.com/mmaisonnave/medical-symptom-disease-dataset/main/dataset.csv',
            
            # Medical QA datasets  
            'medical_qa': 'https://raw.githubusercontent.com/deepset-ai/haystack/main/tutorials/data/medical_qa.json',
            
            # Symptom checker data
            'symptom_checker': 'https://raw.githubusercontent.com/priyansh-anand/symptom-disease-prediction/main/Training.csv'
        }
        
        print("Downloading public medical datasets...")
        
        for name, url in datasets.items():
            try:
                print(f"Downloading {name}...")
                response = requests.get(url, timeout=30)
                
                if response.status_code == 200:
                    if name.endswith('.csv'):
                        df = pd.read_csv(url)
                        df.to_csv(f'data/{name}.csv', index=False)
                        print(f"✓ Saved {name}.csv ({len(df)} rows)")
                    else:
                        with open(f'data/{name}.json', 'w') as f:
                            json.dump(response.json(), f)
                        print(f"✓ Saved {name}.json")
                else:
                    print(f"✗ Failed to download {name}: {response.status_code}")
                    
            except Exception as e:
                print(f"✗ Error downloading {name}: {str(e)}")
    
    def create_synthetic_medical_data(self):
        """
        Create synthetic medical training data based on common patterns
        """
        
        # Common symptoms and their associated conditions
        symptom_patterns = {
            'fever_abdominal_pain': {
                'symptoms': ['fever', 'abdominal pain', 'nausea', 'vomiting'],
                'conditions': ['Appendicitis', 'Cholecystitis', 'Typhoid fever', 'Gastroenteritis'],
                'severity': [7, 8, 6, 5],
                'urgency': ['within 24 hours', 'within 24 hours', 'within a week', 'within a week'],
                'specialist': ['Gastroenterologist', 'Gastroenterologist', 'Infectious Disease', 'General Physician']
            },
            'chest_pain': {
                'symptoms': ['chest pain', 'shortness of breath', 'sweating', 'nausea'],
                'conditions': ['Myocardial Infarction', 'Angina', 'Pulmonary Embolism', 'Anxiety'],
                'severity': [9, 7, 8, 4],
                'urgency': ['immediate', 'within 24 hours', 'immediate', 'routine'],
                'specialist': ['Cardiologist', 'Cardiologist', 'Emergency Medicine', 'Psychiatrist']
            },
            'respiratory': {
                'symptoms': ['cough', 'fever', 'difficulty breathing', 'fatigue'],
                'conditions': ['Pneumonia', 'Bronchitis', 'Asthma', 'COVID-19'],
                'severity': [7, 5, 6, 6],
                'urgency': ['within 24 hours', 'within a week', 'within 24 hours', 'within 24 hours'],
                'specialist': ['Pulmonologist', 'General Physician', 'Pulmonologist', 'Infectious Disease']
            },
            'neurological': {
                'symptoms': ['headache', 'dizziness', 'nausea', 'vision changes'],
                'conditions': ['Migraine', 'Tension headache', 'Stroke', 'Brain tumor'],
                'severity': [5, 3, 9, 8],
                'urgency': ['routine', 'routine', 'immediate', 'within 24 hours'],
                'specialist': ['Neurologist', 'General Physician', 'Emergency Medicine', 'Neurologist']
            }
        }
        
        training_data = []
        
        for pattern_name, pattern_data in symptom_patterns.items():
            for i, condition in enumerate(pattern_data['conditions']):
                # Generate multiple variations for each condition
                for variation in range(5):
                    symptoms_text = f"I have {', '.join(pattern_data['symptoms'][:2+variation%3])}"
                    
                    training_data.append({
                        'symptom_text': symptoms_text,
                        'condition': condition,
                        'severity_score': pattern_data['severity'][i],
                        'urgency': pattern_data['urgency'][i],
                        'recommended_specialist': pattern_data['specialist'][i],
                        'pattern_category': pattern_name
                    })
        
        # Save synthetic data
        df = pd.DataFrame(training_data)
        df.to_csv('data/synthetic_medical_data.csv', index=False)
        print(f"✓ Created synthetic dataset with {len(df)} samples")
        
        return df
    
    def prepare_training_data(self):
        """
        Prepare and clean data for training
        """
        print("Preparing training data...")
        
        # Load all available datasets
        datasets = []
        
        # Load synthetic data
        if os.path.exists('data/synthetic_medical_data.csv'):
            synthetic_df = pd.read_csv('data/synthetic_medical_data.csv')
            datasets.append(synthetic_df)
            print(f"Loaded synthetic data: {len(synthetic_df)} samples")
        
        # Combine all datasets
        if datasets:
            combined_df = pd.concat(datasets, ignore_index=True)
            
            # Clean and preprocess
            combined_df = combined_df.dropna()
            combined_df['symptom_text'] = combined_df['symptom_text'].str.lower().str.strip()
            
            # Save processed data
            combined_df.to_csv('data/processed_training_data.csv', index=False)
            print(f"✓ Prepared training dataset: {len(combined_df)} samples")
            
            return combined_df
        else:
            print("No datasets found. Please run data collection first.")
            return None

if __name__ == "__main__":
    collector = MedicalDataCollector()
    
    # Create data directory
    os.makedirs('data', exist_ok=True)
    
    # Collect public datasets
    collector.collect_public_datasets()
    
    # Create synthetic data
    collector.create_synthetic_medical_data()
    
    # Prepare training data
    collector.prepare_training_data()
    
    print("\n✓ Data collection completed!")