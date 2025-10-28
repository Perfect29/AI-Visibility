"""Visibility analysis service"""
from typing import List, Dict
from app.services.openai_service import OpenAIService


class VisibilityAnalyzer:
    def __init__(self, openai_service: OpenAIService):
        self.openai_service = openai_service
    
    async def simulate_visibility(self, prompts: List[str], brand_name: str) -> Dict:
        """Run visibility simulation for multiple prompts"""
        results = []
        total_score = 0
        
        for prompt in prompts:
            try:
                analysis = await self.openai_service.analyze_visibility(prompt, brand_name)
                results.append(analysis)
                total_score += analysis["overall_score"]
            except Exception as e:
                # Add error result
                results.append({
                    "prompt": prompt,
                    "relevance": 0,
                    "competition": 0,
                    "brand_strength": 0,
                    "overall_score": 0,
                    "explanation": f"Analysis failed: {str(e)}"
                })
        
        # Calculate average score
        avg_score = total_score / len(results) if results else 0
        
        # Generate recommendations
        recommendations = self._generate_recommendations(avg_score, brand_name)
        
        return {
            "brand_name": brand_name,
            "visibility_percentage": round(avg_score, 1),
            "overall_score": round(avg_score, 1),  # Keep for backwards compatibility
            "total_prompts": len(prompts),
            "results": results,
            "recommendations": recommendations
        }
    
    def _generate_recommendations(self, score: float, brand_name: str) -> List[str]:
        """Generate recommendations based on score"""
        recommendations = []
        
        if score < 30:
            recommendations.extend([
                f"Focus on building {brand_name}'s brand awareness in core areas",
                "Create more content around primary keywords",
                "Consider paid advertising to increase visibility",
                "Optimize website content for target keywords"
            ])
        elif score < 60:
            recommendations.extend([
                f"Strengthen {brand_name}'s content marketing strategy",
                "Build more backlinks and authority",
                "Expand into related keyword areas",
                "Improve user experience and engagement"
            ])
        else:
            recommendations.extend([
                f"Maintain {brand_name}'s strong visibility position",
                "Explore new market opportunities",
                "Focus on conversion optimization",
                "Consider international expansion"
            ])
        
        return recommendations[:4]  # Return top 4 recommendations
