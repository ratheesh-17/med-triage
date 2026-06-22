@echo off
echo Starting server...
start /B python app.py
timeout /t 5 /nobreak >nul
echo Running Phase 2 tests...
python test_phase2.py
taskkill /F /IM python.exe >nul 2>&1
