@echo off
REM Quick Setup Script for AgriAI Application

cd /d "%~dp0"

echo.
echo ====================================
echo   AgriAI - Setup Script
echo ====================================
echo.

REM Use the Python version required by runtime.txt.
py -3.10 --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python 3.10 is not installed
    echo Please install Python 3.10 from https://www.python.org
    pause
    exit /b 1
)

REM Recreate an existing virtual environment if it uses an incompatible Python version.
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" -c "import sys; raise SystemExit(0 if sys.version_info[:2] == (3, 10) else 1)"
    if errorlevel 1 (
        echo Existing .venv is not Python 3.10. Recreating it...
        rmdir /s /q .venv
    )
)

if not exist ".venv\Scripts\python.exe" (
    echo Creating Python 3.10 virtual environment...
    py -3.10 -m venv .venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
)

set "PYTHON=.venv\Scripts\python.exe"

echo [1/4] Installing dependencies...
"%PYTHON%" -m pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [2/4] Generating dataset...
cd dataset
"..\%PYTHON%" crop_yield_data.py
cd ..
if errorlevel 1 (
    echo [ERROR] Failed to generate dataset
    pause
    exit /b 1
)

echo.
echo [3/4] Training ML models...
if exist "backend\models\yield_prediction_model.pkl" if exist "backend\models\scaler.pkl" if exist "backend\models\crop_encoder.pkl" if exist "backend\models\region_encoder.pkl" if exist "backend\models\soil_encoder.pkl" (
    echo Existing ML models found. Skipping training.
) else (
    "%PYTHON%" backend\services\train_models.py
    if errorlevel 1 (
        echo [ERROR] Failed to train models
        pause
        exit /b 1
    )
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
cd backend
"..\%PYTHON%" app.py

pause
