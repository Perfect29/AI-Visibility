"""Data models"""
from pydantic import BaseModel, Field
from typing import List, Optional


class KeywordResponse(BaseModel):
    keywords: List[str] = Field(..., description="Extracted keywords")


class PromptResponse(BaseModel):
    prompts: List[str] = Field(..., description="Generated prompts")


class VisibilityResult(BaseModel):
    prompt: str
    relevance: int = Field(..., ge=0, le=100)
    competition: int = Field(..., ge=0, le=100)
    brand_strength: int = Field(..., ge=0, le=100)
    overall_score: float = Field(..., ge=0, le=100)
    explanation: str


class SimulationResponse(BaseModel):
    brand_name: str
    overall_score: float = Field(..., ge=0, le=100)
    total_prompts: int
    results: List[VisibilityResult]
    recommendations: List[str]
