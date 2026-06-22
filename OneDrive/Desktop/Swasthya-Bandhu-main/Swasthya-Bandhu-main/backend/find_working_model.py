import os
import time
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai

api_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=api_key)
print("API Key:", api_key[:15] + "...")

models_to_try = [
    'gemini-2.0-flash',
    'gemini-2.5-flash',
    'gemini-2.0-flash-lite',
    'gemini-2.5-flash-lite',
    'gemini-1.5-flash',
    'gemini-1.5-pro',
]

working_model = None
for model_name in models_to_try:
    try:
        print(f"\nTrying {model_name}...")
        client = genai.GenerativeModel(model_name)
        response = client.generate_content("Reply with: working")
        print(f"SUCCESS: {model_name} -> {response.text.strip()[:50]}")
        working_model = model_name
        break
    except Exception as e:
        msg = str(e)
        if "429" in msg:
            print(f"QUOTA EXCEEDED: {model_name}")
        elif "404" in msg:
            print(f"NOT FOUND: {model_name}")
        else:
            print(f"ERROR: {model_name} -> {msg[:80]}")
        time.sleep(1)

print("\n" + "="*40)
if working_model:
    print(f"USE THIS MODEL: {working_model}")
else:
    print("NO WORKING MODEL FOUND - All quota exceeded")
    print("Solutions:")
    print("1. Wait 24 hours for daily quota reset")
    print("2. Go to https://aistudio.google.com and generate a fresh API key")
    print("3. Enable billing at https://console.cloud.google.com")
