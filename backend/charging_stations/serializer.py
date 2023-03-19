from rest_framework import serializers

from charging_stations.models import Station

class StationSerializer(serializers.ModelSerializer):
   class Meta:
       model = Station
       fields = ('id', 'name', 'address', 'lat', 'long', 'type', 'origin')
