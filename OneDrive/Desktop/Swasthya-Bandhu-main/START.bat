@echo off
echo ========================================
echo   SWASTHYA BANDHU - STARTUP SCRIPT
echo ========================================
echo.

REM Check if we're in the correct directory
if not exist "backend" (
    echo ERROR: backend folder not found!
    echo Please run this script from Swasthya-Bandhu-main directory
    pause
    exit /b 1
)

if not exist "frontend-react" (
    echo ERROR: frontend-react folder not found!
    echo Please run this script from Swasthya-Bandhu-main directory
    pause
    exit /b 1
)

echo [1/2] Starting Backend Server...
echo.
start "Swasthya Bandhu - Backend" cmd /k "cd backend && venv\Scripts\activate && uvicorn main:app --reload --host 0.0.0.0 --port 8000"

echo Waiting 5 seconds for backend to start...
timeout /t 5 /nobreak >nul

echo.
echo [2/2] Starting Frontend Server...
echo.
start "Swasthya Bandhu - Frontend" cmd /k "cd frontend-react && npm run dev"

echo.
echo ========================================
echo   SERVERS STARTING...
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo API Docs: http://localhost:8000/docs
echo.
echo Two terminal windows will open:
echo   1. Backend (FastAPI/Uvicorn)
echo   2. Frontend (Vite/React)
echo.
echo Keep both windows open while using the app!
echo.
echo Waiting 10 seconds before verification...
timeout /t 10 /nobreak >nul

echo.
echo Running connection verification...
python verify_connection.py

echo.
echo Press any key to exit this window...
pause >nul
