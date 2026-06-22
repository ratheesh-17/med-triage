from dotenv import load_dotenv
load_dotenv()

import requests
import os
from jose import jwt

# Get token
response = requests.post("http://localhost:8000/auth/patient/register", json={
    "phone": "7777777777",
    "name": "Debug User",
    "age": 25,
    "gender": "Male"
})

if response.status_code == 200:
    token = response.json()["token"]
    print(f"Token: {token[:50]}...")
    
    # Decode without verification
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production-2024")
    print(f"\nSECRET_KEY from env: {SECRET_KEY}")
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        print(f"\nDecoded payload: {payload}")
    except Exception as e:
        print(f"\nDecode error: {e}")
    
    # Try the endpoint
    headers = {"Authorization": f"Bearer {token}"}
    response2 = requests.get("http://localhost:8000/health-risk", headers=headers)
    print(f"\nEndpoint response: {response2.status_code}")
    print(f"Response body: {response2.text}")
    
    # Cleanup
    from config.database import SessionLocal
    from entity.models import User
    db = SessionLocal()
    db.query(User).filter(User.phone == "7777777777").delete()
    db.commit()
    db.close()
