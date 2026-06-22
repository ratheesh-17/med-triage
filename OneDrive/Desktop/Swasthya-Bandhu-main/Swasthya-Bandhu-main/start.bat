@echo off
echo ========================================
echo Swasthya Bandhu - Quick Setup
echo ========================================
echo.

cd backend

echo [1/4] Installing dependencies...
pip install -r requirements.txt

echo.
echo [2/4] Creating database tables...
python -c "from config.database import init_db; init_db(); print('Tables created')"

echo.
echo [3/4] Seeding demo data...
python seed_data.py

echo.
echo [4/4] Starting server...
echo.
echo ========================================
echo Backend: http://localhost:8000
echo Frontend: Open frontend/index.html
echo Admin Phone: 9999999999 (from .env)
echo ========================================
echo.

python app.py
