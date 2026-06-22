from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from config.database import get_db
from datetime import datetime
from entity.models import ChatSession, User, Doctor
from service.services import AuthService, ChatService, DoctorService, AdminService
from repository.repositories import *
from config.auth import get_current_user
from service.pdf_service import generate_session_report
from service.government_report import generate_government_report

router = APIRouter()

# Schemas
class PatientRegister(BaseModel):
    phone: str
    name: str
    age: int
    gender: str

class DoctorRegister(BaseModel):
    phone: str
    name: str
    specialization: str
    hospital: str
    experience: str
    fees: int
    location_lat: float
    location_lng: float
    medical_council_number: str

class LoginRequest(BaseModel):
    phone: str

class OTPVerify(BaseModel):
    phone: str
    otp: str

class ChatRequest(BaseModel):
    symptom_text: str
    user_lat: Optional[float] = None
    user_lng: Optional[float] = None

class DoctorApproval(BaseModel):
    doctor_id: int
    approved: bool
    rejection_reason: Optional[str] = None

class SlotCreate(BaseModel):
    date: str
    times: List[str]

class AppointmentCreate(BaseModel):
    doctor_id: int
    date: str
    time: str
    slot_type: str
    symptom_notes: str
    family_member_id: Optional[int] = None

class FamilyMemberCreate(BaseModel):
    name: str
    age: int
    relationship: str

# Auth Endpoints
@router.post("/auth/patient/register")
def register_patient(data: PatientRegister, db: Session = Depends(get_db)):
    try:
        return AuthService.register_patient(db, data.phone, data.name, data.age, data.gender)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/auth/doctor/register")
def register_doctor(data: DoctorRegister, db: Session = Depends(get_db)):
    try:
        print(f"\n=== DOCTOR REGISTRATION DEBUG ===")
        print(f"Phone received: '{data.phone}'")
        print(f"Name: {data.name}")
        print(f"Full payload: {data.dict()}")
        result = AuthService.register_doctor(db, data.dict())
        print(f"Registration successful!")
        return result
    except ValueError as e:
        print(f"ValueError: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Unexpected error: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/auth/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    try:
        return AuthService.login(db, data.phone)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/auth/admin/verify-otp")
def verify_admin_otp(data: OTPVerify):
    try:
        return AuthService.verify_admin_otp(data.phone, data.otp)
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))

class ChatRequest(BaseModel):
    symptom_text: str
    user_lat: Optional[float] = None
    user_lng: Optional[float] = None
    answers: Optional[dict] = None  # Follow-up question answers

# Chat Endpoint
@router.post("/chat")
def chat(data: ChatRequest, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user["role"] != "patient":
        raise HTTPException(status_code=403, detail="Only patients can chat")
    
    return ChatService.process_symptoms(
        db, int(current_user["sub"]), 
        data.symptom_text, data.user_lat, data.user_lng,
        data.answers  # Pass answers if provided
    )

@router.get("/patient/profile")
def get_patient_profile(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user["role"] != "patient":
        raise HTTPException(status_code=403, detail="Patient only")
    
    user = db.query(User).filter(User.id == int(current_user["sub"])).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": user.id,
        "name": user.name,
        "phone": user.phone,
        "age": user.age,
        "gender": user.gender
    }

@router.get("/patient/sessions")
def get_patient_sessions(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user["role"] != "patient":
        raise HTTPException(status_code=403, detail="Patient only")
    
    sessions = ChatSessionRepository.find_by_user(db, int(current_user["sub"]), limit=5)
    return {
        "sessions": [
            {
                "id": s.id,
                "symptom_input": s.symptom_input,
                "severity_score": s.severity_score,
                "urgency": s.urgency,
                "recommended_specialist": s.recommended_specialist,
                "created_at": s.created_at.isoformat()
            }
            for s in sessions
        ]
    }

# Doctor Endpoints
@router.get("/doctors/search")
def search_doctors(
    specialization: str,
    user_lat: str,
    user_lng: str,
    db: Session = Depends(get_db)
):
    try:
        lat = float(user_lat)
        lng = float(user_lng)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid coordinates")
    
    doctors = DoctorService.search_doctors(db, specialization, lat, lng)
    return {"doctors": doctors}

@router.get("/doctors/{doctor_id}")
def get_doctor_by_id(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    return {
        "id": doctor.id,
        "name": doctor.name,
        "specialization": doctor.specialization,
        "hospital": doctor.hospital,
        "experience": doctor.experience,
        "fees": doctor.fees,
        "rating": doctor.rating,
        "location_lat": doctor.location_lat,
        "location_lng": doctor.location_lng
    }

@router.post("/doctor/slots")
def create_slots(data: SlotCreate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user["role"] != "doctor":
        raise HTTPException(status_code=403, detail="Doctor only")
    
    DoctorSlotRepository.create_slots(db, int(current_user["sub"]), data.date, data.times)
    return {"message": "Slots created"}

@router.get("/doctor/slots/{doctor_id}")
def get_doctor_slots(doctor_id: int, date: str, db: Session = Depends(get_db)):
    slots = DoctorSlotRepository.find_available(db, doctor_id, date)
    return {"slots": [s.time for s in slots]}

@router.get("/doctor/profile")
def get_doctor_profile(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user["role"] != "doctor":
        raise HTTPException(status_code=403, detail="Doctor only")
    
    doctor_id = int(current_user["sub"])
    print(f"\n=== DOCTOR PROFILE REQUEST ===")
    print(f"Token doctor_id: {doctor_id}")
    print(f"Token phone: {current_user.get('phone')}")
    
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    print(f"Found doctor: ID={doctor.id}, Name={doctor.name}, Phone={doctor.phone}")
    
    return {
        "id": doctor.id,
        "name": doctor.name,
        "phone": doctor.phone,
        "specialization": doctor.specialization,
        "hospital": doctor.hospital,
        "experience": doctor.experience,
        "fees": doctor.fees,
        "rating": doctor.rating,
        "medical_council_number": doctor.medical_council_number
    }

@router.get("/doctor/dashboard")
def doctor_dashboard(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user["role"] != "doctor":
        raise HTTPException(status_code=403, detail="Doctor only")
    
    appointments = AppointmentRepository.find_by_doctor(db, int(current_user["sub"]))
    
    total = len(appointments)
    today = sum(1 for a in appointments if a.date == datetime.now().strftime('%Y-%m-%d'))
    high_severity = sum(1 for a in appointments if a.chat_session_id and 
                       db.query(ChatSession).filter(ChatSession.id == a.chat_session_id).first().severity_score >= 7)
    
    return {
        "total_cases": total,
        "today_cases": today,
        "high_severity_cases": high_severity,
        "avg_severity": 6.5
    }

@router.get("/doctor/analytics")
def doctor_analytics(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user["role"] != "doctor":
        raise HTTPException(status_code=403, detail="Doctor only")
    
    appointments = AppointmentRepository.find_by_doctor(db, int(current_user["sub"]))
    doctor = db.query(Doctor).filter(Doctor.id == int(current_user["sub"])).first()
    
    # Severity distribution
    severity_dist = {"low": 0, "moderate": 0, "high": 0, "emergency": 0}
    for apt in appointments:
        if apt.chat_session_id:
            session = db.query(ChatSession).filter(ChatSession.id == apt.chat_session_id).first()
            if session:
                score = session.severity_score
                if score <= 4: severity_dist["low"] += 1
                elif score <= 6: severity_dist["moderate"] += 1
                elif score <= 8: severity_dist["high"] += 1
                else: severity_dist["emergency"] += 1
    
    return {
        "total_appointments": len(appointments),
        "avg_rating": doctor.rating if doctor else 0,
        "severity_distribution": [
            {"name": "Low (1-4)", "value": severity_dist["low"], "color": "#52c41a"},
            {"name": "Moderate (5-6)", "value": severity_dist["moderate"], "color": "#faad14"},
            {"name": "High (7-8)", "value": severity_dist["high"], "color": "#ff7a45"},
            {"name": "Emergency (9-10)", "value": severity_dist["emergency"], "color": "#f5222d"}
        ]
    }

# Appointment Endpoints
@router.post("/appointments")
def book_appointment(data: AppointmentCreate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user["role"] != "patient":
        raise HTTPException(status_code=403, detail="Patient only")
    
    if data.family_member_id:
        member = FamilyMemberRepository.find_by_id(db, data.family_member_id, int(current_user["sub"]))
        if not member:
            raise HTTPException(status_code=400, detail="Invalid family member")
    
    slot = DoctorSlotRepository.mark_unavailable(db, data.doctor_id, data.date, data.time)
    if not slot:
        try:
            DoctorSlotRepository.create_slots(db, data.doctor_id, data.date, [data.time])
            slot = DoctorSlotRepository.mark_unavailable(db, data.doctor_id, data.date, data.time)
        except:
            pass
    
    latest_session = ChatSessionRepository.find_by_user(db, int(current_user["sub"]), limit=1)
    chat_session_id = latest_session[0].id if latest_session else None
    
    appointment = AppointmentRepository.create(
        db, int(current_user["sub"]), data.doctor_id, data.date, data.time,
        data.slot_type, data.symptom_notes, data.family_member_id, chat_session_id
    )
    
    return {"message": "Appointment booked", "appointment_id": appointment.id}

@router.get("/appointments")
def get_appointments(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    print(f"\n=== GET APPOINTMENTS DEBUG ===")
    print(f"User role: {current_user['role']}")
    print(f"User ID: {current_user['sub']}")
    
    if current_user["role"] == "patient":
        appointments = AppointmentRepository.find_by_user(db, int(current_user["sub"]))
    elif current_user["role"] == "doctor":
        appointments = AppointmentRepository.find_by_doctor(db, int(current_user["sub"]))
        print(f"Found {len(appointments)} appointments for doctor {current_user['sub']}")
    else:
        raise HTTPException(status_code=403, detail="Invalid role")
    
    result = []
    for apt in appointments:
        doctor = db.query(Doctor).filter(Doctor.id == apt.doctor_id).first()
        user = db.query(User).filter(User.id == apt.user_id).first()
        
        print(f"Appointment {apt.id}: Status={apt.status}, Date={apt.date}, ChatSession={apt.chat_session_id}")
        
        apt_data = {
            "id": apt.id,
            "date": apt.date,
            "time": apt.time,
            "slot_type": apt.slot_type,
            "symptom_notes": apt.symptom_notes,
            "status": apt.status
        }
        
        if current_user["role"] == "patient":
            apt_data["doctor"] = {
                "name": doctor.name,
                "specialization": doctor.specialization,
                "hospital": doctor.hospital
            }
        else:
            apt_data["patient"] = {
                "name": user.name,
                "age": user.age,
                "gender": user.gender
            }
            apt_data["payment_amount"] = doctor.fees
            apt_data["payment_status"] = "paid"
            
            if apt.chat_session_id:
                session = db.query(ChatSession).filter(ChatSession.id == apt.chat_session_id).first()
                if session:
                    print(f"  -> Has AI triage: Severity={session.severity_score}, Urgency={session.urgency}")
                    apt_data["pre_consult_summary"] = {
                        "severity_score": session.severity_score,
                        "urgency": session.urgency,
                        "risk_factors": session.risk_factors,
                        "suggested_tests": session.suggested_tests,
                        "differential_diagnoses": session.differential_diagnoses
                    }
                else:
                    print(f"  -> ChatSession {apt.chat_session_id} not found")
            else:
                print(f"  -> No chat_session_id")
        
        result.append(apt_data)
    
    print(f"Returning {len(result)} appointments")
    return {"appointments": result}

@router.patch("/appointments/{appointment_id}/start")
def start_consultation(appointment_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user["role"] != "doctor":
        raise HTTPException(status_code=403, detail="Doctor only")
    
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    appointment.status = "in-progress"
    db.commit()
    
    return {"message": "Consultation started", "appointment_id": appointment.id}

@router.patch("/appointments/{appointment_id}/complete")
def mark_appointment_complete(appointment_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user["role"] != "doctor":
        raise HTTPException(status_code=403, detail="Doctor only")
    
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    appointment.status = "completed"
    db.commit()
    
    return {"message": "Appointment marked as completed"}

# Family Endpoints
@router.post("/family")
def add_family_member(data: FamilyMemberCreate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user["role"] != "patient":
        raise HTTPException(status_code=403, detail="Patient only")
    
    member = FamilyMemberRepository.create(db, int(current_user["sub"]), data.name, data.age, data.relationship)
    return {"message": "Family member added", "member_id": member.id}

@router.get("/family")
def get_family_members(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user["role"] != "patient":
        raise HTTPException(status_code=403, detail="Patient only")
    
    members = FamilyMemberRepository.find_by_user(db, int(current_user["sub"]))
    return {
        "family_members": [
            {"id": m.id, "name": m.name, "age": m.age, "relationship": m.relationship}
            for m in members
        ]
    }

@router.delete("/family/{member_id}")
def remove_family_member(member_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user["role"] != "patient":
        raise HTTPException(status_code=403, detail="Patient only")
    
    member = FamilyMemberRepository.delete(db, member_id, int(current_user["sub"]))
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    return {"message": "Family member removed"}

# Health Risk Endpoint
@router.get("/health-risk")
def get_health_risk(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user["role"] != "patient":
        raise HTTPException(status_code=403, detail="Patient only")
    
    risk_scores = HealthRiskRepository.find_by_user(db, int(current_user["sub"]), limit=10)
    
    if not risk_scores:
        return {"has_data": False, "message": "Need more sessions for risk analysis"}
    
    latest = risk_scores[0]
    
    return {
        "has_data": True,
        "current_risk": {
            "cardiac": latest.cardiac_risk,
            "metabolic": latest.metabolic_risk,
            "neurological": latest.neurological_risk,
            "respiratory": latest.respiratory_risk,
            "overall": latest.overall_risk,
            "trend": latest.trend_direction
        },
        "history": [
            {
                "date": r.created_at.isoformat(),
                "cardiac": r.cardiac_risk,
                "metabolic": r.metabolic_risk,
                "neurological": r.neurological_risk,
                "respiratory": r.respiratory_risk,
                "overall": r.overall_risk
            }
            for r in reversed(risk_scores)
        ]
    }

# PDF Report Endpoint
@router.get("/session/{session_id}/report")
def download_report(session_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if current_user["role"] == "patient" and session.user_id != int(current_user["sub"]):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    user = db.query(User).filter(User.id == session.user_id).first()
    
    session_data = {
        "symptom_input": session.symptom_input,
        "severity_score": session.severity_score,
        "urgency": session.urgency,
        "recommended_specialist": session.recommended_specialist,
        "risk_factors": session.risk_factors or [],
        "suggested_tests": session.suggested_tests or [],
        "differential_diagnoses": session.differential_diagnoses or []
    }
    
    user_data = {
        "id": user.id,
        "name": user.name,
        "age": user.age,
        "gender": user.gender
    }
    
    filepath = generate_session_report(session_data, user_data)
    return {"message": "Report generated", "filepath": filepath}

# Admin Endpoints
@router.get("/admin/doctors/pending")
def get_pending_doctors(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    
    doctors = AdminService.get_pending_doctors(db)
    return {"doctors": doctors}

@router.post("/admin/doctors/approve")
def approve_doctor(data: DoctorApproval, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    
    return AdminService.approve_doctor(db, current_user["phone"], data.doctor_id, data.approved, data.rejection_reason)

@router.get("/admin/analytics")
def admin_analytics(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    
    return AdminService.get_analytics(db)

@router.post("/admin/detect-outbreaks")
def trigger_outbreak_detection(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    
    return AdminService.detect_outbreaks(db)

# Admin Debug Endpoints
@router.get("/admin/debug/system-status")
def get_system_status(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Complete system status for debugging"""
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    
    # Count all entities
    total_users = db.query(User).count()
    total_doctors = db.query(Doctor).count()
    pending_doctors = db.query(Doctor).filter(Doctor.verification_status == "pending").count()
    approved_doctors = db.query(Doctor).filter(Doctor.verification_status == "approved").count()
    rejected_doctors = db.query(Doctor).filter(Doctor.verification_status == "rejected").count()
    total_appointments = db.query(Appointment).count()
    total_chat_sessions = db.query(ChatSession).count()
    
    # Get recent registrations
    recent_doctors = db.query(Doctor).order_by(Doctor.created_at.desc()).limit(5).all()
    recent_users = db.query(User).order_by(User.created_at.desc()).limit(5).all()
    
    return {
        "status": "operational",
        "counts": {
            "total_patients": total_users,
            "total_doctors": total_doctors,
            "pending_doctors": pending_doctors,
            "approved_doctors": approved_doctors,
            "rejected_doctors": rejected_doctors,
            "total_appointments": total_appointments,
            "total_ai_sessions": total_chat_sessions
        },
        "recent_doctors": [
            {
                "id": d.id,
                "name": d.name,
                "phone": d.phone,
                "status": d.verification_status,
                "registered_at": d.created_at.isoformat()
            }
            for d in recent_doctors
        ],
        "recent_patients": [
            {
                "id": u.id,
                "name": u.name,
                "phone": u.phone,
                "registered_at": u.created_at.isoformat()
            }
            for u in recent_users
        ]
    }

@router.get("/admin/debug/doctor/{doctor_id}")
def get_doctor_details(doctor_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get complete doctor details for debugging"""
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    appointments = db.query(Appointment).filter(Appointment.doctor_id == doctor_id).all()
    
    return {
        "doctor": {
            "id": doctor.id,
            "name": doctor.name,
            "phone": doctor.phone,
            "specialization": doctor.specialization,
            "hospital": doctor.hospital,
            "experience": doctor.experience,
            "fees": doctor.fees,
            "location": {"lat": doctor.location_lat, "lng": doctor.location_lng},
            "medical_council_number": doctor.medical_council_number,
            "verification_status": doctor.verification_status,
            "rating": doctor.rating,
            "created_at": doctor.created_at.isoformat(),
            "verified_at": doctor.verified_at.isoformat() if doctor.verified_at else None
        },
        "appointments_count": len(appointments),
        "recent_appointments": [
            {
                "id": a.id,
                "patient_id": a.user_id,
                "date": a.date,
                "time": a.time,
                "status": a.status
            }
            for a in appointments[:5]
        ]
    }

@router.get("/admin/debug/workflow-test")
def test_workflow(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Test complete workflow connectivity"""
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    
    tests = {
        "database_connection": False,
        "doctors_table": False,
        "users_table": False,
        "appointments_table": False,
        "pending_doctors_query": False,
        "approved_doctors_query": False,
        "doctor_search_query": False
    }
    
    try:
        # Test database connection
        db.execute("SELECT 1")
        tests["database_connection"] = True
        
        # Test doctors table
        db.query(Doctor).first()
        tests["doctors_table"] = True
        
        # Test users table
        db.query(User).first()
        tests["users_table"] = True
        
        # Test appointments table
        db.query(Appointment).first()
        tests["appointments_table"] = True
        
        # Test pending doctors query
        pending = db.query(Doctor).filter(Doctor.verification_status == "pending").all()
        tests["pending_doctors_query"] = True
        tests["pending_count"] = len(pending)
        
        # Test approved doctors query
        approved = db.query(Doctor).filter(Doctor.verification_status == "approved").all()
        tests["approved_doctors_query"] = True
        tests["approved_count"] = len(approved)
        
        # Test doctor search query
        searchable = db.query(Doctor).filter(
            Doctor.verification_status == "approved",
            Doctor.is_active == True
        ).all()
        tests["doctor_search_query"] = True
        tests["searchable_count"] = len(searchable)
        
    except Exception as e:
        tests["error"] = str(e)
    
    all_passed = all([v for k, v in tests.items() if isinstance(v, bool)])
    
    return {
        "overall_status": "PASS" if all_passed else "FAIL",
        "tests": tests,
        "message": "All workflow tests passed!" if all_passed else "Some tests failed. Check details."
    }

# Admin User Management Endpoints
@router.get("/admin/users")
def get_all_users(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    
    users = db.query(User).order_by(User.created_at.desc()).all()
    return {
        "users": [
            {
                "id": u.id,
                "name": u.name,
                "phone": u.phone,
                "age": u.age,
                "gender": u.gender,
                "created_at": u.created_at.isoformat()
            }
            for u in users
        ]
    }

@router.get("/admin/doctors")
def get_all_doctors(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    
    doctors = db.query(Doctor).order_by(Doctor.created_at.desc()).all()
    return {
        "doctors": [
            {
                "id": d.id,
                "name": d.name,
                "phone": d.phone,
                "specialization": d.specialization,
                "hospital": d.hospital,
                "experience": d.experience,
                "fees": d.fees,
                "medical_council_number": d.medical_council_number,
                "verification_status": d.verification_status,
                "is_active": d.is_active,
                "rating": d.rating,
                "created_at": d.created_at.isoformat()
            }
            for d in doctors
        ]
    }

@router.delete("/admin/users/{user_id}")
def delete_user(user_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    
    AuditLogRepository.create(
        db, current_user["phone"], "user_deletion", user_id, "user",
        {"name": user.name, "phone": user.phone}
    )
    
    return {"message": "User deleted successfully"}

@router.delete("/admin/doctors/{doctor_id}")
def delete_doctor(doctor_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    db.delete(doctor)
    db.commit()
    
    AuditLogRepository.create(
        db, current_user["phone"], "doctor_deletion", doctor_id, "doctor",
        {"name": doctor.name, "phone": doctor.phone}
    )
    
    return {"message": "Doctor deleted successfully"}

@router.post("/admin/generate-government-report")
def generate_govt_report(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Generate comprehensive government health report"""
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    
    try:
        report = generate_government_report(db)
        return report
    except Exception as e:
        import traceback
        error_detail = f"Report generation failed: {str(e)}\n{traceback.format_exc()}"
        print(error_detail)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/admin/fix-appointment-status")
def fix_appointment_status(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Fix appointment statuses from 'confirmed' to 'scheduled'"""
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    
    confirmed = db.query(Appointment).filter(Appointment.status == "confirmed").all()
    for apt in confirmed:
        apt.status = "scheduled"
    db.commit()
    
    return {"message": f"Updated {len(confirmed)} appointments from 'confirmed' to 'scheduled'", "count": len(confirmed)}
