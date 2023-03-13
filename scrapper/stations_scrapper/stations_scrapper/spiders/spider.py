import scrapy

class ChargeSpot(scrapy.Spider): 
    name = "ChargeSpot"

    start_urls = [ 
      "https://chargespot.gr/simeia-fortisis/"
    ]  

    download_delay = 0.1


    def parse(self, response):
        stations = response.css('.col-lg-3')
        for station in stations:
            info = station.css('::text').extract()
            coords = station.css('a::attr(href)').extract()
            # coords are inside a link
            # print(coords) 
            name = info[0]
            address = info[1]
            # could be missing?
            type = info[3] 
           
class Fortisis(scrapy.Spider): 
    name = "Fortisis"

    start_urls = [ 
      "https://www.fortisis.eu/map/"
    ]  

    download_delay = 0.1


    def parse(self, response):
        stations = response.css('.point-list-item')
        for station in stations:
            name = station.css('.point-list-item-title::text').extract()
            # needs address_to_coords
            address = station.css('.point-list-item-address::text').extract()
            connectors = station.css('.point-list-item-connectors::text').extract()
          
        