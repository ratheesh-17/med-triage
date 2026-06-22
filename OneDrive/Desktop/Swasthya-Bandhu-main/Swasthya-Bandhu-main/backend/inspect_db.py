from dotenv import load_dotenv
import os

# load environment variables before creating the DB engine
load_dotenv()

from config.database import SessionLocal, init_db
from entity.models import Doctor

def main():
    init_db()
    db = SessionLocal()
    doctors = db.query(Doctor).all()
    print('Doctor count:', len(doctors))
    for d in doctors:
        print(d.id, d.name, d.specialization, d.verification_status, d.location_lat, d.location_lng)


if __name__ == '__main__':
    main()
