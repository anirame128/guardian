import requests
from bs4 import BeautifulSoup

def browser_fetch(url: str) -> str:
    """Fetch HTML content from URL"""
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.text

def browser_extract_all_text(html: str) -> str:
    """Extract all visible text from HTML content"""
    soup = BeautifulSoup(html, "html.parser")
    
    # Remove script and style elements
    for element in soup(['script', 'style']):
        element.decompose()
    
    # Extract visible text (automatically skips comments)
    return soup.get_text(separator='\n', strip=True)
