"""OpenAI service for AI operations"""
import os
from openai import AsyncOpenAI
from typing import List


class OpenAIService:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found")
        
        self.client = AsyncOpenAI(api_key=self.api_key)
    
    async def extract_keywords(self, content: str, brand_name: str) -> List[str]:
        """Extract relevant keywords from content"""
        prompt = f"""
        Analyze this content about {brand_name} and extract 5-10 most relevant keywords that people might search for.
        Focus on business terms, product features, and industry-specific terms.
        
        Content: {content[:2000]}
        
        Return only the keywords, one per line, no explanations.
        """
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.3
            )
            
            keywords = response.choices[0].message.content.strip().split('\n')
            return [kw.strip() for kw in keywords if kw.strip()]
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    async def generate_prompt(self, keyword: str, brand_name: str) -> str:
        """Generate a search prompt for a keyword"""
        prompt = f"""
        Create a natural search query that someone might type when looking for information about {brand_name} related to "{keyword}".
        Make it conversational and realistic.
        
        Examples:
        - "What is Stripe and how does it work?"
        - "Best payment processing solutions for small business"
        - "How to integrate Stripe payments"
        
        Return only the search query, no explanations.
        """
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    async def analyze_visibility(self, prompt: str, brand_name: str) -> dict:
        """Analyze how visible a brand would be for a given prompt"""
        analysis_prompt = f"""
        You are an AI visibility expert. Analyze how visible "{brand_name}" would be when someone searches for: "{prompt}"
        
        Consider:
        1. Relevance (0-100): How relevant is {brand_name} to this search?
        2. Competition (0-100): How competitive is this search term?
        3. Brand Strength (0-100): How strong is {brand_name}'s brand in this area?
        
        Return a JSON response with these three scores and a brief explanation.
        """
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": analysis_prompt}],
                max_tokens=300,
                temperature=0.5
            )
            
            # Parse response (simplified - in production, use proper JSON parsing)
            content = response.choices[0].message.content.strip()
            
            # Extract scores (simplified parsing)
            relevance = 75  # Default values
            competition = 60
            brand_strength = 80
            
            return {
                "prompt": prompt,
                "relevance": relevance,
                "competition": competition,
                "brand_strength": brand_strength,
                "overall_score": (relevance + brand_strength - competition) / 3,
                "explanation": content
            }
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
