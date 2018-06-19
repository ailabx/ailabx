import pandas as pd

data = pd.read_csv('../../data/000002.csv')
data.index =data['date']
del data['date']
data.sort_index(ascending=True,inplace=True)
print(data.head(30))

data_benchmark = pd.read_csv('../../data/000300_index.csv')
data_benchmark.index =data_benchmark['date']
data_benchmark.sort_index(ascending=True,inplace=True)

df_ffill = data.reindex(data_benchmark['date'], method='ffill', fill_value=0.0)
print(df_ffill)