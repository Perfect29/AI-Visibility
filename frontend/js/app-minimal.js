// AI Visibility Tool Frontend - Minimal Working Version
let extractedKeywords = [];
let generatedPrompts = [];

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 App loaded successfully');
    // Pre-fill example data
    document.getElementById('brandName').value = 'Stripe';
    document.getElementById('brandDomain').value = 'https://stripe.com';
});

async function extractKeywords() {
    console.log('🔍 Extract Keywords button clicked!');
    
    const brandName = document.getElementById('brandName').value.trim();
    const brandDomain = document.getElementById('brandDomain').value.trim();
    
    console.log('📝 Brand:', brandName, 'Domain:', brandDomain);

    if (!brandName || !brandDomain) {
        alert('Please fill in both brand name and domain');
        return;
    }

    console.log('⏳ Starting keyword extraction...');
    showLoading(true, 'keywords');
    
    try {
        console.log('🌐 Making API call...');
        const response = await fetch('/api/keywords', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ brand_name: brandName, domain: brandDomain })
        });
        
        console.log('📡 Response status:', response.status);
        
        if (!response.ok) {
            throw new Error('Failed to extract keywords');
        }
        
        const data = await response.json();
        console.log('✅ Keywords received:', data.keywords);
        
        extractedKeywords = data.keywords || [];
        
        // Display keywords
        displayKeywords(extractedKeywords);
        document.getElementById('keywordsSection').style.display = 'block';
        
        console.log('🎉 Keywords displayed successfully!');
        
    } catch (error) {
        console.error('❌ Keywords extraction error:', error);
        showError('Failed to extract keywords. Please try again.');
    } finally {
        showLoading(false, 'keywords');
    }
}

function displayKeywords(keywords) {
    console.log('📋 Displaying keywords:', keywords);
    const keywordsContainer = document.getElementById('keywordsContainer');
    if (!keywordsContainer) {
        console.error('❌ keywordsContainer not found!');
        return;
    }
    
    keywordsContainer.innerHTML = keywords.map((keyword, index) => `
        <div class="keyword-item">
            <input type="text" value="${keyword}" class="keyword-input" data-index="${index}" onchange="updateKeyword(${index}, this.value)">
            <button class="remove-keyword" onclick="removeKeyword(${index})">×</button>
        </div>
    `).join('');
}

function updateKeyword(index, newValue) {
    console.log('🔄 Updating keyword:', index, newValue);
    extractedKeywords[index] = newValue;
}

function removeKeyword(index) {
    console.log('🗑️ Removing keyword:', index);
    extractedKeywords.splice(index, 1);
    displayKeywords(extractedKeywords);
}

async function generatePrompts() {
    console.log('🎯 Generate Prompts button clicked!');
    
    if (extractedKeywords.length === 0) {
        alert('Please extract keywords first');
        return;
    }

    showLoading(true, 'prompts');
    
    try {
        // Generate varied prompts for each keyword
        generatedPrompts = [];
        for (const keyword of extractedKeywords) {
            const prompt = generateVariedPrompts(keyword, document.getElementById('brandName').value);
            generatedPrompts.push(prompt);
        }
        
        displayPrompts(generatedPrompts);
        document.getElementById('promptsSection').style.display = 'block';
        
    } catch (error) {
        console.error('Prompts generation error:', error);
        showError('Failed to generate prompts. Please try again.');
    } finally {
        showLoading(false, 'prompts');
    }
}

function generateVariedPrompts(keyword, brandName) {
    // Detect brand type from name
    const brandLower = brandName.toLowerCase();
    let brandType = "companies";
    let year = "2025";
    
    if (brandLower.includes("university") || brandLower.includes("college") || brandLower.includes("school")) {
        brandType = "universities and institutions";
    } else if (brandLower.includes("bank") || brandLower.includes("finance")) {
        brandType = "financial institutions";
    } else if (brandLower.includes("hospital") || brandLower.includes("medical") || brandLower.includes("health")) {
        brandType = "healthcare providers";
    } else if (brandLower.includes("restaurant") || brandLower.includes("food") || brandLower.includes("cafe")) {
        brandType = "restaurants and food services";
    } else if (brandLower.includes("hotel") || brandLower.includes("resort")) {
        brandType = "hospitality providers";
    }
    
    const promptTemplates = [
        `What are the top ${keyword} ${brandType} in ${year}?`,
        `Best ${keyword} ${brandType} for enterprise businesses`,
        `Leading ${keyword} ${brandType} with advanced features`,
        `Most popular ${keyword} ${brandType} for small businesses`,
        `Top-rated ${keyword} ${brandType} with best customer reviews`
    ];
    
    // Return a random template for variety
    return promptTemplates[Math.floor(Math.random() * promptTemplates.length)];
}

function displayPrompts(prompts) {
    console.log('📋 Displaying prompts:', prompts);
    const promptsContainer = document.getElementById('promptsContainer');
    if (!promptsContainer) {
        console.error('❌ promptsContainer not found!');
        return;
    }
    
    promptsContainer.innerHTML = prompts.map((prompt, index) => `
        <div class="prompt-item">
            <textarea class="prompt-input" data-index="${index}" onchange="updatePrompt(${index}, this.value)">${prompt}</textarea>
        </div>
    `).join('');
}

function updatePrompt(index, newValue) {
    console.log('🔄 Updating prompt:', index, newValue);
    generatedPrompts[index] = newValue;
}

async function runAnalysis() {
    console.log('🚀 Run Analysis button clicked!');
    
    const brandName = document.getElementById('brandName').value.trim();
    
    // Get current edited prompts from the UI
    const currentPrompts = [];
    const promptInputs = document.querySelectorAll('.prompt-input');
    promptInputs.forEach(input => {
        if (input.value.trim()) {
            currentPrompts.push(input.value.trim());
        }
    });
    
    if (currentPrompts.length === 0) {
        alert('Please generate prompts first');
        return;
    }
    
    // Update the global prompts array with current edits
    generatedPrompts = currentPrompts;
    
    showLoading(true, 'analyze');
    
    try {
        console.log('🌐 Making analysis API call...');
        const response = await fetch('/api/simulate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                brand_name: brandName,
                prompts: currentPrompts,
                platforms: ['chatgpt']
            })
        });
        
        console.log('📡 Analysis response status:', response.status);
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error('API Error:', errorText);
            throw new Error(`Analysis failed: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('✅ Analysis data received:', data);
        
        // Only show error if we don't have valid data
        if (!data || typeof data.visibility_percentage === 'undefined') {
            throw new Error('Invalid response data');
        }
        
        displayResults(data);
        document.getElementById('resultsSection').style.display = 'block';
        
        console.log('🎉 Analysis completed successfully!');
        
    } catch (error) {
        console.error('Analysis error:', error);
        // Only show error dialog if we don't have results
        if (!document.getElementById('resultsSection').style.display || 
            document.getElementById('resultsSection').style.display === 'none') {
            showError('Analysis failed. Please check the console for details.');
        }
    } finally {
        showLoading(false, 'analyze');
    }
}

function displayResults(data) {
    console.log('📊 Displaying results:', data);
    const resultsSection = document.getElementById('resultsSection');
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth' });

    // Main Unified Score (Prominent Display)
    const metricsGrid = document.getElementById('metricsGrid');
    const scoreColor = data.visibility_percentage >= 80 ? 'excellent' :
                      data.visibility_percentage >= 60 ? 'good' :
                      data.visibility_percentage >= 40 ? 'moderate' :
                      data.visibility_percentage >= 20 ? 'low' : 'critical';

    metricsGrid.innerHTML = `
        <div class="metric-card main-score ${scoreColor}">
            <div class="metric-value">${data.visibility_percentage.toFixed(1)}%</div>
            <div class="metric-label">AI Visibility Score</div>
            <div class="score-description">${getSimpleAdvice(data.visibility_percentage)}</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">${data.total_prompts}</div>
            <div class="metric-label">Total Prompts</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">${data.mentions}</div>
            <div class="metric-label">Successful Mentions</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">${data.average_position ? data.average_position.toFixed(1) : 'N/A'}</div>
            <div class="metric-label">Avg Position</div>
        </div>
    `;

    // Recommendations
    const recommendationsSection = document.getElementById('recommendationsSection');
    if (data.recommendations && data.recommendations.length > 0) {
        recommendationsSection.innerHTML = `
            <h3>💡 Recommendations</h3>
            <ul class="recommendations-list">
                ${data.recommendations.map(rec => `<li>${rec}</li>`).join('')}
            </ul>
        `;
        recommendationsSection.style.display = 'block';
    }
    
    // Show premium modal automatically after results (perfect timing)
    setTimeout(() => {
        showPremiumModal();
    }, 3000); // Show after 3 seconds to let user absorb results
}

function getSimpleAdvice(score) {
    if (score >= 80) return "Excellent visibility! Keep up the great work.";
    if (score >= 60) return "Good visibility. Consider optimizing further.";
    if (score >= 40) return "Moderate visibility. Room for improvement.";
    if (score >= 20) return "Low visibility. Focus on optimization.";
    return "Critical visibility. Immediate action needed.";
}

function showPremiumModal() {
    console.log('✨ Showing premium modal');
    document.getElementById('premiumModal').style.display = 'block';
}

function hidePremiumModal() {
    console.log('❌ Hiding premium modal');
    document.getElementById('premiumModal').style.display = 'none';
}

function submitSimpleContact() {
    console.log('📧 Submitting contact form');
    const name = document.getElementById('simpleName').value.trim();
    const email = document.getElementById('simpleEmail').value.trim();
    
    if (!name || !email) {
        alert('Please fill in both name and email');
        return;
    }
    
    if (!isValidEmail(email)) {
        alert('Please enter a valid email address');
        return;
    }
    
    const submitBtn = document.getElementById('simpleSubmitBtn');
    submitBtn.textContent = 'Submitting...';
    submitBtn.disabled = true;
    
    // Simulate submission
    setTimeout(() => {
        alert('Thank you! We\'ll be in touch soon with early access details.');
        hidePremiumModal();
        submitBtn.textContent = 'Get Early Access + 50% Off';
        submitBtn.disabled = false;
    }, 1500);
}

function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function showLoading(show, type) {
    console.log('⏳ Show loading:', show, type);
    if (type === 'keywords') {
        const keywordsBtnText = document.getElementById('keywordsBtnText');
        const keywordsBtnLoader = document.getElementById('keywordsBtnLoader');
        if (keywordsBtnText && keywordsBtnLoader) {
            keywordsBtnText.style.display = show ? 'none' : 'inline';
            keywordsBtnLoader.style.display = show ? 'inline' : 'none';
        }
    } else if (type === 'prompts') {
        const promptsBtnText = document.getElementById('promptsBtnText');
        const promptsBtnLoader = document.getElementById('promptsBtnLoader');
        if (promptsBtnText && promptsBtnLoader) {
            promptsBtnText.style.display = show ? 'none' : 'inline';
            promptsBtnLoader.style.display = show ? 'inline' : 'none';
        }
    } else if (type === 'analyze') {
        const btnText = document.getElementById('btnText');
        const btnLoader = document.getElementById('btnLoader');
        if (btnText && btnLoader) {
            btnText.style.display = show ? 'none' : 'inline';
            btnLoader.style.display = show ? 'inline' : 'none';
        }
    }
}

function showError(message) {
    console.error('❌ Error:', message);
    alert(message);
}

