import scrapy

class ScraperItem(scrapy.Item):
    
    title = scrapy.Field()
    location = scrapy.Field()
    starts_at = scrapy.Field()
    ends_at = scrapy.Field()
    categories = scrapy.Field()
    organiser_id = scrapy.Field()
    price_from = scrapy.Field()
    url = scrapy.Field()
    lead_url = scrapy.Field()

class LeadsItem(scrapy.Item):
    
    organiser_id = scrapy.Field()
    url = scrapy.Field()
    vendor = scrapy.Field()
    status = scrapy.Field()
    
    