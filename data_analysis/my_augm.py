import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import math
from statsmodels.tsa.seasonal import seasonal_decompose as sm

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

        multi = sum(new_data)/sum(arrivals['days'])

        print(multi) 
        inc += 0.1
    return [new_data,true_medians]
