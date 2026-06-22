"""
Extract Contextual Medical Questions from Conversation Datasets
Processes MedDialog/ChatDoctor to create question generation training data
"""

import json
import pandas as pd
import re
from typing import List, Dict

def extract_questions_from_text(text: str) -> List[str]:
    """Extract questions from doctor's response"""
    # Split by question marks
    potential_questions = text.split('?')
    
    questions = []
    for q in potential_questions:
        q = q.strip()
        if not q:
            continue
        
        # Take last sentence before ?
        sentences = q.split('.')
        question_text = sentences[-1].strip()
        
        # Filter out non-questions
        if len(question_text) < 10:  # Too short
            continue
        if not any(word in question_text.lower() for word in ['what', 'where', 'when', 'how', 'do', 'does', 'have', 'are', 'is', 'can', 'could', 'would']):
            continue
        
        questions.append(question_text + '?')
    
    return questions[:5]  # Max 5 questions

def classify_question_type(question: str) -> str:
    """Classify question type"""
    q_lower = question.lower()
    
    # Yes/No questions
    if any(q_lower.startswith(word) for word in ['do you', 'does', 'have you', 'are you', 'is', 'can you', 'did you']):
        return 'yes_no'
    
    # Choice questions
    if ' or ' in q_lower:
        return 'choice'
    
    # Scale questions
    if 'scale' in q_lower or '1-10' in q_lower or 'rate' in q_lower:
        return 'scale'
    
    # Text questions
    return 'text'

def extract_symptom_keywords(text: str) -> List[str]:
    """Extract key symptoms from patient message"""
    symptom_keywords = [
        'pain', 'fever', 'headache', 'cough', 'nausea', 'vomiting', 'diarrhea',
        'chest', 'abdominal', 'stomach', 'breathing', 'dizzy', 'fatigue',
        'bleeding', 'rash', 'swelling', 'numbness', 'weakness'
    ]
    
    text_lower = text.lower()
    found_symptoms = [s for s in symptom_keywords if s in text_lower]
    return found_symptoms

def process_meddialog(json_path: str, output_path: str):
    """Process MedDialog dataset for question generation"""
    print("Loading MedDialog conversations...")
    
    with open(json_path, 'r', encoding='utf-8') as f:
        conversations = json.load(f)
    
    training_data = []
    
    for conv_id, conv in enumerate(conversations):
        if len(conv) < 2:
            continue
        
        # Extract patient's initial message
        patient_msg = None
        doctor_msg = None
        
        for i, turn in enumerate(conv):
            if turn.get('role') == 'patient' or turn.get('speaker') == 'patient':
                patient_msg = turn.get('content', turn.get('text', ''))
                # Get next doctor response
                if i + 1 < len(conv):
                    next_turn = conv[i + 1]
                    if next_turn.get('role') == 'doctor' or next_turn.get('speaker') == 'doctor':
                        doctor_msg = next_turn.get('content', next_turn.get('text', ''))
                        break
        
        if not patient_msg or not doctor_msg:
            continue
        
        # Extract questions from doctor's message
        questions = extract_questions_from_text(doctor_msg)
        
        if not questions:
            continue
        
        # Extract symptoms
        symptoms = extract_symptom_keywords(patient_msg)
        
        # Create training sample
        training_data.append({
            'patient_symptom': patient_msg[:500],  # Limit length
            'symptom_keywords': ', '.join(symptoms),
            'doctor_questions': ' '.join(questions),
            'num_questions': len(questions),
            'question_types': ', '.join([classify_question_type(q) for q in questions]),
            'input_format': f"generate medical questions: {patient_msg[:200]}",
            'output_format': ' '.join(questions)
        })
        
        if conv_id % 1000 == 0:
            print(f"Processed {conv_id} conversations, found {len(training_data)} valid samples")
    
    # Save
    df = pd.DataFrame(training_data)
    df.to_csv(output_path, index=False)
    print(f"\n✅ Saved {len(training_data)} question generation samples to {output_path}")
    
    # Show statistics
    print(f"\nStatistics:")
    print(f"Average questions per sample: {df['num_questions'].mean():.2f}")
    print(f"Question type distribution:")
    all_types = []
    for types in df['question_types']:
        all_types.extend(types.split(', '))
    type_counts = pd.Series(all_types).value_counts()
    print(type_counts)
    
    return df

def create_symptom_specific_examples():
    """Create high-quality symptom-specific question examples"""
    examples = [
        {
            'patient_symptom': 'I have chest pain',
            'doctor_questions': 'Does the pain radiate to your left arm or jaw? Do you feel crushing pressure or sharp stabbing? Are you experiencing sweating or nausea? How long has this pain been present?',
            'symptom_keywords': 'chest, pain',
            'clinical_reasoning': 'Differentiating cardiac vs non-cardiac chest pain'
        },
        {
            'patient_symptom': 'fever for 7 days and abdominal pain',
            'doctor_questions': 'Where exactly is the abdominal pain located? Have you had any vomiting or diarrhea? Have you traveled outside your city recently? Does the pain worsen when you press and release your abdomen? How high is your fever?',
            'symptom_keywords': 'fever, abdominal, pain',
            'clinical_reasoning': 'Differentiating typhoid, appendicitis, and gastroenteritis'
        },
        {
            'patient_symptom': 'severe headache',
            'doctor_questions': 'Is this the worst headache of your life? Do you have neck stiffness? Are you sensitive to light? Did the headache come on suddenly or gradually? Do you have any vision changes?',
            'symptom_keywords': 'headache',
            'clinical_reasoning': 'Ruling out subarachnoid hemorrhage and meningitis'
        },
        {
            'patient_symptom': 'difficulty breathing and cough',
            'doctor_questions': 'Can you speak in full sentences? Is your cough producing mucus or blood? Do you have chest pain when breathing? Do you have a history of asthma? Have you had fever?',
            'symptom_keywords': 'breathing, cough',
            'clinical_reasoning': 'Assessing respiratory distress and infection'
        },
        {
            'patient_symptom': 'dizziness and weakness',
            'doctor_questions': 'Does the room spin around you or do you feel lightheaded? Do you have any chest pain or palpitations? Have you had any recent falls? Are you taking any blood pressure medications? Have you eaten today?',
            'symptom_keywords': 'dizziness, weakness',
            'clinical_reasoning': 'Differentiating vertigo, cardiac causes, and hypoglycemia'
        }
    ]
    
    df = pd.DataFrame(examples)
    df['input_format'] = df['patient_symptom'].apply(lambda x: f"generate medical questions: {x}")
    df['output_format'] = df['doctor_questions']
    
    df.to_csv('symptom_specific_questions.csv', index=False)
    print("✅ Created symptom-specific question examples")
    return df

if __name__ == "__main__":
    print("Medical Conversational Question Extraction")
    print("=" * 60)
    
    # Create high-quality examples first
    print("\n1. Creating symptom-specific examples...")
    examples_df = create_symptom_specific_examples()
    print(f"Created {len(examples_df)} examples")
    
    # Process MedDialog if available
    print("\n2. To process MedDialog:")
    print("   - Download: git clone https://github.com/UCSD-AI4H/Medical-Dialogue-System")
    print("   - Run: process_meddialog('meddialog.json', 'question_training_data.csv')")
    
    print("\n3. Training format:")
    print("   Input:  'generate medical questions: fever and abdominal pain'")
    print("   Output: 'Where is the pain? Have you vomited? Have you traveled?'")
    
    print("\n4. Use this data to fine-tune T5 or GPT-2 for contextual question generation")
