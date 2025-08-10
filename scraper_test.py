import unittest
from scraper import scrape_and_clean

class TestScraper(unittest.TestCase):

    def test_scrape_valid_url(self):
        """Test scraping a valid URL"""
        result = scrape_and_clean("https://www.india.gov.in/")
        self.assertIsNotNone(result, "Result should not be None")
        self.assertIn("title", result, "Result should contain a title")
        self.assertTrue(len(result["content"]) > 0, "Content should not be empty")

    def test_scrape_invalid_url(self):
        """Test scraping an invalid URL (should return None or handle gracefully)"""
        result = scrape_and_clean("https://thiswebsitedoesnotexist1234.com/")
        self.assertTrue(result is None or result.get("content") == "", "Should handle invalid URL gracefully")

if __name__ == "__main__":
    unittest.main()
