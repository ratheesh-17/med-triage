import os
import time
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
client = genai.GenerativeModel('gemini-2.5-flash')

tests = [
    ("Simple ping", "Say: working"),
    ("Short medical", "Patient has fever. JSON: {\"severity_score\":5,\"urgency\":\"routine\",\"recommended_specialist\":\"GP\",\"differential_diagnoses\":[\"Viral fever\"],\"clinical_summary\":\"brief\"}"),
    ("Full assessment", "Patient has chest pain and shortness of breath for 2 hours. Provide full clinical assessment as JSON with severity_score, urgency, risk_factors, recommended_specialist, suggested_tests, differential_diagnoses, clinical_summary.")
]

print("Gemini Response Time Benchmark")
print("=" * 45)
for label, prompt in tests:
    start = time.time()
    try:
        response = client.generate_content(prompt)
        elapsed = time.time() - start
        print(f"{label}: {elapsed:.2f}s ({len(response.text)} chars)")
    except Exception as e:
        print(f"{label}: FAIL - {str(e)[:60]}")
    time.sleep(2)
