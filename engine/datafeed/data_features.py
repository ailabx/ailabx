from engine.common.mongo_utils import mongo
import numpy as np
import pandas as pd
from datetime import datetime

def parse_feature(df,feature):
    features_support = ['return']

    if '_' in feature:
        feature_name =  feature[:feature.index('_')]
        param = int(feature[feature.index('_')+1:])

    else:
        feature_name = feature
        param = 0


    if feature_name not in features_support:
        return df

    if feature_name == 'return':
        df[feature] = df['close'] /df['close'].shift(param+1) -1
    return df

def feature_extractor(instrument,features,start_date='',end_date='',benchmark='000300_index'):
    items = mongo.query_docs('astock_daily_quotes',{'code':instrument,
                                            'date':{'$gt':start_date,'$lt':end_date}},
                             )

    df = pd.DataFrame(list(items))
    df = df[['open','high','low','close','date','code']]
    df.index = df['date']
    df.sort_index(inplace=True)
    del df['date']

    for feature in features:
        df = parse_feature(df,feature)
    return df

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
    end = datetime(2017,1,31)
    df = feature_extractor('600519',features,start_date=start,end_date=end)
    df = auto_labeler(df,'return',5)
    print(df.head(10))