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


    stl=sm(arrivals['days'], model='additive', period=168) 
    # pd.DataFrame(stl.seasonal).plot()
    seasonal = stl.seasonal
    seasonal = np.nan_to_num(seasonal)

    indexes = np.random.choice(range(0, len(seasonal)), int(len(seasonal)*1),replace=True)
    rs_seas = np.zeros(len(seasonal))
    for i in indexes:
        # if seasonal[i] < 0:
        #     seasonal[i] = abs(seasonal[i]) * 0
        rs_seas[i] = 7*seasonal[i] 
    new_data = np.zeros(len(arrivals))
    noise = np.random.normal(loc=0.0, scale=0.5, size=len(new_data))
    # pd.DataFrame(stl.trend).plot(title="trend")
    # pd.DataFrame(rs_seas).plot(title="season")
    for i in range(len(noise)):
        new_data[i] = noise[i] 
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
    for i in range(0,len(new_data)):
            new_data[i] = np.round(new_data[i] / 1.5, 0)
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
    return [new_data,true_medians]
    # printing the column
    # pd.DataFrame(true_medians).plot(title="true medians")

    # results1 = pd.DataFrame({'finally': new_data, 'first': arrivals['days']})

    # results1.plot()
    # plt.legend(loc='lower right')
    # plt.xlabel("Episode")
    # plt.ylabel("Rewards")

    # pd.DataFrame(new_data).plot(title="final data",)
    # plt.show()