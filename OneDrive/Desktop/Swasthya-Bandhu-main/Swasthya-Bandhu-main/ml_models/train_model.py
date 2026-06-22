"""
Training Script for Medical AI Model
"""

import pandas as pd
import numpy as np
from medical_ai_model import HybridMedicalAI, MedicalQuestionGenerator
from data_collection import MedicalDataCollector
import os
import sys

def main():
    print("🏥 Medical AI Model Training Pipeline")
    print("=" * 50)
    
    # Step 1: Data Collection
    print("\n📊 Step 1: Data Collection")
    collector = MedicalDataCollector()
    
    # Create directories
    os.makedirs('data', exist_ok=True)
    os.makedirs('models', exist_ok=True)
    
    # Check if data exists, if not collect it
    if not os.path.exists('data/processed_training_data.csv'):
        print("No existing data found. Collecting data...")
        collector.collect_public_datasets()
        collector.create_synthetic_medical_data()
        df = collector.prepare_training_data()
    else:
        print("Loading existing training data...")
        df = pd.read_csv('data/processed_training_data.csv')
    
    if df is None or len(df) == 0:
        print("❌ No training data available. Exiting.")
        return
    
    print(f"✅ Training data loaded: {len(df)} samples")
    print(f"Columns: {list(df.columns)}")
    
    # Step 2: Model Training
    print("\n🤖 Step 2: Model Training")
    
    # Initialize model
    model = HybridMedicalAI()
    
    # Train the model
    try:
        model.train(df)
        print("✅ Model training completed successfully!")
    except Exception as e:
        print(f"❌ Training failed: {e}")
        return
    
    # Step 3: Model Testing
    print("\n🧪 Step 3: Model Testing")
    
    test_cases = [
        "I have severe chest pain and difficulty breathing",
        "Fever and abdominal pain for 5 days",
        "Mild headache and feeling tired",
        "Severe stomach pain with vomiting",
        "Cough and fever for 3 days"
    ]
    
    print("Testing model predictions:")
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. Test: '{test_case}'")
        try:
            result = model.predict(test_case)
            print(f"   Condition: {result.get('differential_diagnoses', ['Unknown'])[0]}")
            print(f"   Severity: {result['severity_score']}/10")
            print(f"   Urgency: {result['urgency']}")
            print(f"   Specialist: {result['recommended_specialist']}")
            print(f"   Confidence: {result.get('confidence', 0):.2f}")
        except Exception as e:
            print(f"   ❌ Prediction failed: {e}")
    
    # Step 4: Question Generator Testing
    print("\n❓ Step 4: Question Generator Testing")
    
    question_gen = MedicalQuestionGenerator()
    
    for test_case in test_cases[:2]:  # Test first 2 cases
        print(f"\nGenerating questions for: '{test_case}'")
        questions = question_gen.generate_questions(test_case)
        
        for q in questions['questions'][:2]:  # Show first 2 questions
            print(f"  - {q['question']} ({q['type']})")
    
    print("\n✅ Training pipeline completed successfully!")
    print("\n📋 Next Steps:")
    print("1. Review model performance on test cases")
    print("2. Adjust training data if needed")
    print("3. Integrate with your FastAPI backend")
    print("4. Test with real user inputs")

if __name__ == "__main__":
    main()