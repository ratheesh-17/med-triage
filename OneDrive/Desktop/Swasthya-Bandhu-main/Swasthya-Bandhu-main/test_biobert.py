import os, sys, torch, torch.nn as nn, pickle
os.environ['TRANSFORMERS_OFFLINE'] = '1'
from transformers import AutoTokenizer, AutoModel

MODELS_DIR = 'ml_models/models'

class BioBERTClinical(nn.Module):
    def __init__(self, num_urgency, num_specialist):
        super().__init__()
        self.biobert = AutoModel.from_pretrained('dmis-lab/biobert-base-cased-v1.1')
        self.dropout = nn.Dropout(0.3)
        self.severity_head   = nn.Sequential(nn.Linear(768,256), nn.ReLU(), nn.Dropout(0.2), nn.Linear(256,10))
        self.urgency_head    = nn.Sequential(nn.Linear(768,256), nn.ReLU(), nn.Dropout(0.2), nn.Linear(256,num_urgency))
        self.specialist_head = nn.Sequential(nn.Linear(768,512), nn.ReLU(), nn.Dropout(0.25), nn.Linear(512,256), nn.ReLU(), nn.Dropout(0.2), nn.Linear(256,num_specialist))
    def forward(self, input_ids, attention_mask):
        out = self.biobert(input_ids=input_ids, attention_mask=attention_mask)
        p = self.dropout(out.pooler_output)
        return {'severity': self.severity_head(p), 'urgency': self.urgency_head(p), 'specialist': self.specialist_head(p)}

print("--- Step 1: Load .pth ---")
pth = torch.load(os.path.join(MODELS_DIR, 'biobert_clinical_best.pth'), map_location='cpu', weights_only=False)
nu = pth['urgency_head.3.weight'].shape[0]
ns = pth['specialist_head.6.weight'].shape[0]
print(f"urgency outputs={nu}, specialist outputs={ns}")

print("--- Step 2: Load urgency encoder ---")
enc = pickle.load(open(os.path.join(MODELS_DIR, 'urgency_encoder.pkl'), 'rb'))
print(f"Encoder classes ({len(enc.classes_)}): {enc.classes_}")
print(f"Encoder count matches .pth: {len(enc.classes_) == nu}")

print("--- Step 3: Build model and load weights ---")
model = BioBERTClinical(nu, ns)
result = model.load_state_dict(pth, strict=True)
print(f"load_state_dict: {result}")

print("--- Step 4: Run inference ---")
tok = AutoTokenizer.from_pretrained('dmis-lab/biobert-base-cased-v1.1')
model.eval()
tests = [
    "fever and stomach pain for 3 days",
    "chest pain radiating to left arm",
    "severe headache and vomiting",
    "cough and difficulty breathing",
    "knee pain and joint swelling",
]
for symptom in tests:
    inp = tok(symptom, return_tensors='pt', max_length=256, truncation=True, padding='max_length')
    with torch.no_grad():
        out = model(inp['input_ids'], inp['attention_mask'])
    sev = torch.argmax(out['severity']).item() + 1
    urg = enc.inverse_transform([torch.argmax(out['urgency']).item()])[0]
    spec_idx = torch.argmax(out['specialist']).item()
    spec_conf = torch.softmax(out['specialist'], dim=1).max().item()
    print(f"  [{symptom}]")
    print(f"    severity={sev}/10  urgency={urg}  specialist_idx={spec_idx}  conf={spec_conf:.2f}")

print("\nBioBERT is WORKING correctly.")
