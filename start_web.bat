@echo off
REM SmartCSV Web Application Startup Script for Windows

echo ==========================================
echo SmartCSV Web Application
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo √ Python found
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo X Failed to install dependencies
    pause
    exit /b 1
)

echo √ Dependencies installed
echo.

REM Start the Flask backend
echo Starting Flask backend server...
echo    Backend will run on: http://localhost:5000
echo.
echo To access the web interface:
echo    1. Open index.html in your browser, OR
echo    2. Run: python -m http.server 8000
echo       Then visit: http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo ==========================================
echo.

python app.py

@REM Made with Bob
