import sys
sys.path.append('.')

from dotenv import load_dotenv
load_dotenv()

from config.database import engine, Base
from entity.models import *

print("\n=== Resetting Database ===")
print("Dropping all tables...")

try:
    Base.metadata.drop_all(bind=engine)
    print("[PASS] All tables dropped")
except Exception as e:
    print(f"[INFO] Drop tables: {e}")

print("\nCreating fresh tables...")
try:
    Base.metadata.create_all(bind=engine)
    print("[PASS] All tables created fresh")
    print("\nDatabase reset complete! Run test_phase1.py to verify.")
except Exception as e:
    print(f"[FAIL] Create tables failed: {e}")
    sys.exit(1)
