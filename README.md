# 🌾 AI-Powered Crop Yield Prediction & Smart Agricultural Optimization System

A comprehensive machine learning application that predicts crop yields, recommends suitable crops, and provides smart optimization suggestions for farmers.

## ✨ Features

### 1️⃣ **Crop Yield Prediction** 🌾
- Predict crop yield based on environmental and soil conditions
- Multiple ML models (Linear Regression, Random Forest, Gradient Boosting)
- Real-time predictions with detailed analysis

### 2️⃣ **Crop Recommendation** 🌱
- Get crop suggestions based on soil and weather conditions
- Suitability scoring for different crops
- Ranked recommendations with confidence levels

### 3️⃣ **Smart Optimization** 💧
- Resource optimization recommendations
- Nutrient management suggestions
- Irrigation planning
- Expected yield improvement calculation

### 4️⃣ **Analytics Dashboard** 📊
- Visualize crop yields across regions
- Correlation analysis between factors and yield
- Dataset insights and statistics
- Interactive charts and graphs

### 5️⃣ **Real-Time Recommendations** 💡
- AI-powered suggestions for soil nutrients
- Temperature and humidity optimization
- Rainfall and irrigation advice
- Fertilizer recommendations

## 🛠️ Technology Stack

### Backend
- **Flask** - Web framework
- **Python** - Core language
- **Scikit-learn** - Machine Learning models
- **Pandas & NumPy** - Data processing

### Frontend
- **HTML5** - Structure
- **CSS3** - Styling
- **JavaScript** - Interactivity
- **Plotly.js** - Data visualization

### Database
- **CSV** - Dataset storage (can be upgraded to SQLite/MySQL)

## 📋 Project Structure

```
AI-Crop-Yield-Prediction/
├── backend/
│   ├── app.py                          # Flask application
│   ├── templates/
│   │   └── index.html                  # Main HTML
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css               # Styling
│   │   └── js/
│   │       └── script.js               # Frontend logic
│   ├── services/
│   │   └── train_models.py             # ML model training
│   ├── config/
│   ├── routes/
│   ├── models/                         # Saved ML models
│   └── utils/
├── dataset/
│   ├── crop_yield_data.csv             # Dataset
│   └── crop_yield_data.py              # Dataset generator
├── requirements.txt                     # Python dependencies
└── README.md                           # This file
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Step 1: Clone/Download the Project
```bash
cd AI-Crop-Yield-Prediction
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Generate Dataset
If you don't have the dataset CSV, generate it:
```bash
python dataset/crop_yield_data.py
```

### Step 4: Train ML Models
```bash
python backend/services/train_models.py
```

This will create:
- `models/yield_prediction_model.pkl` - Main prediction model
- `models/crop_recommendations.json` - Crop statistics
- `models/scaler.pkl` - Feature scaler
- `models/*_encoder.pkl` - Category encoders

### Step 5: Run the Application
```bash
cd backend
python app.py
```

The application will start on `http://localhost:5000`

## 📊 Usage

### Home Page
- Overview of features
- Quick navigation to different modules

### Yield Prediction
1. Enter crop details (type, region, soil type)
2. Input environmental conditions (rainfall, temperature, humidity)
3. Enter soil nutrients (N, P, K)
4. Click "Predict Yield"
5. View predicted yield and AI recommendations

Example Input:
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

Expected Output:
```
Predicted Yield: 4.8 tons/hectare
Crop Suitability: 92%
Soil Health: 78%

Recommendations:
✅ Rainfall is suitable (850mm)
✅ Temperature is suitable (28°C)
⚠️ Nitrogen level is optimal
✅ Humidity is suitable (70%)
```

### Crop Recommendation
1. Enter weather conditions
2. Select soil type
3. Click "Find Best Crops"
4. View ranked crop recommendations

### Smart Optimization
1. Select crop
2. Enter current conditions
3. Click "Get Optimization Plan"
4. View improvement suggestions and optimal values

### Analytics Dashboard
- Click "Load Analytics"
- View crop yield trends
- Analyze region-wise performance
- Check correlations between factors and yield

## 🎯 ML Models Used

### Yield Prediction Models
1. **Linear Regression** - Simple baseline model
2. **Random Forest** - Ensemble method with good interpretability
3. **Gradient Boosting** - Advanced ensemble method

The best performing model is automatically selected and saved.

### Model Performance
- **R² Score**: Indicates how well the model explains variance
- **RMSE**: Root Mean Squared Error for prediction accuracy
- **MAE**: Mean Absolute Error

## 📈 Sample Dataset

The dataset includes 1000 samples with:
- **Crops**: Rice, Wheat, Maize, Cotton, Sugarcane, Soybean, Barley, Pulses
- **Features**: Rainfall, Temperature, Humidity, Soil nutrients (N, P, K), Irrigation, Fertilizer
- **Target**: Yield (tons/hectare)

## 🔄 Data Pipeline

```
Raw Data
   ↓
Data Cleaning & Processing
   ↓
Feature Scaling & Encoding
   ↓
Model Training
   ↓
Model Evaluation
   ↓
Flask API Deployment
   ↓
Web Interface
   ↓
User Predictions & Recommendations
```

## 💾 Model Training Details

### Feature Engineering
- One-hot encoding for categorical variables (Crop, Region, Soil Type)
- StandardScaler for numerical features
- Feature normalization for ML models

### Train-Test Split
- 80% training data
- 20% testing data
- Random state: 42 (for reproducibility)

## 🌐 API Endpoints

### POST `/api/predict`
Predict crop yield
```json
{
    "crop": "Rice",
    "region": "North",
    "soil_type": "Loamy",
    "rainfall": 850,
    "temperature": 28,
    "humidity": 70,
    "nitrogen": 80,
    "phosphorus": 40,
    "potassium": 50,
    "area": 2,
    "irrigation": 4,
    "fertilizer": 150
}
```

### POST `/api/recommend-crop`
Get crop recommendations
```json
{
    "rainfall": 850,
    "temperature": 28,
    "humidity": 70,
    "soil_type": "Loamy"
}
```

### POST `/api/optimization`
Get optimization suggestions
```json
{
    "crop": "Rice",
    "rainfall": 850,
    "temperature": 28,
    "humidity": 70,
    "nitrogen": 80,
    "phosphorus": 40,
    "potassium": 50,
    "irrigation": 4
}
```

### GET `/api/dashboard`
Get analytics data for dashboard

## 🎨 UI Features

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Dark/Light Compatible**: Adapts to system theme
- **Interactive Charts**: Plotly.js visualizations
- **Real-time Feedback**: Instant prediction results
- **Color-coded Recommendations**: Easy to understand status
- **Emoji Icons**: Visual indicators for different parameters

## 📚 Learning Resources

### Machine Learning Concepts Used
- Linear Regression
- Random Forest
- Gradient Boosting
- Feature Scaling & Normalization
- Categorical Encoding
- Train-Test Split
- Model Evaluation Metrics

### Agricultural Parameters
- **Nitrogen (N)**: Plant growth and protein synthesis
- **Phosphorus (P)**: Root development and energy transfer
- **Potassium (K)**: Overall plant health and disease resistance
- **Optimal Ranges**: Vary by crop type

## 🐛 Troubleshooting

### Models Not Found Error
```bash
# Re-train the models
python backend/services/train_models.py
```

### Port 5000 Already in Use
```bash
# Use a different port in app.py
app.run(debug=True, port=5001)
```

### CORS Issues
- Flask-CORS is already configured
- Frontend should access `http://localhost:5000`

### No Dataset Error
```bash
# Generate the dataset
python dataset/crop_yield_data.py
```

## 📝 Future Enhancements

- [ ] Weather API integration
- [ ] Real-time weather forecasting
- [ ] User authentication and profiles
- [ ] Historical data tracking
- [ ] Mobile app (React Native)
- [ ] Advanced optimization algorithms (Linear Programming)
- [ ] Crop disease detection (Computer Vision)
- [ ] Cost-benefit analysis
- [ ] Export predictions to PDF/Excel
- [ ] Multi-language support

## 👨‍💻 Contributing

Feel free to fork, modify, and improve this project!

## 📄 License

Open source project - Free to use and modify

## 📞 Support

For issues or questions, please create an issue or contact the developer.

---

**Made with ❤️ for Farmers & Agriculture**

🌾 Help farmers make better decisions with AI 🌾
