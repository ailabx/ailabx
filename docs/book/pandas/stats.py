import pandas as pd


df = pd.read_csv('../../../data/000300_index.csv')
df.index =  df['date']
df.sort_index(inplace=True)
print(df.head())

#计算收益率
df['return'] = df['close']/df['close'].shift(1) - 1
#计算涨跌
df['up_or_down'] = df['close'] > df['close'].shift(1)

print(df.head())
print(df['up_or_down'].value_counts())

print(df['return'].describe())

import matplotlib.pyplot as plt
#df['return'].plot()
df['return'].hist(bins=80, alpha=0.3, color='g', normed=True)
df['return'].plot(kind='kde', style='r',xlim=[-0.1, 0.1],grid=True)
plt.show()