"""
Create mock ML models for testing the yield prediction system
Run this once to generate the required pickle files
"""
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LinearRegression
import json
import os

# Create models directory if it doesn't exist
os.makedirs('../models', exist_ok=True)

print("Creating mock ML models...")

# 1. Create a simple linear regression model for yield prediction
X_train = np.array([
    [1, 1, 1, 850, 28, 65, 80, 40, 50, 2, 4, 150],
    [2, 2, 2, 1000, 25, 70, 90, 35, 45, 2.5, 3, 140],
    [3, 3, 1, 600, 22, 60, 75, 30, 40, 1.5, 2, 120],
    [1, 4, 2, 900, 26, 68, 85, 38, 48, 2.2, 3.5, 145],
    [2, 1, 3, 750, 24, 62, 75, 35, 42, 1.8, 2.5, 130],
])
y_train = np.array([6.5, 7.2, 5.8, 6.8, 6.2])

yield_model = LinearRegression()
yield_model.fit(X_train, y_train)

with open('../models/yield_prediction_model.pkl', 'wb') as f:
    pickle.dump(yield_model, f)
print("✓ Created yield_prediction_model.pkl")

# 2. Create feature scaler
scaler = StandardScaler()
scaler.fit(X_train)
with open('../models/scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)
print("✓ Created scaler.pkl")

# 3. Create crop encoder
crop_encoder = LabelEncoder()
crops = ['Rice', 'Wheat', 'Maize', 'Cotton', 'Sugarcane', 'Soybean', 'Barley', 'Pulses']
crop_encoder.fit(crops)
with open('../models/crop_encoder.pkl', 'wb') as f:
    pickle.dump(crop_encoder, f)
print("✓ Created crop_encoder.pkl")

# 4. Create region encoder
region_encoder = LabelEncoder()
regions = ['North', 'South', 'East', 'West', 'Central', 'Coastal']
region_encoder.fit(regions)
with open('../models/region_encoder.pkl', 'wb') as f:
    pickle.dump(region_encoder, f)
print("✓ Created region_encoder.pkl")

# 5. Create soil encoder
soil_encoder = LabelEncoder()
soils = ['Loamy', 'Sandy', 'Clay', 'Silt', 'Peaty', 'Chalky']
soil_encoder.fit(soils)
with open('../models/soil_encoder.pkl', 'wb') as f:
    pickle.dump(soil_encoder, f)
print("✓ Created soil_encoder.pkl")

# 6. Create feature names
feature_names = [
    'Crop', 'Region', 'Soil', 'Rainfall', 'Temperature',
    'Humidity', 'Nitrogen', 'Phosphorus', 'Potassium',
    'Area', 'Irrigation', 'Fertilizer'
]
with open('../models/feature_names.pkl', 'wb') as f:
    pickle.dump(feature_names, f)
print("✓ Created feature_names.pkl")

# 7. Create crop recommendations data
crop_recommendations = {
    'Rice': {
        'optimal_rainfall': (700, 2500),
        'optimal_temp': (25, 30),
        'optimal_humidity': (60, 90),
        'water_req': 4,
        'yield_avg': 6.5
    },
    'Wheat': {
        'optimal_rainfall': (400, 1000),
        'optimal_temp': (20, 25),
        'optimal_humidity': (50, 75),
        'water_req': 2,
        'yield_avg': 5.2
    },
    'Maize': {
        'optimal_rainfall': (800, 1500),
        'optimal_temp': (21, 27),
        'optimal_humidity': (60, 80),
        'water_req': 4,
        'yield_avg': 7.8
    },
    'Cotton': {
        'optimal_rainfall': (500, 1250),
        'optimal_temp': (21, 32),
        'optimal_humidity': (50, 75),
        'water_req': 3,
        'yield_avg': 2.1
    },
    'Sugarcane': {
        'optimal_rainfall': (1200, 2250),
        'optimal_temp': (20, 30),
        'optimal_humidity': (60, 85),
        'water_req': 6,
        'yield_avg': 80
    },
    'Soybean': {
        'optimal_rainfall': (450, 1100),
        'optimal_temp': (20, 30),
        'optimal_humidity': (50, 75),
        'water_req': 4,
        'yield_avg': 2.8
    },
    'Barley': {
        'optimal_rainfall': (350, 900),
        'optimal_temp': (15, 24),
        'optimal_humidity': (45, 70),
        'water_req': 2,
        'yield_avg': 4.5
    },
    'Pulses': {
        'optimal_rainfall': (400, 800),
        'optimal_temp': (15, 25),
        'optimal_humidity': (50, 70),
        'water_req': 3,
        'yield_avg': 2.2
    }
}

with open('../models/crop_recommendations.json', 'w') as f:
    json.dump(crop_recommendations, f, indent=2)
print("✓ Created crop_recommendations.json")

print("\n✅ All mock models created successfully!")
print("Location: ../models/")
