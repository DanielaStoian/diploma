import json
import os
import django
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import sys
sys.path.insert(0, 'C:\\Users\\Daniela\\OneDrive\\Desktop\\git\\diploma\\data_analysis')
from graphs import bt_augm
from my_augm import my_augm
os.environ['DJANGO_SETTINGS_MODULE'] = 'backend.settings'
django.setup()

from charging_stations.models import *

def get_mean(new_data):
    arr = []
    for i in range(0,len(new_data),168):
        tmp = []
        for j in range(0,168):
            try:
                tmp.append(new_data[j+i])
            except:
                break    
        arr.append(tmp)
    arr.pop()
    nd_max = np.array(arr)
    true_max = []
    for column in nd_max.T:
        true_max.append(int(np.round(np.mean(column))))
    return true_max

try:
    data1 = pd.read_csv('C:\\Users\\Daniela\\OneDrive\\Desktop\\git\\diploma\\backend\\initial_1.csv', sep=';')
    data2 = pd.read_csv('C:\\Users\\Daniela\\OneDrive\\Desktop\\git\\diploma\\backend\\initial_2.csv', sep=';')
    data3 = pd.read_csv('C:\\Users\\Daniela\\OneDrive\\Desktop\\git\\diploma\\backend\\initial_3.csv', sep=';')
    stations = Station.objects.all().order_by('id')
    

    for station in stations[:80]:
        print(station.id)
        # if station.category == '1' :
        #     window_size = 168*int(round((len(data1))/(3*168)))
        #     start = np.random.randint(0,(len(data1)-window_size)/168)*168  
        #     print(window_size,start,len(data1))   
        #     data = data1['arrivals'][start:start+window_size]
        #     data = data.reset_index(drop=True)
        #     augm_data = bt_augm(data, random.uniform(2.0, 4.0))[0]
        #     augm_mean = get_mean(augm_data)
        #     mean = "".join(map(str, augm_mean))
        #     pd.DataFrame(augm_mean).plot()
        #     Station.objects.filter(id=station.id).update(mean=mean)
        # if station.category == '2' :
        #     window_size = 168*int(round((len(data2))/(5*168)))
        #     start = np.random.randint(0,(len(data2)-window_size)/168)*168    
        #     print(window_size,start,len(data2))  
        #     data = data2['arrivals'][start:start+window_size]
        #     data = data.reset_index(drop=True)
        #     augm_data = bt_augm(data, random.uniform(2.0, 4.0))[0]
        #     augm_mean = get_mean(augm_data)
        #     mean = "".join(map(str, augm_mean))
        #     pd.DataFrame(augm_mean).plot()
        #     # Station.objects.filter(id=station.id).update(mean=mean)

        if station.category == '3' :
            window_size = 168*int(round((len(data3))/(2*168)))
            start = np.random.randint(0,(len(data3)-window_size)/168)*168  
            data = data3['arrivals'][start:start+window_size]
            data = data.reset_index(drop=True)
            augm_data = bt_augm(data, random.uniform(2.0, 4.0))[0]
            augm_mean = get_mean(augm_data)
            mean = "".join(map(str, augm_mean))
            pd.DataFrame(augm_mean).plot()
            # Station.objects.filter(id=station.id).update(mean=mean)
    plt.show()
except Exception as e: 
    print(e)    