@echo off
echo ========================================
echo Veelearn Server Keep-Alive Script
echo ========================================
echo.
echo This script will keep your Veelearn server awake
echo by pinging it every 10 minutes.
echo.
echo Press Ctrl+C to stop the script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Check if requests module is installed
python -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo Installing required module: requests...
    pip install requests
    if errorlevel 1 (
        echo ERROR: Failed to install requests module
        echo Please run: pip install requests
        pause
        exit /b 1
    )
)

REM Run the keep-alive script
echo Starting keep-alive script...
python keep-alive-script.py

pause
