"""Quick Connection Verification - Windows Compatible"""
import requests
import sys

print("\n" + "="*60)
print("SWASTHYA BANDHU - CONNECTION VERIFICATION")
print("="*60)

backend_ok = docs_ok = frontend_ok = routes_ok = False

# Test 1: Backend
print("\n[1/4] Testing Backend Connection...")
try:
    response = requests.get("http://localhost:8000/health", timeout=5)
    if response.status_code == 200:
        data = response.json()
        print(f"[PASS] Backend running on port 8000")
        print(f"       Status: {data.get('status', 'unknown')}")
        backend_ok = True
    else:
        print(f"[FAIL] Backend returned status {response.status_code}")
except requests.exceptions.ConnectionError:
    print("[FAIL] Cannot connect to backend on port 8000")
    print("       -> Start backend: cd backend && uvicorn app:app --reload")
except Exception as e:
    print(f"[FAIL] Error: {str(e)}")

# Test 2: API Docs
print("\n[2/4] Testing API Documentation...")
try:
    response = requests.get("http://localhost:8000/docs", timeout=5)
    if response.status_code == 200:
        print("[PASS] API docs available at http://localhost:8000/docs")
        docs_ok = True
    else:
        print("[FAIL] API docs not accessible")
except Exception as e:
    print(f"[FAIL] Error: {str(e)}")

# Test 3: Frontend
print("\n[3/4] Testing Frontend Connection...")
try:
    response = requests.get("http://localhost:5173", timeout=5)
    if response.status_code == 200 and "Swasthya Bandhu" in response.text:
        print("[PASS] Frontend running on port 5173")
        print("       URL: http://localhost:5173")
        frontend_ok = True
    else:
        print("[FAIL] Frontend returned unexpected response")
except requests.exceptions.ConnectionError:
    print("[FAIL] Cannot connect to frontend on port 5173")
    print("       -> Start frontend: cd frontend-react && npm run dev")
except Exception as e:
    print(f"[FAIL] Error: {str(e)}")

# Test 4: Backend Routes
print("\n[4/4] Testing Backend API Routes...")
if backend_ok:
    try:
        response = requests.get("http://localhost:8000/auth/patient/register", timeout=5)
        if response.status_code in [200, 405, 422]:
            print("[PASS] Backend API routes accessible")
            print("       Frontend can call backend via /api proxy")
            routes_ok = True
        else:
            print(f"[FAIL] Unexpected status {response.status_code}")
    except Exception as e:
        print(f"[FAIL] Error: {str(e)}")
else:
    print("[SKIP] Backend not running")

# Summary
print("\n" + "="*60)
print("VERIFICATION SUMMARY")
print("="*60)

tests = [
    ("Backend Server", backend_ok),
    ("API Documentation", docs_ok),
    ("Frontend Server", frontend_ok),
    ("Backend Routes", routes_ok)
]

passed = sum(1 for _, result in tests if result)
total = len(tests)

for test_name, result in tests:
    status = "[PASS]" if result else "[FAIL]"
    print(f"{status} {test_name}")

print(f"\nResult: {passed}/{total} tests passed")

if passed == total:
    print("\n" + "="*60)
    print("SUCCESS! Everything is connected and working!")
    print("="*60)
    print("\nNext Steps:")
    print("  1. Open browser: http://localhost:5173")
    print("  2. Try registering a new patient")
    print("  3. Test the AI triage feature")
    print("  4. Check API docs: http://localhost:8000/docs")
    sys.exit(0)
else:
    print("\n" + "="*60)
    print("WARNING: Some tests failed")
    print("="*60)
    print("\nQuick Fixes:")
    if not backend_ok:
        print("  - Start backend:")
        print("    cd Swasthya-Bandhu-main\\backend")
        print("    venv\\Scripts\\activate")
        print("    uvicorn app:app --reload")
    if not frontend_ok:
        print("  - Start frontend:")
        print("    cd Swasthya-Bandhu-main\\frontend-react")
        print("    npm run dev")
    sys.exit(1)
