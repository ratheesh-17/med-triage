import sys
sys.path.append('.')

from dotenv import load_dotenv
load_dotenv()

import mysql.connector
import os

DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_NAME = os.getenv("DB_NAME", "swasthya_bandhu")

print("\n=== Force Database Reset ===")

try:
    # Connect without database
    conn = mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = conn.cursor()
    
    # Drop database
    print(f"Dropping database '{DB_NAME}'...")
    cursor.execute(f"DROP DATABASE IF EXISTS {DB_NAME}")
    print("[PASS] Database dropped")
    
    # Create database
    print(f"Creating database '{DB_NAME}'...")
    cursor.execute(f"CREATE DATABASE {DB_NAME}")
    print("[PASS] Database created")
    
    cursor.close()
    conn.close()
    
    print("\nNow creating tables...")
    from config.database import Base, engine
    from entity.models import *
    
    Base.metadata.create_all(bind=engine)
    print("[PASS] All tables created successfully")
    
    print("\n[SUCCESS] Database reset complete!")
    print("Run: python test_phase1.py")
    
except Exception as e:
    print(f"[FAIL] Error: {e}")
    sys.exit(1)
