# Define your item pipelines here

from charging_stations.models import Station

class StationPipeline:
    def process_item(self, item, spider):
        if Station.objects.filter(lat=item["lat"], long=item["long"]).exists():
            pass
        elif Station.objects.filter(address=item["address"]).exists():
            pass
        else:
            Station.objects.create(**item)
        return item
