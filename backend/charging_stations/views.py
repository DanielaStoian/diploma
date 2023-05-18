import json
import random
from django.shortcuts import render
from rest_framework import viewsets
from math import radians, sin, cos, sqrt, atan2
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import math

from charging_stations.serializer import StationSerializer, ProfileSerializer
from charging_stations.models import Station, Profile, Dhmos
from rest_framework import viewsets, status, serializers, generics, filters, exceptions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from django.db import DataError
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
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

def optimize(stations, start_time, stay_hours, types, radius):
    candidates = []
    dt = datetime.now()
    wd = dt.weekday()
    for station in stations:
        if (int(station[0].mean_updating[start_time+24*wd])<int(station[0].chargers_num)) and (types in station[0].type):  
            candidates.append(station)
    if len(candidates) == 0:
        return 0
    # init winner station
    winner_st = []

    for st in candidates:    
        mean = [int(i) for i in st[0].mean_updating]
        mean = pd.DataFrame(mean)
        tmp_list = (mean[wd*24:(wd+1)*24].shift(0) + mean[wd*24:(wd+1)*24].shift(1, fill_value=0))/(int(st[0].chargers_num)*2)
        winner_st.append((tmp_list[0][start_time+24*wd],st[0]))

    # make a recomendation percentage
    util_sort = sorted(winner_st, key=lambda tup: (tup[0]))
    dist_sort = sorted(candidates, key=lambda tup: (tup[1]))
    util_percent = 50/(1.0 - util_sort[0][0])
    dist_percent = 50/(radius - dist_sort[0][1])
    new_util = [(50.0,util_sort[0][1])]
    new_dist = [(dist_sort[0][0],50.0)]
    for i in range(1,len(util_sort)):
        new_util.append((util_sort[i][0]*util_percent, util_sort[i][1]))
        new_dist.append((dist_sort[i][0], dist_sort[i][1]*dist_percent))
    final_winner = []
    for i in range(len(new_util)):
        for j in range(len(new_dist)):
            if new_util[i][1] == new_dist[j][0]:
                final_winner.append((int(new_util[i][0] + new_dist[j][1]), new_util[i][1]))
                break      
    return sorted(final_winner, key=lambda tup: (tup[0]), reverse=True)   
    


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
            return Response('No stations found.',
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
                dist = 0.0
                dist = distance(float(request.query_params['lat']),float(request.query_params['long']),float(station.lat),float(station.long))
                if dist<=radius:
                    # TODO remove same station if exists (dist = 0)
                    radius_stations.append((station,dist))      
            opt = optimize(radius_stations, int(request.query_params['start_time']), int(request.query_params['stay_hours']),  request.query_params['type'], radius)        
            final_data = []
            stations = [x[1] for x in opt]
            ser = StationSerializer(stations, many=True).data
            i=0
            for odict in ser:
                final_data.append((odict,opt[i][0]))
                i+=1
            return Response(final_data,
                            status=status.HTTP_200_OK)
        except DataError as e:
            return Response(str(e)[:15], status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            print(e)
            return Response('An unexpected error occured.',
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['post'], detail=False)
    def set_mean_updating(self, request):
        try:
            stations = Station.objects.all()
            for station in stations:
                station.mean_updating = station.mean
                station.save()
            return Response(status=status.HTTP_200_OK)
        except DataError as e:
            return Response(str(e)[:15], status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            print(e)
            return Response('An unexpected error occured.',
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)   

    @action(methods=['post'], detail=False)
    def set_prices(self, request):
        try:
            stations = Station.objects.all()
            for station in stations:
                station.price = round(random.uniform(0.45, 1.00), 2)
                station.save()
            return Response(status=status.HTTP_200_OK)
        except DataError as e:
            return Response(str(e)[:15], status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            print(e)
            return Response('An unexpected error occured.',
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)                         

    @action(methods=['post'], detail=False)
    def add_arrival(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            station = Station.objects.get(id=int(data['id']))
            dt = datetime.now()
            wd = dt.weekday()
            start = int(data['start_time']) + 24*wd
            accepted = False
            if (int(station.mean_updating[start])<int(station.chargers_num)):
                accepted = True
            if accepted == False:        
                return Response(status=status.HTTP_403_FORBIDDEN)
            tmp = list(station.mean_updating)
            for i in range(int(data['stay_hours'])):
                tmp[start+i] = str(int(station.mean_updating[start+i]) + 1)
            str_tmp = ""
            for x in tmp:
                str_tmp += x
            Station.objects.filter(id=station.id).update(mean_updating=str_tmp)
            Profile.objects.filter(id=data['user_id']).update(last_check=timezone.now())
            return Response(status=status.HTTP_200_OK)
        except DataError as e:
            return Response(str(e)[:15], status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            print(e)
            return Response('An unexpected error occured.',
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)                                                     




class ProfilesView(viewsets.ViewSet):

    @action(methods=['get'], detail=False)
    def get_profile(self, request):
        try:
            profile = Profile.objects.filter(email=request.query_params['email'], password=request.query_params["password"])
            if profile.exists():
                profile = profile[0]
                data = ProfileSerializer(data={'id':profile.id, 'first_name':profile.first_name, 'last_name':profile.last_name, 'email': profile.email, 'password':profile.password, 'last_check':profile.last_check})
                data.is_valid()
                data = data.validated_data
                return Response({'data':data, 'id':profile.id}, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response('An unexpected error occured.',
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['post'], detail=False)
    def add_profile(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            if Profile.objects.filter(email=data['email']).exists():
                return Response(status=status.HTTP_302_FOUND)
            else:    
                Profile.objects.create(email=data['email'], password=data['password'], first_name=data['first_name'], last_name=data['last_name'])
                return Response(status=status.HTTP_200_OK)
        except DataError as e:
            return Response(str(e)[:15], status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            print(e)
            return Response('An unexpected error occured.',
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)              
                            
    @action(methods=['get'], detail=False)
    def get_check_permission(self, request):
        try:
            profile = Profile.objects.filter(id=request.query_params['id'])
            if profile.exists():
                time_threshold = timezone.now() - timedelta(hours=4)
                if profile[0].last_check == None:
                    return Response(status=status.HTTP_200_OK)
                elif time_threshold>profile[0].last_check:
                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response(status=status.HTTP_403_FORBIDDEN)    
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response('An unexpected error occured.',
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)        
                            