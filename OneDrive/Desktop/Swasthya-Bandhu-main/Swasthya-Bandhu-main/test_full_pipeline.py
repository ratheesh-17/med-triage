import os, sys
os.environ['TRANSFORMERS_OFFLINE'] = '1'
sys.path.insert(0, 'ml_models/models')

from custom_ai_service import local_ai

print("=" * 60)
print("BioBERT + T5 Full Pipeline Test")
print("=" * 60)
print(f"Model initialized (BioBERT active): {local_ai.initialized}")
print()

# ── Test 1: Clinical Assessment ──────────────────────────────
print("--- TEST 1: Clinical Assessment (BioBERT) ---")
tests = [
    ('fever and stomach pain for 3 days', None),
    ('chest pain radiating to left arm', None),
    ('severe headache and vomiting', None),
    ('cough and difficulty breathing', None),
    ('knee pain and joint swelling', None),
    ('anxiety and panic attacks', None),
    ('skin rash and itching all over body', None),
    ('frequent urination and excessive thirst', None),
]
for symptom, answers in tests:
    r = local_ai.get_clinical_assessment(symptom, answers)
    print(f"  Symptoms : {symptom}")
    print(f"  Specialist: {r['recommended_specialist']}  Severity: {r['severity_score']}/10  Urgency: {r['urgency']}")
    print(f"  Diagnoses : {r['differential_diagnoses'][:2]}")
    print(f"  Tests     : {r['suggested_tests'][:2]}")
    print(f"  Risk      : {r['risk_factors'][0]}")
    print()

# ── Test 2: T5 Follow-up Questions ───────────────────────────
print("--- TEST 2: T5 Follow-up Question Generation ---")
q_tests = [
    'fever and stomach pain for 3 days',
    'chest pain radiating to left arm',
    'severe headache',
]
for symptom in q_tests:
    qs = local_ai.generate_followup_questions(symptom)
    print(f"  Symptoms: {symptom}")
    if isinstance(qs, list):
        for q in qs[:3]:
            print(f"    Q: {q}")
    else:
        for q in qs[:3]:
            print(f"    Q: {q}")
    print()

# ── Test 3: Longitudinal Risk ─────────────────────────────────
print("--- TEST 3: Longitudinal Risk Assessment ---")
sessions = [
    {'severity_score': 6, 'recommended_specialist': 'Cardiologist', 'urgency': 'within_24_hours'},
    {'severity_score': 7, 'recommended_specialist': 'Cardiologist', 'urgency': 'within_24_hours'},
    {'severity_score': 8, 'recommended_specialist': 'Cardiologist', 'urgency': 'immediate'},
    {'severity_score': 9, 'recommended_specialist': 'Cardiologist', 'urgency': 'immediate'},
]
risk = local_ai.get_longitudinal_risk(sessions)
print(f"  cardiac_risk     : {risk['cardiac_risk']}")
print(f"  metabolic_risk   : {risk['metabolic_risk']}")
print(f"  neurological_risk: {risk['neurological_risk']}")
print(f"  respiratory_risk : {risk['respiratory_risk']}")
print(f"  trend_direction  : {risk['trend_direction']}")
print(f"  summary          : {risk['summary']}")
