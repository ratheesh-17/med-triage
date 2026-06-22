import os, json
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
client = genai.GenerativeModel('gemini-2.5-flash')

symptom_text = "I have fever and headache"
specialist = "General Physician"

prompt = f"""You are a {specialist}. Patient says: "{symptom_text}"
Generate 4 specific follow-up questions. Return ONLY compact JSON:
{{"questions":[{{"id":"q1","question":"<question>","type":"yes_no"}},{{"id":"q2","question":"<question>","type":"choice","options":["opt1","opt2","opt3"]}},{{"id":"q3","question":"<question>","type":"text"}},{{"id":"q4","question":"<question>","type":"yes_no"}}],"reasoning":"<one sentence>"}}"""

print("Sending prompt to Gemini...")
print("Prompt length:", len(prompt), "chars")

try:
    response = client.generate_content(prompt)
    result_text = response.text.strip()
    print("\nRAW RESPONSE:")
    print(result_text)

    if result_text.startswith('```'):
        result_text = result_text.split('```')[1]
        if result_text.startswith('json'):
            result_text = result_text[4:]

    parsed = json.loads(result_text.strip())
    print("\nPARSED OK - Questions:")
    for q in parsed.get("questions", []):
        print(f"  [{q['type']}] {q['question']}")
    print("Reasoning:", parsed.get("reasoning"))

except Exception as e:
    print("\nERROR:", type(e).__name__, str(e))
