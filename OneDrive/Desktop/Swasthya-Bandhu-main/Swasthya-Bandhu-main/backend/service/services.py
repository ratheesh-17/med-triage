from dotenv import load_dotenv
load_dotenv()

from sqlalchemy.orm import Session
from repository.repositories import *
from config.database import get_db
from config.auth import create_access_token, generate_otp, verify_otp
from service.emergency import check_emergency, get_emergency_response
from service.ai_service import get_ai_clinical_assessment, get_longitudinal_risk_assessment, generate_followup_questions
from service.utils import find_nearest_doctors, find_nearest_emergency_hospital
from service.analytics import get_dashboard_analytics, detect_outbreaks, get_active_outbreak_alerts
import os

ADMIN_PHONE = os.getenv("ADMIN_PHONE", "9999999999")

class AuthService:
    @staticmethod
    def register_patient(db: Session, phone: str, name: str, age: int, gender: str):
        existing = UserRepository.find_by_phone(db, phone)
        if existing:
            raise ValueError("Phone already registered")
        
        user = UserRepository.create(db, phone, name, age, gender)
        token = create_access_token({"sub": str(user.id), "role": "patient", "phone": user.phone})
        return {"token": token, "user_id": user.id, "role": "patient"}
    
    @staticmethod
    def register_doctor(db: Session, data: dict):
        existing = DoctorRepository.find_by_phone(db, data["phone"])
        if existing:
            raise ValueError("Phone already registered")
        
        DoctorRepository.create(db, data)
        return {"message": "Registration submitted. Awaiting admin approval.", "status": "pending"}
    
    @staticmethod
    def login(db: Session, phone: str):
        if phone == ADMIN_PHONE:
            otp = generate_otp(phone)
            print(f"Admin OTP: {otp}")
            return {"role": "admin", "otp_sent": True, "message": "OTP sent"}
        
        doctor = DoctorRepository.find_by_phone(db, phone)
        if doctor:
            if doctor.verification_status != "approved":
                raise ValueError("Account pending approval")
            token = create_access_token({"sub": str(doctor.id), "role": "doctor", "phone": doctor.phone})
            return {"token": token, "role": "doctor", "doctor_id": doctor.id}
        
        user = UserRepository.find_by_phone(db, phone)
        if not user:
            raise ValueError("User not found")
        
        token = create_access_token({"sub": str(user.id), "role": "patient", "phone": user.phone})
        return {"token": token, "role": "patient", "user_id": user.id}
    
    @staticmethod
    def verify_admin_otp(phone: str, otp: str):
        if phone != ADMIN_PHONE:
            raise ValueError("Unauthorized")
        
        if not verify_otp(phone, otp):
            raise ValueError("Invalid OTP")
        
        token = create_access_token({"sub": "0", "role": "admin", "phone": phone})
        return {"token": token, "role": "admin"}

class ChatService:
    @staticmethod
    def process_symptoms(db: Session, user_id: int, symptom_text: str, user_lat: float = None, user_lng: float = None, answers: dict = None):
        # Check if this is initial message or follow-up
        if answers is None:
            # Initial message - check if we need clarification
            if ChatService._needs_clarification(symptom_text):
                # Generate AI-powered follow-up questions
                questions_data = generate_followup_questions(symptom_text)
                
                return {
                    "needs_clarification": True,
                    "questions": questions_data["questions"],
                    "reasoning": questions_data.get("reasoning", ""),
                    "message": "I need to ask you a few questions to better understand your condition."
                }
        
        # Check for emergency
        is_emergency, keyword = check_emergency(symptom_text)
        
        if is_emergency:
            emergency_data = get_emergency_response(keyword)
            user = UserRepository.find_by_id(db, user_id)
            nearest_hospital = None
            if user_lat and user_lng:
                nearest_hospital = find_nearest_emergency_hospital(user_lat, user_lng)
            
            ChatSessionRepository.create(
                db, user_id, symptom_text, emergency_data, 10, "IMMEDIATE", 
                "Emergency Medicine", [], [], []
            )
            
            return {
                "is_emergency": True,
                "needs_clarification": False,
                "severity_score": 10,
                "urgency": "IMMEDIATE",
                "emergency_contact": {
                    "name": user.emergency_contact_name,
                    "phone": user.emergency_contact_phone
                } if user.emergency_contact_phone else None,
                "nearest_hospital": nearest_hospital,
                "ambulance_number": "108",
                "immediate_actions": emergency_data["immediate_actions"]
            }
        
        # Get AI assessment with answers if provided
        ai_result = get_ai_clinical_assessment(symptom_text, answers)
        
        session = ChatSessionRepository.create(
            db, user_id, symptom_text, ai_result,
            ai_result["severity_score"], ai_result["urgency"],
            ai_result["recommended_specialist"], ai_result["risk_factors"],
            ai_result["suggested_tests"], ai_result["differential_diagnoses"]
        )
        
        sessions = ChatSessionRepository.find_by_user(db, user_id, limit=6)
        
        if len(sessions) >= 2:
            risk_data = get_longitudinal_risk_assessment([
                {"severity_score": s.severity_score, "symptom_input": s.symptom_input}
                for s in reversed(sessions)
            ])
            
            if risk_data:
                HealthRiskRepository.create(
                    db, user_id,
                    risk_data.get("cardiac_risk", 0),
                    risk_data.get("metabolic_risk", 0),
                    risk_data.get("neurological_risk", 0),
                    risk_data.get("respiratory_risk", 0),
                    risk_data.get("trend_direction", "stable")
                )
        
        return {
            "is_emergency": False,
            "needs_clarification": False,
            "severity_score": ai_result["severity_score"],
            "urgency": ai_result["urgency"],
            "risk_factors": ai_result["risk_factors"],
            "recommended_specialist": ai_result["recommended_specialist"],
            "suggested_tests": ai_result["suggested_tests"],
            "differential_diagnoses": ai_result["differential_diagnoses"],
            "clinical_summary": ai_result["clinical_summary"],
            "session_id": session.id,
            "ai_source": ai_result.get("source", "unknown")
        }
    
    @staticmethod
    def _needs_clarification(symptom_text: str) -> bool:
        """Check if symptom description is vague or critical"""
        text = symptom_text.lower()
        
        # Critical symptoms that need clarification
        critical = ["chest pain", "difficulty breathing", "severe headache", "abdominal pain", 
                   "fever", "dizziness", "numbness", "bleeding"]
        
        # Vague descriptions
        vague = ["not feeling well", "feeling sick", "unwell", "pain", "ache"]
        
        # Short descriptions (less than 10 words)
        word_count = len(symptom_text.split())
        
        has_critical = any(symptom in text for symptom in critical)
        has_vague = any(phrase in text for phrase in vague)
        is_short = word_count < 10
        
        return (has_critical and is_short) or has_vague

class DoctorService:
    @staticmethod
    def search_doctors(db: Session, specialization: str, user_lat: float, user_lng: float):
        doctors = DoctorRepository.find_by_specialization(db, specialization)
        if not doctors:
            return []
        
        nearest = find_nearest_doctors(user_lat, user_lng, doctors, limit=5)
        
        return [
            {
                "id": d.id,
                "name": d.name,
                "specialization": d.specialization,
                "hospital": d.hospital,
                "experience": d.experience,
                "fees": d.fees,
                "rating": d.rating,
                "distance_km": d.distance_km,
                "location": {"lat": d.location_lat, "lng": d.location_lng}
            }
            for d in nearest
        ]

class AdminService:
    @staticmethod
    def get_pending_doctors(db: Session):
        doctors = DoctorRepository.find_pending(db)
        return [
            {
                "id": d.id,
                "name": d.name,
                "phone": d.phone,
                "specialization": d.specialization,
                "hospital": d.hospital,
                "experience": d.experience,
                "medical_council_number": d.medical_council_number,
                "created_at": d.created_at.isoformat()
            }
            for d in doctors
        ]
    
    @staticmethod
    def approve_doctor(db: Session, admin_phone: str, doctor_id: int, approved: bool, reason: str = None):
        doctor = DoctorRepository.update_verification(db, doctor_id, approved, reason)
        
        AuditLogRepository.create(
            db, admin_phone, "doctor_verification", doctor_id, "doctor",
            {"approved": approved, "reason": reason}
        )
        
        return {"message": "Doctor verification updated"}
    
    @staticmethod
    def get_analytics(db: Session):
        analytics = get_dashboard_analytics(db)
        outbreaks = get_active_outbreak_alerts(db)
        return {"analytics": analytics, "outbreak_alerts": outbreaks}
    
    @staticmethod
    def detect_outbreaks(db: Session):
        new_alerts = detect_outbreaks(db)
        return {"message": "Outbreak detection completed", "new_alerts": len(new_alerts), "alerts": new_alerts}
