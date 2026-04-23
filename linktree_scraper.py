from scraper import AsyncScraper
from weeztix_scraper import WeeztixScraper
from bs4 import BeautifulSoup

class LinktreeScraper(AsyncScraper):
    def __init__(self, base_url, max_concurrency, max_pages):
        super().__init__(base_url, max_concurrency, max_pages)
        self.scrapers = {
            'weeztix': WeeztixScraper,
            'eventbrite': None
        }

    def get_source_from_url(self, url):
        return super().get_source_from_url(url)
    
    def _create_soup(self, html):
        """Create a BeautifulSoup object from HTML"""
        return BeautifulSoup(html, 'html.parser')
    
    def get_organiser_from_html(self, html):
        soup = self._create_soup(html)
        header = soup.find('h1').get_text()
        return header
    
    
    def get_urls_from_html(self, html, base_url):
        return super().get_urls_from_html(html, base_url)
    
    def get_title_from_html(self, html):
        soup = self._create_soup(html)
        divs = soup.find_all('div', class_=['line-clamp-2'])
        for div in divs:
            return div.get_text()
        
    async def get_outgoing_link_data(self, data_type):
        event_data = list(self.page_data.values())[0]
        link = event_data['outgoing_links'][0]
        source = self.get_source_from_url(link)
        if source in self.scrapers:
            scraper_class = self.scrapers[source]
            async with scraper_class(link, self.max_concurrency, self.max_pages) as scraper_instance:
                await scraper_instance.scrape(self.max_concurrency, self.max_pages)
                scraper_dict = list(scraper_instance.page_data.values())[0]
                return scraper_dict.get(data_type)
        else:
            print(f'No scraper available for source {source}.')
    
    def get_category_from_html(self, html):
        return None
        
    def get_date_from_html(self, html):
       return None
    
    def get_location_from_html(self, html):
        return None
    
    def get_price_from_html(self, html):
        return None
    
    def get_times_from_html(self, html):
        return None
    
    async def scrape(self, max_con, max_pages):
        await super().scrape(max_con, max_pages)
        event_data = list(self.page_data.values())[0]
        event_data['date'] = await self.get_outgoing_link_data('date')
        event_data['address'] = await self.get_outgoing_link_data('address')
        event_data['price'] = await self.get_outgoing_link_data('price')
        event_data['times'] = await self.get_outgoing_link_data('times')
        event_data['outgoing_links'] = event_data['outgoing_links'][0]
        filtered_data = { key: value for key, value in self.page_data.items() if value is not None}
        return filtered_data
    
        
    
async def scrape_site_async(base_url, max_con, max_pages):
    async with LinktreeScraper(base_url, max_con, max_pages) as scraper:
        scraped = await scraper.scrape(max_con, max_pages)
        return scraped
    
    