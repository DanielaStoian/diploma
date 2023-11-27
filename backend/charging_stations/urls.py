
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from charging_stations.views import StationsView, ProfilesView
from django.views.generic.base import TemplateView

router = routers.DefaultRouter()
router.register(r'stations', StationsView, basename="stations")
router.register(r'profiles', ProfilesView, basename="profiles")

urlpatterns = [
   path('', include(router.urls)),
   path('manifest.json', TemplateView.as_view(template_name='manifest.json', content_type='application/json'), name='manifest.json')
]