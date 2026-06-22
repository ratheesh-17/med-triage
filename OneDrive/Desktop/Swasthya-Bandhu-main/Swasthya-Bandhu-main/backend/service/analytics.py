from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta
from entity.models import ChatSession, User, Doctor, Appointment, OutbreakAlert
from collections import Counter

def get_dashboard_analytics(db: Session):
    today = datetime.now().strftime('%Y-%m-%d')
    month_start = datetime.now().replace(day=1).strftime('%Y-%m-%d')
    
    total_patients = db.query(User).filter(User.role == "patient").count()
    total_doctors = db.query(Doctor).filter(Doctor.verification_status == "approved").count()
    pending_verifications = db.query(Doctor).filter(Doctor.verification_status == "pending").count()
    appointments_today = db.query(Appointment).filter(Appointment.date == today).count()
    appointments_month = db.query(Appointment).filter(Appointment.date >= month_start).count()
    emergency_cases = db.query(ChatSession).filter(
        ChatSession.severity_score >= 9,
        ChatSession.created_at >= datetime.now() - timedelta(days=1)
    ).count()
    
    specialist_demand = db.query(
        ChatSession.recommended_specialist,
        func.count(ChatSession.id).label('count')
    ).filter(ChatSession.recommended_specialist.isnot(None)).group_by(ChatSession.recommended_specialist).order_by(func.count(ChatSession.id).desc()).limit(5).all()
    
    severity_ranges = {
        "low": db.query(ChatSession).filter(ChatSession.severity_score.between(1, 4)).count(),
        "moderate": db.query(ChatSession).filter(ChatSession.severity_score.between(5, 6)).count(),
        "high": db.query(ChatSession).filter(ChatSession.severity_score.between(7, 8)).count(),
        "emergency": db.query(ChatSession).filter(ChatSession.severity_score >= 9).count()
    }
    
    recent_sessions = db.query(ChatSession).order_by(ChatSession.created_at.desc()).limit(200).all()
    symptom_words = []
    for session in recent_sessions:
        words = [w.strip('.,!?').lower() for w in session.symptom_input.split() if len(w.strip('.,!?')) > 3]
        symptom_words.extend(words)
    top_symptoms = Counter(symptom_words).most_common(10)
    
    return {
        "platform_metrics": {
            "total_patients": total_patients,
            "total_doctors": total_doctors,
            "appointments_today": appointments_today,
            "appointments_month": appointments_month,
            "pending_verifications": pending_verifications,
            "emergency_cases": emergency_cases
        },
        "specialist_demand": [{"specialization": s[0], "count": s[1]} for s in specialist_demand],
        "urgency_distribution": [
            {"name": "Low (1-4)", "value": severity_ranges["low"], "color": "#52c41a"},
            {"name": "Moderate (5-6)", "value": severity_ranges["moderate"], "color": "#faad14"},
            {"name": "High (7-8)", "value": severity_ranges["high"], "color": "#ff7a45"},
            {"name": "Emergency (9-10)", "value": severity_ranges["emergency"], "color": "#f5222d"}
        ],
        "top_symptoms": [{"symptom": s[0].capitalize(), "count": s[1]} for s in top_symptoms]
    }

def detect_outbreaks(db: Session):
    seven_days_ago = datetime.now() - timedelta(days=7)
    
    recent_sessions = db.query(ChatSession).filter(
        ChatSession.created_at >= seven_days_ago
    ).all()
    
    symptom_clusters = {}
    
    for session in recent_sessions:
        user = db.query(User).filter(User.id == session.user_id).first()
        if not user:
            continue
        
        region = "Unknown"
        
        symptoms_lower = session.symptom_input.lower()
        
        fever_cough = ('fever' in symptoms_lower or 'temperature' in symptoms_lower) and \
                      ('cough' in symptoms_lower or 'cold' in symptoms_lower)
        
        if fever_cough:
            key = f"{region}_fever_cough"
            if key not in symptom_clusters:
                symptom_clusters[key] = {
                    "region": region,
                    "symptoms": ["fever", "cough"],
                    "count": 0
                }
            symptom_clusters[key]["count"] += 1
    
    alerts = []
    for key, cluster in symptom_clusters.items():
        if cluster["count"] >= 5:
            existing = db.query(OutbreakAlert).filter(
                OutbreakAlert.region == cluster["region"],
                OutbreakAlert.status == "active",
                OutbreakAlert.date_detected >= seven_days_ago
            ).first()
            
            if not existing:
                alert = OutbreakAlert(
                    region=cluster["region"],
                    symptom_cluster=cluster["symptoms"],
                    case_count=cluster["count"],
                    severity="moderate" if cluster["count"] < 10 else "high"
                )
                db.add(alert)
                db.commit()
                alerts.append(cluster)
    
    return alerts

def get_active_outbreak_alerts(db: Session):
    alerts = db.query(OutbreakAlert).filter(
        OutbreakAlert.status == "active"
    ).order_by(OutbreakAlert.date_detected.desc()).all()
    
    return [
        {
            "id": a.id,
            "region": a.region,
            "symptom_cluster": a.symptom_cluster,
            "case_count": a.case_count,
            "severity": a.severity,
            "date_detected": a.date_detected.isoformat()
        }
        for a in alerts
    ]
