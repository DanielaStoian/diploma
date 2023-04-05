import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose as sm
from statsmodels.tsa.seasonal import STL
import seaborn as sns
from scipy import stats
from scipy.special import boxcox, inv_boxcox

from arch.bootstrap import MovingBlockBootstrap

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

def MBB(x, window_size):
    bx = np.zeros(int(np.floor(len(x) / window_size + 2) * window_size))
    for i in range(1, int(np.floor(len(x) / window_size)) + 2):
        c = np.random.randint(1, len(x) - window_size + 1)
        bx[(i - 1) * window_size + 1:i * window_size] = x[c:c + window_size - 1]
    start_from = np.random.randint(0, window_size-1) + 1
    return bx[start_from :start_from - 1 + len(x)]

data = pd.read_csv('data_analysis\cluster_A.csv')

arrivals = {'days': data[data.columns[3]]}
arrivals = pd.DataFrame(arrivals)

def bootstrap(arrivals,num,mu):
    # Box-Cox transformation
    # TODO lamda parameter check
    box_cox = stats.boxcox(arrivals, lmbda=1)
    box_cox = pd.DataFrame(box_cox)
    
    # Decomposition
    # TODO frequency check
    stl=sm(box_cox, model='additive', period=168)   
    # stl.plot()

    # Bootstrap
    # TODO window_size = block_size = 2*freq
    # pd.DataFrame(stl.resid).plot()
    mbb = MBB(stl.resid, window_size=2*168)
    # pd.DataFrame(mbb).plot()
    for i in range(0,len(mbb)):
        mbb[i] += stl.trend[i] + stl.seasonal[i] * mu
    xs = []
    xs.append(arrivals)
    # pd.DataFrame(mbb).plot()
    for i in range(1,num):  
    # this is not working properly 
        xs.append(invboxcox(mbb,1))    
    return xs

multi = 1
mu = 1
while(multi<2):
    num_boots = 4
    boots = bootstrap(arrivals=arrivals,num=num_boots,mu=mu)
    new_series =  np.zeros(arrivals.shape[0])
    for i in range(0, num_boots):
        for j in range(0,len(new_series)):
            if len(boots[i])>j :
                if i==0 :
                    new_series[j] += boots[i]['days'][j]
                else:
                    new_series[j] += boots[i][j]   
    # pd.DataFrame(new_series).plot()
    for i in range(0,len(new_series)):   
        if new_series[i]<0:
            new_series[i] = 0               
    for i in range(0,len(new_series)):
        new_series[i] = np.round(new_series[i] / num_boots, 0)
    new_series = np.nan_to_num(new_series)
    mu+=1
    multi = int(np.round(sum(new_series)/sum(arrivals['days'])))
    # print(multi)

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
 
# printing the column
pd.DataFrame(true_medians).plot()

arrivals['Demand'] = new_series
fig, axes = plt.subplots(nrows=2, ncols=1)

arrivals['Demand'].plot(ax=axes[0])
arrivals['days'].plot(ax=axes[1])
plt.show()