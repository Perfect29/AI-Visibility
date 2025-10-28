"""OpenAI API service"""
from openai import OpenAI
from typing import List, Dict, Optional
import json
import re
from app.core.config import get_settings


class OpenAIService:
    """Handle all OpenAI API interactions"""
    
    def __init__(self):
        settings = get_settings()
        # Initialize OpenAI client with explicit configuration to avoid proxy issues
        try:
            self.client = OpenAI(
                api_key=settings.openai_api_key,
                timeout=30.0,
                max_retries=3
            )
        except Exception as e:
            print(f"OpenAI client initialization error: {e}")
            # Fallback initialization
            self.client = OpenAI(api_key=settings.openai_api_key)
        
        self.model = settings.openai_model
        self.max_tokens = settings.openai_max_tokens
        self.temperature = settings.openai_temperature

    def extract_keywords(self, text: str, brand_name: str, count: int = 5) -> List[str]:
        """Extract keywords from scraped content"""
        prompt = f"""Extract {count} core keywords from this text about {brand_name}.

Focus on:
- Main products/services
- Key features
- Industry terms
- Brand attributes

Text: {text[:2000]}

Return ONLY JSON array: ["keyword1", "keyword2", "keyword3"]"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=200
        )
        
        content = self._extract_json(response.choices[0].message.content.strip())
        return json.loads(content)[:count]
    
    def generate_prompts(self, brand_name: str, keyword: str, count: int = 5) -> List[str]:
        """Generate specific, longer prompts optimized to return brand lists"""
        prompt = f"""Generate {count} detailed search queries about "{keyword}" that would return comprehensive lists of brand names.

CRITICAL: DO NOT mention "{brand_name}". Focus on queries that return detailed brand lists.

Make queries more specific and longer, such as:
- "What are the top {keyword} companies and platforms in 2024?"
- "Best {keyword} brands for enterprise businesses"
- "Leading {keyword} providers with advanced features"
- "Most popular {keyword} platforms for small businesses"
- "Top-rated {keyword} companies with best customer reviews"

Return ONLY JSON array: ["query1", "query2", "query3"]"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=200
        )
        
        content = self._extract_json(response.choices[0].message.content.strip())
        return json.loads(content)
    
    async def simulate_query(self, query: str, brand_name: str, platform: str = "chatgpt", runs: int = 3) -> Dict:
        """Simulate a query optimized to get brand lists with consistent format"""
        # STRICT system prompt for consistent format
        system_prompt = f"""You are a helpful assistant that provides ONLY numbered lists of brand names.

CRITICAL RULES:
1. Return ONLY a numbered list (1. BrandName, 2. BrandName, etc.)
2. NO introductory text, NO explanations, NO conclusions
3. NO bold formatting, NO markdown, NO extra characters
4. Each line must start with a number followed by a period and space
5. Brand names only - no descriptions or additional text

Example format:
1. BrandOne
2. BrandTwo
3. BrandThree"""
        
        if platform == "perplexity":
            system_prompt += "\n6. Include sources and citations when possible."
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"List the top brands for: {query}"}
        ]
        
        # Run multiple times for accuracy
        all_results = []
        for run_num in range(runs):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.3,  # Lower temperature for consistency
                    max_tokens=self.max_tokens
                )
                
                answer = response.choices[0].message.content
                all_results.append(answer)
            except Exception as e:
                print(f"Run {run_num + 1} failed: {e}")
                continue
        
        if not all_results:
            return {
                "platform": platform.title(),
                "prompt": query,
                "error": "All runs failed",
                "brand_mentioned": False,
                "mention_count": 0,
                "position": None,
                "sentiment": "neutral",
                "citation_count": 0,
                "runs_completed": 0,
                "visibility_score": 0
            }
        
        # Analyze combined results with improved parsing
        combined_text = " ".join(all_results)
        
        # Enhanced brand detection
        brand_mentioned, mention_count, position = self._enhanced_brand_detection(combined_text, brand_name)
        
        # Count citations/links
        citation_count = self._count_citations(combined_text)
        
        # Sentiment analysis
        sentiment = self._analyze_sentiment(combined_text, brand_name)
        
        # Calculate visibility score (0-100)
        visibility_score = self._calculate_visibility_score(
            brand_mentioned, position, mention_count, citation_count, sentiment, len(all_results)
        )
        
        return {
            "platform": platform.title(),
            "prompt": query,
            "response": combined_text[:500] + "..." if len(combined_text) > 500 else combined_text,
            "brand_mentioned": brand_mentioned,
            "mention_count": mention_count,
            "position": position,
            "sentiment": sentiment,
            "citation_count": citation_count,
            "runs_completed": len(all_results),
            "visibility_score": visibility_score,
            "response_length": len(combined_text)
        }
    
    @staticmethod
    def _extract_json(content: str) -> str:
        """Extract JSON from AI response (handle markdown)"""
        # Remove markdown code blocks
        if content.startswith("```"):
            content = content.replace("```json", "").replace("```", "").strip()
        
        # If not starting with array, find array in content
        if not content.startswith("["):
            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            if json_match:
                content = json_match.group(0)
        
        return content
    
    @staticmethod
    def _count_citations(text: str) -> int:
        """Count citations and links in text"""
        import re
        
        # URL patterns
        url_patterns = [
            r'https?://[^\s]+',
            r'www\.[^\s]+',
            r'\[.*?\]\(https?://[^\)]+\)',  # Markdown links
        ]
        
        # Citation patterns
        citation_patterns = [
            r'\[Source:\s*[^\]]+\]',
            r'\[[0-9]+\]',
            r'\(Source: [^)]+\)',
        ]
        
        urls = sum(len(re.findall(pattern, text, re.IGNORECASE)) for pattern in url_patterns)
        citations = sum(len(re.findall(pattern, text, re.IGNORECASE)) for pattern in citation_patterns)
        
        return urls + citations
    
    @staticmethod
    def _enhanced_brand_detection(text: str, brand_name: str) -> tuple:
        """Enhanced brand detection with multiple parsing strategies"""
        brand_lower = brand_name.lower()
        text_lower = text.lower()
        
        # Check if brand is mentioned at all
        brand_mentioned = brand_lower in text_lower
        mention_count = text_lower.count(brand_lower)
        
        if not brand_mentioned:
            return False, 0, None
        
        # Multiple strategies to find position
        position = None
        
        # Strategy 1: Look for numbered lists (1. Brand, 2. Brand)
        lines = text.split('\n')
        for line in lines:
            line_clean = line.strip()
            if brand_lower in line_clean.lower():
                # Look for number at start
                import re
                match = re.match(r'^(\d+)', line_clean)
                if match:
                    position = int(match.group(1))
                    break
        
        # Strategy 2: Look for markdown bold (**Brand**)
        if position is None:
            import re
            bold_pattern = r'\*\*(\d+)\.\s*' + re.escape(brand_name) + r'\*\*'
            match = re.search(bold_pattern, text, re.IGNORECASE)
            if match:
                position = int(match.group(1))
        
        # Strategy 3: Look for any number before brand name
        if position is None:
            import re
            patterns = [
                r'(\d+)\.\s*' + re.escape(brand_name),  # 1. Brand
                r'(\d+)\s+' + re.escape(brand_name),     # 1 Brand
                r'(\d+):\s*' + re.escape(brand_name),    # 1: Brand
            ]
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    position = int(match.group(1))
                    break
        
        # Strategy 4: Count lines until brand appears
        if position is None:
            lines = text.split('\n')
            for i, line in enumerate(lines):
                if brand_lower in line.lower():
                    position = i + 1
                    break
        
        return brand_mentioned, mention_count, position
    
    @staticmethod
    def _analyze_sentiment(text: str, brand_name: str) -> str:
        """Enhanced sentiment analysis"""
        sentences = [s for s in text.split('.') if brand_name.lower() in s.lower()]
        
        if not sentences:
            return "neutral"
        
        positive_words = ['best', 'great', 'excellent', 'leading', 'top', 'innovative', 'reliable', 'trusted', 'popular', 'recommended', 'preferred']
        negative_words = ['poor', 'bad', 'worst', 'lacking', 'limited', 'disappointing', 'inferior', 'weak', 'problematic']
        
        positive_count = sum(1 for word in positive_words if any(word in s.lower() for s in sentences))
        negative_count = sum(1 for word in negative_words if any(word in s.lower() for s in sentences))
        
        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        return "neutral"
    
    @staticmethod
    def _calculate_visibility_score(
        brand_mentioned: bool, 
        position: Optional[int], 
        mention_count: int, 
        citation_count: int, 
        sentiment: str, 
        runs_completed: int
    ) -> float:
        """Calculate unified visibility score (0-100) with improved weights"""
        if not brand_mentioned:
            return 0.0
        
        # Base score for being mentioned (reduced weight)
        base_score = 15.0
        
        # Position score (increased weight - most important factor)
        position_score = 0.0
        if position:
            if position <= 3:
                position_score = 50.0  # Top 3 - highest weight
            elif position <= 5:
                position_score = 40.0  # Top 5
            elif position <= 10:
                position_score = 30.0  # Top 10
            elif position <= 20:
                position_score = 20.0  # Top 20
            else:
                position_score = 10.0  # Beyond 20
        
        # Mention frequency score (moderate weight)
        mention_score = min(mention_count * 3.0, 15.0)  # Max 15 points
        
        # Citation score (lower weight)
        citation_score = min(citation_count * 1.5, 8.0)  # Max 8 points
        
        # Sentiment bonus (moderate weight)
        sentiment_bonus = 0.0
        if sentiment == "positive":
            sentiment_bonus = 8.0
        elif sentiment == "negative":
            sentiment_bonus = -4.0
        
        # Reliability bonus (lower weight)
        reliability_bonus = min(runs_completed * 1.0, 4.0)  # Max 4 points
        
        # Calculate total score
        total_score = base_score + position_score + mention_score + citation_score + sentiment_bonus + reliability_bonus
        
        # Ensure score is between 0 and 100
        return max(0.0, min(100.0, total_score))