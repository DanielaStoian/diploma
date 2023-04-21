# Define your item pipelines here

from charging_stations.models import Station

class StationPipeline:
    def process_item(self, item, spider):
        if Station.objects.filter(lat=item["lat"], long=item["long"]).exists():
            Station.objects.update(**item)
        else:
            Station.objects.create(**item)
        return item
