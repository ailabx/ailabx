import unittest
from ..datafeed import *
from datetime import datetime

class TestDataFeed(unittest.TestCase):

    def __test_fetch_data(self):
        start_date = datetime(2010,1,1)
        end_date = datetime(2011,1,1)
        url = 'http://ailabx.com/kensho/quotes?code={}&start={}&end={}'.format(
            '600838,600519,000002',
            start_date.strftime('%Y%m%d'),
            end_date.strftime('%Y%m%d')
        )
        df = D.fetch_data(url)
        print(df.head())

        #加载maindata基本面数据
        url = 'http://www.ailabx.com/kensho/maindata?code={}&start={}&end={}'.format(
            '600519',
            start_date.strftime('%Y%m%d'),
            end_date.strftime('%Y%m%d')
        )
        df = D.fetch_data(url)
        print(df)

    def test_load_datas(self):
        start_date = datetime(2001, 12, 29)
        end_date = datetime(2011, 1, 1)
        df = D.load_datas(['600838','600519','000002'],start_date,end_date)
        print(df.head())

    def __test_instruments(self):
        start = datetime(2010, 1, 1)
        end = datetime(2017, 7, 19)
        instruments = D.instruments(start,end)
        print(len(instruments),instruments[:10])

    def __test_extra_func(self):
        feature = 'rank_pe_5'
        parser = FeatureParser(df=None)
        funcs,feature = parser.extra_func(feature)
        print(funcs,feature)

    def __test_extra_features(self):
        feature = ['return_5','avg_amount_5','rank_avg_amount_5_20_60','amount_5 * amount_20']
        parser = FeatureParser(df=None)
        features = parser.extra_features(feature)
        self.assertEqual('return_5',features[0])
        self.assertEqual('amount_5',features[1])
        self.assertEqual('amount_5_20_60',features[2])
        print(features)



    def __test_feature_parser(self):
        print('test_feature_parser...')
        parser = FeatureParser(df=None)
        funcs,args = parser.parse_feature('return_5')
        self.assertEqual(funcs[0],'return')
        self.assertEqual(args[0],5)

        funcs, args = parser.parse_feature('pe_0')
        self.assertEqual(funcs[0], 'pe')
        self.assertEqual(args[0], 0)

        funcs,args = parser.parse_feature('close5')
        self.assertEqual(funcs[0], 'close5')
        self.assertEqual(len(args),0)

        funcs,args = parser.parse_feature('rank_avg_return_20')
        self.assertEqual(funcs[0],'rank')
        self.assertEqual(funcs[1],'avg')
        self.assertEqual(funcs[2],'return')
        self.assertEqual(args[0], 20)

    def __test_fundamentals(self):
        start = datetime(2016, 1, 1)
        end = datetime(2017, 1, 1)

        df = D.fundamentals('600519',start,end)
        print(df)

    def __test_fundamentals_quotes(self):
        start = datetime(2016, 1, 1)
        end = datetime(2017, 1, 1)

        df = D.fundamentals('600519', start, end)
        #print(df)

        df_quotes = D._load_data('600519',start,end)
        print(df_quotes)

    def __test_load_data(self):
        start = datetime(2016,1,1)
        end = datetime(2017,1,1)
        df = D._load_data('600519',start,end)
        print(df.tail())

        features = ['open_10/close_20','amount_10','avg_amount_20','rank_pe_0']
        df = D.calc_features(df,features)
        print(df.tail())

        #df = D.auto_label(df)
        #print(df.tail(20))
        #dfs = D.load_datas(['600519','601318'],features,start,end)
