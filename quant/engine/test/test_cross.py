import unittest
import pandas as pd

from quant.engine.technical.cross import *
class TestCross(unittest.TestCase):
    def test_cross(self):
        data = pd.DataFrame(index=pd.date_range('2010-01-01', periods=5), columns=['AAPL', 'AMZN'])
        data['slow'] = [1.1,1.2,1.15,1.3,1.5]
        data['fast'] = [0.9,1.1,1.2,1.4,1.0]
        sig = cross_up(data['fast'],data['slow'])
        #print(sig)
        self.assertEqual(sig.iloc[2],1)
        sig_down = cross_down(data['fast'],data['slow'])
        #print(sig_down)
        self.assertEqual(sig_down.iloc[4],-1)


    def test_cross_eval(self):
        rule = 'cross_up(close,ma(close,2))'
        data = pd.DataFrame(index=pd.date_range('2010-01-01', periods=5), columns=['AAPL', 'AMZN'])
        #data['slow'] = [1.1, 1.2, 1.15, 1.3, 1.5]
        data['close'] = [0.9, 0.45, 1.0, 1.1, 1.2]


        close = data['close']

        sig = eval(rule)
        print(sig)