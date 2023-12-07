import json
import os
import django
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import sys
from statsmodels.tsa.seasonal import seasonal_decompose as sm
from statsmodels.tsa.seasonal import STL
import seaborn as sns
from scipy import stats
# from scipy.special import boxcox, inv_boxcox

from arch.bootstrap import MovingBlockBootstrap
sys.path.insert(0, '../data_analysis')
# from graphs import bt_augm
# from my_augm import my_augm
os.environ['DJANGO_SETTINGS_MODULE'] = 'backend.settings'
django.setup()

from charging_stations.models import *


def my_augm(dataframe):

    # data = pd.read_csv('data_analysis\cluster_A.csv')
    data = dataframe
    # arrivals = {'days': data[data.columns[3]]}

    arrivals = {'days': data}
    arrivals = pd.DataFrame(arrivals)

    # pd.DataFrame(arrivals['days']).plot(title="start data")

    multi = 1
    inc = 0
    mu = 3 + random.uniform(-1, 1)
    while multi<3:

        stl=sm(arrivals['days'], model='additive', period=168) 
        # pd.DataFrame(stl.seasonal).plot()
        seasonal = stl.seasonal
        seasonal = np.nan_to_num(seasonal)

        resid = stl.resid
        resid = np.nan_to_num(resid) 
        # pd.DataFrame(resid).plot()

        indexes = np.random.choice(range(0, len(seasonal)), int(len(seasonal)*1),replace=True)
        rs_seas = np.zeros(len(seasonal))
        for i in indexes:
            rs_seas[i] = (7+inc*10)*seasonal[i] 
        new_data = np.zeros(len(arrivals))
        noise = np.random.normal(loc=0.0, scale=0.5+inc, size=len(new_data))
        # pd.DataFrame(stl.trend).plot(title="trend")
        # pd.DataFrame(rs_seas).plot(title="season")
        for i in range(len(noise)):
            new_data[i] = noise[i] * resid[i] * 0.5
            if noise[i] < 0:
                noise[i] = 0

        # pd.DataFrame(noise).plot(title="noise")
        for i in range(0,arrivals.shape[0]):
            # if rs_seas[i] + noise[i] < 0.5:
            #     print(i)
            new_data[i] = arrivals['days'][i] + (rs_seas[i] + noise[i])
            if new_data[i] < 0:
                new_data[i] = 0
            # print(arrivals)
        
        multi = np.round(sum(new_data)/sum(arrivals['days']))

        for i in range(0,len(new_data)):
                new_data[i] = np.round(new_data[i]/(multi/3), 0)
        medians = []
        for i in range(0,len(new_data),168):
            tmp = []
            for j in range(0,168):
                try:
                    tmp.append(new_data[j+i])
                except:
                    break    
            medians.append(tmp)
        medians.pop()
        nd_medians = np.array(medians)
        true_medians = []
        for column in nd_medians.T:
            true_medians.append(np.median(column))

        multi = np.round(sum(new_data)/sum(arrivals['days']))

        print(multi) 
        inc += 0.1
    return [new_data,true_medians]

def invboxcox(y,ld):
   if ld == 0:
      return(np.exp(y))
   else:
      t_list = []
      for i in y:
        if i<=0:
            t_list.append(i)
        else:
            t_list.append(np.exp(np.log(ld*i+1)/ld))
      return t_list

def boxcox(y,ld):
   if ld == 0:
      return(np.log(y))
   else:
      t_list = []
      for i in y:
        t_list.append(((i**ld)-1)/ld)
      return t_list

def MBB(x, window_size):
    bx = np.zeros(int(np.floor(len(x) / window_size + 2) * window_size))
    for i in range(1, int(np.floor(len(x) / window_size)) + 2):
        c = np.random.randint(1, len(x) - window_size + 1)
        bx[((i - 1) * window_size + 1):(i * window_size)] = x[c:c + window_size - 1]
    start_from = np.random.randint(0, window_size-1) + 1
    return bx[start_from :start_from - 1 + len(x)]

def bootstrap(arrivals,num,mu):
    # Box-Cox transformation
    if np.min(arrivals['days']) > 1e-6:
        box_cox, lambda_ = stats.boxcox(arrivals['days'], lmbda=None)
        box_cox = pd.DataFrame(box_cox)
    else:
        box_cox, lambda_ = arrivals['days'], 1
        box_cox = pd.DataFrame(box_cox)

    # Decomposition
    stl=sm(box_cox, model='additive', period=168)   

    stl_print = sm(box_cox, model='additive', period=168)   
    stl_print.plot()
    plt.show()
    # Bootstrap
    # window_size = block_size = 2*freq
    mbb = MBB(stl.resid, window_size=2*168)
    for i in range(0,len(mbb)):
        mbb[i] += stl.trend[i] + stl.seasonal[i] * mu
    xs = []
    mbb =  np.nan_to_num(mbb)
    xs.append(arrivals['days'])
    for i in range(1,num):  
        # tmp = invboxcox(mbb,lambda_)
        tmp =  np.nan_to_num(mbb)
        xs.append(tmp)  

    return xs

def bt_augm(dataframe, mul = 3):
    data = dataframe
    arrivals = {'days': data}
    arrivals = pd.DataFrame(arrivals)
    multi = 1
    mu = 1
    while(multi<mul):
        num_boots = 4
        boots = bootstrap(arrivals=arrivals,num=num_boots,mu=mu)
        new_series =  np.zeros(len(arrivals))
        for i in range(0, num_boots):
            for j in range(0,len(new_series)):
                if len(boots[i])>j :
                    new_series[j] += boots[i][j]   
        # pd.DataFrame(new_series).plot()
        for i in range(0,len(new_series)):   
            if new_series[i]<0:
                new_series[i] = 0                      
        for i in range(0,len(new_series)):
            new_series[i] = np.round(new_series[i] / (num_boots), 0)
        new_series = np.nan_to_num(new_series)
        mu+=1
        multi = int(np.round(sum(new_series)/sum(arrivals['days'])))
        # print(multi,mu)

    medians = []
    for i in range(0,len(new_series),168):
        tmp = []
        for j in range(0,168):
            try:
                tmp.append(new_series[j+i])
            except:
                break    
        medians.append(tmp)
    medians.pop()
    nd_medians = np.array(medians)
    true_medians = []
    for column in nd_medians.T:
        true_medians.append(np.median(column))
    return [new_series,true_medians]

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

def check_max(data, max_mu):
    for i in range(len(data)):
        if data[i] > max_mu:
            data[i] = max_mu
    return data      

def double_hours(data, max_st):
    doubled_data = []
    doubled_data.append(data[0])
    for i in range(1,len(data)):
        tmp = data[i] + data[i-1]
        if tmp > max_st:
            data[i] = max_st - data[i-1]
            tmp = max_st
        doubled_data.append(tmp)
    return doubled_data

try:
    data1 = pd.read_csv('initial_1.csv', sep=';')
    data2 = pd.read_csv('initial_2.csv', sep=';')
    data3 = pd.read_csv('initial_3.csv', sep=';')
    stations = Station.objects.all().order_by('id')
    



    for station in stations:
        print(station.id)
        dhmos = Dhmos.objects.get(id=station.dhmos_id)
        if dhmos.category == '1':
            window_size = 168*int(round((len(data1))/(3*168)))
            start = np.random.randint(0,(len(data1)-window_size)/168)*168  
            data = data1['arrivals'][start:start+window_size]
            data = data.reset_index(drop=True)
            max_st = int(station.chargers_num)
            idx = max_st
            if max_st < 3:
                idx = 4
            random_mu = random.uniform(idx-2, idx)
            augm_data = bt_augm(data, random_mu)[0]
            augm_data = check_max(augm_data,max_st)
            augm_mean = get_mean(augm_data)
            augm_mean = double_hours(augm_mean,max_st)
            mean = "".join(map(str, augm_mean))
            # pd.DataFrame(augm_mean).plot(title=str(max_st))
            Station.objects.filter(id=station.id).update(mean=mean)
        elif dhmos.category == '2' :
            window_size = 168*int(round((len(data2))/(5*168)))
            start = np.random.randint(0,(len(data2)-window_size)/168)*168
            data = data2['arrivals'][start:start+window_size]
            data = data.reset_index(drop=True)
            max_st = int(station.chargers_num)
            idx = max_st
            if max_st < 3:
                idx = 4
            random_mu = random.uniform(idx-2, idx)
            augm_data = bt_augm(data, random_mu)[0]
            augm_data = check_max(augm_data,max_st)
            augm_mean = get_mean(augm_data)
            augm_mean = double_hours(augm_mean,max_st)
            mean = "".join(map(str, augm_mean))
            # pd.DataFrame(augm_mean).plot()
            Station.objects.filter(id=station.id).update(mean=mean)
        elif dhmos.category == '3' :
            window_size = 168*int(round((len(data3))/(2*168)))
            start = np.random.randint(0,(len(data3)-window_size)/168)*168  
            data = data3['arrivals'][start:start+window_size]
            data = data.reset_index(drop=True)
            max_st = int(station.chargers_num)
            idx = max_st
            if max_st < 3:
                idx = 4
            random_mu = random.uniform(idx-2, idx)
            augm_data = bt_augm(data, random_mu)[0]
            augm_data = check_max(augm_data,max_st)
            augm_mean = get_mean(augm_data)
            augm_mean = double_hours(augm_mean,max_st)
            mean = "".join(map(str, augm_mean))
            # pd.DataFrame(augm_mean).plot()
            Station.objects.filter(id=station.id).update(mean=mean)
    # plt.show()
except Exception as e: 
    print(e)    