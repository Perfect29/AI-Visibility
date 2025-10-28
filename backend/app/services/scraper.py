"""Web scraping service"""
import aiohttp
from bs4 import BeautifulSoup
from typing import List
import re
from collections import Counter


class ScraperService:
    """Handle website scraping and keyword extraction"""
    
    @staticmethod
    async def scrape_domain(url: str) -> str:
        """Scrape domain content for keyword extraction"""
        async with aiohttp.ClientSession() as session:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            async with session.get(str(url), headers=headers, timeout=30) as response:
                if response.status != 200:
                    raise Exception(f"Failed to fetch: Status {response.status}")
                
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                # Remove unwanted elements
                for script in soup(["script", "style", "nav", "footer"]):
                    script.decompose()
                
                # Extract important text
                important_text = []
                
                # Title and meta
                title = soup.find('title')
                if title:
                    important_text.append(title.get_text())
                
                meta_desc = soup.find('meta', attrs={'name': 'description'})
                if meta_desc and meta_desc.get('content'):
                    important_text.append(meta_desc['content'])
                
                # Headings
                for heading in soup.find_all(['h1', 'h2', 'h3']):
                    important_text.append(heading.get_text())
                
                # Main content
                main_content = soup.find(['main', 'article']) or soup.find('body')
                if main_content:
                    paragraphs = main_content.find_all('p')[:10]
                    for p in paragraphs:
                        important_text.append(p.get_text())
                
                return ' '.join(important_text)
    
    @staticmethod
    def extract_keywords_fallback(text: str, brand_name: str, top_n: int = 5) -> List[str]:
        """Fallback keyword extraction without AI"""
        words = re.findall(r'\b[a-z]{3,15}\b', text.lower())
        stop_words = {
            'the', 'and', 'for', 'with', 'this', 'that', 'from', 
            'have', 'been', 'will', 'are', 'our', 'your'
        }
        filtered = [
            w for w in words 
            if w not in stop_words and w not in brand_name.lower()
        ]
        common = Counter(filtered).most_common(top_n)
        return [word for word, count in common]

