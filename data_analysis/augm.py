import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from my_augm import my_augm
from graphs import bt_augm

# data = pd.read_csv('data_analysis\cluster_A.csv')

def naive_augm(dataframe):
    arrivals = {'days': dataframe[dataframe.columns[3]]}
    arrivals = pd.DataFrame(arrivals)

    noise = np.random.normal(loc=0.0, scale=1, size=len(arrivals))
    new_data = arrivals['days']
    s_sum = sum(arrivals['days'])
    for i in range(len(arrivals)):
        if noise[i] < 0:
            noise[i] = 0
        new_data[i] += noise[i]
        new_data[i] = np.round(new_data[i]/1.5, 0)
    multi = np.round(sum(new_data)/s_sum,0)
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

    return [new_data, true_medians]    

# for i in range(5):


#     res1 = my_augm(data)
#     res2 = bt_augm(data)
#     res3 = naive_augm(data)

#     final_series = pd.DataFrame({'my': res1[0][168:168*2], 'bt': res2[0][168:168*2],'naive': res3[0][168:168*2]})
#     final_series.plot(title=str(i))

#     final_medians = pd.DataFrame({'1': res1[1], '2': res2[1], "3": res3[1]})
#     final_medians.plot()

# plt.show()

data = pd.read_csv('data_analysis\EV_transactions_datasets.csv',sep=';')

stations = data.stationID.unique()

st_data = {i:[] for i in stations}
data['connectionTime'] = pd.to_datetime(data['connectionTime'])
for i in range(len(data)):
    st_data[data['stationID'][i]].append(data['connectionTime'][i])



hours_df = pd.DataFrame({'date':pd.date_range(start=data['connectionTime'].min(), end=data['connectionTime'].max(),freq='H')})

timed_arrivals = np.zeros((len(hours_df),len(st_data)))  



j = 0
for st in st_data.keys():
    idx = 0
    for i in range(0,len(hours_df)):
        while(st_data[st][idx]<=hours_df['date'][i]):
            timed_arrivals[i][j] += 1
            if idx == len(st_data[st])-1:
                break
            else:
                idx += 1
    j += 1        


# pd.DataFrame(timed_arrivals[:,0]).plot()
# plt.show()   

# print(pd.DataFrame(timed_arrivals).iloc[:, :1])
res1 = my_augm(timed_arrivals[:,0])


final_series = pd.DataFrame(res1[0])
final_series.plot()
final_medians = pd.DataFrame(res1[1])
final_medians.plot()

plt.show()    