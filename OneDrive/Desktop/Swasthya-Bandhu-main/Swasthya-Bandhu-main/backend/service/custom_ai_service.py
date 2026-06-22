"""
Custom AI Service - Replacement for Gemini API
This service provides the same functionality as Gemini but using our custom trained model
"""

import os
import sys
import json
from typing import Dict, List, Optional

# Add ml_models to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ml_models'))

try:
    from medical_ai_model import HybridMedicalAI, MedicalQuestionGenerator
    CUSTOM_MODEL_AVAILABLE = True
except ImportError:
    CUSTOM_MODEL_AVAILABLE = False
    print("Warning: Custom medical AI model not available. Using fallback.")

class CustomMedicalAI:
    """
    Custom Medical AI Service to replace Gemini API
    """
    def __init__(self):
        self.model = None
        self.question_generator = None
        self.initialized = False
        
        if CUSTOM_MODEL_AVAILABLE:
            try:
                self.model = HybridMedicalAI()
                self.question_generator = MedicalQuestionGenerator()
                
                # Try to load pre-trained models
                models_path = os.path.join(os.path.dirname(__file__), '..', 'ml_models', 'models')
                if os.path.exists(os.path.join(models_path, 'rf_model.pkl')):
                    if self.model.load_models():
                        self.initialized = True
                        print("✅ Custom Medical AI initialized successfully")
                    else:
                        print("⚠️ Failed to load pre-trained models. Using untrained model.")
                else:
                    print("⚠️ No pre-trained models found. Please run training first.")
                    
            except Exception as e:
                print(f"❌ Failed to initialize custom model: {e}")
                CUSTOM_MODEL_AVAILABLE = False

# Initialize the custom model
custom_ai = CustomMedicalAI()

def generate_followup_questions(symptom_text: str) -> Dict:
    """
    Generate follow-up questions using custom model
    Replacement for Gemini's question generation
    """
    try:
        if custom_ai.initialized and custom_ai.question_generator:
            return custom_ai.question_generator.generate_questions(symptom_text)
        else:
            # Fallback question generation
            return _fallback_question_generation(symptom_text)
            
    except Exception as e:
        print(f"Custom question generation failed: {e}")
        return _fallback_question_generation(symptom_text)

def get_ai_clinical_assessment(symptom_text: str, answers: dict = None, chat_history: list = None) -> Dict:
    """
    Get clinical assessment using custom model
    Replacement for Gemini's clinical assessment
    """
    try:
        if custom_ai.initialized and custom_ai.model:
            # Use custom model for prediction
            result = custom_ai.model.predict(symptom_text)
            
            # Enhance with answers if provided
            if answers:
                result = _enhance_with_answers(result, answers)
            
            return result
        else:
            # Use enhanced fallback
            return _enhanced_fallback_assessment(symptom_text, answers)
            
    except Exception as e:
        print(f"Custom clinical assessment failed: {e}")
        return _enhanced_fallback_assessment(symptom_text, answers)

def get_longitudinal_risk_assessment(sessions: list) -> Optional[Dict]:
    """
    Analyze patient sessions for risk assessment
    Replacement for Gemini's longitudinal analysis
    """
    if not sessions or len(sessions) < 2:
        return None
    
    try:
        # Calculate risk based on session patterns
        severities = [s.get('severity_score', 5) for s in sessions]
        avg_severity = sum(severities) / len(severities)
        trend = _calculate_trend(severities)
        
        # Risk assessment based on patterns
        cardiac_risk = min(10, avg_severity * 0.8)
        metabolic_risk = min(10, avg_severity * 0.7)
        neurological_risk = min(10, avg_severity * 0.6)
        respiratory_risk = min(10, avg_severity * 0.7)
        
        # Adjust based on symptoms
        for session in sessions[-3:]:  # Last 3 sessions
            symptoms = session.get('symptom_input', '').lower()
            if 'chest' in symptoms or 'heart' in symptoms:
                cardiac_risk = min(10, cardiac_risk + 1)
            if 'breathing' in symptoms or 'cough' in symptoms:
                respiratory_risk = min(10, respiratory_risk + 1)
            if 'headache' in symptoms or 'dizzy' in symptoms:
                neurological_risk = min(10, neurological_risk + 1)
        
        return {
            "cardiac_risk": round(cardiac_risk, 1),
            "metabolic_risk": round(metabolic_risk, 1),
            "neurological_risk": round(neurological_risk, 1),
            "respiratory_risk": round(respiratory_risk, 1),
            "trend_direction": trend,
            "summary": f"Risk assessment based on {len(sessions)} sessions. Average severity: {avg_severity:.1f}"
        }
        
    except Exception as e:
        print(f"Risk assessment failed: {e}")
        return None

def _fallback_question_generation(symptom_text: str) -> Dict:
    """
    Fallback question generation when custom model is not available
    """
    symptom_lower = symptom_text.lower()
    
    # Base questions
    questions = [
        {
            "id": "severity",
            "question": "On a scale of 1-10, how severe are your symptoms?",
            "type": "scale"
        },
        {
            "id": "duration",
            "question": "How long have you had these symptoms?",
            "type": "choice",
            "options": ["Less than 24 hours", "1-3 days", "3-7 days", "More than a week"]
        }
    ]
    
    # Add specific questions based on symptoms
    if 'pain' in symptom_lower:
        questions.append({
            "id": "pain_type",
            "question": "How would you describe the pain?",
            "type": "choice",
            "options": ["Sharp", "Dull", "Throbbing", "Burning", "Cramping"]
        })
    
    if 'fever' in symptom_lower:
        questions.append({
            "id": "temperature",
            "question": "Have you measured your temperature? If yes, what was it?",
            "type": "text"
        })
    
    if 'chest' in symptom_lower:
        questions.append({
            "id": "chest_radiation",
            "question": "Does the chest discomfort spread to other areas?",
            "type": "choice",
            "options": ["No", "Left arm", "Jaw", "Back", "Both arms"]
        })
    
    questions.append({
        "id": "other_symptoms",
        "question": "Are you experiencing any other symptoms?",
        "type": "text"
    })
    
    return {
        "questions": questions,
        "reasoning": "These questions help assess the severity and nature of your symptoms for better medical guidance."
    }

def _enhanced_fallback_assessment(symptom_text: str, answers: dict = None) -> Dict:
    """
    Enhanced fallback assessment with better medical logic
    """
    symptom_lower = symptom_text.lower()
    
    # Initialize default values
    severity = 5
    specialist = "General Physician"
    urgency = "within a week"
    risk_factors = []
    tests = []
    diagnoses = []
    
    # Enhanced symptom analysis
    if any(word in symptom_lower for word in ['chest pain', 'heart attack', 'cardiac']):
        severity = 8
        specialist = "Cardiologist"
        urgency = "within 24 hours"
        risk_factors = [
            "Cardiovascular emergency risk",
            "Age and gender factors",
            "Family history of heart disease",
            "Smoking or diabetes history",
            "High blood pressure risk"
        ]
        tests = [
            "12-lead ECG",
            "Cardiac enzymes (Troponin)",
            "Chest X-ray",
            "Complete blood count",
            "Basic metabolic panel",
            "Echocardiogram if indicated"
        ]
        diagnoses = [
            "Acute coronary syndrome",
            "Myocardial infarction",
            "Unstable angina",
            "Aortic dissection",
            "Pulmonary embolism",
            "Pericarditis"
        ]
    
    elif any(word in symptom_lower for word in ['fever', 'temperature']) and any(word in symptom_lower for word in ['abdominal', 'stomach', 'belly']):
        # Check duration from answers
        duration_severe = False
        if answers:
            duration = answers.get('duration', '')
            if 'week' in duration.lower() or 'days' in duration.lower():
                duration_severe = True
        
        if duration_severe or 'severe' in symptom_lower:
            severity = 7
            specialist = "Gastroenterologist"
            urgency = "within 24 hours"
            risk_factors = [
                "Prolonged fever with abdominal pain suggests serious infection",
                "Risk of appendicitis or intra-abdominal abscess",
                "Possible enteric fever (Typhoid)",
                "Dehydration risk",
                "Recent travel or food exposure history"
            ]
            tests = [
                "Complete Blood Count with differential",
                "C-Reactive Protein (CRP)",
                "Blood culture",
                "Stool culture and analysis",
                "Abdominal ultrasound",
                "Urinalysis",
                "Liver function tests"
            ]
            diagnoses = [
                "Typhoid fever (Enteric fever)",
                "Acute appendicitis",
                "Cholecystitis",
                "Pyelonephritis",
                "Intra-abdominal abscess",
                "Bacterial gastroenteritis",
                "Inflammatory bowel disease"
            ]
        else:
            severity = 5
            specialist = "General Physician"
            urgency = "within a week"
            risk_factors = ["Possible viral or bacterial infection", "Monitor for dehydration"]
            tests = ["Complete blood count", "Basic examination"]
            diagnoses = ["Viral gastroenteritis", "Food poisoning"]
    
    elif any(word in symptom_lower for word in ['breathing', 'shortness of breath', 'cough']):
        severity = 6
        specialist = "Pulmonologist"
        urgency = "within 24 hours"
        risk_factors = [
            "Respiratory distress",
            "Possible pneumonia or bronchitis",
            "Smoking history increases risk",
            "Age-related complications"
        ]
        tests = [
            "Chest X-ray",
            "Oxygen saturation",
            "Complete blood count",
            "Sputum culture if productive cough",
            "Spirometry if chronic"
        ]
        diagnoses = [
            "Pneumonia",
            "Acute bronchitis",
            "Asthma exacerbation",
            "COPD exacerbation",
            "Upper respiratory infection"
        ]
    
    elif any(word in symptom_lower for word in ['headache', 'head pain']):
        if 'severe' in symptom_lower or 'worst' in symptom_lower:
            severity = 7
            specialist = "Neurologist"
            urgency = "within 24 hours"
            risk_factors = [
                "Severe headache requires urgent evaluation",
                "Risk of secondary headache",
                "Possible intracranial pathology"
            ]
            tests = [
                "Neurological examination",
                "CT scan of head",
                "Blood pressure check",
                "Complete blood count"
            ]
            diagnoses = [
                "Migraine",
                "Cluster headache",
                "Tension headache",
                "Secondary headache",
                "Intracranial pathology"
            ]
        else:
            severity = 4
            specialist = "General Physician"
            urgency = "routine"
            risk_factors = ["Common headache", "Stress or tension related"]
            tests = ["Clinical examination", "Blood pressure check"]
            diagnoses = ["Tension headache", "Migraine", "Stress headache"]
    
    # Enhance with answers if provided
    if answers:
        severity_answer = answers.get('severity')
        if severity_answer and str(severity_answer).isdigit():
            reported_severity = int(severity_answer)
            severity = max(severity, reported_severity)  # Take higher of calculated or reported
        
        duration_answer = answers.get('duration', '')
        if 'week' in duration_answer.lower():
            severity = min(severity + 1, 10)  # Increase severity for longer duration
    
    # Adjust urgency based on final severity
    if severity >= 8:
        urgency = "within 24 hours"
    elif severity >= 6:
        urgency = "within a week"
    else:
        urgency = "routine"
    
    # Default fallbacks
    if not risk_factors:
        risk_factors = ["General health monitoring recommended"]
    if not tests:
        tests = ["Complete blood count", "Basic clinical examination"]
    if not diagnoses:
        diagnoses = ["Requires clinical evaluation"]
    
    return {
        "severity_score": severity,
        "urgency": urgency,
        "risk_factors": risk_factors,
        "recommended_specialist": specialist,
        "suggested_tests": tests,
        "differential_diagnoses": diagnoses,
        "clinical_summary": f"Based on symptoms analysis: {symptom_text[:100]}. Severity assessed as {severity}/10. Recommend consultation with {specialist}."
    }

def _enhance_with_answers(result: Dict, answers: dict) -> Dict:
    """
    Enhance prediction results with user answers
    """
    # Adjust severity based on user input
    if 'severity' in answers:
        try:
            user_severity = int(answers['severity'])
            # Take average of model prediction and user input
            result['severity_score'] = (result['severity_score'] + user_severity) / 2
        except (ValueError, TypeError):
            pass
    
    # Adjust urgency based on duration
    if 'duration' in answers:
        duration = answers['duration'].lower()
        if 'week' in duration and result['urgency'] == 'routine':
            result['urgency'] = 'within a week'
    
    return result

def _calculate_trend(severities: List[float]) -> str:
    """
    Calculate trend direction from severity scores
    """
    if len(severities) < 2:
        return "stable"
    
    recent = severities[-3:]  # Last 3 sessions
    if len(recent) < 2:
        return "stable"
    
    avg_recent = sum(recent) / len(recent)
    avg_earlier = sum(severities[:-3]) / len(severities[:-3]) if len(severities) > 3 else avg_recent
    
    if avg_recent > avg_earlier + 0.5:
        return "worsening"
    elif avg_recent < avg_earlier - 0.5:
        return "improving"
    else:
        return "stable"