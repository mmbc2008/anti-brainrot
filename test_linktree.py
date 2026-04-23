import unittest
from linktree_scraper import LinktreeScraper

BASE_URL = "https://linktr.ee/chocolatecity"

class TestScraper(unittest.TestCase):

    
    lt_scraper = LinktreeScraper(BASE_URL, 3, 10)
    
    with open('linktree_test.html', 'r', encoding='utf-8') as file:
        input_html = file.read()
        
    def test_get_organiser_from_html(self):
        actual = self.lt_scraper.get_organiser_from_html(self.input_html)
        expected = "Chocolate City Amsterdam"
        self.assertEqual(actual, expected)
        
    def test_get_title_from_html(self):
        actual = self.lt_scraper.get_title_from_html(self.input_html)
        expected = "Tickets Queens & Kings Night"
        self.assertEqual(actual, expected)
        
                 

                
if __name__ == "__main__":
    unittest.main()
                