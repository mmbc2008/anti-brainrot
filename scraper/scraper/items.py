# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScraperItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    location = scrapy.Field()
    starts_at = scrapy.Field()
    ends_at = scrapy.Field()
    categories = scrapy.Field()
    organiser = scrapy.Field()
    price_from = scrapy.Field()
    url = scrapy.Field()
