from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, Depends, Header
from sqlalchemy.orm import Session
import os
import random
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production-2024")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

otp_storage = {}

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = authorization.split(" ")[1]
    payload = verify_token(token)
    return payload

def generate_otp(phone: str):
    otp = str(random.randint(100000, 999999))
    otp_storage[phone] = {"otp": otp, "expires": datetime.utcnow() + timedelta(minutes=5)}
    return otp

def verify_otp(phone: str, otp: str):
    if phone not in otp_storage:
        return False
    stored = otp_storage[phone]
    if datetime.utcnow() > stored["expires"]:
        del otp_storage[phone]
        return False
    if stored["otp"] == otp:
        del otp_storage[phone]
        return True
    return False
