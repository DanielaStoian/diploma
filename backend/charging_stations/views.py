import json
from django.shortcuts import render
from rest_framework import viewsets

from charging_stations.serializer import StationSerializer
from charging_stations.models import Station
from rest_framework import viewsets, status, serializers, generics, filters, exceptions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from django.db import DataError
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.


class StationsView(viewsets.ViewSet):

    @action(methods=['get'], detail=False)
    def get_dhm_geojson(self, request, *args, **kwargs):
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
    def get_stations(self, request, *args, **kwargs):
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


