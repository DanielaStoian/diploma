import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import math
from statsmodels.tsa.seasonal import seasonal_decompose as sm

def resample(data, percentage):
    length = int(len(data)*percentage)
    indexes = np.zeros(length)
    for i in range(0,length-1):
        indexes[i] = np.random.randint(0,len(data))
    return indexes

data = pd.read_csv('data_analysis\cluster_A.csv')

arrivals = {'days': data[data.columns[3]]}
arrivals = pd.DataFrame(arrivals)

stl=sm(arrivals, model='additive', period=168) 

trend = stl.trend
trend = np.nan_to_num(trend)
# indexes = resample(trend, percentage=0.5)

indexes = random.sample(range(0, len(trend)), int(len(trend)*0.5))
rs_trend = np.zeros(len(trend))
for i in indexes:
    rs_trend[i] = math.ceil(trend[i])
new_data = np.zeros(len(arrivals))
for i in range(0,arrivals.shape[0]):
    new_data[i] = arrivals['days'][i] + rs_trend[i]
    # print(arrivals)

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
 
# printing the column
pd.DataFrame(true_medians).plot()

pd.DataFrame(new_data).plot()
plt.show()