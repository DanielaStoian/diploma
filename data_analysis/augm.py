import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from my_augm import my_augm
from graphs import bt_augm
from matplotlib import style
plt.style.use('ggplot')
datac = pd.read_csv('data_analysis\cluster_A.csv')

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

# for i in range(1):


#     res1 = my_augm(data[data.columns[3]])
#     res2 = bt_augm(data)
#     res3 = naive_augm(data)
#     pd.DataFrame(res1[0])[:168].plot(title="my_augm")
#     pd.DataFrame(res2[0]).plot(title="bt_augm")
#     pd.DataFrame(res3[0]).plot(title="naive")
#     pd.DataFrame(res1[1]).plot(title="med 1")
#     pd.DataFrame(res2[1]).plot(title="med 2")
#     pd.DataFrame(res3[1]).plot(title="med 3")
    # final_series = pd.DataFrame({'my': res1[0][168:168*2], 'bt': res2[0][168:168*2],'naive': res3[0][168:168*2]})
    # final_series.plot(title=str(i))

    # final_medians = pd.DataFrame({'1': res1[1], '2': res2[1], "3": res3[1]})
    # final_medians.plot()


def extract_data(file_name,column_name,format):
    data = pd.read_csv('data_analysis'+file_name, sep=';')
    # stations = data.stationID.unique()
    data[column_name] = pd.to_datetime(data[column_name], errors='coerce',format=format, exact=False)
    data = data.sort_values(by=[column_name]) 
    data = data.dropna().reset_index(drop=True)

    # st_data = {i:[] for i in stations}
    # for i in range(len(data)):
    #     st_data[data['stationID'][i]].append(data['connectionTime'][i])


    
    hours_df = pd.DataFrame({'date':pd.date_range(start=data[column_name].min(), end=data[column_name].max(),freq='H')})
    timed_arrivals = np.zeros((len(hours_df)))  
    idx = 0
    for i in range(0,len(hours_df)):
        while(data[column_name][idx]<=hours_df['date'][i]):
            timed_arrivals[i] += 1
            if idx == len(data[column_name])-1:
                break
            else:
                idx += 1
    return timed_arrivals,hours_df   
# pd.DataFrame(timed_arrivals).plot(title="data start")

def get_med(new_data):
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
    return true_medians

def get_percentiles(new_data):
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
    nd_percent = np.array(arr)
    true_perc = []
    for column in nd_percent.T:
        true_perc.append(np.percentile(column,[75,90]))
    return true_perc

def get_minmax(new_data):
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
        true_max.append([min(column), max(column)])
    return true_max

# pd.DataFrame(get_med(timed_arrivals)).plot(title="medians start")
timed_arrivals,hours_df = extract_data('\Boulder.csv', 'Start_Date___Time', '%Y/%m/%d %H:%M')
res1 = bt_augm(timed_arrivals)
# csv1 = pd.DataFrame(timed_arrivals, columns=['arrivals']).to_csv("before_1.csv")
# csv2 = pd.DataFrame(res1[0], columns=['arrivals']).to_csv("after_1.csv")
timed_data = pd.DataFrame({'time':hours_df['date'], 'arrivals':timed_arrivals})

# timed_data['arrivals'].plot()
# pd.DataFrame(res1[0]).plot()
# pd.DataFrame(res1[1]).plot()
ax = pd.DataFrame(get_minmax(res1[0])).plot.area(title="max",color=('#CCCCCC'),label='minmax')
pd.DataFrame(get_percentiles(res1[0])).plot.area(title="perc", color=('#87CEEB','#ADD8E6') ,ax=ax)
pd.DataFrame(res1[1]).plot(title="Augmented_1",ax=ax,color=('#4672E1'))
plt.legend()
plt.show()    