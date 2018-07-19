import unittest
from ..datafeed import *
from datetime import datetime

class TestDataFeed(unittest.TestCase):
    def test_feature_parser(self):
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
        features = ['close_5','return_20','ma_5','ma_10','cross(ma_5,ma_10)']
        all_dfs = D.load_data_with_features(instruments=['600519',],
                                            features=features,start_date=start,end_date=end)
        df = all_dfs['600519']
        print(df.tail(20))