"""
Test script to verify all endpoints are working
"""
import requests
import json

API_BASE = 'http://localhost:5000/api'

print("=" * 60)
print("🧪 AgriAI API Test Suite")
print("=" * 60)

# Test 1: Send OTP
print("\n1️⃣  Testing OTP Send...")
try:
    response = requests.post(f'{API_BASE}/auth/send-otp', 
        json={'phone': '+919876543210'},
        timeout=5)
    data = response.json()
    print(f"✅ Status: {data['status']}")
    print(f"📱 OTP: {data.get('otp', 'N/A')}")
    otp = data.get('otp')
except Exception as e:
    print(f"❌ Error: {e}")
    otp = None

# Test 2: Weather API
print("\n2️⃣  Testing Weather API...")
try:
    response = requests.get(f'{API_BASE}/weather?location=Delhi', timeout=5)
    data = response.json()
    if data['status'] == 'success':
        params = data.get('agricultural_parameters', {})
        print(f"✅ Status: {data['status']}")
        print(f"🌡️  Temperature: {params.get('temperature')}°C")
        print(f"🌧️  Rainfall: {params.get('rainfall_mm')} mm")
        print(f"💨 Humidity: {params.get('humidity')}%")
    else:
        print(f"❌ Error: {data.get('message')}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 3: Location Fetch
print("\n3️⃣  Testing Location Fetch...")
try:
    response = requests.get(f'{API_BASE}/location/fetch?location=Delhi', timeout=5)
    data = response.json()
    if data['status'] == 'success':
        print(f"✅ Status: {data['status']}")
        print(f"📍 Location: {data.get('location')}")
        print(f"🪨 Soil Type: {data['location_info'].get('soil_type')}")
        print(f"🌍 Region: {data['location_info'].get('region')}")
    else:
        print(f"❌ Error: {data.get('message')}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 4: Crop Prediction
print("\n4️⃣  Testing Yield Prediction...")
try:
    prediction_data = {
        'crop': 'Rice',
        'region': 'North',
        'soil_type': 'Loamy',
        'rainfall': 850,
        'temperature': 28,
        'humidity': 70,
        'nitrogen': 80,
        'phosphorus': 40,
        'potassium': 50,
        'area': 2.5,
        'irrigation': 4,
        'fertilizer': 150
    }
    response = requests.post(f'{API_BASE}/predict',
        json=prediction_data,
        timeout=5)
    data = response.json()
    if data['status'] == 'success':
        print(f"✅ Status: {data['status']}")
        print(f"🌾 Predicted Yield: {data.get('predicted_yield')} tons/hectare")
        print(f"🎯 Suitability: {data.get('suitability')}%")
        print(f"🌱 Soil Health: {data.get('soil_health')}")
    else:
        print(f"❌ Error: {data.get('message')}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 5: Crop Recommendations
print("\n5️⃣  Testing Crop Recommendations...")
try:
    response = requests.get(f'{API_BASE}/location/crops?location=Punjab', timeout=5)
    data = response.json()
    if data['status'] == 'success':
        print(f"✅ Status: {data['status']}")
        print(f"📍 Location: {data.get('location')}")
        crops = data.get('recommended_crops', [])
        for crop_info in crops[:3]:
            print(f"   • {crop_info['crop']}: {crop_info['suitability']} ({crop_info['suitability_score']} score)")
    else:
        print(f"❌ Error: {data.get('message')}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 6: Available Locations
print("\n6️⃣  Testing Location List...")
try:
    response = requests.get(f'{API_BASE}/location/list', timeout=5)
    data = response.json()
    if data['status'] == 'success':
        print(f"✅ Status: {data['status']}")
        print(f"📍 Total Locations: {data.get('total')}")
        locs = data.get('locations', [])
        print(f"   Sample: {', '.join(locs[:5])}...")
    else:
        print(f"❌ Error: {data.get('message')}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 60)
print("✅ Test suite completed!")
print("=" * 60)
