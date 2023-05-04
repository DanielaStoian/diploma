import json
from django.shortcuts import render
from rest_framework import viewsets
from math import radians, sin, cos, sqrt, atan2
from datetime import datetime
import pandas as pd
import numpy as np
import math

from charging_stations.serializer import StationSerializer
from charging_stations.models import Station
from rest_framework import viewsets, status, serializers, generics, filters, exceptions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from django.db import DataError
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

def distance(lat1, lon1, lat2, lon2):
    # approximate radius of earth in km
    R = 6373.0
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c

    return distance

def optimize(stations,start_time,stay_hours,types):
    candidates = []
    dt = datetime.now()
    wd = dt.weekday()
    for station in stations:
        if (int(station.mean[start_time+24*wd])<int(station.chargers_num)) and (types in station.type):
            candidates.append(station)
    if len(candidates) == 0:
        return 0
    initial_utilization = pd.DataFrame({'HoD': np.arange(0,24,1)})
    # init winner station
    winner_st = []

    for st in candidates:    
        mean = [int(i) for i in st.mean]
        mean = pd.DataFrame(mean)
        tmp_list = (mean[wd*24:(wd+1)*24].shift(0) + mean[wd*24:(wd+1)*24].shift(1, fill_value=0))/int(st.chargers_num)
        winner_st.append((tmp_list[0][start_time+24*wd],st))
    # print(sorted(winner_st, key=lambda tup: (tup[0])))
    return sorted(winner_st, key=lambda tup: (tup[0]))   
    


class StationsView(viewsets.ViewSet):

    @action(methods=['get'], detail=False)
    def get_dhm_geojson(self, request):
        try:
            shp_path = "C:\\Users\\Daniela\\OneDrive\\Desktop\\git\\diploma\\backend\\charging_stations\\dhmoi.geojson"
            myshp = open(shp_path,'rb')
            data = json.load(myshp)
            return Response(data, status=status.HTTP_200_OK)
    
        except Exception as e:
            print(e)
            return Response('An unexpected error occured.',
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['get'], detail=False)
    def get_stations(self, request):
        try:
            stations = Station.objects.all()
            # st_dhmoi = stations.select_related()
            ser = StationSerializer(stations, many=True).data
            return Response(ser,
                            status=status.HTTP_200_OK)
        except DataError as e:
            return Response(str(e)[:15], status=status.HTTP_403_FORBIDDEN)
        except ObjectDoesNotExist as e:
            return Response('There is no product with this name.',
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response('An unexpected error occured.',
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['get'], detail=False)
    def get_radius(self, request):
        try:
            radius = int(request.query_params['radius'][0])
            stations = Station.objects.filter()
            radius_stations = []
            for station in stations:
                # print(distance(float(request.query_params['lat']),float(request.query_params['long']),float(station.lat),float(station.long)))
                if distance(float(request.query_params['lat']),float(request.query_params['long']),float(station.lat),float(station.long))<=radius:
                    # TODO remove same station if exists (dist = 0)
                    radius_stations.append(station) 
            opt = optimize(radius_stations, int(request.query_params['start_time']), request.query_params['stay_hours'],  request.query_params['type'])        
            ser = StationSerializer(opt[0][1]).data
            return Response(ser,
                            status=status.HTTP_200_OK)
        except DataError as e:
            return Response(str(e)[:15], status=status.HTTP_403_FORBIDDEN)
        except ObjectDoesNotExist as e:
            return Response('There is no product with this name.',
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response('An unexpected error occured.',
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


