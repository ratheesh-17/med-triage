"""
Fix existing appointments status from 'confirmed' to 'scheduled'
Run this once to migrate existing data
"""
from config.database import SessionLocal
from entity.models import Appointment

def fix_appointment_statuses():
    db = SessionLocal()
    try:
        # Find all appointments with 'confirmed' status
        confirmed_appointments = db.query(Appointment).filter(
            Appointment.status == "confirmed"
        ).all()
        
        print(f"Found {len(confirmed_appointments)} appointments with 'confirmed' status")
        
        # Update them to 'scheduled'
        for apt in confirmed_appointments:
            apt.status = "scheduled"
            print(f"Updated appointment {apt.id}: {apt.user_id} -> Doctor {apt.doctor_id}")
        
        db.commit()
        print(f"✅ Successfully updated {len(confirmed_appointments)} appointments to 'scheduled' status")
        
        # Show summary
        all_appointments = db.query(Appointment).all()
        print(f"\n📊 Current appointment status summary:")
        print(f"Total appointments: {len(all_appointments)}")
        scheduled = sum(1 for a in all_appointments if a.status == "scheduled")
        in_progress = sum(1 for a in all_appointments if a.status == "in-progress")
        completed = sum(1 for a in all_appointments if a.status == "completed")
        print(f"  - Scheduled: {scheduled}")
        print(f"  - In-Progress: {in_progress}")
        print(f"  - Completed: {completed}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_appointment_statuses()
