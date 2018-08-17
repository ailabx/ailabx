import unittest
from engine.feature_parser import FeatureCalc,extra_features
import pandas as pd

class TestFeatureParser(unittest.TestCase):
    def __test_extra_basic(self):
        a=1,
        b=2
        eval('a*b')
        items = ['rank(close_0 )', '(close_0+rank(pe_10,pe_20)/rank(pe_0+pe_1)', 'cross(ma_5_0,ma_10_0)', 'rank(close_0/pe_0)']
        basics = extra_features(items)
        print(basics)

    def __test_by_eval(self):
        df = pd.DataFrame({'cross': [1, 0, 0, 0, -1], 'code': ['600838', '600838', '600838', '600838', '600838'],
                           'close': [1.1, 1.2, 1.3, 1.4, 1.5], 'pe': [-1.11, -1.21, 1.31, 1.42, 1.51]},
                          index=pd.date_range(start='20100228', periods=5))

        basics = ['close_0', 'pe_0']
        items = ['rank(close_0)','close_0/rank(pe_0+pe_1)','cross(close_1,close_2)','rank(close_0/pe_0)']
        calc = FeatureCalc()

        df = calc.calc_basic_features(df,items)
        df = calc.calc_by_eval(df,items,calc.extra_basic_features(items))
        print(df)


    def test_feature_calc(self):
        calc = FeatureCalc()
        df = pd.DataFrame({'pe':[12,15,16,18,11],'close':[1.1,1.2,1.3,1.4,1.5]},index=pd.date_range('20180101',periods=5))
        items = ['close_5/close_0','close_10/close_0',
                    'close_20/close_0','rank(return_1)','rank(return_5)','rank(return_10)',
                   'rank(return_1)/rank(return_5)','rank(return_5)/rank(return_10)','pe_0']

        basic_features = calc.extra_basic_features(items)
        print(basic_features)
        df = calc.calc_basic_features(df,items)
        print(df)
        df = calc.calc_by_eval(df, items, basic_features)
        print(df)

