import unittest
from ..datafeed import *
from datetime import datetime

class TestDataFeed(unittest.TestCase):
    def __test_feature_parser(self):
        parser = FeatureParser(df=None)
        feature,arg = parser.parse_feature('return_5')
        self.assertEqual(feature,'return')
        self.assertEqual(arg,5)

        feature, arg = parser.parse_feature('close_5')
        self.assertEqual(feature, 'close')
        self.assertEqual(arg, 5)

        rets = parser.parse_feature('close5')
        self.assertEqual(rets, None)

        func,arg1,arg2 = parser.parse_feature('cross(ma_5,ma_10)')
        self.assertEqual(func,'cross')
        self.assertEqual(arg1,'ma_5')
        self.assertEqual(arg2,'ma_10')
        #self.assertEqual(arg, 5)

    def test_load_data(self):
        start = datetime(2016,1,1)
        end = datetime(2017,1,1)
        df = D._load_data('600519',start,end)
        print(df.tail())

        features = ['close_5', 'return_20', 'ma_5', 'ma_10']
        df = D.calc_features(df,features)
        print(df.tail())

        df = D.auto_label(df)
        print(df.tail())


        dfs = D.load_datas(['600519','601318'],features,start,end)




