import scrapy
from scrapy.spiders import SitemapSpider
from stations_scrapper.items import StationItem
import googlemaps
from .protergiaCharge import protergiaCharge
from .plugShare import plugShare
from .inCharge import inCharge
from .elpeFuture import elpeFuture
import json
from shapely.geometry import shape, Point
import pandas as pd

API_KEY = 'AIzaSyAoNP6N8mFdG3M3vanWtRKty5sPghWPqQ4'

def address_to_coords(address):
  gmaps = googlemaps.Client(key=API_KEY)

# Geocoding an address
  geocode_result = gmaps.geocode(address)
  try:
    lat = geocode_result[0]['geometry']['location']['lat']
    long = geocode_result[0]['geometry']['location']['lng']
    return lat,long
  except:
    return None, None

def add_manually(name):
    if name == "ΝΑΟΥΣΑΣ":
        return ["ΗΡΩΙΚΗΣ ΠΟΛΕΩΣ ΝΑΟΥΣΑΣ",2]
    elif name == "ΣΕΡΒΙΩΝ-ΒΕΛΒΕΝΤΟΥ":
        return ["ΣΕΡΒΙΩΝ",3]
    elif name == "ΟΡΕΣΤΙΔΟΣ":
        return ["ΟΡΕΣΤΙΑΔΑΣ",2]
    elif name == "ΛΑΡΙΣΑΙΩΝ":
        return ["ΛΑΡΙΣΑΣ",1]
    elif name == "ΚΑΛΑΜΠΑΚΑΣ":
        return ["ΜΕΤΕΩΡΩΝ",3] 
    elif name == "ΦΑΡΚΑΔΟΝΑΣ":
        return ["ΦΑΡΚΑΔΟΝΟΣ",3]  
    elif name == "ΜΩΛΟΥ-ΑΓΙΟΥ ΚΩΝΣΤΑΝΤΙΝΟΥ":
        return ["ΚΑΜΕΝΩΝ ΒΟΥΡΛΩΝ",3]     
    elif name == "ΣΤΥΛΙΔΟΣ":
        return ["ΣΤΥΛΙΔΑΣ",3]   
    elif name == "ΚΕΡΚΥΡΑΣ":
        return ["ΚΕΝΤΡΙΚΗΣ ΚΕΡΚΥΡΑΣ ΚΑΙ ΔΙΑΠΟΝΤΙΩΝ ΝΗΣΩΝ",2]     
    elif name == "ΚΕΦΑΛΟΝΙΑΣ":
        return ["ΑΡΓΟΣΤΟΛΙΟΥ",2]  
    elif name == "ΙΕΡΑΣ ΠΟΛΗΣ ΜΕΣΟΛΟΓΓΙΟΥ":
        return ["ΙΕΡΑΣ ΠΟΛΕΩΣ ΜΕΣΟΛΟΓΓΙΟΥ",2]
    elif name == "ΉΛΙΔΑΣ":
        return ["ΗΛΙΔΑΣ",2]
    elif name == "ΗΛΙΟΥΠΟΛΕΩΣ":
        return ["ΗΛΙΟΥΠΟΛΗΣ",1]
    elif name == "ΦΙΛΑΔΕΛΦΕΙΑΣ-ΧΑΛΚΗΔΟΝΟΣ":
        return ["ΝΕΑΣ ΦΙΛΑΔΕΛΦΕΙΑΣ-ΝΕΑΣ ΧΑΛΚΗΔΟΝΑΣ",1]
    elif name == "ΗΡΑΚΛΕΙΟΥ":
        return ["ΗΡΑΚΛΕΙΟΥ ΚΡΗΤΗΣ",1]     
    elif name == "ΠΕΤΡΟΥΠΟΛΕΩΣ":
        return ["ΠΕΤΡΟΥΠΟΛΗΣ",1]
    elif name == "ΠΕΙΡΑΙΩΣ":
        return ["ΠΕΙΡΑΙΑ",1]
    elif name == "ΣΑΛΑΜΙΝΟΣ":
        return ["ΣΑΛΑΜΙΝΑΣ",2]
    elif name == "ΎΔΡΑΣ":
        return ["ΥΔΡΑΣ",3]    
        # THIS DOES NOT EXIST 
    elif name == "ΑΓΚΙΣΤΡΙΟΥ":
        return ["ΑΓΚΙΣΤΡΙΟΥ",3]  
    elif name == "ΛΕΣΒΟΥ":
        return ["ΔΥΤΙΚΗΣ ΛΕΣΒΟΥ",3]   
    elif name == "ΣΑΜΟΥ":
        return ["ΔΥΤΙΚΗΣ ΣΑΜΟΥ",3]    
    elif name == "ΨΑΡΩΝ":
        return ["ΗΡΩΙΚΗΣ ΝΗΣΟΥ ΨΑΡΩΝ",3]   
        # THIS DOES NOT EXIST 
    elif name == "ΑΓΑΘΟΝΗΣΙΟΥ":
        return ["ΑΓΑΘΟΝΗΣΙΟΥ",3]  
    elif name == "ΚΑΣΟΥ":
        return ["ΗΡΩΙΚΗΣ ΝΗΣΟΥ ΚΑΣΟΥ",3]   
        # THIS DOES NOT EXIST                              
    elif name == "ΓΑΥΔΟΥ":
        return ["ΓΑΥΔΟΥ",3]   
        # THIS DOES NOT EXIST 
    elif name == "ΑΓΙΟ ΟΡΟΣ (Αυτοδιοίκητο)":
        return ["ΑΓΙΟ ΟΡΟΣ (Αυτοδιοίκητο)",3]   
    else:
        return [0,0]                                              

def add_category(lat,long):
    # load GeoJSON file containing sectors
    with open('C:\\Users\\Daniela\\OneDrive\\Desktop\\git\\diploma\\scrapper\\stations_scrapper\\stations_scrapper\\spiders\\dhmoi.geojson', encoding = 'utf-8') as f:
        js = json.load(f)

    organized_dhmoi = data = pd.read_csv('C:\\Users\\Daniela\\OneDrive\\Desktop\\git\\diploma\\scrapper\\stations_scrapper\\stations_scrapper\\spiders\\organized_dhmoi.csv')    

    # construct point based on lon/lat returned by geocoder
    # point = Point(23.818465,38.672728)
    point = Point(float(long),float(lat))

    # check each polygon to see if it contains the point
    for feature in js['features']:
        polygon = shape(feature['geometry'])
        # print(polygon.distance(point))
        if polygon.contains(point):
            # print('Found containing polygon:', feature['properties']["LEKTIKO"])
            name = feature['properties']["LEKTIKO"]
            # ΔΗΜΟΣ
            name = name.replace("ΔΗΜΟΣ ","")
            # spaces
            name = name.replace(" - ","-")
            # ' -> A
            name = name.replace("’","Α")
            tmp = 0
            for i in range(0,organized_dhmoi.shape[0]):
                dhmos = organized_dhmoi[data.columns[1]][i]
                if dhmos==name:
                    # return organized_dhmoi[data.columns[3]][i]
                    return [dhmos,organized_dhmoi[data.columns[3]][i]]
                    tmp = 1
            if tmp==0:
                res = add_manually(name)
                if res[0]!=0:
                    return res
                else:
                    return [0,0]
    return 0   

class ChargeSpot(scrapy.Spider): 
    name = "ChargeSpot"

    start_urls = [ 
      "https://chargespot.gr/simeia-fortisis/"
    ]  

    download_delay = 0.1


    def parse(self, response):
        items = StationItem()
        stations = response.css('.col-lg-3')
        for station in stations:
            info = station.css('::text').extract()
            coords = station.css('a::attr(href)').extract()
            coords = coords[0].split("/")[-1]
            lat = coords.split(",")[0]
            long = coords.split(",")[1]
            name = info[0]
            address = info[1]
            if len(info) < 4:
              type = info[2]
            else:  
              type = info[3] 

            dhmos = add_category(lat,long)
            if dhmos[0]!=0:
                items['dhmos'] = dhmos[0]
                items['category'] = str(dhmos[1])
            else: 
              items['dhmos'] = ""  
              items['category'] = ""

            items['name'] = name
            items['address'] = address
            items['lat'] = lat
            items['long'] = long
            items['type'] = type
            items['origin'] = "ChargeSpot"
            yield items

           
class Fortisis(scrapy.Spider): 
    name = "Fortisis"

    start_urls = [ 
      "https://www.fortisis.eu/map/"
    ]  

    download_delay = 0.1


    def parse(self, response):

        items = StationItem()
        stations = response.css('.point-list-item')
        for station in stations:
            name = station.css('.point-list-item-title::text').extract()
            address = station.css('.point-list-item-address::text').extract()
            connectors = station.css('.point-list-item-connectors::text').extract()
            origin = "Fortisis"
            if len(address) < 1:
              continue
            else:
              lat,long = address_to_coords(address[0])

              dhmos = add_category(lat,long)
            if dhmos[0]!=0:
                items['dhmos'] = dhmos[0]
                items['category'] = str(dhmos[1])
            else: 
              items['dhmos'] = ""  
              items['category'] = "" 

              items["name"] = name[0]
              items["address"] = address[0]
              if len(connectors) >=1:
                items["type"] = connectors[0]
              items["lat"] = str(lat)
              items["long"] = str(long)
              items["origin"] = origin
              yield items

class ProtergiaCharge(scrapy.Spider): 
    name = "ProtergiaCharge"

    download_delay = 0.1

    # this is only needed for the spider to start
    start_urls = [ 
          "https://protergiacharge.gr/charge-map/"
        ] 

    def parse(self, response):

        data = protergiaCharge()
        for station in data:
            name = station["name"]
            lat = station["lat"]
            long = station["long"]
            yield scrapy.Request(station["url"], callback=self.parse_page,cb_kwargs={'name':name,'lat':lat,'long':long})
            

    def parse_page(self, response,name,lat,long):
        items = StationItem()
        address = response.css('.sidebar-address::text').extract()
        address = address[0].replace('\n',"")
        address = address.replace('  ',"")
        type = response.css('.connector-label::text').extract()
        origin = "ProtergiaCharge"

        dhmos = add_category(lat,long)
        if dhmos[0]!=0:
            items['dhmos'] = dhmos[0]
            items['category'] = str(dhmos[1])
        else: 
          items['dhmos'] = ""  
          items['category'] = ""

        items["name"] = name
        items["address"] = address
        items["type"] = type[0]
        items["lat"] = str(lat)
        items["long"] = str(long)
        items["origin"] = origin
        yield items
            
class PlugShare(scrapy.Spider): 
    name = "PlugShare"

    download_delay = 0.1

    # this is only needed for the spider to start
    start_urls = [ 
          "https://www.plugshare.com/"
        ] 

    def parse(self, response):
        items = StationItem()
        data = plugShare()
        for station in data:

            dhmos = add_category(station["lat"],station["long"])
            if dhmos[0]!=0:
                items['dhmos'] = dhmos[0]
                items['category'] = str(dhmos[1])
            else: 
              items['dhmos'] = ""  
              items['category'] = ""

            items["name"] = station["name"]
            items["address"] = station["address"]
            items["type"] = station["type"]
            items["lat"] = station["lat"]
            items["long"] = station["long"]
            items["origin"] = station["origin"]
            yield items

class InCharge(scrapy.Spider): 
    name = "InCharge"

    download_delay = 0.1

    # this is only needed for the spider to start
    start_urls = [ 
          "https://www.nrgincharge.gr/el/xartis-fortiston"
        ] 

    def parse(self, response):
        items = StationItem()
        data = inCharge()
        for station in data:

            dhmos = add_category(station["lat"],station["long"])
            if dhmos[0]!=0:
                items['dhmos'] = dhmos[0]
                items['category'] = str(dhmos[1])
            else: 
              items['dhmos'] = ""  
              items['category'] = ""

            items["name"] = station["name"]
            items["address"] = station["address"]
            items["type"] = station["type"]
            items["lat"] = station["lat"]
            items["long"] = station["long"]
            items["origin"] = station["origin"]
            yield items
   
class ElpeFuture(scrapy.Spider): 
    name = "ElpeFuture"

    download_delay = 0.1

    # this is only needed for the spider to start
    start_urls = [ 
          "https://elpefuture.gr/location"
        ] 

    def parse(self, response):
        items = StationItem()
        data = elpeFuture()
        for station in data:

            dhmos = add_category(station["lat"],station["long"])
            if dhmos[0]!=0:
                items['dhmos'] = dhmos[0]
                items['category'] = str(dhmos[1])
            else: 
              items['dhmos'] = ""  
              items['category'] = ""

            items["name"] = station["name"]
            items["address"] = station["address"]
            items["type"] = station["type"]
            items["lat"] = station["lat"]
            items["long"] = station["long"]
            items["origin"] = station["origin"]
            yield items          


class BlinkCharging(SitemapSpider):
  
    name = "BlinkCharging"
    download_delay = 0.1
    sitemap_urls = ["https://blinkcharging.gr/portfolio-sitemap.xml"] 

    def parse(self, response):
        items = StationItem()
        name = response.css("#gdlr-core-wrapper-1 .gdlr-core-skin-title::text").extract()
        type = response.css(".gdlr-core-port-info:nth-child(1) .gdlr-core-port-info-value::text").extract()
        address = response.css(".gdlr-core-port-info+ .gdlr-core-port-info .gdlr-core-port-info-value").css("::text").extract()
        lat,long = address_to_coords(address[0])

        dhmos = add_category(lat,long)
        if dhmos[0]!=0:
            items['dhmos'] = dhmos[0]
            items['category'] = str(dhmos[1])
        else: 
          items['dhmos'] = ""  
          items['category'] = ""

        items["name"] = name[0]
        items["address"] = address[0]
        items["type"] = type[0]
        items["lat"] = str(lat)
        items["long"] = str(long)
        items["origin"] = "BlinkCharging"
        yield items   
        