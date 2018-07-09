import pandas as pd
from pandas import Series,DataFrame
#http://wiki.jikexueyuan.com/project/start-learning-python/311.html
def test():
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

def test_series():
    se = Series(['hello','pandas',2018])
    print(se)
    print('Series的values：',type(se.values),se.values)
    print('Series的index：',type(se.index),se.index)

    se = Series([1,2,3,4,5],index=['a','b','c',1,2])
    print(se)
    print(se.index)

if __name__ == '__main__':
    test_series()
