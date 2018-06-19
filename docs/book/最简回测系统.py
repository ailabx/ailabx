import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv('../../data/000300_index.csv')
data.index = data['date']
del data['date']
data.sort_index(ascending=True,inplace=True)

data['20d'] = data['close'].rolling(window=20).mean()
data['60d'] = data['close'].rolling(window=60).mean()

#data[['close','20d','60d']].plot(grid=True,figsize=(8,5))
data['20-60'] = data['20d'] - data['60d']

data['points'] = np.where(data['20-60']>50,1,0)
data['points'] = np.where(data['20-60']<-50,-1,data['points'])

#data['points'].plot()
data['market'] = np.log(data['close']/data['close'].shift(1))
data['strategy'] = data['points'].shift(1) * data['market']
data[['market','strategy']].cumsum().apply(np.exp).plot()

plt.show()

