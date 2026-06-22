"""
Run from project root:
    cd C:\Users\91934\OneDrive\Desktop\Swasthya-Bandhu-main\Swasthya-Bandhu-main
    python test_biobert_accuracy.py
"""
import os, sys
os.environ["TRANSFORMERS_OFFLINE"] = "1"
sys.path.append("ml_models/models")

from custom_ai_service import local_ai, _assign_specialist_keyword, _assign_urgency_keyword, _assign_severity_keyword

TEST_CASES = [
    # (symptom, expected_specialist, expected_urgency, expected_severity_range)
    ("I have chest pain radiating to my left arm and sweating",        "Cardiologist",       "immediate",        (8,10)),
    ("fever and stomach pain for 3 days",                              "Gastroenterologist", "within_24_hours",  (5,7)),
    ("severe headache and neck stiffness and sensitivity to light",    "Neurologist",        "within_24_hours",  (7,9)),
    ("mild skin rash on arms for 2 days",                              "Dermatologist",      "routine",          (2,4)),
    ("shortness of breath and wheezing",                               "Pulmonologist",      "within_24_hours",  (6,8)),
    ("anxiety and panic attacks for a week",                           "Psychiatrist",       "within_a_week",    (4,6)),
    ("knee pain and swelling after fall",                              "Orthopedist",        "within_a_week",    (4,6)),
    ("burning urination and frequent urination",                       "Urologist",          "within_a_week",    (4,6)),
    ("irregular periods and pelvic pain",                              "Gynecologist",       "within_a_week",    (4,6)),
    ("mild cough and runny nose",                                      "General Physician",  "routine",          (2,4)),
]

print(f"\n{'='*90}")
print(f"{'SYMPTOM':<45} {'EXPECTED':<20} {'BIOBERT':<20} {'KW':<20} {'OK?'}")
print(f"{'='*90}")

correct = 0
for symptom, exp_spec, exp_urg, exp_sev_range in TEST_CASES:
    result   = local_ai.get_clinical_assessment(symptom)
    kw_spec  = _assign_specialist_keyword(symptom)
    kw_urg   = _assign_urgency_keyword(symptom)
    kw_sev   = _assign_severity_keyword(symptom)

    bio_spec = result["recommended_specialist"]
    bio_urg  = result["urgency"]
    bio_sev  = result["severity_score"]
    bio_conf = result.get("specialist_confidence", 0)

    spec_ok  = bio_spec == exp_spec
    urg_ok   = bio_urg  == exp_urg
    sev_ok   = exp_sev_range[0] <= bio_sev <= exp_sev_range[1]
    all_ok   = spec_ok and urg_ok and sev_ok
    if all_ok: correct += 1

    status = "OK" if all_ok else "FAIL"
    print(f"\n{symptom[:44]:<45}")
    print(f"  Specialist : expected={exp_spec:<22} biobert={bio_spec:<22} kw={kw_spec:<22} conf={bio_conf}%  {'OK' if spec_ok else 'WRONG'}")
    print(f"  Urgency    : expected={exp_urg:<22} biobert={bio_urg:<22} kw={kw_urg:<22} {'OK' if urg_ok else 'WRONG'}")
    print(f"  Severity   : expected={str(exp_sev_range):<22} biobert={bio_sev:<22} kw={kw_sev:<22} {'OK' if sev_ok else 'WRONG'}")
    print(f"  --> {status}")

print(f"\n{'='*90}")
print(f"SCORE: {correct}/{len(TEST_CASES)} correct")
print(f"{'='*90}\n")

# Also show raw BioBERT confidence for all outputs
print("\nRAW BIOBERT CONFIDENCE CHECK (specialist confidence < 80% means keyword fallback is used):")
for symptom, exp_spec, _, _ in TEST_CASES:
    result = local_ai._biobert_assessment(symptom)
    print(f"  {symptom[:50]:<52} spec_conf={result['specialist_confidence']}%  urg_conf={result['urgency_confidence']}%")
