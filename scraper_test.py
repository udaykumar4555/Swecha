import scraper

def test_scraper():
    url = "https://www.india.gov.in/"
    data = scraper.scrape_and_clean(url)

    assert data is not None, "❌ scrape_and_clean returned None"
    assert "title" in data, "❌ No title in result"
    assert len(data["content"]) > 0, "❌ Content is empty"

    print("✅ All tests passed!")

if __name__ == "__main__":
    test_scraper()
