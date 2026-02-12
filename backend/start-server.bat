@echo off
echo ========================================
echo Starting Physical AI Book Backend Server
echo ========================================
echo.

cd /d "%~dp0"

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo Starting FastAPI server on http://localhost:8000
echo Press Ctrl+C to stop the server
echo.
echo ========================================
echo.

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
