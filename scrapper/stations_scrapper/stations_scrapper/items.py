from scrapy_djangoitem import DjangoItem
import scrapy
# from backend.charging_stations.models import Station

class StationItem(DjangoItem):
    name = scrapy.Field() 
    long = scrapy.Field() 
    lat  = scrapy.Field() 
    address = scrapy.Field()
    type = scrapy.Field()
    origin = scrapy.Field()
    # djando_model = Station
