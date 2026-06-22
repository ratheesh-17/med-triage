from config.database import SessionLocal
from entity.models import Doctor

db = SessionLocal()

print("=== ALL DOCTORS IN DATABASE ===")
doctors = db.query(Doctor).all()
print(f"Total doctors: {len(doctors)}")

for doc in doctors:
    print(f"\nID: {doc.id}")
    print(f"Name: {doc.name}")
    print(f"Phone: {doc.phone}")
    print(f"Specialization: {doc.specialization}")
    print(f"Status: {doc.verification_status}")
    print(f"Medical Council: {doc.medical_council_number}")
    print("-" * 50)

print("\n=== PENDING DOCTORS ===")
pending = db.query(Doctor).filter(Doctor.verification_status == "pending").all()
print(f"Total pending: {len(pending)}")

for doc in pending:
    print(f"ID: {doc.id}, Name: {doc.name}, Phone: {doc.phone}")

db.close()
