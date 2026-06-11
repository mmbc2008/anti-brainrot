import scrapy
from db import get_connection
from scraper.items import LeadsItem

VENDORS = ['eventbrite', 'fourvenues', 'weeztix', 'paradiso']
    
class LinktreeSpider(scrapy.Spider):
    name = "linktree"
    allowed_domains = ["linktr.ee"]
    
    async def start(self):
       with get_connection() as conn:
           cursor = conn.cursor()
           cursor.execute("SELECT id, profile_url FROM organisers;")
           rows = cursor.fetchall()
       
       for row in rows:
            if row:
                yield scrapy.Request(
                    url=row[1],
                    callback=self.parse,
                    meta={"playwright": True,
                          "organiser_id": row[0]},
                )

    def parse(self, response):
        for container in response.css('div[data-testid="NewLinkContainerInner"]'):
            href = container.css("a::attr(href)").get()
            if href:
                vendor = self.find_vendor(href)
                if vendor:
                    yield LeadsItem(
                        organiser_id=response.meta["organiser_id"],
                        url=href,
                        vendor=vendor,
                        status="pending"
                    )
                
    def find_vendor(self, url):
        for vendor in VENDORS:
            if vendor in url:
                return vendor
        
