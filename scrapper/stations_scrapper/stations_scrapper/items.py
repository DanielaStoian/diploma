# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class StationsScrapperItem(scrapy.Item):
    name = scrapy.Field() 
    long = scrapy.Field() 
    lat  = scrapy.Field() 
    address = scrapy.Field()
    type = scrapy.Field()
    origin = scrapy.Field()
    