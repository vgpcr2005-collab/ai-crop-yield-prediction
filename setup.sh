#!/bin/bash

# Quick Setup Script for AgriAI Application (Linux/Mac)

echo ""
echo "===================================="
echo "  AgriAI - Setup Script"
echo "===================================="
echo ""

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org"
    exit 1
fi

echo "[1/4] Installing dependencies..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install dependencies"
    exit 1
fi

echo ""
echo "[2/4] Generating dataset..."
cd dataset
python3 crop_yield_data.py
cd ..
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to generate dataset"
    exit 1
fi

echo ""
echo "[3/4] Training ML models..."
cd backend
python3 ../backend/services/train_models.py
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to train models"
    exit 1
fi

echo ""
echo "[4/4] Starting Flask server..."
echo ""
echo "===================================="
echo "  ✓ Setup Complete!"
echo "===================================="
echo ""
echo "Starting application on http://localhost:5000"
echo ""
python3 app.py
