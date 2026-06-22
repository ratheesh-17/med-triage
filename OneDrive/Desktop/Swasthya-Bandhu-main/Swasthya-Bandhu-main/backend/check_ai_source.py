"""
HOW TO USE:
  1. Keep uvicorn running in one terminal
  2. Open a NEW terminal
  3. cd to backend folder:
       cd C:\Users\91934\OneDrive\Desktop\Swasthya-Bandhu-main\Swasthya-Bandhu-main\backend
  4. Run:
       python check_ai_source.py
"""
import urllib.request
import urllib.error
import json

BASE = "http://127.0.0.1:8000"
PHONE = "8888888888"   # any test phone number

def post(path, data, token=None):
    req = urllib.request.Request(BASE + path, data=json.dumps(data).encode(), method="POST")
    req.add_header("Content-Type", "application/json")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode()), r.status
    except urllib.error.HTTPError as e:
        return json.loads(e.read().decode()), e.code

# ── Step 1: Register (ok if already exists) ──────────────────
print("\n[1] Registering test patient...")
res, code = post("/auth/patient/register", {
    "phone": PHONE, "name": "AI Test User", "age": 25, "gender": "male"
})
print(f"    {code}: {res.get('message', res)}")

# ── Step 2: Login → get token directly ───────────────────────
print("\n[2] Logging in...")
res, code = post("/auth/login", {"phone": PHONE})
print(f"    {code}: {res}")
token = res.get("token")
if not token:
    print("    ERROR: No token in login response.")
    exit(1)
print(f"    Token OK: {token[:40]}...")

# ── Step 3: Call /chat ────────────────────────────────────────
SYMPTOMS = "I have fever and stomach pain for 3 days"
print(f"\n[3] Sending symptoms: '{SYMPTOMS}'")
print("    (This may take 10-30 seconds while BioBERT runs...)\n")

res, code = post("/chat", {"symptom_text": SYMPTOMS}, token=token)

print(f"    HTTP Status: {code}")

# ── Step 4: Show result ───────────────────────────────────────
print(f"\n{'='*55}")

if res.get("needs_clarification"):
    # BioBERT triggered follow-up questions first
    q_source = res.get("source", "unknown")
    print(f"  RESULT: Follow-up questions requested")
    print(f"  AI SOURCE: {q_source}")
    if q_source == "biobert":
        print("  --> Your trained BioBERT+T5 model generated questions!")
    elif q_source == "gemini":
        print("  --> Gemini fallback generated questions")
    print(f"\n  Questions:")
    for q in res.get("questions", []):
        print(f"    - {q.get('question')}")
else:
    source = res.get("ai_source", "NOT FOUND")
    print(f"  AI SOURCE: {source}")
    if source == "biobert":
        print("  --> Your trained BioBERT model answered!")
    elif source == "gemini":
        print("  --> Gemini fallback was used (BioBERT failed)")
    elif source == "fallback":
        print("  --> Static fallback used (both AIs failed)")
    else:
        print("  --> Unknown source. Check uvicorn console for errors.")

    print(f"\n  Severity Score : {res.get('severity_score', 'N/A')} / 10")
    print(f"  Urgency        : {res.get('urgency', 'N/A')}")
    print(f"  Specialist     : {res.get('recommended_specialist', 'N/A')}")
    print(f"  Diagnoses      : {res.get('differential_diagnoses', [])[:2]}")

print(f"{'='*55}")
print(f"\n  All response keys: {list(res.keys())}")
