import pandas as pd
import os
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'backend.settings'
django.setup()
from charging_stations.models import *

organized_dhmoi = data = pd.read_csv('./scrapper/stations_scrapper/stations_scrapper/spiders/organized_dhmoi.csv')
for i in range(0,len(organized_dhmoi)):
    Dhmos.objects.create(name = organized_dhmoi['ΚΑΛΛΙΚΡΑΤΙΚΟΙ ΔΗΜΟΙ'][i], category_name = organized_dhmoi['ΧΑΡΑΚΤΗΡΙΣΜΟΣ ΔΗΜΟΥ'][i], category = organized_dhmoi['category'][i])
