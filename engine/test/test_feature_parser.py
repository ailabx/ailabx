import unittest
from engine.feature_parser import FeatureCalc
import pandas as pd

class TestFeatureParser(unittest.TestCase):


    def test_feature_calc(self):
        calc = FeatureCalc()
        df = pd.DataFrame({'pe':[12,15,16,18,11],'close':[1.1,1.2,1.3,1.4,1.5]},index=pd.date_range('20180101',periods=5))
        items = ['close_5/close_0','close_10/close_0',
                    'close_20/close_0','rank_return_1','rank_return_5','rank_return_10',
                   'rank_return_1/rank_return_5','rank_return_5/rank_return_10','pe_0']

        basic_features = calc.extra_basic_features(items)
        print(basic_features)
        df = calc.calc_basic_features(df,basic_features)


        df = calc.calc_func(df,items)
        df = calc.calc_operators(df, items)
        print(df)
