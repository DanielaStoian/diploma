import scrapy

from scrapy_djangoitem import DjangoItem
from charging_stations.models import Station

class StationItem(DjangoItem): 
   django_model = Station

