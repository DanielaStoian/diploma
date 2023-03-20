
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from charging_stations.views import StationsView

router = routers.DefaultRouter()
router.register(r'stations', StationsView, basename="stations")

urlpatterns = [
   path('', include(router.urls)),
]