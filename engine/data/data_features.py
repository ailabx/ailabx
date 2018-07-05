from engine.common.mongo_utils import mongo
from engine.common.talib_utils import TalibHelper
import numpy as np
import pandas as pd
from datetime import datetime




#自动标注数据
def auto_labeler(df,label,hold_days):
    label_name = ''
    if label == 'return':
        label_name = 'label_return_'+str(hold_days)
        df[label_name] = df['close'].shift(-hold_days)/df['close']  - 1

    rank20 = df[label_name].quantile(0.2)
    rank40 = df[label_name].quantile(0.4)
    rank60 = df[label_name].quantile(0.6)
    rank80 = df[label_name].quantile(0.8)
    df['label'] = np.where(df[label_name]<rank20,0,None)
    df['label'] = np.where(df[label_name] > rank20, 1, df['label'])
    df['label'] = np.where(df[label_name] > rank40, 2, df['label'])
    df['label'] = np.where(df[label_name] > rank60, 3, df['label'])
    df['label'] = np.where(df[label_name] > rank80, 4, df['label'])
    return df

if __name__ == '__main__':
    instruments = ['600519','000858']
    features = ['return_0','return_4']
    start = datetime(2017,1,1)
    end = datetime(2017,6,30)
    ta= TalibHelper()

    df = feature_extractor('600519',features,start_date=start,end_date=end)
    df['ta_MA5'] = ta.MA(df['close'],5)
    df['ta_EMA6'] = ta.EMA(df['close'],6)
    df['pd_MA5'] =  df['close'].rolling(5).mean()
    df['MACD'],df['MACD_SIGNAL'],df['MACD_HIST'] = ta.MACD(df['close'])

    df = auto_labeler(df,'return',5)
    print(df.tail(50))