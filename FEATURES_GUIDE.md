# 🌾 AgriAI - New Features Guide

## ✨ What's New

Your application now has **3 major new features** implemented:

### 1. 🔐 **Phone Number + OTP Authentication**
- Users register/login using their phone number
- OTP (One-Time Password) sent automatically
- No password needed - more secure and user-friendly
- User data stored locally in `data/users.json`

### 2. 📍 **Location-Based Auto-Fetch**
- Users select their location/area after login
- **Automatically fetches:**
  - Real-time weather (temperature, humidity, rainfall)
  - Regional information
  - Soil type data
  - Agricultural parameters
- All data pre-fills the prediction form

### 3. 🌦️ **Automatic Weather Integration**
- Connects to free OpenMeteo API (no API key needed)
- Updates weather data automatically every time user opens the app
- Weather data immediately available for crop predictions
- Supports 15+ Indian locations

---

## 📋 How to Use

### **Step 1: User Registration/Login**

#### **First-Time User (Registration)**
1. Go to http://localhost:5000
2. Click **Register** tab
3. Enter:
   - Full Name
   - Email
   - Phone Number (format: +91XXXXXXXXXX)
4. Click "Register" button
5. **OTP will be sent** - Check browser console for demo OTP

#### **Returning User (Login)**
1. Click **Login** tab
2. Enter phone number
3. Click "Send OTP"
4. **Check console for OTP code** (shows in browser dev tools)
5. Enter OTP and click "Verify & Login"

### **Step 2: Location Setup**

After successful login:
1. Select your location from dropdown
   - Available: Delhi, Mumbai, Bangalore, Punjab, Tamil Nadu, Karnataka, etc.
2. Click the location
3. **All parameters auto-populate:**
   - 🌡️ Current Temperature
   - 🌧️ Rainfall Amount
   - 💨 Humidity Level
   - 🪨 Soil Type
4. Click "Continue to Dashboard"

### **Step 3: Crop Yield Prediction**

1. Navigate to "📊 Yield Prediction"
2. **Weather fields are pre-filled** with location data
3. Fill remaining fields:
   - Crop Type (Rice, Wheat, Maize, etc.)
   - Region
   - Soil Type
   - Nutrient levels (Nitrogen, Phosphorus, Potassium)
4. Click "🚀 Predict Yield"
5. Get instant predictions and recommendations!

---

## 🔌 API Endpoints

### **Authentication Endpoints**

```bash
# Send OTP
POST /api/auth/send-otp
{
  "phone": "+91XXXXXXXXXX"
}

# Verify OTP
POST /api/auth/verify-otp
{
  "phone": "+91XXXXXXXXXX",
  "otp": "123456"
}

# Register User
POST /api/auth/register
{
  "phone": "+91XXXXXXXXXX",
  "name": "John Farmer",
  "email": "john@farm.com"
}

# Get Current User
GET /api/auth/get-user

# Logout
POST /api/auth/logout
```

### **Location Endpoints**

```bash
# Fetch location data with weather
GET /api/location/fetch?location=Delhi

# Get crop recommendations for location
GET /api/location/crops?location=Delhi

# Get list of available locations
GET /api/location/list
```

### **Weather Endpoint**

```bash
# Get weather for location
GET /api/weather?location=Delhi
```

---

## 📁 New Files Created

### **Backend Services**
- `backend/services/auth_service.py` - OTP and user management
- `backend/services/weather_service.py` - Weather API integration
- `backend/services/location_service.py` - Location-based auto-fetch
- `backend/services/create_mock_models.py` - ML model generation

### **Frontend**
- Updated `backend/templates/index.html` - Added auth modal and location setup
- Updated `backend/static/js/script.js` - Auth and location logic
- Updated `backend/static/css/style.css` - Auth modal styling

### **Backend Updates**
- Updated `backend/app.py` - Added 12+ new endpoints
- Updated `requirements.txt` - Added `requests` library

### **Data Storage**
- `backend/data/users.json` - User registration data
- `backend/data/otp_log.json` - OTP log (optional)

---

## 🌍 Available Locations

The system supports these Indian locations with real weather data:

```
Delhi, Mumbai, Bangalore, Punjab, Tamil Nadu, 
Karnataka, Maharashtra, Uttar Pradesh, Haryana, 
Rajasthan, Bihar, Odisha, West Bengal, 
Telangana, Andhra Pradesh
```

Want to add more? Edit `backend/services/location_service.py` and add locations to `LOCATION_DATABASE`.

---

## 🔒 Security Notes

### **For Development (Demo Mode)**
- OTP is displayed in browser console
- Users data saved locally in JSON file
- Secret key is hardcoded

### **For Production**
1. **Use Real OTP Service:**
   ```python
   # In auth_service.py, replace OTP sending with Twilio/Firebase
   import twilio.rest
   ```

2. **Use Real Database:**
   ```python
   # Replace JSON storage with PostgreSQL/MongoDB
   from sqlalchemy import create_engine
   ```

3. **Enable HTTPS & Secure Sessions:**
   ```python
   app.config['SESSION_COOKIE_SECURE'] = True
   app.config['SESSION_COOKIE_HTTPONLY'] = True
   ```

4. **Use Environment Variables:**
   ```python
   import os
   SECRET_KEY = os.environ.get('SECRET_KEY')
   ```

---

## 🧪 Testing the Features

### **Test 1: Register New User**
```
Phone: +919876543210
Name: Test Farmer
Email: test@farm.com
Check console for OTP
```

### **Test 2: Auto-Fetch Weather**
1. Login
2. Select "Delhi" from location dropdown
3. Watch fields auto-populate with current weather!

### **Test 3: Make Prediction**
1. Use auto-populated weather data
2. Fill crop and soil details
3. Get yield prediction instantly

---

## 📊 Data Flow

```
User Registration
    ↓
OTP Verification
    ↓
Location Selection
    ↓
Auto-Fetch: Weather + Region + Soil Data
    ↓
Form Pre-Population
    ↓
Crop Yield Prediction
    ↓
Get Recommendations
```

---

## ⚠️ Known Demo Limitations

1. **OTP shown in console** (use Twilio for production)
2. **Users data in JSON** (use database for production)
3. **No email notifications** (add email service)
4. **Limited locations** (easy to add more)

---

## 🚀 Next Steps

To deploy this app:

1. **Fix limitations** (OTP service, database, email)
2. **Train real ML models** (improve yield predictions)
3. **Add more locations** (expand to all of India)
4. **Deploy to cloud** (Render, Railway, or Cloud Run)
5. **Add mobile app** (React Native/Flutter)

---

## 📞 Support

For issues or questions about the new features:

1. Check browser console (F12) for error messages
2. Check Flask server logs for API errors
3. Verify phone number format: `+91XXXXXXXXXX`
4. Clear browser cache if UI doesn't update

---

**Created:** August 2026  
**Version:** 2.0 (With Auth & Location Features)  
**Status:** Ready for Testing ✅
