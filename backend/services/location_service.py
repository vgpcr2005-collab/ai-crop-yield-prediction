"""
Location Service - Auto-fetch weather and agricultural parameters by area/location
"""
from weather_service import WeatherService
import json

class LocationService:
    """Fetch all agricultural parameters for a specific location"""
    
    # Indian locations database (can be extended)
    LOCATION_DATABASE = {
        'Delhi': {'lat': 28.7041, 'lon': 77.1025, 'region': 'North', 'soil': 'Loamy'},
        'Mumbai': {'lat': 19.0760, 'lon': 72.8777, 'region': 'West', 'soil': 'Sandy'},
        'Bangalore': {'lat': 12.9716, 'lon': 77.5946, 'region': 'South', 'soil': 'Loamy'},
        'Punjab': {'lat': 31.5204, 'lon': 74.3587, 'region': 'North', 'soil': 'Loamy'},
        'Tamil Nadu': {'lat': 11.1271, 'lon': 79.2088, 'region': 'South', 'soil': 'Loamy'},
        'Karnataka': {'lat': 15.3173, 'lon': 75.7139, 'region': 'South', 'soil': 'Loamy'},
        'Maharashtra': {'lat': 19.7515, 'lon': 75.7139, 'region': 'West', 'soil': 'Black'},
        'Uttar Pradesh': {'lat': 26.8467, 'lon': 80.9462, 'region': 'Central', 'soil': 'Loamy'},
        'Haryana': {'lat': 29.0588, 'lon': 77.0745, 'region': 'North', 'soil': 'Loamy'},
        'Rajasthan': {'lat': 27.0238, 'lon': 74.2179, 'region': 'Central', 'soil': 'Sandy'},
        'Bihar': {'lat': 25.5941, 'lon': 85.1376, 'region': 'East', 'soil': 'Clay'},
        'Odisha': {'lat': 20.9517, 'lon': 85.0985, 'region': 'East', 'soil': 'Laterite'},
        'West Bengal': {'lat': 24.8915, 'lon': 88.2868, 'region': 'East', 'soil': 'Clay'},
        'Telangana': {'lat': 17.3850, 'lon': 78.4867, 'region': 'South', 'soil': 'Black'},
        'Andhra Pradesh': {'lat': 14.1995, 'lon': 79.8243, 'region': 'South', 'soil': 'Loamy'},
    }
    
    @staticmethod
    def get_location_data(location_name):
        """
        Get complete data for a location
        Returns weather, region, soil type, and other parameters
        """
        # Normalize location name
        location_name = location_name.strip().title()
        
        if location_name not in LocationService.LOCATION_DATABASE:
            return {'status': 'error', 'message': f'Location "{location_name}" not found'}
        
        location_info = LocationService.LOCATION_DATABASE[location_name]
        
        # Fetch real-time weather
        weather_data = WeatherService.get_weather_for_location(
            latitude=location_info['lat'],
            longitude=location_info['lon']
        )
        
        if not weather_data or weather_data.get('status') == 'error':
            return {'status': 'error', 'message': 'Could not fetch weather data'}
        
        # Combine location data with weather
        result = {
            'status': 'success',
            'location': location_name,
            'location_info': {
                'latitude': location_info['lat'],
                'longitude': location_info['lon'],
                'region': location_info['region'],
                'soil_type': location_info['soil']
            },
            'weather': weather_data.get('current_weather', {}),
            'agricultural_parameters': {
                'rainfall_mm': weather_data.get('agricultural_parameters', {}).get('rainfall_mm', 600),
                'temperature': weather_data.get('agricultural_parameters', {}).get('temperature', 25),
                'humidity': weather_data.get('agricultural_parameters', {}).get('humidity', 65),
                'region': location_info['region'],
                'soil_type': location_info['soil'],
                'wind_speed': weather_data.get('agricultural_parameters', {}).get('wind_speed', 10)
            },
            'forecast': weather_data.get('daily_forecast', {}),
            'timestamp': weather_data.get('timestamp')
        }
        
        return result
    
    @staticmethod
    def get_suggested_crops(location_name):
        """
        Get crop recommendations for a location based on weather/soil
        """
        location_data = LocationService.get_location_data(location_name)
        
        if location_data.get('status') == 'error':
            return location_data
        
        # Crop suitability rules
        params = location_data['agricultural_parameters']
        rainfall = params['rainfall_mm']
        temp = params['temperature']
        soil = params['soil_type']
        
        crop_scores = {
            'Rice': 0,
            'Wheat': 0,
            'Maize': 0,
            'Cotton': 0,
            'Sugarcane': 0,
            'Soybean': 0,
            'Barley': 0,
            'Pulses': 0
        }
        
        # Score based on rainfall
        if 700 <= rainfall <= 2500:
            crop_scores['Rice'] += 30
            crop_scores['Sugarcane'] += 25
        if 400 <= rainfall <= 1000:
            crop_scores['Wheat'] += 30
            crop_scores['Barley'] += 25
        if 800 <= rainfall <= 1500:
            crop_scores['Maize'] += 30
            crop_scores['Soybean'] += 25
        if 500 <= rainfall <= 1250:
            crop_scores['Cotton'] += 30
        if 450 <= rainfall <= 1100:
            crop_scores['Soybean'] += 15
        if 400 <= rainfall <= 800:
            crop_scores['Pulses'] += 30
        
        # Score based on temperature
        if 25 <= temp <= 30:
            crop_scores['Rice'] += 20
        if 20 <= temp <= 25:
            crop_scores['Wheat'] += 20
            crop_scores['Barley'] += 20
        if 21 <= temp <= 27:
            crop_scores['Maize'] += 20
        if 21 <= temp <= 32:
            crop_scores['Cotton'] += 20
        if 20 <= temp <= 30:
            crop_scores['Sugarcane'] += 20
            crop_scores['Soybean'] += 20
        if 15 <= temp <= 25:
            crop_scores['Pulses'] += 20
        
        # Sort by score
        sorted_crops = sorted(crop_scores.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'status': 'success',
            'location': location_name,
            'agricultural_parameters': params,
            'recommended_crops': [
                {
                    'rank': i + 1,
                    'crop': crop,
                    'suitability_score': score,
                    'suitability': 'High' if score >= 70 else 'Medium' if score >= 40 else 'Low'
                }
                for i, (crop, score) in enumerate(sorted_crops[:5])
            ]
        }
    
    @staticmethod
    def get_available_locations():
        """Get list of all available locations"""
        return {
            'status': 'success',
            'locations': list(LocationService.LOCATION_DATABASE.keys()),
            'total': len(LocationService.LOCATION_DATABASE)
        }

# Test
if __name__ == '__main__':
    print("Testing Location Service...")
    
    # Test get location data
    result = LocationService.get_location_data('Delhi')
    print(f"\n1. Location Data for Delhi:")
    print(json.dumps({k: v for k, v in result.items() if k != 'forecast'}, indent=2))
    
    # Test crop suggestions
    result = LocationService.get_suggested_crops('Punjab')
    print(f"\n2. Suggested Crops for Punjab:")
    print(json.dumps(result, indent=2))
    
    # Test available locations
    result = LocationService.get_available_locations()
    print(f"\n3. Available Locations: {result['total']}")
    print(f"   {', '.join(result['locations'][:5])}...")
    
    print("\n✅ Location service working!")
