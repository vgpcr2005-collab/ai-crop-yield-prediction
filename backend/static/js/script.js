// JavaScript for AgriAI Application

const API_BASE_URL = '/api';

function normalizePhoneNumber(phone) {
    const trimmed = phone.trim();
    if (/^\d{10}$/.test(trimmed)) {
        return `+91${trimmed}`;
    }
    return trimmed;
}

// ============================================
// AUTHENTICATION FUNCTIONS
// ============================================

let currentEmail = null;

function switchAuthTab(tab) {
    // Hide all tabs
    document.querySelectorAll('.auth-tab-content').forEach(el => {
        el.classList.remove('active');
    });
    
    // Remove active from all buttons
    document.querySelectorAll('.auth-tab').forEach(el => {
        el.classList.remove('active');
    });
    
    // Show selected tab
    document.getElementById(tab + 'Tab').classList.add('active');
    event.target.classList.add('active');
}

async function sendEmailCode() {
    try {
        const email = document.getElementById('loginEmail').value.trim().toLowerCase();
        
        if (!email) {
            showAuthError('Please enter your Gmail address');
            return;
        }
        
        const response = await fetch(`${API_BASE_URL}/auth/send-email-code`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email })
        });
        
        const result = await response.json();
        
        if (result.status === 'success') {
            currentEmail = email;
            document.getElementById('emailCodeSection').classList.remove('hidden');
            showAuthError(''); // Clear errors
            console.log(result.message);
        } else {
            showAuthError(result.message || 'Error sending OTP');
        }
    } catch (error) {
        showAuthError('Error: ' + error.message);
    }
}

async function verifyEmailCode() {
    try {
        const email = currentEmail;
        const code = document.getElementById('loginEmailCode').value.trim();
        
        if (!code || code.length !== 6) {
            showAuthError('Please enter the 6-digit email code');
            return;
        }
        
        const response = await fetch(`${API_BASE_URL}/auth/verify-email-code`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, code })
        });
        
        const result = await response.json();
        
        if (result.status === 'success') {
            console.log('Login successful!', result.user);
            localStorage.setItem('email', email);
            localStorage.setItem('user', JSON.stringify(result.user));
            
            // Hide auth modal
            document.getElementById('authModal').classList.add('hidden');
            
            // Show location setup
            showLocationSetup();
        } else {
            showAuthError(result.message || 'OTP verification failed');
        }
    } catch (error) {
        showAuthError('Error: ' + error.message);
    }
}

function resetEmailCode() {
    document.getElementById('loginEmailCode').value = '';
    document.getElementById('emailCodeSection').classList.add('hidden');
    document.getElementById('loginEmail').value = '';
    currentEmail = null;
}

async function registerUser() {
    try {
        const name = document.getElementById('regName').value.trim();
        const email = document.getElementById('regEmail').value.trim();
        const phone = '';
        
        if (!name || !email) {
            showAuthError('All fields are required');
            return;
        }
        
        const response = await fetch(`${API_BASE_URL}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email, phone })
        });
        
        const result = await response.json();
        
        if (result.status === 'success') {
            showAuthError('');
            alert('Registration successful! A verification code was sent to ' + email);
            
            // Switch to login tab and populate phone
            switchAuthTab('login');
            document.getElementById('loginEmail').value = email;
            
            // Auto-send OTP
            currentEmail = email;
            document.getElementById('emailCodeSection').classList.remove('hidden');
        } else {
            showAuthError(result.message || 'Registration failed');
        }
    } catch (error) {
        showAuthError('Error: ' + error.message);
    }
}

function showAuthError(message) {
    const errorDiv = document.getElementById('authError');
    if (message) {
        errorDiv.textContent = message;
        errorDiv.classList.remove('hidden');
    } else {
        errorDiv.classList.add('hidden');
    }
}

// ============================================
// LOCATION SETUP FUNCTIONS
// ============================================

async function showLocationSetup() {
    try {
        // Fetch available locations
        const response = await fetch(`${API_BASE_URL}/location/list`);
        const result = await response.json();
        
        if (result.status === 'success') {
            const select = document.getElementById('locationSelect');
            result.locations.forEach(location => {
                const option = document.createElement('option');
                option.value = location;
                option.textContent = location;
                select.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error loading locations:', error);
    }
    
    document.getElementById('locationSection').classList.remove('hidden');
}

async function fetchLocationParameters() {
    try {
        const location = document.getElementById('locationSelect').value;
        
        if (!location) return;
        
        const response = await fetch(`${API_BASE_URL}/location/fetch?location=${encodeURIComponent(location)}`);
        const result = await response.json();
        
        if (result.status === 'success') {
            const params = result.agricultural_parameters;
            
            // Display location data
            document.getElementById('selectedLocation').textContent = location;
            document.getElementById('locTemp').textContent = params.temperature + '°C';
            document.getElementById('locRainfall').textContent = params.rainfall_mm + ' mm';
            document.getElementById('locHumidity').textContent = params.humidity + '%';
            document.getElementById('locSoil').textContent = params.soil_type;
            
            document.getElementById('locationData').classList.remove('hidden');
            
            // Store location data
            localStorage.setItem('location', location);
            localStorage.setItem('locationData', JSON.stringify(result));
        }
    } catch (error) {
        console.error('Error fetching location data:', error);
    }
}

function confirmLocation() {
    const location = document.getElementById('locationSelect').value;
    if (!location) {
        alert('Please select a location');
        return;
    }
    
    // Hide location section
    document.getElementById('locationSection').classList.add('hidden');
    
    // Show main navigation and sections
    document.getElementById('mainNav').classList.remove('hidden');
    document.querySelector('.container').classList.remove('hidden');
    
    // Auto-populate yield prediction form with location data
    const locationDataStr = localStorage.getItem('locationData');
    if (locationDataStr) {
        const locationData = JSON.parse(locationDataStr);
        const params = locationData.agricultural_parameters;
        
        document.getElementById('yieldRainfall').value = Math.round(params.rainfall_mm);
        document.getElementById('yieldTemperature').value = params.temperature;
        document.getElementById('yieldHumidity').value = params.humidity;
        
        // Show notification
        showWeatherNotification({
            current_weather: locationData.weather,
            location_name: location
        });
    }
}

function skipLocationSetup() {
    document.getElementById('locationSection').classList.add('hidden');
    document.getElementById('mainNav').classList.remove('hidden');
    document.querySelector('.container').classList.remove('hidden');
}

// Initialize authentication on page load
document.addEventListener('DOMContentLoaded', function() {
    // Check if user is already logged in
    const phone = localStorage.getItem('phone');
    
    if (phone) {
        // User is logged in
        console.log('User logged in:', phone);
        document.getElementById('authModal').classList.add('hidden');
        
        // Show location setup or main app
        const location = localStorage.getItem('location');
        if (location) {
            document.getElementById('locationSection').classList.add('hidden');
            document.getElementById('mainNav').classList.remove('hidden');
            document.querySelector('.container').classList.remove('hidden');
        } else {
            showLocationSetup();
        }
    } else {
        // Show auth modal
        document.getElementById('authModal').classList.remove('hidden');
        document.getElementById('mainNav').classList.add('hidden');
        document.querySelector('.container').classList.add('hidden');
    }
    
    console.log('🔐 Auth system initialized');
});

function logoutUser() {
    localStorage.removeItem('phone');
    localStorage.removeItem('user');
    localStorage.removeItem('location');
    localStorage.removeItem('locationData');
    
    // Reload page
    location.reload();
}

// Navigation
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const section = link.getAttribute('data-section');
        navigateTo(section);
    });
});

function navigateTo(section) {
    // Hide all sections
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    
    // Show selected section
    document.getElementById(section).classList.add('active');
    
    // Update nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('data-section') === section) {
            link.classList.add('active');
        }
    });
    
    // Scroll to top
    window.scrollTo(0, 0);
}

// Yield Prediction
async function predictYield() {
    try {
        const data = {
            crop: document.getElementById('yieldCrop').value,
            region: document.getElementById('yieldRegion').value,
            soil_type: document.getElementById('yieldSoil').value,
            rainfall: document.getElementById('yieldRainfall').value,
            temperature: document.getElementById('yieldTemperature').value,
            humidity: document.getElementById('yieldHumidity').value,
            nitrogen: document.getElementById('yieldNitrogen').value,
            phosphorus: document.getElementById('yieldPhosphorus').value,
            potassium: document.getElementById('yieldPotassium').value,
            area: document.getElementById('yieldArea').value,
            irrigation: document.getElementById('yieldIrrigation').value,
            fertilizer: document.getElementById('yieldFertilizer').value
        };
        
        // Validate inputs
        if (!data.crop || !data.region || !data.soil_type) {
            alert('Please fill all required fields');
            return;
        }
        
        const response = await fetch(`${API_BASE_URL}/predict`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) throw new Error('Prediction failed');
        
        const result = await response.json();
        displayYieldResults(result);
        
    } catch (error) {
        console.error('Error:', error);
        alert('Error predicting yield: ' + error.message);
    }
}

function displayYieldResults(result) {
    // Show results
    document.getElementById('yieldResults').classList.remove('hidden');
    document.getElementById('yieldRecommendations').classList.remove('hidden');
    
    // Display values
    document.getElementById('predictedYieldValue').textContent = result.predicted_yield;
    document.getElementById('suitabilityScore').textContent = result.suitability;
    document.getElementById('soilHealthScore').textContent = result.soil_health;
    
    // Display recommendations
    const recList = document.getElementById('recommendationsList');
    recList.innerHTML = '';
    
    result.recommendations.forEach(rec => {
        const recDiv = document.createElement('div');
        recDiv.className = `recommendation-item ${rec.status}`;
        recDiv.innerHTML = `
            <div class="recommendation-emoji">${rec.emoji}</div>
            <div class="recommendation-content">
                <h4>${rec.parameter}</h4>
                <p>${rec.message}</p>
            </div>
        `;
        recList.appendChild(recDiv);
    });
    
    // Scroll to results
    document.getElementById('yieldResults').scrollIntoView({ behavior: 'smooth' });
}

// Crop Recommendation
async function recommendCrop() {
    try {
        const data = {
            rainfall: document.getElementById('recRainfall').value,
            temperature: document.getElementById('recTemperature').value,
            humidity: document.getElementById('recHumidity').value,
            soil_type: document.getElementById('recSoil').value,
            region: 'Central'
        };
        
        // Validate inputs
        if (!data.rainfall || !data.temperature || !data.humidity) {
            alert('Please fill all required fields');
            return;
        }
        
        const response = await fetch(`${API_BASE_URL}/recommend-crop`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) throw new Error('Recommendation failed');
        
        const result = await response.json();
        displayCropRecommendations(result);
        
    } catch (error) {
        console.error('Error:', error);
        alert('Error recommending crops: ' + error.message);
    }
}

function displayCropRecommendations(result) {
    document.getElementById('cropRecommendations').classList.remove('hidden');
    
    const cropsList = document.getElementById('cropsList');
    cropsList.innerHTML = '';
    
    result.recommendations.forEach(crop => {
        const cropDiv = document.createElement('div');
        cropDiv.className = 'crop-recommendation';
        
        let colorClass = crop.suitability > 80 ? 'high' : 
                        crop.suitability > 60 ? 'medium' : 'low';
        
        cropDiv.innerHTML = `
            <div class="crop-rec-info">
                <h4>#${crop.rank} ${crop.crop}</h4>
                <p>Best match for your conditions</p>
            </div>
            <div class="crop-rec-badge ${colorClass}">
                ${crop.suitability}% Suitable
            </div>
        `;
        cropsList.appendChild(cropDiv);
    });
    
    document.getElementById('cropRecommendations').scrollIntoView({ behavior: 'smooth' });
}

// Optimization
async function getOptimization() {
    try {
        const data = {
            crop: document.getElementById('optCrop').value,
            rainfall: document.getElementById('optRainfall').value,
            temperature: document.getElementById('optTemperature').value,
            humidity: document.getElementById('optHumidity').value,
            nitrogen: document.getElementById('optNitrogen').value,
            phosphorus: document.getElementById('optPhosphorus').value,
            potassium: document.getElementById('optPotassium').value,
            irrigation: document.getElementById('optIrrigation').value
        };
        
        // Validate inputs
        if (!data.crop) {
            alert('Please select a crop');
            return;
        }
        
        const response = await fetch(`${API_BASE_URL}/optimization`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) throw new Error('Optimization failed');
        
        const result = await response.json();
        displayOptimizationResults(result);
        
    } catch (error) {
        console.error('Error:', error);
        alert('Error getting optimization: ' + error.message);
    }
}

function displayOptimizationResults(result) {
    document.getElementById('optimizationResults').classList.remove('hidden');
    
    // Display metrics
    document.getElementById('expectedImprovement').textContent = result.expected_improvement + '%';
    document.getElementById('optimalNitrogen').textContent = result.optimal_nutrients.nitrogen + ' ppm';
    document.getElementById('optimalPhosphorus').textContent = result.optimal_nutrients.phosphorus + ' ppm';
    document.getElementById('optimalWater').textContent = result.optimal_water + ' times/week';
    
    // Display recommendations
    const recContainer = document.getElementById('optimizationRecommendations');
    recContainer.innerHTML = '<h3>💡 Optimization Recommendations</h3>';
    
    result.recommendations.forEach(rec => {
        const recDiv = document.createElement('div');
        recDiv.className = `recommendation-item ${rec.status}`;
        recDiv.innerHTML = `
            <div class="recommendation-emoji">${rec.emoji}</div>
            <div class="recommendation-content">
                <h4>${rec.parameter}</h4>
                <p>${rec.message}</p>
            </div>
        `;
        recContainer.appendChild(recDiv);
    });
    
    document.getElementById('optimizationResults').scrollIntoView({ behavior: 'smooth' });
}

// Dashboard
async function loadDashboard() {
    try {
        const response = await fetch(`${API_BASE_URL}/dashboard`);
        
        if (!response.ok) throw new Error('Dashboard data failed');
        
        const result = await response.json();
        displayDashboard(result);
        
    } catch (error) {
        console.error('Error:', error);
        alert('Error loading dashboard: ' + error.message);
    }
}

function displayDashboard(result) {
    document.getElementById('dashboardContent').classList.remove('hidden');
    
    // Crop yield chart
    const cropNames = Object.keys(result.crop_yield);
    const cropYields = Object.values(result.crop_yield);
    
    const cropTrace = {
        x: cropNames,
        y: cropYields,
        type: 'bar',
        marker: { color: 'rgba(46, 204, 113, 0.8)' }
    };
    
    const cropLayout = {
        title: 'Average Yield by Crop',
        xaxis: { title: 'Crop Type' },
        yaxis: { title: 'Yield (tons/hectare)' },
        plot_bgcolor: 'rgba(240, 240, 240, 0.5)',
        paper_bgcolor: 'rgba(255, 255, 255, 0.9)'
    };
    
    Plotly.newPlot('cropYieldChart', [cropTrace], cropLayout);
    
    // Region yield chart
    const regionNames = Object.keys(result.region_yield);
    const regionYields = Object.values(result.region_yield);
    
    const regionTrace = {
        x: regionNames,
        y: regionYields,
        type: 'bar',
        marker: { color: 'rgba(52, 152, 219, 0.8)' }
    };
    
    const regionLayout = {
        title: 'Average Yield by Region',
        xaxis: { title: 'Region' },
        yaxis: { title: 'Yield (tons/hectare)' },
        plot_bgcolor: 'rgba(240, 240, 240, 0.5)',
        paper_bgcolor: 'rgba(255, 255, 255, 0.9)'
    };
    
    Plotly.newPlot('regionYieldChart', [regionTrace], regionLayout);
    
    // Stats
    const statsDiv = document.getElementById('dashboardStats');
    statsDiv.innerHTML = `
        <div class="stat-item">
            <span class="stat-label">Total Records in Dataset:</span>
            <span class="stat-value">${result.dataset_stats.total_records}</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">Number of Crops:</span>
            <span class="stat-value">${result.dataset_stats.crops.length}</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">Number of Regions:</span>
            <span class="stat-value">${result.dataset_stats.regions.length}</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">Rainfall-Yield Correlation:</span>
            <span class="stat-value">${result.correlations.rainfall_yield}</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">Temperature-Yield Correlation:</span>
            <span class="stat-value">${result.correlations.temperature_yield}</span>
        </div>
    `;
    
    document.getElementById('dashboardContent').scrollIntoView({ behavior: 'smooth' });
}

// ============================================
// AUTOMATIC WEATHER DATA INTEGRATION
// ============================================

// Fetch weather data automatically on page load
async function autoFetchWeather(location = 'Delhi') {
    try {
        console.log('🌦️ Fetching weather data for:', location);
        
        const response = await fetch(`${API_BASE_URL}/weather?location=${encodeURIComponent(location)}`);
        
        if (!response.ok) {
            throw new Error('Weather API error');
        }
        
        const weatherData = response.json();
        return weatherData;
        
    } catch (error) {
        console.error('Weather fetch error:', error);
        return null;
    }
}

// Auto-populate weather data into yield prediction form
async function autoPopulateWeather() {
    try {
        // Get weather for default location (Delhi)
        const weather = await autoFetchWeather('Delhi');
        
        if (weather && weather.agricultural_parameters) {
            const params = weather.agricultural_parameters;
            
            // Auto-populate the form fields
            document.getElementById('yieldRainfall').value = Math.round(params.rainfall_mm);
            document.getElementById('yieldTemperature').value = params.temperature;
            document.getElementById('yieldHumidity').value = params.humidity;
            
            console.log('✅ Weather data auto-populated:', params);
            
            // Show notification
            showWeatherNotification(weather);
        }
    } catch (error) {
        console.error('Auto-populate weather error:', error);
    }
}

// Show weather notification banner
function showWeatherNotification(weatherData) {
    if (!weatherData.current_weather) return;
    
    const weather = weatherData.current_weather;
    
    // Create notification HTML
    const notificationHTML = `
        <div id="weatherNotification" class="weather-notification" style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 20px;
            margin-bottom: 20px;
            border-radius: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            animation: slideDown 0.5s ease-out;
        ">
            <div>
                <strong>🌦️ Live Weather Data Loaded</strong><br/>
                <small>Temperature: ${weather.temperature}°C | Humidity: ${weather.humidity}% | Wind: ${weather.wind_speed} km/h</small>
            </div>
            <button onclick="document.getElementById('weatherNotification').style.display='none';" style="
                background: rgba(255,255,255,0.2);
                border: none;
                color: white;
                cursor: pointer;
                padding: 5px 10px;
                border-radius: 4px;
            ">✕</button>
        </div>
    `;
    
    // Insert after home section or at the beginning of yield section
    const yieldSection = document.getElementById('yield');
    if (yieldSection) {
        const formContainer = yieldSection.querySelector('.form-container');
        if (formContainer && !document.getElementById('weatherNotification')) {
            formContainer.insertAdjacentHTML('beforebegin', notificationHTML);
        }
    }
}

// Initialize weather data on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log('Page loaded - initializing automatic weather data...');
    autoPopulateWeather();
});

// Also fetch weather when user navigates to yield prediction section
document.addEventListener('click', function(e) {
    if (e.target.getAttribute('data-section') === 'yield') {
        // Re-fetch weather data
        autoPopulateWeather();
    }
});

// Initialize
console.log('AgriAI Application loaded successfully!');
