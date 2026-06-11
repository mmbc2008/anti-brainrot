import scrapy
from db import get_connection
from scraper.items import ScraperItem


API_BASE = "https://shop.api.openticket.tech"
WEEZTIX_SHOP_BASE = "https://shop.weeztix.com"

class WeeztixSpider(scrapy.Spider):
    
    name = "weeztix"
    
    async def start(self):
       with get_connection() as conn:
           cursor = conn.cursor()
           cursor.execute("SELECT url, organiser_id FROM leads WHERE vendor='weeztix' AND status='pending';")
           rows = cursor.fetchall()
       for row in rows:
            if row:
                yield scrapy.Request(
                    url=row[0],
                    callback=self.parse,
                    meta={"playwright": True,
                          "lead_url": row[0],
                          "organiser_id": row[1]}
                )
    def parse(self, response):
        guid = response.url.split("/")[3]
        yield scrapy.Request(
            url=f"{API_BASE}/{guid}/data",
            callback=self.parse_event,
            meta={"lead_url": response.meta["lead_url"],
                  "organiser_id": response.meta["organiser_id"]}
        )
        
    def parse_event(self, response):
        data = response.json()
        event = data['events']
        guid = response.url.split("/")[3]
        prices = []
        if isinstance(data['tickets'], dict):
            tickets = data['tickets']
            for info  in tickets.values():
                if info['status'] == 'available':
                    prices.append(info['min_price'])

        if event:
            yield ScraperItem(
                title=event[0]['name'],
                location=event[0]['location']['address'],
                starts_at=event[0]['start'],
                ends_at=event[0]['end'],
                categories=None,
                organiser_id=response.meta['organiser_id'],
                price_from=prices,
                url=f"{WEEZTIX_SHOP_BASE}/{guid}/tickets",
                lead_url=response.meta["lead_url"]
            )
            
        

        
            
        