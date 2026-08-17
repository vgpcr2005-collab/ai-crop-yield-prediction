// JavaScript for AgriAI Application

const API_BASE_URL = 'http://localhost:5000/api';

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

// Initialize
console.log('AgriAI Application loaded successfully!');
