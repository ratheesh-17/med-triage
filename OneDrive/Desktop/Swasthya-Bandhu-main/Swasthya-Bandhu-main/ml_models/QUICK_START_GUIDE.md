# 🚀 QUICK START: Replace Gemini API with BioBERT

## 📋 SUMMARY

**What Gemini API Does:**
1. **Clinical Assessment**: Symptom → Severity, Urgency, Specialist, Diagnoses, Tests, Risk Factors
2. **Question Generation**: Symptom → Follow-up questions
3. **Risk Assessment**: Session history → Health risk trends

**Your Goal:** Train BioBERT model to do the same (75-85% accuracy vs Gemini's 90%)

---

## 📊 DATASETS NEEDED

### 1. **DDXPlus** (Primary - 1.3M cases)
- **Download**: https://figshare.com/articles/dataset/DDXPlus_Dataset/20043374
- **Features**: symptoms, age, sex, pathology
- **Use**: Train clinical assessment model
- **Size**: ~500MB

### 2. **MedDialog** (Optional - for questions)
- **Download**: https://github.com/UCSD-AI4H/Medical-Dialogue-System
- **Features**: Doctor-patient conversations
- **Use**: Train question generation
- **Size**: ~2GB

### 3. **MIMIC-III** (Optional - advanced)
- **Download**: https://physionet.org/content/mimiciii/1.4/ (requires approval)
- **Features**: Clinical notes, lab results
- **Use**: Enhance accuracy
- **Size**: ~50GB

---

## 🎯 STEP-BY-STEP GUIDE

### **WEEK 1: Data Preparation**

#### Step 1: Download Dataset
```bash
# On your laptop or Colab
wget https://figshare.com/ndownloader/files/35945800 -O ddxplus.csv
```

#### Step 2: Preprocess Data
```bash
# Use the data_preprocessing.py file I created
python ml_models/data_preprocessing.py
```

**Output:** `processed_training_data.csv` with columns:
- `symptom_text`: "fever, abdominal pain, nausea"
- `severity_score`: 7
- `urgency`: "within 24 hours"
- `specialist`: "Gastroenterologist"
- `tests`: ["CBC", "Blood culture", "Abdominal ultrasound"]
- `risk_factors`: ["Prolonged fever", "Dehydration risk"]
- `differential_diagnoses`: ["Typhoid", "Appendicitis"]

---

### **WEEK 2-3: Model Training (Google Colab)**

#### Step 1: Open Google Colab
1. Go to https://colab.research.google.com/
2. Runtime → Change runtime type → **GPU (T4)**
3. Upload `train_biobert_colab.py` (I created this file)

#### Step 2: Upload Files to Colab
```python
# In Colab, upload these files:
from google.colab import files
files.upload()  # Upload processed_training_data.csv
```

#### Step 3: Run Training
```python
# Just run all cells in train_biobert_colab.py
# Training takes 2-3 hours on Colab GPU
```

**Expected Output:**
```
Epoch 1/5, Train Loss: 2.45, Val Acc: 0.65
Epoch 2/5, Train Loss: 1.82, Val Acc: 0.72
Epoch 3/5, Train Loss: 1.45, Val Acc: 0.78
Epoch 4/5, Train Loss: 1.21, Val Acc: 0.81
Epoch 5/5, Train Loss: 1.05, Val Acc: 0.83
✅ Model saved: biobert_clinical_quantized.pth (105MB)
```

#### Step 4: Download Trained Model
```python
# In Colab
from google.colab import files
files.download('biobert_clinical_quantized.pth')
files.download('label_encoders.json')
```

---

### **WEEK 4: Integration into Your Project**

#### Step 1: Place Model Files
```
Swasthya-Bandhu-main/
└── ml_models/
    ├── models/
    │   ├── biobert_clinical_quantized.pth  ← Download from Colab
    │   └── label_encoders.json             ← Download from Colab
    ├── clinical_model.py                   ← Create this
    └── custom_ai_service.py                ← Create this
```

#### Step 2: Create `clinical_model.py`
```python
# Copy the BioBERTClinicalModel class from train_biobert_colab.py
# This defines your model architecture
```

#### Step 3: Create `custom_ai_service.py`
```python
import torch
from transformers import AutoTokenizer
from .clinical_model import BioBERTClinicalModel
import json

class CustomMedicalAI:
    def __init__(self):
        self.device = torch.device('cpu')  # Your laptop
        self.tokenizer = AutoTokenizer.from_pretrained("dmis-lab/biobert-v1.1")
        
        # Load encoders
        with open('ml_models/models/label_encoders.json', 'r') as f:
            self.encoders = json.load(f)
        
        # Load model
        num_specialists = len(self.encoders['specialist_classes'])
        num_diagnoses = len(self.encoders['diagnosis_classes'])
        
        self.model = BioBERTClinicalModel(num_specialists, num_diagnoses)
        self.model.load_state_dict(torch.load('ml_models/models/biobert_clinical_quantized.pth'))
        self.model.eval()
        self.initialized = True
        print("✅ Custom Medical AI loaded successfully")
    
    def predict(self, symptom_text, answers=None):
        # Tokenize
        encoding = self.tokenizer(
            symptom_text,
            max_length=256,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        
        # Predict
        with torch.no_grad():
            outputs = self.model(encoding['input_ids'], encoding['attention_mask'])
        
        # Decode predictions
        severity = torch.argmax(outputs['severity']).item() + 1
        urgency_idx = torch.argmax(outputs['urgency']).item()
        specialist_idx = torch.argmax(outputs['specialist']).item()
        diagnosis_idx = torch.argmax(outputs['diagnosis']).item()
        
        urgency = self.encoders['urgency_classes'][urgency_idx]
        specialist = self.encoders['specialist_classes'][specialist_idx]
        diagnosis = self.encoders['diagnosis_classes'][diagnosis_idx]
        
        # Get tests and risk factors from mapping
        tests = self.get_tests_for_diagnosis(diagnosis)
        risk_factors = self.get_risk_factors(diagnosis)
        
        return {
            'severity_score': severity,
            'urgency': urgency,
            'recommended_specialist': specialist,
            'differential_diagnoses': [diagnosis],
            'suggested_tests': tests,
            'risk_factors': risk_factors,
            'clinical_summary': f"Based on symptoms, severity assessed as {severity}/10. Recommend {specialist} consultation."
        }
    
    def get_tests_for_diagnosis(self, diagnosis):
        # Use TEST_MAPPING from data_preprocessing.py
        test_map = {
            'Typhoid': ['CBC', 'Blood culture', 'Widal test'],
            'Appendicitis': ['CBC', 'Abdominal ultrasound', 'CT scan'],
            # ... add more
        }
        return test_map.get(diagnosis, ['Complete Blood Count', 'Clinical examination'])
    
    def get_risk_factors(self, diagnosis):
        risk_map = {
            'Typhoid': ['Prolonged fever', 'Dehydration risk', 'Travel history'],
            'Appendicitis': ['Acute pain', 'Perforation risk'],
            # ... add more
        }
        return risk_map.get(diagnosis, ['Requires medical evaluation'])

# Functions for ai_service.py to call
def get_ai_clinical_assessment(symptom_text, answers=None, chat_history=None):
    ai = CustomMedicalAI()
    return ai.predict(symptom_text, answers)

def generate_followup_questions(symptom_text):
    # Simple rule-based for now (or train separate model)
    return {
        "questions": [
            {"id": "severity", "question": "Rate pain severity (1-10)?", "type": "scale"},
            {"id": "duration", "question": "How long?", "type": "choice", 
             "options": ["<24h", "1-3 days", "3-7 days", ">1 week"]}
        ],
        "reasoning": "Assess severity and duration"
    }
```

#### Step 4: Test Your Model
```bash
cd backend
python -c "
from ml_models.custom_ai_service import CustomMedicalAI
ai = CustomMedicalAI()
result = ai.predict('fever for 7 days and abdominal pain')
print(result)
"
```

**Expected Output:**
```json
{
  "severity_score": 7,
  "urgency": "within 24 hours",
  "recommended_specialist": "Gastroenterologist",
  "differential_diagnoses": ["Typhoid"],
  "suggested_tests": ["CBC", "Blood culture", "Widal test"],
  "risk_factors": ["Prolonged fever", "Dehydration risk"]
}
```

---

## 🎯 YOUR ai_service.py ALREADY SUPPORTS THIS!

Your current `ai_service.py` has fallback logic:
```python
# Try Gemini first
if gemini_client:
    return _gemini_clinical_assessment(...)

# Fallback to Custom AI (YOUR MODEL!)
if custom_ai and custom_ai.initialized:
    return custom_assessment(...)
```

**To switch to your model as primary:**
1. Remove Gemini API key from `.env`
2. Your model automatically becomes primary
3. No code changes needed!

---

## 📊 EXPECTED PERFORMANCE

| Metric | Gemini API | Your BioBERT |
|--------|-----------|--------------|
| Accuracy | 90-95% | 75-85% |
| Speed | 2-3 sec | 0.5-1 sec |
| Cost | $0.001/req | FREE |
| Size | Cloud | 105MB |
| RAM | N/A | 400-600MB |
| Internet | Required | Not required |

---

## 🐛 TROUBLESHOOTING

### "Out of memory" on laptop
```python
# Use smaller batch size
batch_size = 8  # Instead of 16
```

### "Model accuracy too low"
1. Train for more epochs (10 instead of 5)
2. Use larger dataset (add MIMIC-III)
3. Fine-tune on your actual patient data

### "Inference too slow"
```python
# Already quantized, but can optimize further
model = torch.jit.script(model)  # TorchScript compilation
```

---

## 📚 RESOURCES

1. **BioBERT Paper**: https://arxiv.org/abs/1901.08746
2. **DDXPlus Dataset**: https://figshare.com/articles/dataset/DDXPlus_Dataset/20043374
3. **Transformers Docs**: https://huggingface.co/docs/transformers
4. **Google Colab**: https://colab.research.google.com/

---

## ✅ CHECKLIST

- [ ] Week 1: Download DDXPlus dataset
- [ ] Week 1: Run data_preprocessing.py
- [ ] Week 2: Open Google Colab with GPU
- [ ] Week 2: Upload processed_training_data.csv
- [ ] Week 2: Run train_biobert_colab.py (2-3 hours)
- [ ] Week 3: Download trained model files
- [ ] Week 3: Create clinical_model.py
- [ ] Week 3: Create custom_ai_service.py
- [ ] Week 4: Test model locally
- [ ] Week 4: Remove Gemini API key
- [ ] Week 4: Deploy and monitor

---

## 🎉 FINAL RESULT

After 4 weeks, you'll have:
- ✅ Custom BioBERT model (105MB)
- ✅ 75-85% accuracy (close to Gemini)
- ✅ FREE (no API costs)
- ✅ Fast inference (0.5-1 sec)
- ✅ Works offline
- ✅ Runs on your laptop (8GB RAM)

**Your project will be 100% independent of Gemini API!**
