import unittest
from ..technical.indicators import *
import pandas as pd

class TestIndicators(unittest.TestCase):
    def test_indicator(self):
        #df = pd.DataFrame(index=pd.date_range('2010-01-01',periods=10),columns=['close'])
        #df['close'] = list(range(10))
        df = pd.read_csv('D:/devgit/ailabx/quant/engine/test/TsingTao.csv')

        df['sma'] = ma(df['Close'],5)
        df['ema'] = ema(df['Close'],5)
        df['macd'],df['macd_sig'],df['macd_hist'] = macd(df['Close'])
        df['rsi'] = rsi(df['Close'],n=12)
        df['obv'] = obv(df['Close'],df['Volume'],9)
        df['mom'] = mom(df['Close'],n=9)
        df['b_upper'],df['b_middle'],df['b_lower'] =bbands(df['Close'],n=20)
        print(df.head())
        print(df.tail())