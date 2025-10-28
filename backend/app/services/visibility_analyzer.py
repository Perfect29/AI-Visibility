"""Visibility analysis and metrics calculation"""
from typing import List, Dict
from collections import Counter


class VisibilityAnalyzer:
    """Analyze visibility metrics from simulation results"""
    
    @staticmethod
    def calculate_metrics(brand_name: str, results: List[Dict]) -> Dict:
        """Calculate comprehensive visibility metrics with unified scoring"""
        print(f"🔍 Calculating metrics for {brand_name} with {len(results)} results")
        
        total_prompts = len(results)
        mentions = sum(1 for r in results if r.get("brand_mentioned", False))
        
        print(f"📊 Total prompts: {total_prompts}, Mentions: {mentions}")
        
        # Calculate overall visibility score (0-100)
        visibility_scores = [r.get("visibility_score", 0) for r in results]
        overall_score = sum(visibility_scores) / len(visibility_scores) if visibility_scores else 0
        
        print(f"🎯 Individual scores: {visibility_scores}")
        print(f"🎯 Overall score: {overall_score}")
        
        # Enhanced metrics for detailed view
        total_mention_count = sum(r.get("mention_count", 0) for r in results)
        total_citation_count = sum(r.get("citation_count", 0) for r in results)
        
        # Position analysis
        positions = [r.get("position") for r in results if r.get("position") is not None]
        average_position = sum(positions) / len(positions) if positions else None
        
        # Position distribution
        position_distribution = {
            "top_3": sum(1 for pos in positions if pos <= 3),
            "top_10": sum(1 for pos in positions if pos <= 10),
            "beyond_10": sum(1 for pos in positions if pos > 10)
        }
        
        # Sentiment analysis
        sentiments = [r.get("sentiment", "neutral") for r in results if r.get("brand_mentioned")]
        sentiment_counts = Counter(sentiments)
        
        # Calculate sentiment score (-1 to 1)
        sentiment_score = 0
        if sentiments:
            positive = sentiment_counts.get("positive", 0)
            negative = sentiment_counts.get("negative", 0)
            total_sentiment = len(sentiments)
            sentiment_score = (positive - negative) / total_sentiment if total_sentiment > 0 else 0
        
        # Platform breakdown
        platform_breakdown = {}
        for result in results:
            platform = result.get("platform", "unknown")
            if platform not in platform_breakdown:
                platform_breakdown[platform] = {
                    "total_queries": 0,
                    "mentions": 0,
                    "visibility_rate": 0.0,
                    "mention_count": 0,
                    "citation_count": 0,
                    "avg_position": None,
                    "avg_score": 0.0
                }
            
            platform_breakdown[platform]["total_queries"] += 1
            platform_breakdown[platform]["mention_count"] += result.get("mention_count", 0)
            platform_breakdown[platform]["citation_count"] += result.get("citation_count", 0)
            
            if result.get("brand_mentioned"):
                platform_breakdown[platform]["mentions"] += 1
        
        # Calculate platform metrics
        for platform in platform_breakdown:
            total = platform_breakdown[platform]["total_queries"]
            mentions_count = platform_breakdown[platform]["mentions"]
            platform_breakdown[platform]["visibility_rate"] = (
                (mentions_count / total * 100) if total > 0 else 0
            )
            
            # Calculate average position and score for this platform
            platform_positions = [r.get("position") for r in results 
                                 if r.get("platform") == platform and r.get("position")]
            platform_scores = [r.get("visibility_score", 0) for r in results 
                              if r.get("platform") == platform]
            
            if platform_positions:
                platform_breakdown[platform]["avg_position"] = sum(platform_positions) / len(platform_positions)
            
            if platform_scores:
                platform_breakdown[platform]["avg_score"] = sum(platform_scores) / len(platform_scores)
        
        # Generate recommendations based on unified score
        recommendations = VisibilityAnalyzer._generate_recommendations(
            overall_score, sentiment_score, platform_breakdown, total_mention_count, total_citation_count
        )
        
        return {
            "brand_name": brand_name,
            "visibility_percentage": round(overall_score, 2),  # Main unified score
            "total_prompts": total_prompts,
            "mentions": mentions,
            "total_mention_count": total_mention_count,
            "total_citation_count": total_citation_count,
            "sentiment_score": round(sentiment_score, 2),
            "sentiment_distribution": dict(sentiment_counts),
            "average_position": round(average_position, 2) if average_position else None,
            "position_distribution": position_distribution,
            "platform_breakdown": platform_breakdown,
            "recommendations": recommendations,
            "score_breakdown": {
                "individual_scores": visibility_scores,
                "min_score": min(visibility_scores) if visibility_scores else 0,
                "max_score": max(visibility_scores) if visibility_scores else 0,
                "score_variance": VisibilityAnalyzer._calculate_variance(visibility_scores)
            }
        }
    
    @staticmethod
    def _generate_recommendations(
        overall_score: float,
        sentiment_score: float,
        platform_breakdown: Dict,
        total_mentions: int,
        total_citations: int
    ) -> List[str]:
        """Generate actionable recommendations based on unified score"""
        recommendations = []
        
        # Overall score recommendations
        if overall_score >= 80:
            recommendations.append("🏆 EXCELLENT visibility! You're dominating AI search results.")
        elif overall_score >= 60:
            recommendations.append("✅ Good visibility! You're well-positioned in AI search.")
        elif overall_score >= 40:
            recommendations.append("⚠️ Moderate visibility. Focus on improving your AI presence.")
        elif overall_score >= 20:
            recommendations.append("🚨 Low visibility. Urgent action needed to improve AI search presence.")
        else:
            recommendations.append("💥 CRITICAL: Very low visibility. Immediate strategy overhaul required.")
        
        # Specific improvement areas
        if overall_score < 60:
            recommendations.append("📝 Create more brand-focused content and thought leadership.")
            recommendations.append("🔗 Build authoritative backlinks and citations.")
            recommendations.append("📊 Optimize for AI search platforms with structured data.")
        
        # Sentiment recommendations
        if sentiment_score < -0.2:
            recommendations.append("⚠️ Negative sentiment detected. Address customer concerns.")
        elif sentiment_score > 0.3:
            recommendations.append("✅ Positive sentiment! Leverage this in marketing.")
        
        # Platform-specific recommendations
        for platform, data in platform_breakdown.items():
            if data["avg_score"] < 40:
                recommendations.append(f"📊 Low performance on {platform} (Score: {data['avg_score']:.1f}). Optimize for this platform.")
            elif data["avg_score"] > 80:
                recommendations.append(f"🎯 Strong performance on {platform} (Score: {data['avg_score']:.1f})! Use as competitive advantage.")
        
        return recommendations
    
    @staticmethod
    def _calculate_variance(scores: List[float]) -> float:
        """Calculate variance of scores for consistency analysis"""
        if len(scores) < 2:
            return 0.0
        
        mean = sum(scores) / len(scores)
        variance = sum((score - mean) ** 2 for score in scores) / len(scores)
        return round(variance, 2)

