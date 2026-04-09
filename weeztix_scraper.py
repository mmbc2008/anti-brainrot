from scraper import AsyncScraper
from bs4 import BeautifulSoup

class WeeztixScraper(AsyncScraper):

    def __init__(self, base_url, max_concurrency, max_pages):
        super().__init__(base_url, max_concurrency, max_pages)

    def _create_soup(self, html):
        """Create a BeautifulSoup object from HTML"""
        return BeautifulSoup(html, 'html.parser')

    def get_title_from_html(self, html):
        soup = self._create_soup(html)
        title = soup.find('h4', class_='card-heading__content__title').get_text()
        return title

    def get_date_from_html(self, html):
        soup = self._create_soup(html)
        span = soup.find('span', class_='subtitle ot-text-small').get_text().split("Cut")
        new_span = span[0].split(" ")
        date = new_span[1] + " " + new_span[4] +" "+ new_span[5]
        formatted_date = date.replace(",", "")
        return formatted_date

    def get_times_from_html(self, html):
        soup = self._create_soup(html)
        span = soup.find('span', class_='subtitle ot-text-small').get_text().split("Cut")
        raw_times = span[0].split(" ")
        times = raw_times[2] + raw_times[3] + " - " + raw_times[6] + raw_times[7]
        return times

    def get_location_from_html(self, html):
        soup = self._create_soup(html)
        location = soup.find('span', class_='event-summary-header__location__address').get_text().strip(" ")
        return location

    def get_category_from_html(self, html):
        return None

    def get_organiser_from_html(self, html):
        # soup = self._create_soup(html)
        # header = soup.find('h4', class_='card-heading__content__title').get_text()
        # organiser = header.split("-")[0]
        # return organiser
        return None

    def get_price_from_html(self, html):
        soup = self._create_soup(html)
        divs = soup.find_all('div', class_=['available'])
        for div in divs:
            span = div.find_all('span', class_='ot-text-tiny')
            for price in span:
                return price.get_text()
                


async def scrape_site_async(base_url, max_con, max_pages):
    async with WeeztixScraper(base_url, max_con, max_pages) as scraper:
        scraped = await scraper.scrape(max_con, max_pages)
        return scraped