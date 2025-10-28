"""Web scraping service"""
import aiohttp
from bs4 import BeautifulSoup
from typing import Optional


class ScraperService:
    def __init__(self):
        self.session = None
    
    async def scrape_website(self, url: str) -> str:
        """Scrape website content"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')
                        
                        # Remove script and style elements
                        for script in soup(["script", "style"]):
                            script.decompose()
                        
                        # Get text content
                        text = soup.get_text()
                        
                        # Clean up text
                        lines = (line.strip() for line in text.splitlines())
                        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                        text = ' '.join(chunk for chunk in chunks if chunk)
                        
                        return text[:5000]  # Limit content length
                    else:
                        raise Exception(f"Failed to fetch website: {response.status}")
        except Exception as e:
            raise Exception(f"Scraping error: {str(e)}")
    
    async def close(self):
        """Close session"""
        if self.session:
            await self.session.close()
