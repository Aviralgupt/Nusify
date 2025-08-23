@echo off
echo ========================================
echo    Nusify AI Music Generator
echo ========================================
echo.

echo Starting Nusify backend server...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Check if requirements are installed
echo Checking dependencies...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo.
echo Starting server...
echo Web interface will be available at: http://localhost:5000
echo Frontend should be started separately with: cd frontend && npm start
echo.
echo Press Ctrl+C to stop the server
echo.

python start.py

pause
