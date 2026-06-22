from sqlalchemy.orm import Session
from entity.models import User, Doctor, ChatSession, HealthRiskScore, FamilyMember, Appointment, DoctorSlot, AuditLog, OutbreakAlert
from datetime import datetime

class UserRepository:
    @staticmethod
    def create(db: Session, phone: str, name: str, age: int, gender: str):
        user = User(phone=phone, name=name, age=age, gender=gender, role="patient")
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def find_by_phone(db: Session, phone: str):
        return db.query(User).filter(User.phone == phone).first()
    
    @staticmethod
    def find_by_id(db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

class DoctorRepository:
    @staticmethod
    def create(db: Session, data: dict):
        doctor = Doctor(**data, verification_status="pending")
        db.add(doctor)
        db.commit()
        db.refresh(doctor)
        return doctor
    
    @staticmethod
    def find_by_phone(db: Session, phone: str):
        return db.query(Doctor).filter(Doctor.phone == phone).first()
    
    @staticmethod
    def find_pending(db: Session):
        return db.query(Doctor).filter(Doctor.verification_status == "pending").all()
    
    @staticmethod
    def find_by_specialization(db: Session, specialization: str):
        return db.query(Doctor).filter(
            Doctor.specialization == specialization,
            Doctor.verification_status == "approved",
            Doctor.is_active == True
        ).all()
    
    @staticmethod
    def update_verification(db: Session, doctor_id: int, approved: bool, reason: str = None):
        doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
        if doctor:
            doctor.verification_status = "approved" if approved else "rejected"
            doctor.verified_at = datetime.utcnow() if approved else None
            doctor.rejection_reason = reason
            db.commit()
        return doctor

class ChatSessionRepository:
    @staticmethod
    def create(db: Session, user_id: int, symptom_input: str, ai_response: dict, severity_score: int, urgency: str, specialist: str, risk_factors: list, suggested_tests: list, differential_diagnoses: list):
        session = ChatSession(
            user_id=user_id,
            symptom_input=symptom_input,
            ai_response=ai_response,
            severity_score=severity_score,
            urgency=urgency,
            recommended_specialist=specialist,
            risk_factors=risk_factors,
            suggested_tests=suggested_tests,
            differential_diagnoses=differential_diagnoses
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        return session
    
    @staticmethod
    def find_by_user(db: Session, user_id: int, limit: int = 6):
        return db.query(ChatSession).filter(
            ChatSession.user_id == user_id
        ).order_by(ChatSession.created_at.desc()).limit(limit).all()

class HealthRiskRepository:
    @staticmethod
    def create(db: Session, user_id: int, cardiac: float, metabolic: float, neurological: float, respiratory: float, trend: str):
        overall = (cardiac + metabolic + neurological + respiratory) / 4
        risk = HealthRiskScore(
            user_id=user_id,
            cardiac_risk=cardiac,
            metabolic_risk=metabolic,
            neurological_risk=neurological,
            respiratory_risk=respiratory,
            overall_risk=overall,
            trend_direction=trend
        )
        db.add(risk)
        db.commit()
        return risk
    
    @staticmethod
    def find_by_user(db: Session, user_id: int, limit: int = 10):
        return db.query(HealthRiskScore).filter(
            HealthRiskScore.user_id == user_id
        ).order_by(HealthRiskScore.created_at.desc()).limit(limit).all()

class AppointmentRepository:
    @staticmethod
    def create(db: Session, user_id: int, doctor_id: int, date: str, time: str, slot_type: str, symptom_notes: str, family_member_id: int = None, chat_session_id: int = None):
        appointment = Appointment(
            user_id=user_id,
            doctor_id=doctor_id,
            family_member_id=family_member_id,
            chat_session_id=chat_session_id,
            date=date,
            time=time,
            slot_type=slot_type,
            symptom_notes=symptom_notes,
            status="scheduled"
        )
        db.add(appointment)
        db.commit()
        db.refresh(appointment)
        return appointment
    
    @staticmethod
    def find_by_user(db: Session, user_id: int):
        return db.query(Appointment).filter(
            Appointment.user_id == user_id
        ).order_by(Appointment.created_at.desc()).all()
    
    @staticmethod
    def find_by_doctor(db: Session, doctor_id: int):
        return db.query(Appointment).filter(
            Appointment.doctor_id == doctor_id
        ).order_by(Appointment.date, Appointment.time).all()

class FamilyMemberRepository:
    @staticmethod
    def create(db: Session, user_id: int, name: str, age: int, relationship: str):
        member = FamilyMember(user_id=user_id, name=name, age=age, relationship=relationship)
        db.add(member)
        db.commit()
        db.refresh(member)
        return member
    
    @staticmethod
    def find_by_user(db: Session, user_id: int):
        return db.query(FamilyMember).filter(FamilyMember.user_id == user_id).all()
    
    @staticmethod
    def find_by_id(db: Session, member_id: int, user_id: int):
        return db.query(FamilyMember).filter(
            FamilyMember.id == member_id,
            FamilyMember.user_id == user_id
        ).first()
    
    @staticmethod
    def delete(db: Session, member_id: int, user_id: int):
        member = db.query(FamilyMember).filter(
            FamilyMember.id == member_id,
            FamilyMember.user_id == user_id
        ).first()
        if member:
            db.delete(member)
            db.commit()
        return member

class DoctorSlotRepository:
    @staticmethod
    def create_slots(db: Session, doctor_id: int, date: str, times: list):
        for time in times:
            slot = DoctorSlot(doctor_id=doctor_id, date=date, time=time, is_available=True)
            db.add(slot)
        db.commit()
    
    @staticmethod
    def find_available(db: Session, doctor_id: int, date: str):
        return db.query(DoctorSlot).filter(
            DoctorSlot.doctor_id == doctor_id,
            DoctorSlot.date == date,
            DoctorSlot.is_available == True
        ).all()
    
    @staticmethod
    def mark_unavailable(db: Session, doctor_id: int, date: str, time: str):
        slot = db.query(DoctorSlot).filter(
            DoctorSlot.doctor_id == doctor_id,
            DoctorSlot.date == date,
            DoctorSlot.time == time,
            DoctorSlot.is_available == True
        ).first()
        if slot:
            slot.is_available = False
            db.commit()
        return slot

class AuditLogRepository:
    @staticmethod
    def create(db: Session, admin_phone: str, action_type: str, target_id: int, target_type: str, details: dict):
        log = AuditLog(
            admin_phone=admin_phone,
            action_type=action_type,
            target_id=target_id,
            target_type=target_type,
            details=details
        )
        db.add(log)
        db.commit()
