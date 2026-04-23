from weeztix_scraper import WeeztixScraper
import unittest

class TestScraper(unittest.TestCase):
    
    BASE_URL = "https://shop.weeztix.com/0339c682-d3e5-40bb-9ca1-1942a0dee164/tickets?shop_code=fkeqnq8c"
    
    weez_scarper = WeeztixScraper(BASE_URL, 3, 10)
    with open("weeztix_test.html", "r", encoding="utf-8") as file:
            input_html = file.read()
    
    def test_get_title_from_html(self):
        actual = self.weez_scarper.get_title_from_html(self.input_html)
        expected = " Queens & Kings Night "
        self.assertEqual(actual, expected)
            
    def test_get_date_from_html(self):
        actual = self.weez_scarper.get_date_from_html(self.input_html)
        expected = "4/26/26 - 4/27/26"
        self.assertEqual(actual, expected)
        
    def test_get_times_from_html(self):
        actual = self.weez_scarper.get_times_from_html(self.input_html)
        expected = "7:00PM - 12:00AM"
        self.assertEqual(actual, expected)
        
    def test_get_location_from_html(self):
        actual = self.weez_scarper.get_location_from_html(self.input_html)
        expected = "Beursplein 5, 1012 JW Amsterdam, Nederland"
        self.assertEqual(actual, expected)
    
    def test_get_price_from_html(self):
        actual = self.weez_scarper.get_price_from_html(self.input_html)
        expected = " €15.00 + €1.00 fee. "
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()