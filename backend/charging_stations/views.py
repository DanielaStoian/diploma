from django.shortcuts import render
from rest_framework import viewsets

from charging_stations.serializer import StationSerializer
from charging_stations.models import Station
from rest_framework import viewsets, status, serializers, generics, filters, exceptions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action

# Create your views here.


class Stations(viewsets.ViewSet):

    @action(methods=['get'], detail=False)
    def get_unknown_products(self, request, *args, **kwargs):
        try:
            products = Station.objects.get(id = request.query_params['id'])
            ser = UnknownProductSerializer(products).data
            return Response({'data': ser}, status=status.HTTP_200_OK)
        except DataError as e:
            return Response(str(e)[:15], status=status.HTTP_403_FORBIDDEN)
        except ObjectDoesNotExist as e:
            return Response('There is no product with this name.',
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response('An unexpected error occured.',
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)