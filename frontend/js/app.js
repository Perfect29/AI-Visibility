// AI Visibility Tool - Production Frontend
const API_BASE_URL = 'https://ai-visibility-api.railway.app';

// State Management
let appState = {
    keywords: [],
    prompts: [],
    isLoading: false
};

// Initialize App
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 AI Visibility Tool Loaded');
    prefillExampleData();
});

function prefillExampleData() {
    const examples = [
        { name: 'Stripe', domain: 'https://stripe.com' },
        { name: 'Shopify', domain: 'https://shopify.com' },
        { name: 'Notion', domain: 'https://notion.so' }
    ];
    
    const randomExample = examples[Math.floor(Math.random() * examples.length)];
    document.getElementById('brandName').value = randomExample.name;
    document.getElementById('brandDomain').value = randomExample.domain;
}

// API Service
async function apiRequest(endpoint, data) {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    
    if (!response.ok) {
        throw new Error(`API Error: ${response.status}`);
    }
    
    return response.json();
}

// Main Functions
async function extractKeywords() {
    const brandName = document.getElementById('brandName').value.trim();
    const brandDomain = document.getElementById('brandDomain').value.trim();
    
    if (!brandName || !brandDomain) {
        showError('Please fill in all fields');
        return;
    }
    
    if (!isValidUrl(brandDomain)) {
        showError('Please enter a valid URL');
        return;
    }

    setLoading(true, 'keywords');
    
    try {
        const data = await apiRequest('/api/keywords', { brand_name: brandName, brand_domain: brandDomain });
        appState.keywords = data.keywords || [];
        displayKeywords(appState.keywords);
        document.getElementById('keywordsSection').style.display = 'block';
    } catch (error) {
        console.error('Error:', error);
        showError('Failed to extract keywords');
    } finally {
        setLoading(false, 'keywords');
    }
}

async function generatePrompts() {
    if (appState.keywords.length === 0) {
        showError('Please extract keywords first');
        return;
    }

    setLoading(true, 'prompts');
    
    try {
        const brandName = document.getElementById('brandName').value.trim();
        const data = await apiRequest('/api/prompts', { keywords: appState.keywords, brand_name: brandName });
        appState.prompts = data.prompts || [];
        displayPrompts(appState.prompts);
        document.getElementById('promptsSection').style.display = 'block';
    } catch (error) {
        console.error('Error:', error);
        showError('Failed to generate prompts');
    } finally {
        setLoading(false, 'prompts');
    }
}

async function runAnalysis() {
    if (appState.prompts.length === 0) {
        showError('Please generate prompts first');
        return;
    }
    
    setLoading(true, 'analyze');
    
    try {
        const brandName = document.getElementById('brandName').value.trim();
        const data = await apiRequest('/api/simulate', { prompts: appState.prompts, brand_name: brandName });
        displayResults(data);
        document.getElementById('resultsSection').style.display = 'block';
    } catch (error) {
        console.error('Error:', error);
        showError('Analysis failed');
    } finally {
        setLoading(false, 'analyze');
    }
}

// UI Functions
function displayKeywords(keywords) {
    const container = document.getElementById('keywordsContainer');
    container.innerHTML = keywords.map((keyword, index) => `
        <div class="keyword-item">
            <input type="text" value="${keyword}" maxlength="50" onchange="updateKeyword(${index}, this.value)">
            <button onclick="removeKeyword(${index})">×</button>
        </div>
    `).join('');
}

function displayPrompts(prompts) {
    const container = document.getElementById('promptsContainer');
    container.innerHTML = prompts.map((prompt, index) => `
        <div class="prompt-item">
            <textarea maxlength="200" onchange="updatePrompt(${index}, this.value)">${prompt}</textarea>
            <button onclick="removePrompt(${index})">×</button>
        </div>
    `).join('');
}

function displayResults(data) {
    const metricsGrid = document.getElementById('metricsGrid');
    const scoreColor = data.visibility_percentage >= 80 ? 'excellent' :
                      data.visibility_percentage >= 60 ? 'good' :
                      data.visibility_percentage >= 40 ? 'moderate' : 'low';

    metricsGrid.innerHTML = `
        <div class="metric-card main-score ${scoreColor}">
            <div class="metric-value">${data.visibility_percentage.toFixed(1)}%</div>
            <div class="metric-label">AI Visibility Score</div>
            <div class="score-description">${getAdvice(data.visibility_percentage)}</div>
        </div>
    `;

    const recommendationsDiv = document.getElementById('recommendations');
    recommendationsDiv.innerHTML = `
        <div class="recommendations-card">
            <h3>💡 Quick Recommendations</h3>
            <div class="recommendations-list">
                ${getRecommendations(data.visibility_percentage)}
            </div>
        </div>
    `;
    
    setTimeout(() => showPremiumModal(), 3000);
}

// Utility Functions
function setLoading(loading, type) {
    appState.isLoading = loading;
    
    const buttons = document.querySelectorAll('button');
    buttons.forEach(btn => btn.disabled = loading);
    
    const textEl = document.getElementById(`${type}BtnText`);
    const loaderEl = document.getElementById(`${type}BtnLoader`);
    
    if (textEl && loaderEl) {
        textEl.style.display = loading ? 'none' : 'inline';
        loaderEl.style.display = loading ? 'inline-block' : 'none';
    }
}

function updateKeyword(index, value) {
    appState.keywords[index] = value;
}

function removeKeyword(index) {
    appState.keywords.splice(index, 1);
    displayKeywords(appState.keywords);
}

function updatePrompt(index, value) {
    appState.prompts[index] = value;
}

function removePrompt(index) {
    appState.prompts.splice(index, 1);
    displayPrompts(appState.prompts);
}

function isValidUrl(string) {
    try {
        new URL(string);
        return true;
    } catch (_) {
        return false;
    }
}

function getAdvice(score) {
    if (score >= 80) return "Excellent visibility! Keep up the great work.";
    if (score >= 60) return "Good visibility. Consider optimizing further.";
    if (score >= 40) return "Moderate visibility. Room for improvement.";
    return "Low visibility. Focus on optimization.";
}

function getRecommendations(score) {
    const recommendations = [];
    
    if (score >= 80) {
        recommendations.push("🎯 Maintain your current AI optimization strategy", "📈 Monitor competitor changes regularly");
    } else if (score >= 60) {
        recommendations.push("🔍 Optimize your website content for AI training", "📝 Create more comprehensive product descriptions");
    } else if (score >= 40) {
        recommendations.push("📚 Add detailed FAQ sections to your website", "🏷️ Improve product categorization and tags");
    } else {
        recommendations.push("⚡ Completely revamp your website content", "📊 Add structured data markup");
    }
    
    return recommendations.map(rec => `<div class="recommendation-item">${rec}</div>`).join('');
}

// Modal Functions
function showPremiumModal() {
    document.getElementById('premiumModal').style.display = 'block';
}

function hidePremiumModal() {
    document.getElementById('premiumModal').style.display = 'none';
}

function submitContact() {
    const name = document.getElementById('contactName').value.trim();
    const email = document.getElementById('contactEmail').value.trim();
    
    if (!name || !email) {
        showError('Please fill in all fields');
        return;
    }
    
    console.log('Contact submitted:', { name, email });
    showSuccess('Thank you! We\'ll be in touch soon.');
    hidePremiumModal();
}

// Error/Success Handling
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.style.cssText = `
        position: fixed; top: 20px; right: 20px; z-index: 10000;
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white; padding: 16px 24px; border-radius: 12px;
        font-weight: 600; max-width: 400px;
        box-shadow: 0 10px 30px rgba(255, 107, 107, 0.4);
    `;
    errorDiv.textContent = message;
    document.body.appendChild(errorDiv);
    
    setTimeout(() => {
        if (errorDiv.parentNode) {
            errorDiv.parentNode.removeChild(errorDiv);
        }
    }, 5000);
}

function showSuccess(message) {
    const successDiv = document.createElement('div');
    successDiv.style.cssText = `
        position: fixed; top: 20px; right: 20px; z-index: 10000;
        background: linear-gradient(135deg, #51cf66 0%, #40c057 100%);
        color: white; padding: 16px 24px; border-radius: 12px;
        font-weight: 600; max-width: 400px;
        box-shadow: 0 10px 30px rgba(81, 207, 102, 0.4);
    `;
    successDiv.textContent = message;
    document.body.appendChild(successDiv);
    
    setTimeout(() => {
        if (successDiv.parentNode) {
            successDiv.parentNode.removeChild(successDiv);
        }
    }, 3000);
}
