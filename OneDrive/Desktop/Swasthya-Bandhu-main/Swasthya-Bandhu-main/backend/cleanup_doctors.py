from config.database import SessionLocal
from entity.models import Doctor

db = SessionLocal()

print("=== CLEANING UP DOCTORS ===")

# Delete doctors with empty names (bad data)
bad_doctors = db.query(Doctor).filter(Doctor.name == '').all()
print(f"Found {len(bad_doctors)} doctors with empty names")

for doc in bad_doctors:
    print(f"Deleting doctor ID {doc.id}")
    db.delete(doc)

db.commit()
print("✅ Cleanup complete!")

# Show remaining doctors
remaining = db.query(Doctor).all()
print(f"\n=== REMAINING DOCTORS ({len(remaining)}) ===")
for doc in remaining:
    print(f"ID: {doc.id}, Name: {doc.name}, Status: {doc.verification_status}")

db.close()
