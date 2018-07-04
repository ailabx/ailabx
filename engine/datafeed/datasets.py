import pandas as pd
import os
def get_data():
    train = pd.read_csv('D:/devgit/ailabx/engine/datafeed/train_modified.csv')
    print(train.head())
    print(train['Disbursed'].value_counts())

    target = 'Disbursed'  # Disbursed的值就是二元分类的输出
    IDcol = 'ID'
    x_columns = [x for x in train.columns if x not in [target, IDcol]]
    X = train[x_columns]
    y = train['Disbursed']
    return X,y