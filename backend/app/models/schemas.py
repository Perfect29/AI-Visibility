"""Pydantic models for request/response validation"""
from pydantic import BaseModel, HttpUrl
from typing import List, Dict, Optional, Any


# Request Models
class BrandInput(BaseModel):
    """Brand information input"""
    brand_name: str
    domain: HttpUrl


class CustomPromptsRequest(BaseModel):
    """Request with custom user prompts"""
    brand_name: str
    custom_prompts: List[str]


class SimulationRequest(BaseModel):
    """Simulation request"""
    brand_name: str
    prompts: List[str]
    platforms: List[str] = ["chatgpt", "perplexity"]


# Response Models
class KeywordResponse(BaseModel):
    """Keywords extracted from domain"""
    brand_name: str
    domain: str
    keywords: List[str]


class PromptItem(BaseModel):
    """Individual prompt with metadata"""
    keyword: str
    prompt: str
    intent_type: str


class PromptsResponse(BaseModel):
    """Generated prompts response"""
    brand_name: str
    prompts: List[PromptItem]
    total_prompts: int


class PlatformStats(BaseModel):
    """Statistics for a single platform"""
    total_queries: int
    mentions: int
    visibility_rate: float
    mention_count: int
    citation_count: int
    avg_position: Optional[float]


class VisibilityMetrics(BaseModel):
    """Simplified visibility analysis for user display"""
    brand_name: str
    visibility_percentage: float
    total_prompts: int
    mentions: int
    average_position: Optional[float]
    recommendations: List[str]

