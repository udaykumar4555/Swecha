import requests
from bs4 import BeautifulSoup

def scrape_and_clean(url):
    try:
        # Timeout handling
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.Timeout:
        print(f"⏳ Timeout while trying to reach {url}")
        return None
    except requests.RequestException as e:
        print(f"❌ Request failed: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # Remove unwanted tags
    for tag in soup(['script', 'style', 'header', 'footer', 'nav', 'aside']):
        tag.decompose()

    # Get title
    title = soup.title.string.strip() if soup.title else "No Title Found"

    # Extract paragraphs
    paragraphs = [p.get_text(strip=True) for p in soup.find_all('p') if p.get_text(strip=True)]

    # Empty content handling
    if not paragraphs:
        print(f"⚠️ No readable content found for {url}")
        return None

    return {
        "url": url,
        "title": title,
        "content": paragraphs
    }
