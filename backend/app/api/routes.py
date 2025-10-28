"""API Routes"""
from fastapi import APIRouter, HTTPException
from typing import List
import asyncio

from app.models.schemas import (
    BrandInput,
    CustomPromptsRequest,
    SimulationRequest,
    KeywordResponse,
    PromptsResponse,
    PromptItem,
    VisibilityMetrics
)
from app.services.scraper import ScraperService
from app.services.openai_service import OpenAIService
from app.services.visibility_analyzer import VisibilityAnalyzer

router = APIRouter()

# Initialize services
scraper = ScraperService()
openai_service = OpenAIService()
analyzer = VisibilityAnalyzer()


@router.get("/")
async def root():
    """API health check"""
    return {
        "message": "AI Visibility Tool API",
        "version": "1.0.0",
        "status": "operational"
    }


@router.post("/keywords", response_model=KeywordResponse)
async def extract_keywords(request: BrandInput):
    """Extract keywords from domain"""
    try:
        # Scrape domain
        content = await scraper.scrape_domain(str(request.domain))
        
        # Extract keywords with AI (fallback to simple method if fails)
        try:
            keywords = openai_service.extract_keywords(content, request.brand_name, 5)
        except Exception as e:
            print(f"AI extraction failed: {e}, using fallback")
            keywords = scraper.extract_keywords_fallback(content, request.brand_name, 5)
        
        # If no keywords extracted, provide generic fallback based on brand name
        if not keywords:
            keywords = generate_fallback_keywords(request.brand_name)
        
        return KeywordResponse(
            brand_name=request.brand_name,
            domain=str(request.domain),
            keywords=keywords
        )
    except Exception as e:
        print(f"Scraping failed for {request.domain}: {e}")
        # Provide fallback keywords even if scraping fails
        keywords = generate_fallback_keywords(request.brand_name)
        return KeywordResponse(
            brand_name=request.brand_name,
            domain=str(request.domain),
            keywords=keywords
        )


@router.post("/prompts/custom", response_model=PromptsResponse)
async def generate_custom_prompts(request: CustomPromptsRequest):
    """Use custom user-provided prompts"""
    prompts = [
        PromptItem(
            keyword="custom",
            prompt=p,
            intent_type=_classify_intent(p, request.brand_name)
        )
        for p in request.custom_prompts
    ]
    
    return PromptsResponse(
        brand_name=request.brand_name,
        prompts=prompts,
        total_prompts=len(prompts)
    )


@router.post("/simulate", response_model=VisibilityMetrics)
async def simulate_visibility(request: SimulationRequest):
    """Simulate brand visibility across platforms with multiple runs"""
    try:
        # Run simulations concurrently with multiple runs per prompt
        tasks = []
        for prompt in request.prompts:
            for platform in request.platforms:
                tasks.append(
                    openai_service.simulate_query(prompt, request.brand_name, platform, runs=3)
                )
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions and log them
        valid_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"❌ Task {i} failed: {result}")
            else:
                print(f"✅ Task {i} completed: {result.get('platform', 'unknown')} - Score: {result.get('visibility_score', 0)}")
                print(f"   Brand mentioned: {result.get('brand_mentioned', False)}")
                print(f"   Position: {result.get('position', 'None')}")
                print(f"   Full result: {result}")
                valid_results.append(result)
        
        print(f"📈 Valid results: {len(valid_results)}/{len(results)}")
        print(f"📈 Results details: {[r.get('brand_mentioned', False) for r in valid_results]}")
        
        # Calculate metrics
        metrics = VisibilityAnalyzer.calculate_metrics(request.brand_name, valid_results)
        
        # Clean up metrics for user - hide backend details
        clean_metrics = {
            "brand_name": metrics["brand_name"],
            "visibility_percentage": metrics["visibility_percentage"],
            "total_prompts": metrics["total_prompts"],
            "mentions": metrics["mentions"],
            "average_position": metrics["average_position"],
            "recommendations": metrics["recommendations"]
        }
        
        return clean_metrics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze", response_model=VisibilityMetrics)
async def full_analysis(request: BrandInput):
    """Complete end-to-end analysis: Keywords → Prompts → Results"""
    try:
        # Step 1: Extract keywords
        content = await scraper.scrape_domain(str(request.domain))
        try:
            keywords = openai_service.extract_keywords(content, request.brand_name, 5)
        except:
            keywords = scraper.extract_keywords_fallback(content, request.brand_name, 5)
        
        # Step 2: Generate prompts (1 per keyword = 5 total maximum)
        all_prompts = []
        for keyword in keywords[:5]:  # Limit to 5 keywords maximum
            try:
                queries = openai_service.generate_prompts(request.brand_name, keyword, 1)
                all_prompts.extend(queries)
            except Exception as e:
                print(f"Error generating prompts for {keyword}: {e}")
                # Fallback prompts optimized for lists
                all_prompts.extend([
                    f"Top {keyword} tools",
                    f"Best {keyword} platforms"
                ])
        
        # Step 3: Simulate with multiple runs
        sim_request = SimulationRequest(
            brand_name=request.brand_name,
            prompts=all_prompts[:10],  # Limit to 10 for efficiency
            platforms=["chatgpt", "perplexity"]
        )
        
        return await simulate_visibility(sim_request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def generate_fallback_keywords(brand_name: str) -> List[str]:
    """Generate fallback keywords when scraping fails"""
    # Common business keywords based on brand name
    fallback_keywords = [
        "Business solutions",
        "Technology services", 
        "Digital platform",
        "Enterprise software",
        "Online services"
    ]
    
    # Try to infer from brand name
    brand_lower = brand_name.lower()
    if any(word in brand_lower for word in ["pay", "payment", "stripe"]):
        return ["Payments", "Billing", "Financial services", "E-commerce", "Online transactions"]
    elif any(word in brand_lower for word in ["tech", "software", "app"]):
        return ["Software", "Technology", "Applications", "Digital solutions", "Platform"]
    elif any(word in brand_lower for word in ["university", "education", "school"]):
        return ["Education", "Learning", "Academic services", "Student platform", "Online learning"]
    elif any(word in brand_lower for word in ["bank", "finance", "money"]):
        return ["Banking", "Financial services", "Money management", "Investment", "Fintech"]
    else:
        return fallback_keywords


def _classify_intent(query: str, brand_name: str) -> str:
    """Classify query intent"""
    query_lower = query.lower()
    brand_lower = brand_name.lower()
    
    if brand_lower in query_lower:
        if any(word in query_lower for word in ['vs', 'versus', 'compare']):
            return "comparison"
        elif any(word in query_lower for word in ['review', 'rating']):
            return "review"
        return "brand-specific"
    elif any(word in query_lower for word in ['best', 'top', 'leading']):
        return "category"
    return "informational"

