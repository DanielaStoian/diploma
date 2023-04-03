import scrapy

class StationItem(scrapy.Item):
    name = scrapy.Field() 
    lat  = scrapy.Field() 
    long = scrapy.Field() 
    address = scrapy.Field()
    type = scrapy.Field()
    origin = scrapy.Field()
    dhmos = scrapy.Field()
    category = scrapy.Field()

