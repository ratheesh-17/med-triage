from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from entity.models import User, Doctor, ChatSession, Appointment, OutbreakAlert
from collections import Counter
import json

def generate_government_report(db: Session):
    """Generate comprehensive government health report"""
    
    # Collect all platform data
    total_patients = db.query(User).count()
    total_doctors = db.query(Doctor).filter(Doctor.verification_status == "approved").count()
    total_appointments = db.query(Appointment).count()
    
    # Get recent data (last 30 days)
    thirty_days_ago = datetime.now() - timedelta(days=30)
    recent_sessions = db.query(ChatSession).filter(ChatSession.created_at >= thirty_days_ago).all()
    
    # Symptom analysis
    severity_distribution = {"low": 0, "moderate": 0, "high": 0, "emergency": 0}
    specialist_demand = Counter()
    
    for session in recent_sessions:
        if session.severity_score <= 4:
            severity_distribution["low"] += 1
        elif session.severity_score <= 6:
            severity_distribution["moderate"] += 1
        elif session.severity_score <= 8:
            severity_distribution["high"] += 1
        else:
            severity_distribution["emergency"] += 1
        
        if session.recommended_specialist:
            specialist_demand[session.recommended_specialist] += 1
    
    # Outbreak data
    active_outbreaks = db.query(OutbreakAlert).filter(OutbreakAlert.status == "active").all()
    
    # Doctor distribution
    doctor_specializations = db.query(Doctor.specialization).filter(
        Doctor.verification_status == "approved"
    ).all()
    specialization_count = Counter([d[0] for d in doctor_specializations])
    
    # Prepare data summary
    data_summary = {
        "platform_overview": {
            "total_patients": total_patients,
            "total_doctors": total_doctors,
            "total_appointments": total_appointments,
            "analysis_period": "Last 30 days"
        },
        "health_trends": {
            "total_consultations": len(recent_sessions),
            "severity_distribution": severity_distribution,
            "specialist_demand": dict(specialist_demand.most_common(10))
        },
        "outbreak_alerts": [
            {
                "region": o.region,
                "symptoms": o.symptom_cluster,
                "cases": o.case_count,
                "severity": o.severity
            }
            for o in active_outbreaks
        ],
        "healthcare_capacity": {
            "doctor_distribution": dict(specialization_count),
            "demand_vs_supply": dict(specialist_demand.most_common(5))
        }
    }
    
    # Generate analysis
    total_cases = len(recent_sessions)
    emergency_rate = (severity_distribution['emergency'] / total_cases * 100) if total_cases > 0 else 0
    
    analysis = f"""GOVERNMENT HEALTH REPORT - COMPREHENSIVE ANALYSIS

1. EXECUTIVE SUMMARY
   Platform serves {total_patients} patients with {total_doctors} verified doctors.
   {total_cases} consultations in last 30 days.
   Emergency rate: {emergency_rate:.1f}%
   Active outbreaks: {len(active_outbreaks)}

2. SEVERITY DISTRIBUTION
   - Low (1-4): {severity_distribution['low']} cases
   - Moderate (5-6): {severity_distribution['moderate']} cases
   - High (7-8): {severity_distribution['high']} cases
   - Emergency (9-10): {severity_distribution['emergency']} cases

3. SPECIALIST DEMAND (Top 5)
{chr(10).join([f'   - {spec}: {count} consultations' for spec, count in list(specialist_demand.most_common(5))])}

4. HEALTHCARE CAPACITY
{chr(10).join([f'   - {spec}: {count} doctors' for spec, count in list(specialization_count.most_common(5))])}

5. OUTBREAK ALERTS
{chr(10).join([f'   - {o["region"]}: {o["cases"]} cases ({o["severity"]} severity)' for o in data_summary['outbreak_alerts']]) if active_outbreaks else '   No active outbreaks'}

6. RECOMMENDATIONS
   IMMEDIATE: {'Deploy emergency response' if emergency_rate > 5 else 'Continue monitoring'}
   MEDIUM-TERM: Recruit specialists in high-demand areas
   LONG-TERM: Expand healthcare infrastructure

7. RISK LEVEL: {'HIGH' if emergency_rate > 5 or active_outbreaks else 'MODERATE' if emergency_rate > 3 else 'LOW'}
"""
    
    return {
        "report_generated_at": datetime.now().isoformat(),
        "data_summary": data_summary,
        "ai_analysis": analysis,
        "report_period": "Last 30 days",
        "platform_name": "Swasthya Bandhu Healthcare Platform"
    }
