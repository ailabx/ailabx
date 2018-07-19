from .common.mongo_utils import mongo
import pandas as pd
import re
import talib
import numpy as np

class FeatureParser(object):
    def __init__(self,df):
        self.df = df
        self.features_support={
            'return':self._parse_return,
            'close':self._parse_close,
            'ma':self._parse_ma,
            'cross':self._parse_cross,
        }
    def _parse_cross(self,args):
        para1 = args[0],
        para2 = args[1]

        diff = self.df[para1] - self.df[para2]
        diff_lag =  diff.shift(1)
        diff>=0 and diff_lag<0

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

    #加载所有instruments的数据
    def load_data_with_features(self,instruments,features, start_date, end_date, benchmark='000300_index'):
        self.instruments = instruments
        self.features = features
        self.start_date = start_date
        self.end_date = end_date
        self.benchmark = benchmark

        self.all_dfs = {}

        self.all_dfs[self.benchmark] = self._load_data(self.benchmark)

        for instrument in instruments:
            df = self._load_data(instrument)
            self.all_dfs[instrument] = df

        return self.all_dfs

    def _load_data(self,instrument):
        items = mongo.query_docs('astock_daily_quotes', {'code': instrument,
                                                         'date': {'$gt': self.start_date, '$lt': self.end_date}},
                                 )

        df = pd.DataFrame(list(items))
        df = df[['open', 'high', 'low', 'close', 'date', 'code']]
        df.index = df['date']
        df.sort_index(inplace=True)
        del df['date']

        parser = FeatureParser(df=df)
        parser.parse_all_features(features=self.features)
        return df




D = DataFeed()