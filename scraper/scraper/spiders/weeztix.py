import scrapy
import json
from db import get_connection
from scraper.items import ScraperItem
from scrapy_playwright.page import PageMethod 

class WeeztixSpider(scrapy.Spider):
    
    name = "weeztix"
    
    async def start(self):
       with get_connection() as conn:
           cursor = conn.cursor()
           cursor.execute("SELECT url FROM leads WHERE vendor='weeztix' AND status='pending';")
           rows = cursor.fetchall()
       
       print(f"DEBUG: row = {rows}")
       for row in rows:
            if row:
                print(f"DEBUG: yielding {row}")
                yield scrapy.Request(
                    url=row[0],
                    callback=self.parse,
                    meta={"playwright": True,
                          "lead_url": row[0]}
                        #   "playwright_page_methods":[PageMethod("wait_for_selector", "span.subtitle.ot-text-small")]},
                )
    def parse(self, response):
        guid = response.url.split("/")[3]
        print(guid)
        yield scrapy.Request(
            url=f"https://shop.api.openticket.tech/{guid}/data",
            callback=self.parse_event,
            meta={"lead_url": response.meta["lead_url"]}
        )
        
    def parse_event(self, response):
        data = response.json()
        # with open("debug.json", "a") as f:
        #     json.dump(data, f, indent=2)
        event = data['events']
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
                organiser_id=None,
                price_from=str(prices),
                url=response.url,
                lead_url=response.meta["lead_url"]
            )
            
        

        
            
        