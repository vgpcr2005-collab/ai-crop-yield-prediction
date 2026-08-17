"""
Train ML models for crop yield prediction and crop recommendation
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import pickle
import json

def load_and_prepare_data():
    """Load and prepare the dataset"""
    df = pd.read_csv('dataset/crop_yield_data.csv')
    
    # Encode categorical variables
    le_crop = LabelEncoder()
    le_region = LabelEncoder()
    le_soil = LabelEncoder()
    
    df['Crop_encoded'] = le_crop.fit_transform(df['Crop'])
    df['Region_encoded'] = le_region.fit_transform(df['Region'])
    df['Soil_Type_encoded'] = le_soil.fit_transform(df['Soil_Type'])
    
    # Save label encoders
    with open('models/crop_encoder.pkl', 'wb') as f:
        pickle.dump(le_crop, f)
    with open('models/region_encoder.pkl', 'wb') as f:
        pickle.dump(le_region, f)
    with open('models/soil_encoder.pkl', 'wb') as f:
        pickle.dump(le_soil, f)
    
    # Features and target
    feature_cols = ['Crop_encoded', 'Region_encoded', 'Soil_Type_encoded', 
                   'Rainfall_mm', 'Temperature_C', 'Humidity_percent',
                   'Nitrogen_ppm', 'Phosphorus_ppm', 'Potassium_ppm',
                   'Area_hectares', 'Irrigation_times_per_week', 'Fertilizer_kg_per_hectare']
    
    X = df[feature_cols]
    y = df['Yield_tons_per_hectare']
    
    # Save feature names
    with open('models/feature_names.pkl', 'wb') as f:
        pickle.dump(feature_cols, f)
    
    return X, y, df, le_crop, le_region, le_soil

def train_models(X, y):
    """Train multiple models and select the best"""
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Save scaler
    with open('models/scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    
    models = {}
    
    # Linear Regression
    lr_model = LinearRegression()
    lr_model.fit(X_train_scaled, y_train)
    lr_pred = lr_model.predict(X_test_scaled)
    lr_r2 = r2_score(y_test, lr_pred)
    lr_rmse = np.sqrt(mean_squared_error(y_test, lr_pred))
    models['Linear Regression'] = {'model': lr_model, 'r2': lr_r2, 'rmse': lr_rmse}
    
    # Random Forest
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    rf_model.fit(X_train_scaled, y_train)
    rf_pred = rf_model.predict(X_test_scaled)
    rf_r2 = r2_score(y_test, rf_pred)
    rf_rmse = np.sqrt(mean_squared_error(y_test, rf_pred))
    models['Random Forest'] = {'model': rf_model, 'r2': rf_r2, 'rmse': rf_rmse}
    
    # Gradient Boosting
    gb_model = GradientBoostingRegressor(n_estimators=100, random_state=42)
    gb_model.fit(X_train_scaled, y_train)
    gb_pred = gb_model.predict(X_test_scaled)
    gb_r2 = r2_score(y_test, gb_pred)
    gb_rmse = np.sqrt(mean_squared_error(y_test, gb_pred))
    models['Gradient Boosting'] = {'model': gb_model, 'r2': gb_r2, 'rmse': gb_rmse}
    
    # Print comparison
    print("\n=== Model Performance Comparison ===")
    for name, metrics in models.items():
        print(f"\n{name}:")
        print(f"  R² Score: {metrics['r2']:.4f}")
        print(f"  RMSE: {metrics['rmse']:.4f}")
    
    # Select best model (highest R²)
    best_model_name = max(models, key=lambda x: models[x]['r2'])
    best_model = models[best_model_name]['model']
    
    print(f"\n✓ Best Model: {best_model_name}")
    
    # Save best model
    with open('models/yield_prediction_model.pkl', 'wb') as f:
        pickle.dump(best_model, f)
    
    return best_model, models, scaler

def train_crop_recommendation_model(df, le_crop):
    """Train a simple crop recommendation model based on conditions"""
    # Calculate average yield for each crop
    crop_stats = df.groupby('Crop').agg({
        'Yield_tons_per_hectare': 'mean',
        'Rainfall_mm': 'mean',
        'Temperature_C': 'mean',
        'Humidity_percent': 'mean',
        'Nitrogen_ppm': 'mean'
    }).to_dict()
    
    # Save crop recommendations data
    with open('models/crop_recommendations.json', 'w') as f:
        json.dump(crop_stats, f, indent=4)
    
    print("\n=== Crop Statistics ===")
    for crop in df['Crop'].unique():
        crop_data = df[df['Crop'] == crop]
        avg_yield = crop_data['Yield_tons_per_hectare'].mean()
        print(f"{crop}: Avg Yield = {avg_yield:.2f} tons/hectare")
    
    return crop_stats

def main():
    print("Loading and preparing data...")
    X, y, df, le_crop, le_region, le_soil = load_and_prepare_data()
    
    print("\nTraining models...")
    best_model, all_models, scaler = train_models(X, y)
    
    print("\nTraining crop recommendation model...")
    crop_stats = train_crop_recommendation_model(df, le_crop)
    
    print("\n✓ All models trained and saved successfully!")
    print("  - yield_prediction_model.pkl")
    print("  - crop_recommendations.json")
    print("  - scaler.pkl")
    print("  - Encoders (crop, region, soil)")

if __name__ == "__main__":
    main()
