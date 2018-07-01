from engine.common.mongo_utils import mongo
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

    print(feature_name, param)

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


if __name__ == '__main__':
    instruments = ['600519','000858']
    features = ['return_0','return_4']
    start = datetime(2017,1,1)
    end = datetime(2017,1,31)
    print(feature_extractor('600519',features,start_date=start,end_date=end))