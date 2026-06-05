import scrapy
from db import get_connection
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
                    meta={"playwright": True},
                )
    def parse(self, response):
        pass