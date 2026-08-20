"""
Weather Service - Fetch real-time weather data from OpenMeteo API (free, no API key required)
"""
import requests
import json
from datetime import datetime

class WeatherService:
    """Fetch weather data for agricultural predictions"""
    
    # OpenMeteo API (free, no API key needed)
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
    
    # Default coordinates (can be changed based on user location)
    DEFAULT_COORDS = {
        'latitude': 28.6139,  # Delhi, India
        'longitude': 77.2090,
        'name': 'Delhi, India'
    }
    
    @staticmethod
    def get_coordinates_from_location(location_name):
        """
        Get latitude and longitude from location name
        Args:
            location_name (str): City/location name
        Returns:
            dict: {'latitude': float, 'longitude': float, 'name': str}
        """
        try:
            params = {
                'name': location_name,
                'count': 1,
                'language': 'en',
                'format': 'json'
            }
            response = requests.get(WeatherService.GEOCODING_URL, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if 'results' in data and len(data['results']) > 0:
                    result = data['results'][0]
                    return {
                        'latitude': result['latitude'],
                        'longitude': result['longitude'],
                        'name': f"{result['name']}, {result.get('country', '')}"
                    }
        except Exception as e:
            print(f"Error getting coordinates: {e}")
        
        # Return default if error
        return WeatherService.DEFAULT_COORDS
    
    @staticmethod
    def get_weather(latitude, longitude):
        """
        Fetch current weather and forecast data
        Args:
            latitude (float): Latitude of location
            longitude (float): Longitude of location
        Returns:
            dict: Weather data with current conditions and forecast
        """
        try:
            params = {
                'latitude': latitude,
                'longitude': longitude,
                'current': 'temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m',
                'daily': 'weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,relative_humidity_2m_max',
                'timezone': 'auto',
                'forecast_days': 7
            }
            
            response = requests.get(WeatherService.BASE_URL, params=params, timeout=5)
            
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error fetching weather: {e}")
        
        return None
    
    @staticmethod
    def parse_weather_data(weather_data):
        """
        Parse raw weather data into agricultural parameters
        Args:
            weather_data (dict): Raw weather data from API
        Returns:
            dict: Parsed weather with temperature, humidity, rainfall forecast
        """
        if not weather_data:
            return None
        
        try:
            current = weather_data.get('current', {})
            daily = weather_data.get('daily', {})
            
            # Current conditions
            temperature = current.get('temperature_2m', 25)
            humidity = current.get('relative_humidity_2m', 60)
            
            # Extract meaningful rainfall (precipitation forecast for next 7 days)
            precipitation_data = daily.get('precipitation_sum', [])
            rainfall_week = sum(precipitation_data[:7]) if precipitation_data else 0
            
            # Convert to monthly estimate (rainfall_mm)
            rainfall_mm = rainfall_week * 4.3  # Approximate weeks per month
            
            parsed = {
                'status': 'success',
                'timestamp': current.get('time', datetime.now().isoformat()),
                'location': {
                    'latitude': weather_data.get('latitude'),
                    'longitude': weather_data.get('longitude'),
                    'timezone': weather_data.get('timezone')
                },
                'current_weather': {
                    'temperature': round(temperature, 1),
                    'humidity': round(humidity, 1),
                    'wind_speed': current.get('wind_speed_10m', 0),
                    'weather_code': current.get('weather_code')
                },
                'agricultural_parameters': {
                    'temperature': round(temperature, 1),
                    'humidity': round(humidity, 1),
                    'rainfall_mm': round(rainfall_mm, 1),
                    'wind_speed': round(current.get('wind_speed_10m', 0), 1),
                    'rainfall_forecast_7days': round(rainfall_week, 1)
                },
                'daily_forecast': {
                    'dates': daily.get('time', []),
                    'max_temp': daily.get('temperature_2m_max', []),
                    'min_temp': daily.get('temperature_2m_min', []),
                    'precipitation': daily.get('precipitation_sum', []),
                    'humidity': daily.get('relative_humidity_2m_max', [])
                }
            }
            
            return parsed
        
        except Exception as e:
            print(f"Error parsing weather data: {e}")
            return None
    
    @staticmethod
    def get_weather_for_location(location_name=None, latitude=None, longitude=None):
        """
        Main method to get weather for a location
        Args:
            location_name (str): Name of location (e.g., 'New Delhi')
            latitude (float): Latitude (alternative to location_name)
            longitude (float): Longitude (alternative to location_name)
        Returns:
            dict: Parsed weather data
        """
        # Get coordinates
        if location_name:
            coords = WeatherService.get_coordinates_from_location(location_name)
        elif latitude and longitude:
            coords = {'latitude': latitude, 'longitude': longitude}
        else:
            coords = WeatherService.DEFAULT_COORDS
        
        # Fetch weather
        weather_data = WeatherService.get_weather(coords['latitude'], coords['longitude'])
        
        # Parse and return
        parsed = WeatherService.parse_weather_data(weather_data)
        
        if parsed:
            parsed['location_info'] = location_name or f"{coords['latitude']}, {coords['longitude']}"
        
        return parsed

# Test the service
if __name__ == '__main__':
    # Test with Delhi
    weather = WeatherService.get_weather_for_location('Delhi')
    print(json.dumps(weather, indent=2))
