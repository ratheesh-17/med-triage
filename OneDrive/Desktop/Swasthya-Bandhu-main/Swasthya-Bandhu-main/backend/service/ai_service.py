import os
import json
import sys
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv(override=True)

# ── Gemini (primary) ──────────────────────────────────────────
GEMINI_MODELS = [
    'gemini-2.5-flash-lite',
    'gemini-2.0-flash-lite',
    'gemini-1.5-flash',
]

gemini_clients = []
try:
    api_key = os.getenv('GEMINI_API_KEY')
    if api_key:
        genai.configure(api_key=api_key)
        for model_name in GEMINI_MODELS:
            gemini_clients.append(genai.GenerativeModel(
                model_name,
                generation_config={'temperature': 0.3, 'top_p': 0.8, 'top_k': 40}
            ))
        print(f'[AI] Gemini primary initialised with {len(gemini_clients)} models')
except Exception as e:
    print(f'[AI] Gemini init failed: {e}')

# ── BioClinicalBERT (fallback) ────────────────────────────────
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'ml_models', 'inference'))

local_ai = None
try:
    from local_ai_service import local_ai
    if local_ai._loaded:
        print('[AI] BioClinicalBERT loaded as fallback')
    else:
        print('[AI] BioClinicalBERT failed to load')
        local_ai = None
except Exception as e:
    print(f'[AI] BioClinicalBERT import failed: {e}')
    local_ai = None


def _gemini_call(prompt: str) -> str:
    last_error = None
    for i, client in enumerate(gemini_clients):
        try:
            response = client.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f'[AI] Gemini model {i+1} failed: {type(e).__name__}: {str(e)[:60]}')
            last_error = e
    raise RuntimeError(f'All Gemini models exhausted. Last: {last_error}')


def _parse_json(text: str) -> dict:
    if text.startswith('```'):
        text = text.split('```')[1]
        if text.startswith('json'):
            text = text[4:]
    return json.loads(text.strip())


def _format_questions(raw_questions: list) -> dict:
    formatted = []
    for i, q in enumerate(raw_questions[:5], 1):
        q = q.strip()
        if not q.endswith('?'):
            q += '?'
        q_lower = q.lower()
        if any(w in q_lower for w in ['how long', 'how many', 'when did', 'describe', 'tell me']):
            qtype = 'text'
        elif any(w in q_lower for w in ['do you', 'have you', 'are you', 'did you', 'is there', 'does it']):
            qtype = 'yes_no'
        else:
            qtype = 'text'
        formatted.append({'id': f'q{i}', 'question': q, 'type': qtype})
    return {'questions': formatted, 'reasoning': 'Clinical questions based on symptoms', 'source': 'bioclinicalbert'}


# ── Public API ────────────────────────────────────────────────

def generate_followup_questions(symptom_text: str):
    # Primary: Gemini
    if gemini_clients:
        try:
            specialist = 'General Physician'
            if local_ai:
                try:
                    assessment = local_ai.get_clinical_assessment(symptom_text)
                    specialist = assessment.get('recommended_specialist', 'General Physician')
                except Exception:
                    pass
            prompt = (f'You are a {specialist}. Patient says: "{symptom_text}"\n'
                      f'Generate 4 specific clinical follow-up questions a {specialist} would ask.\n'
                      f'Return ONLY valid JSON:\n'
                      f'{{"questions":[{{"id":"q1","question":"<question>","type":"yes_no"}},'
                      f'{{"id":"q2","question":"<question>","type":"choice","options":["opt1","opt2","opt3"]}},'
                      f'{{"id":"q3","question":"<question>","type":"text"}},'
                      f'{{"id":"q4","question":"<question>","type":"yes_no"}}],"reasoning":"<one sentence>"}}')
            result = _parse_json(_gemini_call(prompt))
            print(f'[AI] Questions by Gemini (specialist={specialist})')
            return result
        except Exception as e:
            print(f'[AI] Gemini question generation failed: {e}')

    # Fallback: BioClinicalBERT T5
    if local_ai:
        try:
            questions = local_ai.generate_followup_questions(symptom_text)
            if questions and len(questions) >= 2:
                print('[AI] Questions by BioClinicalBERT T5 (fallback)')
                return _format_questions(questions)
        except Exception as e:
            print(f'[AI] BioClinicalBERT question generation failed: {e}')

    raise RuntimeError('All AI models unavailable for question generation')


def get_ai_clinical_assessment(symptom_text: str, answers: dict = None, chat_history: list = None):
    # Primary: Gemini
    if gemini_clients:
        try:
            full_context = symptom_text
            if answers:
                details = ', '.join([f'{k}: {v}' for k, v in answers.items()])
                full_context = f'{symptom_text}. Details: {details}'
            prompt = (f'Medical triage for: {full_context}\n'
                      f'Return ONLY valid JSON:\n'
                      f'{{"severity_score":<1-10>,"urgency":"<immediate|within 24 hours|within a week|routine>",'
                      f'"risk_factors":["f1","f2","f3"],"recommended_specialist":"<specialist>",'
                      f'"suggested_tests":["t1","t2","t3","t4"],"differential_diagnoses":["d1","d2","d3","d4"],'
                      f'"clinical_summary":"<2 sentences>"}}')
            result = _parse_json(_gemini_call(prompt))
            print('[AI] Clinical assessment by Gemini')
            return result
        except Exception as e:
            print(f'[AI] Gemini assessment failed: {e}')

    # Fallback: BioClinicalBERT
    if local_ai:
        try:
            result = local_ai.get_clinical_assessment(symptom_text, answers)
            print('[AI] Clinical assessment by BioClinicalBERT (fallback)')
            return result
        except Exception as e:
            print(f'[AI] BioClinicalBERT assessment failed: {e}')

    raise RuntimeError('All AI models unavailable for clinical assessment')


def get_longitudinal_risk_assessment(sessions: list):
    if not sessions or len(sessions) < 2:
        return None

    # Primary: Gemini
    if gemini_clients:
        try:
            session_data = [
                f'Session {i+1}: Severity {s["severity_score"]}, Symptoms: {s["symptom_input"][:80]}'
                for i, s in enumerate(sessions[-6:])
            ]
            prompt = (f'Analyze patient sessions and return ONLY valid JSON:\n'
                      f'{chr(10).join(session_data)}\n'
                      f'{{"cardiac_risk":<0-10>,"metabolic_risk":<0-10>,"neurological_risk":<0-10>,'
                      f'"respiratory_risk":<0-10>,"trend_direction":"<improving|stable|worsening>",'
                      f'"summary":"<brief>"}}')
            result = _parse_json(_gemini_call(prompt))
            print('[AI] Longitudinal risk by Gemini')
            return result
        except Exception as e:
            print(f'[AI] Gemini risk failed: {e}')

    # Fallback: BioClinicalBERT
    if local_ai:
        try:
            result = local_ai.get_longitudinal_risk(sessions)
            if result:
                print('[AI] Longitudinal risk by BioClinicalBERT (fallback)')
                return result
        except Exception as e:
            print(f'[AI] BioClinicalBERT risk failed: {e}')

    return None
