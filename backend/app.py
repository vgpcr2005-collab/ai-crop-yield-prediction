"""
Flask Backend for AI Crop Yield Prediction and Optimization System
"""
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pickle
import json
import numpy as np
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Load models and preprocessing objects
try:
    with open('models/yield_prediction_model.pkl', 'rb') as f:
        yield_model = pickle.load(f)
    
    with open('models/scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    
    with open('models/crop_encoder.pkl', 'rb') as f:
        crop_encoder = pickle.load(f)
    
    with open('models/region_encoder.pkl', 'rb') as f:
        region_encoder = pickle.load(f)
    
    with open('models/soil_encoder.pkl', 'rb') as f:
        soil_encoder = pickle.load(f)
    
    with open('models/feature_names.pkl', 'rb') as f:
        feature_names = pickle.load(f)
    
    with open('models/crop_recommendations.json', 'r') as f:
        crop_stats = json.load(f)
    
    print("✓ All models loaded successfully")
except Exception as e:
    print(f"Error loading models: {e}")
    yield_model = None

# Constants for optimal ranges
OPTIMAL_RANGES = {
    'Rice': {'rainfall': (700, 2500), 'temperature': (25, 30), 'humidity': (60, 90)},
    'Wheat': {'rainfall': (400, 1000), 'temperature': (20, 25), 'humidity': (50, 75)},
    'Maize': {'rainfall': (800, 1500), 'temperature': (21, 27), 'humidity': (60, 80)},
    'Cotton': {'rainfall': (500, 1250), 'temperature': (21, 32), 'humidity': (50, 75)},
    'Sugarcane': {'rainfall': (1200, 2250), 'temperature': (20, 30), 'humidity': (60, 85)},
    'Soybean': {'rainfall': (450, 1100), 'temperature': (20, 30), 'humidity': (50, 75)},
    'Barley': {'rainfall': (350, 900), 'temperature': (15, 24), 'humidity': (45, 70)},
    'Pulses': {'rainfall': (400, 800), 'temperature': (15, 25), 'humidity': (50, 70)}
}

NUTRIENT_RECOMMENDATIONS = {
    'Rice': {'nitrogen': 80, 'phosphorus': 40, 'potassium': 50},
    'Wheat': {'nitrogen': 90, 'phosphorus': 35, 'potassium': 45},
    'Maize': {'nitrogen': 100, 'phosphorus': 45, 'potassium': 55},
    'Cotton': {'nitrogen': 70, 'phosphorus': 30, 'potassium': 40},
    'Sugarcane': {'nitrogen': 85, 'phosphorus': 38, 'potassium': 48},
    'Soybean': {'nitrogen': 75, 'phosphorus': 32, 'potassium': 42},
    'Barley': {'nitrogen': 95, 'phosphorus': 40, 'potassium': 50},
    'Pulses': {'nitrogen': 65, 'phosphorus': 28, 'potassium': 38}
}

WATER_REQUIREMENTS = {
    'Rice': 4, 'Wheat': 2, 'Maize': 4, 'Cotton': 3,
    'Sugarcane': 6, 'Soybean': 4, 'Barley': 2, 'Pulses': 3
}

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/api/predict', methods=['POST'])
def predict():
    """Predict crop yield based on input parameters"""
    try:
        data = request.json
        
        # Extract input data
        crop = data['crop']
        region = data['region']
        soil_type = data['soil_type']
        rainfall = float(data['rainfall'])
        temperature = float(data['temperature'])
        humidity = float(data['humidity'])
        nitrogen = float(data['nitrogen'])
        phosphorus = float(data['phosphorus'])
        potassium = float(data['potassium'])
        area = float(data['area'])
        irrigation = float(data['irrigation'])
        fertilizer = float(data['fertilizer'])
        
        # Encode categorical variables
        crop_encoded = crop_encoder.transform([crop])[0]
        region_encoded = region_encoder.transform([region])[0]
        soil_encoded = soil_encoder.transform([soil_type])[0]
        
        # Prepare features in correct order
        input_features = np.array([[
            crop_encoded, region_encoded, soil_encoded,
            rainfall, temperature, humidity,
            nitrogen, phosphorus, potassium,
            area, irrigation, fertilizer
        ]])
        
        # Scale features
        input_scaled = scaler.transform(input_features)
        
        # Predict yield
        predicted_yield = yield_model.predict(input_scaled)[0]
        predicted_yield = max(0, predicted_yield)  # Ensure non-negative
        
        # Get crop recommendations
        recommendations = generate_recommendations(crop, rainfall, temperature, humidity, 
                                                   nitrogen, phosphorus, potassium)
        
        # Calculate soil health score (0-100)
        soil_health = calculate_soil_health(nitrogen, phosphorus, potassium)
        
        # Get suitability score
        suitability = calculate_crop_suitability(crop, rainfall, temperature, humidity)
        
        return jsonify({
            'status': 'success',
            'predicted_yield': round(predicted_yield, 2),
            'yield_unit': 'tons/hectare',
            'suitability': round(suitability, 1),
            'soil_health': round(soil_health, 1),
            'recommendations': recommendations,
            'input_summary': {
                'crop': crop,
                'region': region,
                'area': area,
                'rainfall': rainfall,
                'temperature': temperature,
                'humidity': humidity
            }
        })
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/api/recommend-crop', methods=['POST'])
def recommend_crop():
    """Recommend suitable crops based on conditions"""
    try:
        data = request.json
        
        rainfall = float(data['rainfall'])
        temperature = float(data['temperature'])
        humidity = float(data['humidity'])
        soil_type = data.get('soil_type', 'Loamy')
        region = data.get('region', 'Central')
        
        # Calculate suitability for each crop
        suitability_scores = {}
        for crop in OPTIMAL_RANGES.keys():
            score = calculate_crop_suitability_detailed(crop, rainfall, temperature, humidity)
            suitability_scores[crop] = score
        
        # Sort by suitability
        sorted_crops = sorted(suitability_scores.items(), key=lambda x: x[1], reverse=True)
        
        recommendations = [
            {
                'rank': i + 1,
                'crop': crop,
                'suitability': round(score, 1),
                'color': 'green' if score > 80 else 'yellow' if score > 60 else 'red'
            }
            for i, (crop, score) in enumerate(sorted_crops[:5])
        ]
        
        return jsonify({
            'status': 'success',
            'recommendations': recommendations,
            'input_summary': {
                'rainfall': rainfall,
                'temperature': temperature,
                'humidity': humidity,
                'soil_type': soil_type,
                'region': region
            }
        })
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/api/optimization', methods=['POST'])
def optimization():
    """Get optimization recommendations"""
    try:
        data = request.json
        
        crop = data['crop']
        nitrogen = float(data['nitrogen'])
        phosphorus = float(data['phosphorus'])
        potassium = float(data['potassium'])
        rainfall = float(data['rainfall'])
        irrigation = float(data['irrigation'])
        temperature = float(data['temperature'])
        humidity = float(data['humidity'])
        
        recommendations = generate_recommendations(crop, rainfall, temperature, humidity,
                                                   nitrogen, phosphorus, potassium)
        
        # Calculate potential improvement
        optimal_nutrients = NUTRIENT_RECOMMENDATIONS[crop]
        optimal_water = WATER_REQUIREMENTS[crop]
        
        improvements = {
            'nitrogen': optimal_nutrients['nitrogen'] - nitrogen,
            'phosphorus': optimal_nutrients['phosphorus'] - phosphorus,
            'potassium': optimal_nutrients['potassium'] - potassium,
            'irrigation': optimal_water - irrigation
        }
        
        # Calculate expected yield improvement
        improvement_percentage = sum([
            (abs(improvements[k]) / optimal_nutrients[k] * 100) 
            for k in ['nitrogen', 'phosphorus', 'potassium']
        ]) / 3
        improvement_percentage = min(improvement_percentage, 15)  # Cap at 15%
        
        return jsonify({
            'status': 'success',
            'recommendations': recommendations,
            'improvements': improvements,
            'expected_improvement': round(improvement_percentage, 1),
            'optimal_nutrients': optimal_nutrients,
            'optimal_water': optimal_water
        })
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/api/dashboard', methods=['GET'])
def dashboard_data():
    """Get data for analytics dashboard"""
    try:
        # Load dataset for statistics
        df = pd.read_csv('dataset/crop_yield_data.csv')
        
        # Crop-wise average yield
        crop_yield = df.groupby('Crop')['Yield_tons_per_hectare'].mean().to_dict()
        
        # Region-wise average yield
        region_yield = df.groupby('Region')['Yield_tons_per_hectare'].mean().to_dict()
        
        # Rainfall vs Yield correlation
        rainfall_yield_corr = df['Rainfall_mm'].corr(df['Yield_tons_per_hectare'])
        
        # Temperature vs Yield correlation
        temp_yield_corr = df['Temperature_C'].corr(df['Yield_tons_per_hectare'])
        
        return jsonify({
            'status': 'success',
            'crop_yield': crop_yield,
            'region_yield': region_yield,
            'correlations': {
                'rainfall_yield': round(rainfall_yield_corr, 3),
                'temperature_yield': round(temp_yield_corr, 3)
            },
            'dataset_stats': {
                'total_records': len(df),
                'crops': list(df['Crop'].unique()),
                'regions': list(df['Region'].unique())
            }
        })
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

def generate_recommendations(crop, rainfall, temperature, humidity, nitrogen, phosphorus, potassium):
    """Generate smart recommendations based on conditions"""
    recommendations = []
    optimal = OPTIMAL_RANGES[crop]
    nutrients = NUTRIENT_RECOMMENDATIONS[crop]
    
    # Rainfall check
    if rainfall < optimal['rainfall'][0]:
        recommendations.append({
            'parameter': 'Rainfall/Irrigation',
            'status': 'warning',
            'message': f'Rainfall is low ({rainfall}mm). Increase irrigation.',
            'emoji': '💧'
        })
    elif rainfall > optimal['rainfall'][1]:
        recommendations.append({
            'parameter': 'Rainfall/Irrigation',
            'status': 'warning',
            'message': f'Rainfall is high ({rainfall}mm). Reduce irrigation.',
            'emoji': '💧'
        })
    else:
        recommendations.append({
            'parameter': 'Rainfall/Irrigation',
            'status': 'success',
            'message': f'Rainfall is suitable ({rainfall}mm).',
            'emoji': '💧'
        })
    
    # Temperature check
    if temperature < optimal['temperature'][0]:
        recommendations.append({
            'parameter': 'Temperature',
            'status': 'warning',
            'message': f'Temperature is low ({temperature}°C). May need frost protection.',
            'emoji': '🌡️'
        })
    elif temperature > optimal['temperature'][1]:
        recommendations.append({
            'parameter': 'Temperature',
            'status': 'warning',
            'message': f'Temperature is high ({temperature}°C). Increase shade/water.',
            'emoji': '🌡️'
        })
    else:
        recommendations.append({
            'parameter': 'Temperature',
            'status': 'success',
            'message': f'Temperature is suitable ({temperature}°C).',
            'emoji': '🌡️'
        })
    
    # Humidity check
    if humidity < optimal['humidity'][0]:
        recommendations.append({
            'parameter': 'Humidity',
            'status': 'warning',
            'message': f'Humidity is low ({humidity}%). Increase irrigation.',
            'emoji': '💧'
        })
    elif humidity > optimal['humidity'][1]:
        recommendations.append({
            'parameter': 'Humidity',
            'status': 'warning',
            'message': f'Humidity is high ({humidity}%). Risk of fungal diseases.',
            'emoji': '🍄'
        })
    else:
        recommendations.append({
            'parameter': 'Humidity',
            'status': 'success',
            'message': f'Humidity is suitable ({humidity}%).',
            'emoji': '💨'
        })
    
    # Nitrogen check
    if nitrogen < nutrients['nitrogen'] - 10:
        recommendations.append({
            'parameter': 'Nitrogen',
            'status': 'warning',
            'message': f'Nitrogen is low ({nitrogen}ppm). Add nitrogen fertilizer.',
            'emoji': '🧪'
        })
    elif nitrogen > nutrients['nitrogen'] + 15:
        recommendations.append({
            'parameter': 'Nitrogen',
            'status': 'info',
            'message': f'Nitrogen is high ({nitrogen}ppm). Slightly excessive.',
            'emoji': '🧪'
        })
    else:
        recommendations.append({
            'parameter': 'Nitrogen',
            'status': 'success',
            'message': f'Nitrogen level is optimal ({nitrogen}ppm).',
            'emoji': '🧪'
        })
    
    # Phosphorus check
    if phosphorus < nutrients['phosphorus'] - 5:
        recommendations.append({
            'parameter': 'Phosphorus',
            'status': 'warning',
            'message': f'Phosphorus is low ({phosphorus}ppm). Add phosphorus fertilizer.',
            'emoji': '🧪'
        })
    else:
        recommendations.append({
            'parameter': 'Phosphorus',
            'status': 'success',
            'message': f'Phosphorus level is adequate ({phosphorus}ppm).',
            'emoji': '🧪'
        })
    
    # Potassium check
    if potassium < nutrients['potassium'] - 5:
        recommendations.append({
            'parameter': 'Potassium',
            'status': 'warning',
            'message': f'Potassium is low ({potassium}ppm). Add potassium fertilizer.',
            'emoji': '🧪'
        })
    else:
        recommendations.append({
            'parameter': 'Potassium',
            'status': 'success',
            'message': f'Potassium level is adequate ({potassium}ppm).',
            'emoji': '🧪'
        })
    
    return recommendations

def calculate_soil_health(nitrogen, phosphorus, potassium):
    """Calculate soil health score (0-100)"""
    # Normalize nutrients (assuming max values)
    n_score = min(nitrogen / 150 * 100, 100)
    p_score = min(phosphorus / 80 * 100, 100)
    k_score = min(potassium / 500 * 100, 100)
    
    # Average score
    health = (n_score + p_score + k_score) / 3
    return health

def calculate_crop_suitability(crop, rainfall, temperature, humidity):
    """Calculate crop suitability score (0-100)"""
    score = calculate_crop_suitability_detailed(crop, rainfall, temperature, humidity)
    return score

def calculate_crop_suitability_detailed(crop, rainfall, temperature, humidity):
    """Detailed crop suitability calculation"""
    optimal = OPTIMAL_RANGES[crop]
    score = 100
    
    # Rainfall score
    r_min, r_max = optimal['rainfall']
    if rainfall < r_min:
        score -= (r_min - rainfall) / r_min * 20
    elif rainfall > r_max:
        score -= (rainfall - r_max) / r_max * 20
    
    # Temperature score
    t_min, t_max = optimal['temperature']
    if temperature < t_min:
        score -= (t_min - temperature) * 2
    elif temperature > t_max:
        score -= (temperature - t_max) * 2
    
    # Humidity score
    h_min, h_max = optimal['humidity']
    if humidity < h_min:
        score -= (h_min - humidity) * 0.5
    elif humidity > h_max:
        score -= (humidity - h_max) * 0.5
    
    return max(10, min(100, score))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
