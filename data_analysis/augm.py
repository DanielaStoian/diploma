import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from my_augm import my_augm
from graphs import bt_augm
from matplotlib import style
from datetime import timezone, datetime
import pytz
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


def extract_data(file_name,column_name,format):
    data = pd.read_csv('data_analysis'+file_name, sep=';')
    # stations = data.stationID.unique()
    data[column_name] = pd.to_datetime(data[column_name], errors='coerce',format=format, exact=False, utc=True)
    data = data.sort_values(by=[column_name]) 
    data = data.dropna().reset_index(drop=True)
    start = data[column_name].min().date()
 
    # fix timezone gaps
    
    timestamp = datetime.combine(start, datetime.min.time())
    timezone = data[column_name].dt.tz
    start = timezone.localize(timestamp)
    hours_df = pd.DataFrame({'date':pd.date_range(start=start, end=data[column_name].max(),freq='H')})
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
        true_max.append(np.mean(column))
    return true_max


file_names = ['\Boulder.csv', '\London_2.csv', '\potential3_2.csv']
column_names = ['Start_Date___Time', 'Plug in Date and Time', 'Transaction Start']
formats = ['%Y/%m/%d %H:%M', '%d/%m/%Y %H:%M', '%d/%m/%Y %H:%M']
for i in range(0,3):
    timed_arrivals,hours_df = extract_data(file_names[i], column_names[i], formats[i])
    res1 = bt_augm(timed_arrivals)
    csv1 = pd.DataFrame(timed_arrivals, columns=['arrivals']).to_csv("before_"+str(i+1)+".csv")
    csv2 = pd.DataFrame(res1[0], columns=['arrivals']).to_csv("after_"+str(i+1)+".csv")
    # timed_data = pd.DataFrame({'time':hours_df['date'], 'arrivals':timed_arrivals})

    ax1 = pd.DataFrame(get_minmax(timed_arrivals),columns=['mix','max']).plot.area(color=('#CCCCCC'), title='Category '+str(i+1)+' Before Augmentation')
    pd.DataFrame(get_percentiles(timed_arrivals),columns=['75%','90%']).plot.area( color=('#87CEEB','#ADD8E6'), ax=ax1 )
    pd.DataFrame(get_med(timed_arrivals),columns=['median']).plot(color=('#4672E1'),ax=ax1)
    
    ax2 = pd.DataFrame(get_minmax(res1[0]),columns=['mix','max']).plot.area(color=('#CCCCCC'), title='Category '+str(i+1)+' After Augmentation')
    pd.DataFrame(get_percentiles(res1[0]),columns=['75%','90%']).plot.area( color=('#87CEEB','#ADD8E6'), ax=ax2 )
    pd.DataFrame(res1[1],columns=['median']).plot(color=('#4672E1'),ax=ax2)
    pd.DataFrame(get_mean(res1[0]),columns=['mean']).plot(color=('#4672E1'),title="Mean")

plt.show()    