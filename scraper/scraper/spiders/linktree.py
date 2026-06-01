import scrapy
from db import get_connection


class LinktreeSpider(scrapy.Spider):
    name = "linktree"
    allowed_domains = ["linktr.ee"]
    
    
    async def start(self):
       with get_connection() as conn:
           cursor = conn.cursor()
           cursor.execute("SELECT profile_url FROM organisers;")
           row = cursor.fetchone()
       
       print(f"DEBUG: row = {row}")
       
       if row:
           print(f"DEBUG: yielding {row[0]}")
           yield scrapy.Request(
               url=row[0],
               callback=self.parse,
               meta={"playwright": True},
           )

    def parse(self, response):
        for container in response.css('div[data-testid="NewLinkContainerInner"]'):
            href = container.css("a::attr(href)").get()
            title = container.css("a::text").get()
            if href:
                yield {
                    "title": title.strip() if title else None,
                    "url": href,
                    "source":response.url
                }
