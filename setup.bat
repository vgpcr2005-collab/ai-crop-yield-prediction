@echo off
REM Quick Setup Script for AgriAI Application

echo.
echo ====================================
echo   AgriAI - Setup Script
echo ====================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org
    pause
    exit /b 1
)

echo [1/4] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [2/4] Generating dataset...
cd dataset
python crop_yield_data.py
cd ..
if errorlevel 1 (
    echo [ERROR] Failed to generate dataset
    pause
    exit /b 1
)

echo.
echo [3/4] Training ML models...
cd backend
python ..\services\train_models.py
if errorlevel 1 (
    echo [ERROR] Failed to train models
    pause
    exit /b 1
)

echo.
echo [4/4] Starting Flask server...
echo.
echo ====================================
echo   ✓ Setup Complete!
echo ====================================
echo.
echo Starting application on http://localhost:5000
echo.
python app.py

pause
