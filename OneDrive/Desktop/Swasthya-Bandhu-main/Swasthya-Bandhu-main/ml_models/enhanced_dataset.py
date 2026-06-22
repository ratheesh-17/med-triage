"""
Enhanced Medical Dataset - More comprehensive training data
"""

import pandas as pd
import numpy as np

def create_enhanced_medical_dataset():
    """Create a more comprehensive medical training dataset"""
    
    # Expanded medical conditions with detailed symptom patterns
    medical_conditions = {
        # Cardiovascular
        'Myocardial Infarction': {
            'symptoms': ['chest pain', 'shortness of breath', 'sweating', 'nausea', 'left arm pain'],
            'severity': 9, 'urgency': 'immediate', 'specialist': 'Cardiologist'
        },
        'Angina': {
            'symptoms': ['chest pain', 'pressure', 'tightness', 'exertion'],
            'severity': 7, 'urgency': 'within 24 hours', 'specialist': 'Cardiologist'
        },
        
        # Gastrointestinal
        'Appendicitis': {
            'symptoms': ['abdominal pain', 'fever', 'nausea', 'vomiting', 'right lower quadrant pain'],
            'severity': 8, 'urgency': 'within 24 hours', 'specialist': 'Gastroenterologist'
        },
        'Typhoid Fever': {
            'symptoms': ['fever', 'abdominal pain', 'headache', 'weakness', 'rose spots'],
            'severity': 7, 'urgency': 'within 24 hours', 'specialist': 'Infectious Disease'
        },
        'Cholecystitis': {
            'symptoms': ['right upper abdominal pain', 'fever', 'nausea', 'jaundice'],
            'severity': 7, 'urgency': 'within 24 hours', 'specialist': 'Gastroenterologist'
        },
        
        # Respiratory
        'Pneumonia': {
            'symptoms': ['cough', 'fever', 'difficulty breathing', 'chest pain', 'fatigue'],
            'severity': 7, 'urgency': 'within 24 hours', 'specialist': 'Pulmonologist'
        },
        'Asthma Exacerbation': {
            'symptoms': ['wheezing', 'shortness of breath', 'chest tightness', 'cough'],
            'severity': 6, 'urgency': 'within 24 hours', 'specialist': 'Pulmonologist'
        },
        
        # Neurological
        'Stroke': {
            'symptoms': ['sudden weakness', 'facial drooping', 'speech difficulty', 'confusion'],
            'severity': 10, 'urgency': 'immediate', 'specialist': 'Emergency Medicine'
        },
        'Migraine': {
            'symptoms': ['severe headache', 'nausea', 'light sensitivity', 'visual aura'],
            'severity': 6, 'urgency': 'routine', 'specialist': 'Neurologist'
        },
        
        # Infectious Diseases
        'Malaria': {
            'symptoms': ['fever', 'chills', 'headache', 'muscle aches', 'fatigue'],
            'severity': 7, 'urgency': 'within 24 hours', 'specialist': 'Infectious Disease'
        },
        'Dengue Fever': {
            'symptoms': ['high fever', 'severe headache', 'muscle pain', 'rash', 'bleeding'],
            'severity': 8, 'urgency': 'within 24 hours', 'specialist': 'Infectious Disease'
        }
    }
    
    # Generate comprehensive training data
    training_data = []
    
    for condition, details in medical_conditions.items():
        # Generate multiple symptom combinations
        symptoms = details['symptoms']
        
        for i in range(10):  # 10 variations per condition
            # Random symptom combinations
            num_symptoms = np.random.randint(2, min(5, len(symptoms)))
            selected_symptoms = np.random.choice(symptoms, num_symptoms, replace=False)
            
            # Create symptom text variations
            symptom_texts = [
                f"I have {', '.join(selected_symptoms)}",
                f"I'm experiencing {' and '.join(selected_symptoms)}",
                f"I've been having {', '.join(selected_symptoms)} for days",
                f"Severe {selected_symptoms[0]} with {', '.join(selected_symptoms[1:])}",
                f"Patient presents with {', '.join(selected_symptoms)}"
            ]
            
            symptom_text = np.random.choice(symptom_texts)
            
            # Add severity variations
            base_severity = details['severity']
            severity_variation = np.random.randint(-1, 2)  # -1, 0, or 1
            final_severity = max(1, min(10, base_severity + severity_variation))
            
            training_data.append({
                'symptom_text': symptom_text,
                'condition': condition,
                'severity_score': final_severity,
                'urgency': details['urgency'],
                'recommended_specialist': details['specialist'],
                'primary_symptoms': ', '.join(selected_symptoms)
            })
    
    return pd.DataFrame(training_data)

# Create the enhanced dataset
if __name__ == "__main__":
    df = create_enhanced_medical_dataset()
    df.to_csv('data/enhanced_medical_dataset.csv', index=False)
    print(f"Created enhanced dataset with {len(df)} samples")
    print(f"Conditions covered: {df['condition'].nunique()}")
    print(f"Specialists: {df['recommended_specialist'].nunique()}")