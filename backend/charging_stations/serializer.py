from rest_framework import serializers

from charging_stations.models import Station, Profile

class StationSerializer(serializers.ModelSerializer):
   class Meta:
       model = Station
       fields = ('id', 'name', 'address', 'lat', 'long', 'type', 'origin', 'dhmos', 'mean', 'mean_updating', 'chargers_num', 'price')

class ProfileSerializer(serializers.ModelSerializer):
   class Meta:
       model = Profile
       fields = ('id', 'first_name', 'last_name', 'email', 'password', 'last_check')
