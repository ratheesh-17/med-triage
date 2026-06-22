from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship as db_relationship
from datetime import datetime
from config.database import Base
import enum

class RoleEnum(enum.Enum):
    PATIENT = "patient"
    DOCTOR = "doctor"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String(15), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(10), nullable=False)
    role = Column(String(20), default="patient")
    emergency_contact_phone = Column(String(15))
    emergency_contact_name = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    family_members = db_relationship("FamilyMember", back_populates="user", cascade="all, delete-orphan")
    appointments = db_relationship("Appointment", back_populates="user", cascade="all, delete-orphan")
    chat_sessions = db_relationship("ChatSession", back_populates="user", cascade="all, delete-orphan")
    health_risk_scores = db_relationship("HealthRiskScore", back_populates="user", cascade="all, delete-orphan")

class Doctor(Base):
    __tablename__ = "doctors"
    
    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String(15), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    specialization = Column(String(100), nullable=False, index=True)
    hospital = Column(String(200), nullable=False)
    experience = Column(String(50), nullable=False)
    fees = Column(Integer, nullable=False)
    location_lat = Column(Float, nullable=False)
    location_lng = Column(Float, nullable=False)
    medical_council_number = Column(String(50), unique=True, nullable=False)
    rating = Column(Float, default=4.5)
    verification_status = Column(String(20), default="pending", index=True)
    rejection_reason = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    verified_at = Column(DateTime)
    is_active = Column(Boolean, default=True)
    
    appointments = db_relationship("Appointment", back_populates="doctor")
    slots = db_relationship("DoctorSlot", back_populates="doctor", cascade="all, delete-orphan")

class FamilyMember(Base):
    __tablename__ = "family_members"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    relationship = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = db_relationship("User", back_populates="family_members")
    appointments = db_relationship("Appointment", back_populates="family_member")

class DoctorSlot(Base):
    __tablename__ = "doctor_slots"
    
    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    date = Column(String(20), nullable=False, index=True)
    time = Column(String(20), nullable=False)
    is_available = Column(Boolean, default=True)
    
    doctor = db_relationship("Doctor", back_populates="slots")

class Appointment(Base):
    __tablename__ = "appointments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    family_member_id = Column(Integer, ForeignKey("family_members.id"))
    chat_session_id = Column(Integer, ForeignKey("chat_sessions.id"))
    date = Column(String(20), nullable=False, index=True)
    time = Column(String(20), nullable=False)
    slot_type = Column(String(20), nullable=False)
    symptom_notes = Column(Text)
    status = Column(String(20), default="scheduled", index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = db_relationship("User", back_populates="appointments")
    doctor = db_relationship("Doctor", back_populates="appointments")
    family_member = db_relationship("FamilyMember", back_populates="appointments")
    chat_session = db_relationship("ChatSession")

class ChatSession(Base):
    __tablename__ = "chat_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    family_member_id = Column(Integer, ForeignKey("family_members.id"))
    symptom_input = Column(Text, nullable=False)
    ai_response = Column(JSON, nullable=False)
    severity_score = Column(Integer, nullable=False, index=True)
    urgency = Column(String(50), nullable=False)
    recommended_specialist = Column(String(100))
    risk_factors = Column(JSON)
    suggested_tests = Column(JSON)
    differential_diagnoses = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    user = db_relationship("User", back_populates="chat_sessions")

class HealthRiskScore(Base):
    __tablename__ = "health_risk_scores"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    cardiac_risk = Column(Float, default=0.0)
    metabolic_risk = Column(Float, default=0.0)
    neurological_risk = Column(Float, default=0.0)
    respiratory_risk = Column(Float, default=0.0)
    overall_risk = Column(Float, default=0.0)
    trend_direction = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    user = db_relationship("User", back_populates="health_risk_scores")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    admin_phone = Column(String(15), nullable=False)
    action_type = Column(String(50), nullable=False, index=True)
    target_id = Column(Integer)
    target_type = Column(String(50))
    details = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

class OutbreakAlert(Base):
    __tablename__ = "outbreak_alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    region = Column(String(100), nullable=False, index=True)
    symptom_cluster = Column(JSON, nullable=False)
    case_count = Column(Integer, nullable=False)
    severity = Column(String(20), nullable=False)
    date_detected = Column(DateTime, default=datetime.utcnow, index=True)
    status = Column(String(20), default="active")
