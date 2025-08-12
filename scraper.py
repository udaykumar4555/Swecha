import sys
import os
import requests
from bs4 import BeautifulSoup

def chunk_text(text, chunk_size=500):
    """Split text into smaller chunks for easier processing."""
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    if len(chunks) > 1:
        print(f"🪓 Chunked into {len(chunks)} parts (each ~{chunk_size} chars)")
    return chunks

def scrape_and_clean(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.Timeout:
        print(f"⏳ Timeout while trying to reach {url}")
        return None
    except requests.RequestException as e:
        print(f"❌ Request failed: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    for tag in soup(['script', 'style', 'header', 'footer', 'nav', 'aside']):
        tag.decompose()

    title = soup.title.string.strip() if soup.title else "No Title Found"

    paragraphs = []
    for p in soup.find_all('p'):
        text = p.get_text(strip=True)
        if text:
            paragraphs.extend(chunk_text(text, 500))  # Chunking

    if not paragraphs:
        print(f"⚠️ No readable content found for {url}")
        return None

    return {
        "url": url,
        "title": title,
        "content": paragraphs
    }

def save_to_file(data):
    os.makedirs("scraped_data", exist_ok=True)
    count = len(os.listdir("scraped_data")) + 1
    filename = f"scraped_data/sample{count}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"URL: {data['url']}\n")
        f.write(f"Title: {data['title']}\n\n")
        for para in data['content']:
            f.write(para + "\n\n")

    print(f"✅ Saved {len(data['content'])} paragraph(s) to {filename}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scraper.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    result = scrape_and_clean(url)

    if result:
        print(f"\n🔍 Scraping: {result['url']}")
        print(f"📄 Title: {result['title']}")
        print("\nContent:")
        for para in result['content']:
            print(f"- {para}")

        save_to_file(result)
