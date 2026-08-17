# 🚀 AgriAI - Quick Start Guide

## Installation in 5 Minutes

### Option 1: Automatic Setup (Windows)
```bash
# Double-click setup.bat
setup.bat
```

### Option 2: Automatic Setup (Linux/Mac)
```bash
# Make it executable
chmod +x setup.sh

# Run setup
./setup.sh
```

### Option 3: Manual Setup

#### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

#### 2. Generate Dataset
```bash
cd dataset
python crop_yield_data.py
cd ..
```

#### 3. Train ML Models
```bash
cd backend
python ../backend/services/train_models.py
cd ..
```

#### 4. Start the Application
```bash
cd backend
python app.py
```

## Access the Application

Open your browser and go to: **http://localhost:5000**

## Common Tasks

### 1. Predict Crop Yield
1. Navigate to "Yield Prediction" tab
2. Fill in crop details and environmental conditions
3. Click "Predict Yield"
4. View predictions and recommendations

### 2. Get Crop Recommendations
1. Go to "Crop Recommendation" tab
2. Enter rainfall, temperature, humidity
3. Click "Find Best Crops"
4. See ranked crop suggestions

### 3. Optimize Resources
1. Go to "Optimization" tab
2. Select crop and current conditions
3. Click "Get Optimization Plan"
4. Get improvement suggestions

### 4. View Analytics
1. Go to "Analytics" tab
2. Click "Load Analytics"
3. Explore charts and correlations

## 📊 Sample Test Data

Try these values to see predictions:

### Rice in North Region
```
Crop: Rice
Region: North
Soil: Loamy
Rainfall: 850 mm
Temperature: 28°C
Humidity: 70%
Nitrogen: 80 ppm
Phosphorus: 40 ppm
Potassium: 50 ppm
Area: 2 hectares
Irrigation: 4 times/week
Fertilizer: 150 kg/hectare
```

### Wheat in Central Region
```
Crop: Wheat
Region: Central
Soil: Clay
Rainfall: 650 mm
Temperature: 22°C
Humidity: 65%
Nitrogen: 90 ppm
Phosphorus: 35 ppm
Potassium: 45 ppm
Area: 3 hectares
Irrigation: 3 times/week
Fertilizer: 160 kg/hectare
```

### Maize in East Region
```
Crop: Maize
Region: East
Soil: Sandy
Rainfall: 1200 mm
Temperature: 24°C
Humidity: 72%
Nitrogen: 100 ppm
Phosphorus: 45 ppm
Potassium: 55 ppm
Area: 2 hectares
Irrigation: 5 times/week
Fertilizer: 170 kg/hectare
```

## 🔧 Troubleshooting

### Problem: Port 5000 already in use
**Solution:** Open `backend/app.py` and change:
```python
app.run(debug=True, port=5001)  # Use port 5001 instead
```

### Problem: Module not found error
**Solution:** Reinstall dependencies:
```bash
pip install --upgrade -r requirements.txt
```

### Problem: Models not found
**Solution:** Re-train models:
```bash
cd backend
python ../backend/services/train_models.py
```

### Problem: CORS error in browser console
**Solution:** Flask-CORS is configured. Make sure frontend uses `http://localhost:5000` (not HTTPS)

### Problem: Dataset CSV not found
**Solution:** Generate dataset:
```bash
cd dataset
python crop_yield_data.py
cd ..
```

## 📁 Project Files

### Backend
- `app.py` - Main Flask application
- `services/train_models.py` - ML model training

### Frontend
- `templates/index.html` - Web interface
- `static/css/style.css` - Styling
- `static/js/script.js` - JavaScript logic

### Data
- `dataset/crop_yield_data.csv` - Training dataset

### Models (Generated after training)
- `models/yield_prediction_model.pkl` - Prediction model
- `models/scaler.pkl` - Feature scaler
- `models/*_encoder.pkl` - Category encoders

## 🎯 Next Steps

1. ✅ Complete Setup
2. ✅ Run Application
3. ✅ Test with sample data
4. ✅ Explore all features
5. 📝 Customize for your needs
6. 🚀 Deploy to production

## 📞 Help & Support

- Check `README.md` for detailed documentation
- Review code comments for implementation details
- Check `requirements.txt` for all dependencies

## ✨ Features Summary

| Feature | Status | Module |
|---------|--------|--------|
| Yield Prediction | ✅ | Prediction |
| Crop Recommendation | ✅ | Recommendation |
| Resource Optimization | ✅ | Optimization |
| Analytics Dashboard | ✅ | Dashboard |
| Real-time Recommendations | ✅ | All Modules |
| Multiple ML Models | ✅ | Backend |
| Responsive UI | ✅ | Frontend |

## 🚀 Performance Tips

1. **First Load**: May take 2-3 seconds to load models
2. **Predictions**: Usually complete within 100ms
3. **Dashboard**: Analytics load in 1-2 seconds
4. **Browser**: Use Chrome, Firefox, Edge, Safari

---

**Ready to start? Run `setup.bat` (Windows) or `setup.sh` (Linux/Mac)**
