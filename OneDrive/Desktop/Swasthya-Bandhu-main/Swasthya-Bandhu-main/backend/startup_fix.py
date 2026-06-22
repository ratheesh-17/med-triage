"""
Auto-fix appointment statuses on startup
"""
from config.database import SessionLocal
from entity.models import Appointment

def auto_fix_appointment_statuses():
    """Automatically fix appointment statuses from 'confirmed' to 'scheduled'"""
    try:
        db = SessionLocal()
        confirmed_appointments = db.query(Appointment).filter(
            Appointment.status == "confirmed"
        ).all()
        
        if confirmed_appointments:
            for apt in confirmed_appointments:
                apt.status = "scheduled"
            db.commit()
            print(f"✅ Auto-fixed {len(confirmed_appointments)} appointments: 'confirmed' -> 'scheduled'")
        
        db.close()
    except Exception as e:
        print(f"⚠️ Could not auto-fix appointments: {e}")

if __name__ == "__main__":
    auto_fix_appointment_statuses()
