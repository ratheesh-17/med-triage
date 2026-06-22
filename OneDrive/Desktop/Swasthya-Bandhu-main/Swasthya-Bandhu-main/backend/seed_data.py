from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables BEFORE importing database config
load_dotenv()

from config.database import SessionLocal, init_db
from entity.models import Doctor, User

def seed_database():
    init_db()
    db = SessionLocal()
    
    # Seed verified doctors (Coimbatore Focus) — skip any that already exist by phone
    doctors = [
        Doctor(
            phone="9876543210",
            name="Dr. Amit Verma",
            specialization="General Physician",
            hospital="Ganga Hospital, Coimbatore",
            experience="10 years",
            fees=500,
            location_lat=11.0081,
            location_lng=76.9650,
            medical_council_number="MCI-12345",
            rating=4.6,
            verification_status="approved",
            verified_at=datetime.utcnow()
        ),
        Doctor(
            phone="9876543211",
            name="Dr. Priya Sharma",
            specialization="Cardiologist",
            hospital="Apollo Hospitals Coimbatore",
            experience="15 years",
            fees=1500,
            location_lat=11.0161,
            location_lng=76.9755,
            medical_council_number="MCI-12346",
            rating=4.8,
            verification_status="approved",
            verified_at=datetime.utcnow()
        ),
        Doctor(
            phone="9876543212",
            name="Dr. Rajesh Kumar",
            specialization="Neurologist",
            hospital="Ramakrishna Hospital Coimbatore",
            experience="20 years",
            fees=2000,
            location_lat=10.9990,
            location_lng=76.9500,
            medical_council_number="MCI-12347",
            rating=4.9,
            verification_status="approved",
            verified_at=datetime.utcnow()
        ),
        Doctor(
            phone="9876543213",
            name="Dr. Meera Reddy",
            specialization="Pediatrician",
            hospital="Srimanto Hospital Coimbatore",
            experience="12 years",
            fees=800,
            location_lat=11.0200,
            location_lng=76.9450,
            medical_council_number="MCI-12348",
            rating=4.7,
            verification_status="approved",
            verified_at=datetime.utcnow()
        ),
        Doctor(
            phone="9876543214",
            name="Dr. Suresh Patel",
            specialization="Orthopedic",
            hospital="Sri Ramakrishna Hospital Coimbatore",
            experience="18 years",
            fees=1200,
            location_lat=11.0050,
            location_lng=76.9600,
            medical_council_number="MCI-12349",
            rating=4.5,
            verification_status="approved",
            verified_at=datetime.utcnow()
        ),
        Doctor(
            phone="9876543215",
            name="Dr. Anjali Singh",
            specialization="Dermatologist",
            hospital="KG Hospital Coimbatore",
            experience="8 years",
            fees=700,
            location_lat=11.0120,
            location_lng=76.9700,
            medical_council_number="MCI-12350",
            rating=4.4,
            verification_status="approved",
            verified_at=datetime.utcnow()
        ),
        Doctor(
            phone="9876543216",
            name="Dr. Vikram Malhotra",
            specialization="Psychiatrist",
            hospital="Aruna Nursing Home Coimbatore",
            experience="14 years",
            fees=1000,
            location_lat=11.0140,
            location_lng=76.9550,
            medical_council_number="MCI-12351",
            rating=4.6,
            verification_status="approved",
            verified_at=datetime.utcnow()
        ),
        Doctor(
            phone="9876543217",
            name="Dr. Deepa Menon",
            specialization="Gynecologist",
            hospital="Garbha Niketan Hospital Coimbatore",
            experience="11 years",
            fees=900,
            location_lat=11.0070,
            location_lng=76.9680,
            medical_council_number="MCI-12352",
            rating=4.7,
            verification_status="approved",
            verified_at=datetime.utcnow()
        ),
        Doctor(
            phone="9876543218",
            name="Dr. Sanjay Sharma",
            specialization="Orthopedic",
            hospital="Asan Nursing Home Coimbatore",
            experience="16 years",
            fees=1300,
            location_lat=11.0100,
            location_lng=76.9620,
            medical_council_number="MCI-12353",
            rating=4.5,
            verification_status="approved",
            verified_at=datetime.utcnow()
        ),
        Doctor(
            phone="9876543219",
            name="Dr. Kavya Reddy",
            specialization="Ophthalmologist",
            hospital="Aravind Eye Hospital Coimbatore",
            experience="9 years",
            fees=600,
            location_lat=11.0150,
            location_lng=76.9580,
            medical_council_number="MCI-12354",
            rating=4.8,
            verification_status="approved",
            verified_at=datetime.utcnow()
        ),
        # Pending doctor for demo
        Doctor(
            phone="9876543220",
            name="Dr. Veena Patel",
            specialization="ENT",
            hospital="Sanniti Hospital Coimbatore",
            experience="13 years",
            fees=750,
            location_lat=11.0110,
            location_lng=76.9640,
            medical_council_number="MCI-12355",
            rating=4.6,
            verification_status="pending"
        )
    ]
    
    added = 0
    for doctor in doctors:
        if not db.query(Doctor).filter(Doctor.phone == doctor.phone).first():
            db.add(doctor)
            added += 1
    db.commit()
    
    print(f"✅ Seeded {added} new doctors (skipped existing ones)")
    print("✅ All doctors focused on Coimbatore area (lat: 11.0081, lng: 76.9650)")
    print("✅ Database ready for demo with Leaflet mapping")
    
    db.close()

if __name__ == "__main__":
    seed_database()
