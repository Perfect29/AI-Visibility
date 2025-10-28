// AI Visibility Tool Frontend - Enhanced UX Version
let extractedKeywords = [];
let generatedPrompts = [];
let isLoading = false;

// Enhanced state management
const AppState = {
    currentStep: 'input',
    isLoading: false,
    error: null,
    data: null
};

// Initialize with enhanced UX
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 App loaded successfully');
    initializeApp();
    setupEventListeners();
    prefillExampleData();
});

function initializeApp() {
    // Add loading states to buttons
    addLoadingStates();
    
    // Setup keyboard navigation
    setupKeyboardNavigation();
    
    // Add form validation
    setupFormValidation();
    
    // Initialize accessibility
    setupAccessibility();
}

function addLoadingStates() {
    const buttons = document.querySelectorAll('button');
    buttons.forEach(button => {
        button.classList.add('interactive-element');
    });
}

function setupKeyboardNavigation() {
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && e.target.tagName === 'INPUT') {
            const nextStep = getNextStep();
            if (nextStep) {
                nextStep();
            }
        }
    });
}

function setupFormValidation() {
    const inputs = document.querySelectorAll('input[required], textarea[required]');
    inputs.forEach(input => {
        input.addEventListener('blur', validateField);
        input.addEventListener('input', clearFieldError);
    });
}

function setupAccessibility() {
    // Add ARIA labels
    const buttons = document.querySelectorAll('button');
    buttons.forEach(button => {
        if (!button.getAttribute('aria-label')) {
            button.setAttribute('aria-label', button.textContent.trim());
        }
    });
}

function prefillExampleData() {
    // Pre-fill with better examples
    const examples = [
        { name: 'Stripe', domain: 'https://stripe.com' },
        { name: 'Shopify', domain: 'https://shopify.com' },
        { name: 'Notion', domain: 'https://notion.so' }
    ];
    
    const randomExample = examples[Math.floor(Math.random() * examples.length)];
    document.getElementById('brandName').value = randomExample.name;
    document.getElementById('brandDomain').value = randomExample.domain;
}

async function extractKeywords() {
    console.log('🔍 Extract Keywords button clicked!');
    
    const brandName = document.getElementById('brandName').value.trim();
    const brandDomain = document.getElementById('brandDomain').value.trim();
    
    console.log('📝 Brand:', brandName, 'Domain:', brandDomain);

    if (!brandName || !brandDomain) {
        showError('Please fill in both brand name and domain');
        return;
    }
    
    // Validate domain format
    if (!isValidUrl(brandDomain)) {
        showError('Please enter a valid URL (e.g., https://example.com)');
        return;
    }

    console.log('⏳ Starting keyword extraction...');
    setLoadingState(true, 'keywords');
    
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
        setLoadingState(false, 'keywords');
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
            <input type="text" value="${keyword}" class="keyword-input" data-index="${index}" onchange="updateKeyword(${index}, this.value)" maxlength="50" title="Максимум 50 символов">
            <button class="btn-remove" onclick="removeKeyword(${index})">×</button>
        </div>
    `).join('');
}

function updateKeyword(index, newValue) {
    console.log('🔄 Updating keyword:', index, newValue);
    extractedKeywords[index] = newValue;
    updateCharacterCounter(event.target);
}

function removeKeyword(index) {
    console.log('🗑️ Removing keyword:', index);
    extractedKeywords.splice(index, 1);
    displayKeywords(extractedKeywords);
}

async function generatePrompts() {
    console.log('🎯 Generate Prompts button clicked!');
    
    if (extractedKeywords.length === 0) {
        showError('Please extract keywords first');
        return;
    }

    setLoadingState(true, 'prompts');
    
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
        setLoadingState(false, 'prompts');
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
            <textarea class="prompt-input" data-index="${index}" onchange="updatePrompt(${index}, this.value)" maxlength="200" title="Максимум 200 символов">${prompt}</textarea>
            <button class="btn-remove" onclick="removePrompt(${index})">×</button>
        </div>
    `).join('');
}

function updatePrompt(index, newValue) {
    console.log('🔄 Updating prompt:', index, newValue);
    generatedPrompts[index] = newValue;
    updateCharacterCounter(event.target);
}

function updateCharacterCounter(input) {
    if (input) {
        const currentLength = input.value.length;
        const maxLength = input.getAttribute('maxlength');
        input.setAttribute('data-count', currentLength);
        
        // Add visual feedback
        if (currentLength > maxLength * 0.9) {
            input.style.borderColor = '#ff6b6b';
        } else {
            input.style.borderColor = '#51cf66';
        }
    }
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
        showError('Please generate prompts first');
        return;
    }
    
    // Update the global prompts array with current edits
    generatedPrompts = currentPrompts;
    
    setLoadingState(true, 'analyze');
    
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
        setLoadingState(false, 'analyze');
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
    `;

    // Add Simple Recommendations
    const recommendationsDiv = document.getElementById('recommendations');
    if (recommendationsDiv) {
        recommendationsDiv.innerHTML = `
            <div class="recommendations-card">
                <h3>💡 Quick Recommendations</h3>
                <div class="recommendations-list">
                    ${getRecommendations(data.visibility_percentage)}
                </div>
            </div>
        `;
    }

    // Hide recommendations section
    const recommendationsSection = document.getElementById('recommendationsSection');
    if (recommendationsSection) {
        recommendationsSection.style.display = 'none';
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

function getRecommendations(score) {
    const recommendations = [];
    
    if (score >= 80) {
        recommendations.push(
            "🎯 Maintain your current AI optimization strategy",
            "📈 Monitor competitor changes regularly",
            "🚀 Consider expanding to new AI platforms"
        );
    } else if (score >= 60) {
        recommendations.push(
            "🔍 Optimize your website content for AI training",
            "📝 Create more comprehensive product descriptions",
            "🤖 Test your brand mentions in ChatGPT and Claude"
        );
    } else if (score >= 40) {
        recommendations.push(
            "📚 Add detailed FAQ sections to your website",
            "🏷️ Improve product categorization and tags",
            "💬 Include customer testimonials and reviews",
            "🔗 Build more backlinks from reputable sources"
        );
    } else if (score >= 20) {
        recommendations.push(
            "⚡ Completely revamp your website content",
            "📊 Add structured data markup (Schema.org)",
            "🎨 Improve your brand's online presence",
            "📱 Ensure mobile-first content strategy",
            "🔍 Focus on long-tail keyword optimization"
        );
    } else {
        recommendations.push(
            "🚨 Urgent: Redesign your entire digital presence",
            "📝 Create comprehensive, AI-friendly content",
            "🏢 Establish strong brand authority online",
            "📊 Implement advanced SEO strategies",
            "🤝 Consider hiring AI optimization experts"
        );
    }
    
    return recommendations.map(rec => `
        <div class="recommendation-item">
            <div class="recommendation-content">
                ${rec}
            </div>
        </div>
    `).join('');
}

function showPremiumModal() {
    console.log('✨ Showing premium modal');
    document.getElementById('premiumModal').style.display = 'block';
}

function hidePremiumModal() {
    console.log('❌ Hiding premium modal');
    document.getElementById('premiumModal').style.display = 'none';
}

// Close modal when clicking outside
document.addEventListener('click', function(event) {
    const modal = document.getElementById('premiumModal');
    const modalContent = document.querySelector('.simple-modal-content');
    
    if (event.target === modal) {
        hidePremiumModal();
    }
});

function submitSimpleContact() {
    console.log('📧 Submitting contact form');
    const name = document.getElementById('simpleName').value.trim();
    const email = document.getElementById('simpleEmail').value.trim();
    
    if (!name || !email) {
        showError('Please fill in both name and email');
        return;
    }
    
    if (!isValidEmail(email)) {
        showError('Please enter a valid email address');
        return;
    }
    
    const submitBtn = document.getElementById('simpleSubmitBtn');
    submitBtn.textContent = 'Submitting...';
    submitBtn.disabled = true;
    
    // Simulate submission
    setTimeout(() => {
        // Create success notification
        const successDiv = document.createElement('div');
        successDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
            padding: 16px 24px;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(16, 185, 129, 0.4);
            z-index: 10000;
            font-weight: 600;
            max-width: 400px;
            animation: slideInRight 0.3s ease-out;
        `;
        successDiv.textContent = 'Thank you! We\'ll be in touch soon with early access details.';
        
        document.body.appendChild(successDiv);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            successDiv.style.animation = 'slideOutRight 0.3s ease-in';
            setTimeout(() => {
                if (successDiv.parentNode) {
                    successDiv.parentNode.removeChild(successDiv);
                }
            }, 300);
        }, 5000);
        
        hidePremiumModal();
        submitBtn.textContent = 'Get Early Access + 50% Off';
        submitBtn.disabled = false;
    }, 1500);
}

function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function isValidUrl(string) {
    try {
        new URL(string);
        return true;
    } catch (_) {
        return false;
    }
}

// Enhanced helper functions
function getNextStep() {
    const currentStep = AppState.currentStep;
    switch (currentStep) {
        case 'input': return extractKeywords;
        case 'keywords': return generatePrompts;
        case 'prompts': return runAnalysis;
        default: return null;
    }
}

function validateField(event) {
    const field = event.target;
    const value = field.value.trim();
    
    // Remove existing error styling
    field.classList.remove('error');
    
    if (field.hasAttribute('required') && !value) {
        showFieldError(field, 'This field is required');
        return false;
    }
    
    if (field.type === 'url' && value && !isValidUrl(value)) {
        showFieldError(field, 'Please enter a valid URL');
        return false;
    }
    
    if (field.type === 'email' && value && !isValidEmail(value)) {
        showFieldError(field, 'Please enter a valid email address');
        return false;
    }
    
    return true;
}

function showFieldError(field, message) {
    field.classList.add('error');
    
    // Remove existing error message
    const existingError = field.parentNode.querySelector('.field-error');
    if (existingError) {
        existingError.remove();
    }
    
    // Add new error message
    const errorDiv = document.createElement('div');
    errorDiv.className = 'field-error';
    errorDiv.textContent = message;
    errorDiv.style.cssText = `
        color: #ef4444;
        font-size: 0.875rem;
        margin-top: 0.25rem;
        font-weight: 500;
    `;
    
    field.parentNode.appendChild(errorDiv);
}

function clearFieldError(event) {
    const field = event.target;
    field.classList.remove('error');
    
    const errorDiv = field.parentNode.querySelector('.field-error');
    if (errorDiv) {
        errorDiv.remove();
    }
}

function setupEventListeners() {
    // Add event listeners for better UX
    document.addEventListener('click', function(e) {
        if (e.target.matches('.btn-primary, .btn-secondary')) {
            e.target.classList.add('success-animation');
            setTimeout(() => {
                e.target.classList.remove('success-animation');
            }, 600);
        }
    });
}

// Enhanced loading state management
function setLoadingState(loading, type) {
    AppState.isLoading = loading;
    isLoading = loading;
    
    // Update UI based on loading state
    const buttons = document.querySelectorAll('button');
    buttons.forEach(button => {
        button.disabled = loading;
    });
    
    // Show/hide loading indicators
    showLoading(loading, type);
    
    // Update step tracking
    if (loading) {
        AppState.currentStep = type;
    }
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
    
    // Create a beautiful error notification instead of alert
    const errorDiv = document.createElement('div');
    errorDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
        padding: 16px 24px;
        border-radius: 12px;
        box-shadow: 0 10px 30px rgba(255, 107, 107, 0.4);
        z-index: 10000;
        font-weight: 600;
        max-width: 400px;
        animation: slideInRight 0.3s ease-out;
    `;
    errorDiv.textContent = message;
    
    document.body.appendChild(errorDiv);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        errorDiv.style.animation = 'slideOutRight 0.3s ease-in';
        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.parentNode.removeChild(errorDiv);
            }
        }, 300);
    }, 5000);
}

// Add CSS animations for error notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
