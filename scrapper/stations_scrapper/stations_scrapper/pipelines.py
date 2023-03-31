# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class StationsScrapperPipeline:
    def process_item(self, item, spider):
        print(item['name'])
        # item.save()
        # return item

# pipelines.py

import psycopg2

class StationsScrapperPipeline:

    def __init__(self):
        ## Connection Details
        hostname = 'localhost'
        username = 'postgres'
        password = 'pitarda12' # your password
        database = 'ChargingStations'

        ## Create/Connect to database
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database, port = 5000)
        
        ## Create cursor, used to execute commands
        self.cur = self.connection.cursor()
        
        ## Create quotes table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS charging_stations_station(
            id serial PRIMARY KEY, 
            name Char(200),
            address Char(200),
            lat Char(50),
            long Char(50),
            type Char(500),
            origin Char(50)
        )
        """)

    def process_item(self, item, spider):
        print(item["lat"], item["long"])
        ## Check to see if text is already in database 
        self.cur.execute("select * from charging_stations_station where (lat = %s AND long = %s) OR address = %s", (item['lat'],item['long'],item["address"]))
        result = self.cur.fetchone()

        ## If it is in DB, create log message
        if result:
            spider.logger.warn("Item already in database")
        ## If text isn't in the DB, insert data
        else:

            ## Define insert statement
            self.cur.execute(""" insert into charging_stations_station (name, address, lat, long, type, origin) values (%s,%s,%s,%s,%s,%s)""", (
                item["name"],
                item["address"],
                item["lat"],
                item["long"],
                item["type"],
                item["origin"],
            ))

            ## Execute insert of data into database
            self.connection.commit()
        return item

    
    def close_spider(self, spider):

        ## Close cursor & connection to database 
        self.cur.close()
        self.connection.close()

