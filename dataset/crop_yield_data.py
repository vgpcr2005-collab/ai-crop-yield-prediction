"""
Generate synthetic crop yield dataset
"""
import pandas as pd
import numpy as np
import os

def generate_crop_yield_dataset(n_samples=1000):
    """
    Generate a realistic crop yield dataset
    """
    np.random.seed(42)
    
    crops = ['Rice', 'Wheat', 'Maize', 'Cotton', 'Sugarcane', 'Soybean', 'Barley', 'Pulses']
    soil_types = ['Loamy', 'Sandy', 'Clay', 'Silt', 'Peaty', 'Chalky']
    regions = ['North', 'South', 'East', 'West', 'Central', 'Coastal']
    
    data = {
        'Crop': np.random.choice(crops, n_samples),
        'Region': np.random.choice(regions, n_samples),
        'Soil_Type': np.random.choice(soil_types, n_samples),
        'Rainfall_mm': np.random.uniform(400, 2500, n_samples),
        'Temperature_C': np.random.uniform(15, 35, n_samples),
        'Humidity_percent': np.random.uniform(30, 90, n_samples),
        'Nitrogen_ppm': np.random.uniform(20, 150, n_samples),
        'Phosphorus_ppm': np.random.uniform(10, 80, n_samples),
        'Potassium_ppm': np.random.uniform(100, 500, n_samples),
        'Area_hectares': np.random.uniform(0.5, 50, n_samples),
        'Irrigation_times_per_week': np.random.uniform(0, 7, n_samples),
        'Fertilizer_kg_per_hectare': np.random.uniform(50, 300, n_samples),
    }
    
    df = pd.DataFrame(data)
    
    # Generate yield based on conditions (with some realistic patterns)
    yield_base = np.random.uniform(1, 5, n_samples)
    
    # Crop-specific patterns
    for idx, row in df.iterrows():
        crop = row['Crop']
        rainfall = row['Rainfall_mm']
        temp = row['Temperature_C']
        nitrogen = row['Nitrogen_ppm']
        humidity = row['Humidity_percent']
        
        # Adjust yield based on crop type
        if crop == 'Rice':
            yield_base[idx] = 4.0 + (rainfall / 1000) * 1.5 - abs(temp - 28) * 0.05
        elif crop == 'Wheat':
            yield_base[idx] = 3.5 + (rainfall / 1500) * 1.2 - abs(temp - 22) * 0.04
        elif crop == 'Maize':
            yield_base[idx] = 4.5 + (rainfall / 1200) * 1.3 - abs(temp - 24) * 0.05
        elif crop == 'Cotton':
            yield_base[idx] = 2.0 + (rainfall / 1000) * 0.8 - abs(temp - 26) * 0.03
        elif crop == 'Sugarcane':
            yield_base[idx] = 60 + (rainfall / 800) * 20 - abs(temp - 25) * 1
        elif crop == 'Soybean':
            yield_base[idx] = 2.5 + (rainfall / 1000) * 1.0 - abs(temp - 23) * 0.04
        elif crop == 'Barley':
            yield_base[idx] = 3.0 + (rainfall / 1200) * 0.9 - abs(temp - 20) * 0.04
        else:  # Pulses
            yield_base[idx] = 1.8 + (rainfall / 1000) * 0.7 - abs(temp - 22) * 0.03
        
        # Soil nutrient impact
        yield_base[idx] += (nitrogen / 100) * 0.2
        
        # Add noise
        yield_base[idx] += np.random.normal(0, 0.3)
        yield_base[idx] = max(0.5, yield_base[idx])  # Ensure positive yield
    
    df['Yield_tons_per_hectare'] = yield_base
    
    return df

def main():
    # Create dataset
    df = generate_crop_yield_dataset(1000)
    
    # Save to CSV
    dataset_path = 'crop_yield_data.csv'
    df.to_csv(dataset_path, index=False)
    print(f"Dataset created: {dataset_path}")
    print(f"Shape: {df.shape}")
    print(f"\nFirst few rows:\n{df.head()}")
    print(f"\nDataset statistics:\n{df.describe()}")

if __name__ == "__main__":
    main()
