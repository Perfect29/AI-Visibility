"""API routes"""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field, HttpUrl
from typing import List

from app.services.scraper import ScraperService
from app.services.openai_service import OpenAIService
from app.services.visibility_analyzer import VisibilityAnalyzer

router = APIRouter()

# Request models
class BrandInfo(BaseModel):
    brand_name: str = Field(..., min_length=1, max_length=100, example="Stripe")
    brand_domain: HttpUrl = Field(..., example="https://stripe.com")

class KeywordsRequest(BaseModel):
    keywords: List[str] = Field(..., min_items=1, example=["online payments", "fintech"])
    brand_name: str = Field(..., min_length=1, max_length=100, example="Stripe")

class SimulateRequest(BaseModel):
    prompts: List[str] = Field(..., min_items=1, example=["What is Stripe?", "How does Stripe handle payments?"])
    brand_name: str = Field(..., min_length=1, max_length=100, example="Stripe")

@router.post("/keywords")
async def extract_keywords_endpoint(brand_info: BrandInfo):
    try:
        scraper = ScraperService()
        content = await scraper.scrape_website(str(brand_info.brand_domain))
        
        openai_service = OpenAIService()
        keywords = await openai_service.extract_keywords(content, brand_info.brand_name)
        
        return {"keywords": keywords}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/prompts")
async def generate_prompts_endpoint(request: KeywordsRequest):
    try:
        openai_service = OpenAIService()
        generated_prompts = []
        for keyword in request.keywords:
            prompt = await openai_service.generate_prompt(keyword, request.brand_name)
            generated_prompts.append(prompt)
        return {"prompts": generated_prompts}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/simulate")
async def simulate_visibility_endpoint(request: SimulateRequest):
    try:
        openai_service = OpenAIService()
        analyzer = VisibilityAnalyzer(openai_service)
        
        results = await analyzer.simulate_visibility(request.prompts, request.brand_name)
        
        return results
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
