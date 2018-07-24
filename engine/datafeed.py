from .common.mongo_utils import mongo
import pandas as pd
import re
import talib
import numpy as np
import requests
import json
from datetime import datetime

class FeatureParser(object):
    def __init__(self,df):
        self.df = df
        self.features_support={
            'return':self._parse_return,
            'close':self._parse_close,
            'ma':self._parse_ma,
            #'cross':self._parse_cross,
        }
    def _parse_cross(self,args):
        pass

    def _parse_ma(self,arg):
        close = self.df['close']
        return talib.EMA(np.array(close), timeperiod=arg)

    def _parse_close(self,arg):
        return self.df['close'].shift(arg)

    def _parse_return(self,arg):
        close = self.df['close']
        return close / close.shift(arg) - 1

    #==============================
    def _parse_func(self,feature):
        #cross(ma_5,ma_10)这种格式
        pattern = '(.*?)\((.*?),(.*?)\)'
        ret = re.search(pattern, feature)
        if ret and len(ret.groups()) == 3:
            return ret.groups()[0], ret.groups()[1], ret.groups()[2]
        return None

    def _parse_arg(self,feature):
        # return_20这种格式
        pattern = '(.*?)_(\d+)'
        ret = re.search(pattern, feature)
        if ret and len(ret.groups()) == 2:
            return ret.groups()[0], int(ret.groups()[1])
        return None


    def parse_feature(self,feature):
        rets = self._parse_func(feature)
        if not rets:
            rets = self._parse_arg(feature)
        return rets


    def parse_all_features(self,features):
        for feature in features:
            rets = self.parse_feature(feature)
            if rets is not None and rets[0] in self.features_support.keys():
                self.df[feature] =self.features_support[rets[0]](rets[1])

        return self.df

class DataFeed(object):
    def __init__(self):
        self.idx = 0

    def get_benchmark_index(self):
        return self.all_dfs[self.benchmark].index

    def get_benchmark_return(self):
        return self.all_dfs[self.benchmark]['return_0']

    #往前走一步，如果超过范围返回done
    def step(self):
        bars = {}
        for instrument in self.all_dfs.keys():
            bars[instrument] = self.all_dfs[instrument].iloc[self.idx]
        self.idx += 1
        done = self.idx >= len(self.all_dfs[self.benchmark])
        return bars, done

    def calc_features(self,df,features):
        parser = FeatureParser(df=df)
        return parser.parse_all_features(features=features)

    def auto_label(self,df,hold_days=5):
        return_hold = 'return_hold'
        df[return_hold] = (df['close'].shift(hold_days) / df['close'] - 1) * 100

        label_name = return_hold
        # df[return_hold]= df[return_hold].dropna()
        rank20 = df[label_name].quantile(0.2)
        rank40 = df[label_name].quantile(0.4)
        rank60 = df[label_name].quantile(0.6)
        rank80 = df[label_name].quantile(0.8)
        df['label'] = np.where(df[label_name] < rank20, 0, None)
        df['label'] = np.where(df[label_name] > rank20, 1, df['label'])
        df['label'] = np.where(df[label_name] > rank40, 2, df['label'])
        df['label'] = np.where(df[label_name] > rank60, 3, df['label'])
        df['label'] = np.where(df[label_name] > rank80, 4, df['label'])
        return df

    #加载所有instruments的数据
    def load_datas(self,instruments,features, start_date, end_date, benchmark='000300_index'):
        self.all_dfs = {}
        self.all_dfs[benchmark] = self._load_data(benchmark,start_date,end_date)

        for instrument in instruments:
            df = self._load_data(instrument,start_date,end_date)
            df = self.calc_features(df,features)
            df = self.auto_label(df)
            self.all_dfs[instrument] = df
        return self.all_dfs

    def _load_data(self,instrument,start_date,end_date):
        #items = mongo.query_docs('astock_daily_quotes', {'code': instrument,
        #                                                 'date': {'$gt': start_date, '$lt': end_date}},
        #                         )

        url = 'http://ailabx.com/kensho/quotes?code=600519&start={}&end={}'.format(
            start_date.strftime('%Y%m%d'),
            end_date.strftime('%Y%m%d')
        )

        json_data = requests.get(url).json()
        data = json.loads(json_data['data'])
        df = pd.DataFrame(data)
        #print(df)
        #if '_index' not in instrument:
        #    df = df[['open', 'high', 'low', 'close', 'date', 'code', 'volume','factor']]
        #else:
        #    df = df[['open', 'high', 'low', 'close', 'date', 'code', 'volume']]


        df.index = df['date']
        df.sort_index(inplace=True)
        del df['date']
        return df

D = DataFeed()