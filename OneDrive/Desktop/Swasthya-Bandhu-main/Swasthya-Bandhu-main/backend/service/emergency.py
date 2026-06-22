EMERGENCY_KEYWORDS = [
    'chest pain', 'heart attack', 'stroke', 'bleeding', 'unconscious',
    'difficulty breathing', 'choking', 'seizure', 'suicide', 'overdose',
    'severe burn', 'broken bone', 'severe bleeding', 'can\'t breathe',
    'unresponsive', 'collapsed', 'severe injury'
]

def check_emergency(symptom_text: str):
    text_lower = symptom_text.lower()
    for keyword in EMERGENCY_KEYWORDS:
        if keyword in text_lower:
            return True, keyword
    return False, None

def get_emergency_response(keyword: str):
    return {
        "is_emergency": True,
        "severity_score": 10,
        "urgency": "IMMEDIATE",
        "detected_keyword": keyword,
        "immediate_actions": [
            "Call 108 ambulance immediately",
            "Contact emergency contact",
            "Do not move unless necessary",
            "Stay calm and monitor breathing"
        ]
    }
