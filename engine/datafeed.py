from .common.mongo_utils import mongo
import pandas as pd

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

        print(self.all_dfs)

    def _load_data(self,instrument):
        items = mongo.query_docs('astock_daily_quotes', {'code': instrument,
                                                         'date': {'$gt': self.start_date, '$lt': self.end_date}},
                                 )

        df = pd.DataFrame(list(items))
        df = df[['open', 'high', 'low', 'close', 'date', 'code']]
        df.index = df['date']
        df.sort_index(inplace=True)
        del df['date']

        df = self._parse_fetures(df,self.features)
        return df

    def _parse_fetures(self,df,features):
        for feature in features:
            df = self._parse_feature(df, feature)
        return df

    def _parse_feature(self,df, feature):
        features_support = ['return']

        if '_' in feature:
            feature_name = feature[:feature.index('_')]
            param = int(feature[feature.index('_') + 1:])

        else:
            feature_name = feature
            param = 0

        if feature_name not in features_support:
            return df

        if feature_name == 'return':
            df[feature] = df['close'] / df['close'].shift(param + 1) - 1
        return df

D = DataFeed()