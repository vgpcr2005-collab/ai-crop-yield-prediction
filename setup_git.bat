@echo off
REM Initialize Git and prepare for GitHub upload

echo.
echo ====================================
echo   AgriAI - Git Setup Script
echo ====================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Git is not installed or not in PATH
    echo Please install Git from https://git-scm.com
    pause
    exit /b 1
)

REM Check if already initialized
if exist .git (
    echo [INFO] Git repository already initialized
    echo Running: git status
    git status
    echo.
    echo To push to GitHub:
    echo 1. Create repository at https://github.com/new
    echo 2. Run: git remote add origin https://github.com/YOUR_USERNAME/AI-Crop-Yield-Prediction.git
    echo 3. Run: git push -u origin main
    pause
    exit /b 0
)

REM Initialize git
echo [1/4] Initializing git repository...
git init
if errorlevel 1 (
    echo [ERROR] Failed to initialize git
    pause
    exit /b 1
)

REM Configure user
echo.
echo [2/4] Configuring git user...
set /p GIT_NAME="Enter your full name (for git commits): "
set /p GIT_EMAIL="Enter your email (for git commits): "

git config user.name "%GIT_NAME%"
git config user.email "%GIT_EMAIL%"

echo Configured: %GIT_NAME% <%GIT_EMAIL%>

REM Add all files
echo.
echo [3/4] Staging all files...
git add .
git status

REM Initial commit
echo.
echo [4/4] Creating initial commit...
git commit -m "Initial commit: AgriAI - AI-Powered Crop Yield Prediction System"

echo.
echo ====================================
echo   ✓ Git Setup Complete!
echo ====================================
echo.
echo Next steps:
echo 1. Create a new repository at https://github.com/new
echo    Name: AI-Crop-Yield-Prediction
echo    Description: AI-Powered Crop Yield Prediction System
echo    Make it PUBLIC
echo.
echo 2. After creating, run these commands:
echo    git remote add origin https://github.com/YOUR_USERNAME/AI-Crop-Yield-Prediction.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 3. Replace YOUR_USERNAME with your actual GitHub username!
echo.
echo View your repository at:
echo https://github.com/YOUR_USERNAME/AI-Crop-Yield-Prediction
echo.
pause
