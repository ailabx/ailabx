from statsmodels.tsa import stattools
import pandas as pd

data_benchmark = pd.read_csv('../../data/000300_index.csv')
data_benchmark.index =data_benchmark['date']
data_benchmark.sort_index(ascending=True,inplace=True)

rets = data_benchmark['close'] / data_benchmark['close'].shift(1) - 1
rets = rets[1:]

print(rets.head())
print(rets.tail())
acfs = stattools.acf(rets)
print('自相关系数：',acfs)

pacfs = stattools.pacf(rets)
print('偏相关系数：',pacfs)

from statsmodels.graphics.tsaplots import *
plot_acf(rets,use_vlines=True,lags=30)
plot_pacf(rets,use_vlines=True,lags=30)

import matplotlib.pyplot as plt
plt.show()