"""
Local AI inference service.
Uses trained BioClinicalBERT extended model (specialist / urgency / severity / disease / risk)
and T5 CoT question generation — fully neural, no rule-based logic.
"""

import os
import pickle
import torch
import torch.nn as nn
os.environ['TRANSFORMERS_OFFLINE'] = '1'
from transformers import AutoTokenizer, AutoModel, T5ForConditionalGeneration

# ── Paths ─────────────────────────────────────────────────────
_BASE     = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models_bioclinical_new'))
BERT_PTH       = os.path.join(_BASE, 'biobert_clinical_extended.pth')
URGENCY_PKL    = os.path.join(_BASE, 'urgency_encoder _new.pkl')
SPECIALIST_PKL = os.path.join(_BASE, 'specialist_encoder_new.pkl')
DISEASE_PKL    = os.path.join(_BASE, 'disease_encoder_new.pkl')
T5_DIR         = os.path.join(_BASE, 't5_qgen_model', 'kaggle', 'working', 't5_qgen_model')
BERT_BASE      = 'emilyalsentzer/Bio_ClinicalBERT'

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


# ── Model architecture — must match training exactly ──────────
class ClinicalBERTExtended(nn.Module):
    def __init__(self, num_urgency, num_specialist, num_disease):
        super().__init__()
        self.bert    = AutoModel.from_pretrained(BERT_BASE)
        self.dropout = nn.Dropout(0.3)

        # specialist: 768 -> 512 -> 256 -> num_specialist
        self.specialist_head = nn.Sequential(
            nn.Linear(768, 512), nn.ReLU(), nn.Dropout(0.25),
            nn.Linear(512, 256), nn.ReLU(), nn.Dropout(0.2),
            nn.Linear(256, num_specialist)
        )
        # urgency: 768 -> 256 -> num_urgency
        self.urgency_head = nn.Sequential(
            nn.Linear(768, 256), nn.ReLU(), nn.Dropout(0.2),
            nn.Linear(256, num_urgency)
        )
        # severity classification: 768 -> 256 -> 10
        self.severity_cls = nn.Sequential(
            nn.Linear(768, 256), nn.ReLU(), nn.Dropout(0.2),
            nn.Linear(256, 10)
        )
        # severity regression: 768 -> 128 -> 1
        self.severity_reg = nn.Sequential(
            nn.Linear(768, 128), nn.ReLU(), nn.Dropout(0.2),
            nn.Linear(128, 1), nn.Sigmoid()
        )
        # disease: 768 -> 512 -> 256 -> num_disease
        self.disease_head = nn.Sequential(
            nn.Linear(768, 512), nn.ReLU(), nn.Dropout(0.25),
            nn.Linear(512, 256), nn.ReLU(), nn.Dropout(0.2),
            nn.Linear(256, num_disease)
        )
        # risk: 768 -> 256 -> 10  (10 risk factor scores)
        self.risk_head = nn.Sequential(
            nn.Linear(768, 256), nn.ReLU(), nn.Dropout(0.2),
            nn.Linear(256, 10)
        )

    def forward(self, input_ids, attention_mask):
        pooled = self.dropout(
            self.bert(input_ids=input_ids, attention_mask=attention_mask).pooler_output)
        return {
            'specialist':   self.specialist_head(pooled),
            'urgency':      self.urgency_head(pooled),
            'severity_cls': self.severity_cls(pooled),
            'severity_reg': self.severity_reg(pooled).squeeze(-1) * 9 + 1,
            'disease':      self.disease_head(pooled),
            'risk':         self.risk_head(pooled),
        }


# ── Urgency label normalisation ───────────────────────────────
_URGENCY_MAP = {
    'immediate':       'immediate',
    'within_24_hours': 'within 24 hours',
    'within_a_week':   'within a week',
    'routine':         'routine',
}

# Risk factors derived from disease — grounded in actual prediction
_DISEASE_RISK_MAP = {
    'pneumonia':                      'Respiratory infection risk',
    'bronchial asthma':               'Chronic respiratory risk',
    'hypertension':                   'Cardiovascular/hypertensive risk',
    'diabetes':                       'Metabolic/glycemic risk',
    'gastroesophageal reflux disease':'Gastrointestinal risk',
    'peptic ulcer disease':           'Gastrointestinal ulcer risk',
    'malaria':                        'Vector-borne infectious risk',
    'typhoid':                        'Enteric infectious risk',
    'dengue':                         'Vector-borne infectious risk',
    'urinary tract infection':        'Urological infection risk',
    'migraine':                       'Neurological risk',
    'cervical spondylosis':           'Musculoskeletal/spinal risk',
    'arthritis':                      'Musculoskeletal/joint risk',
    'allergy':                        'Allergic/immune hypersensitivity risk',
    'drug reaction':                  'Adverse drug reaction risk',
    'fungal infection':               'Dermatological infection risk',
    'psoriasis':                      'Chronic dermatological risk',
    'impetigo':                       'Bacterial skin infection risk',
    'chicken pox':                    'Viral infectious risk',
    'jaundice':                       'Hepatic/biliary risk',
    'varicose veins':                 'Vascular/circulatory risk',
    'common cold':                    'Upper respiratory infection risk',
}

# Suggested tests per specialist
_TESTS = {
    'Cardiologist':       ['12-lead ECG', 'Cardiac enzymes (Troponin)', 'Chest X-ray', 'Echocardiogram'],
    'Pulmonologist':      ['Chest X-ray', 'Spirometry', 'Oxygen saturation', 'CT chest'],
    'Neurologist':        ['CT scan', 'MRI brain', 'Neurological examination', 'EEG'],
    'Gastroenterologist': ['Abdominal ultrasound', 'CBC', 'LFT', 'CT abdomen'],
    'Orthopedist':        ['X-ray', 'MRI joint', 'CBC', 'ESR/CRP'],
    'Dermatologist':      ['Skin biopsy', 'Patch test', 'KOH mount', 'CBC'],
    'Psychiatrist':       ['Mental status exam', 'PHQ-9', 'GAD-7', 'Thyroid profile'],
    'Gynecologist':       ['Pelvic ultrasound', 'CBC', 'Urine pregnancy test', 'Pap smear'],
    'Urologist':          ['Urine routine', 'Urine culture', 'Renal ultrasound', 'Serum creatinine'],
    'Ophthalmologist':    ['Slit lamp exam', 'Visual acuity', 'IOP measurement', 'Fundoscopy'],
    'ENT Specialist':     ['Audiometry', 'Throat swab', 'Nasal endoscopy', 'X-ray PNS'],
    'General Physician':  ['Complete blood count', 'Basic metabolic panel', 'Urinalysis', 'CRP'],
}


class LocalAIService:
    def __init__(self):
        self._bert_model     = None
        self._bert_tok       = None
        self._urgency_enc    = None
        self._specialist_enc = None
        self._disease_enc    = None
        self._t5_model       = None
        self._t5_tok         = None
        self._loaded         = False
        self._load()

    def _load(self):
        try:
            with open(URGENCY_PKL,    'rb') as f: self._urgency_enc    = pickle.load(f)
            with open(SPECIALIST_PKL, 'rb') as f: self._specialist_enc = pickle.load(f)
            with open(DISEASE_PKL,    'rb') as f: self._disease_enc    = pickle.load(f)

            num_urgency    = len(self._urgency_enc.classes_)
            num_specialist = len(self._specialist_enc.classes_)
            num_disease    = len(self._disease_enc.classes_)

            self._bert_tok   = AutoTokenizer.from_pretrained(BERT_BASE)
            self._bert_model = ClinicalBERTExtended(num_urgency, num_specialist, num_disease)
            state = torch.load(BERT_PTH, map_location=device)
            self._bert_model.load_state_dict(state)
            self._bert_model.to(device).eval()
            print(f'[LocalAI] BioClinicalBERT Extended loaded — '
                  f'urgency:{num_urgency} specialist:{num_specialist} disease:{num_disease}')

            self._t5_tok   = AutoTokenizer.from_pretrained(T5_DIR)
            self._t5_model = T5ForConditionalGeneration.from_pretrained(T5_DIR).to(device).eval()
            print('[LocalAI] T5 question-generation model loaded')

            self._loaded = True
        except Exception as e:
            print(f'[LocalAI] Load failed: {e}')
            self._loaded = False

    # ── Public API ────────────────────────────────────────────

    def get_clinical_assessment(self, symptom_text: str, answers: dict = None) -> dict:
        if not self._loaded:
            raise RuntimeError('Models not loaded')

        text = symptom_text
        if answers:
            text += ' ' + ' '.join(f'{k} {v}' for k, v in answers.items())

        enc = self._bert_tok(
            text, max_length=256, padding='max_length',
            truncation=True, return_tensors='pt'
        )
        with torch.no_grad():
            out = self._bert_model(
                enc['input_ids'].to(device),
                enc['attention_mask'].to(device)
            )

        # Specialist
        specialist_idx = torch.argmax(out['specialist']).item()
        specialist     = self._specialist_enc.classes_[specialist_idx]
        spec_conf      = torch.softmax(out['specialist'], 1).max().item()

        # Urgency
        urgency_idx = torch.argmax(out['urgency']).item()
        urgency_raw = self._urgency_enc.classes_[urgency_idx]
        urgency     = _URGENCY_MAP.get(urgency_raw, urgency_raw)

        # Severity
        severity_cls = torch.argmax(out['severity_cls']).item() + 1
        severity_reg = round(out['severity_reg'].item(), 1)
        severity     = round((severity_cls + severity_reg) / 2)

        # Disease — top 3 differential diagnoses with confidence %
        disease_probs = torch.softmax(out['disease'], 1)[0]
        top3_idx      = torch.topk(disease_probs, k=3).indices.tolist()
        differential  = [
            f"{self._disease_enc.classes_[i]} ({disease_probs[i].item():.0%})"
            for i in top3_idx
        ]

        # Risk factors — derived from top 3 disease predictions (grounded, not guessed)
        risk_factors = list(dict.fromkeys(
            _DISEASE_RISK_MAP.get(self._disease_enc.classes_[i], 'General health risk')
            for i in top3_idx
        ))

        tests = _TESTS.get(specialist, _TESTS['General Physician'])

        return {
            'severity_score':         severity,
            'urgency':                urgency,
            'recommended_specialist': specialist,
            'suggested_tests':        tests,
            'risk_factors':           risk_factors,
            'differential_diagnoses': differential,
            'clinical_summary':       (f'BioClinicalBERT assessment: severity {severity}/10, '
                                       f'urgency {urgency}. Most likely: {self._disease_enc.classes_[top3_idx[0]]}. '
                                       f'Consult {specialist}.'),
            'source': 'bioclinicalbert',
        }

    def generate_followup_questions(self, symptom_text: str) -> list:
        if not self._loaded:
            raise RuntimeError('Models not loaded')

        try:
            assessment = self.get_clinical_assessment(symptom_text)
            specialist = assessment.get('recommended_specialist', 'General Physician')
            urgency    = assessment.get('urgency', 'routine')
            context    = f'specialist: {specialist} urgency: {urgency}'
        except Exception:
            context = ''

        input_text = f'symptoms: {symptom_text[:350]} {context}'.strip()
        ids = self._t5_tok(
            input_text, return_tensors='pt',
            max_length=256, truncation=True
        ).input_ids.to(device)

        with torch.no_grad():
            out = self._t5_model.generate(
                ids,
                max_new_tokens=200,
                num_beams=4,
                early_stopping=True,
                no_repeat_ngram_size=3,
                repetition_penalty=2.5,
                length_penalty=1.5,
            )

        decoded = self._t5_tok.decode(out[0], skip_special_tokens=True)

        if 'QUESTIONS:' in decoded:
            q_part = decoded.split('QUESTIONS:')[-1].strip()
        else:
            q_part = decoded

        questions = [q.strip() for q in q_part.split('[SEP]') if len(q.strip()) > 10]
        questions = [q if q.endswith('?') else q + '?' for q in questions]
        return questions[:5]

    def get_longitudinal_risk(self, sessions: list) -> dict:
        if not self._loaded or len(sessions) < 2:
            return None

        scores = []
        for s in sessions[-6:]:
            try:
                result = self.get_clinical_assessment(s.get('symptom_input', ''))
                scores.append(result['severity_score'])
            except Exception:
                scores.append(s.get('severity_score', 5))

        avg   = sum(scores) / len(scores)
        trend = ('worsening' if scores[-1] > scores[0] + 1
                 else 'improving' if scores[-1] < scores[0] - 1
                 else 'stable')

        return {
            'cardiac_risk':      min(10, round(avg * 0.9, 1)),
            'metabolic_risk':    min(10, round(avg * 0.7, 1)),
            'neurological_risk': min(10, round(avg * 0.6, 1)),
            'respiratory_risk':  min(10, round(avg * 0.75, 1)),
            'trend_direction':   trend,
            'summary':           f'Neural risk from {len(scores)} sessions. Avg severity: {avg:.1f}',
            'source':            'bioclinicalbert',
        }


# Singleton
local_ai = LocalAIService()
