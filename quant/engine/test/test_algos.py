import unittest
import pandas as pd
import numpy as np
from quant.engine import algos,portfolio

class TestAlgos(unittest.TestCase):
    def test_selectwhere(self):
        data = pd.DataFrame(index=pd.date_range('2010-01-01', periods=5), columns=['AAPL', 'AMZN'])
        data['AAPL'] = 10
        data['AMZN'] = 20
        s = portfolio.Strategy(data=data)
        s.onbar()

        sig = pd.DataFrame(index=pd.date_range('2010-01-01',periods=5),columns=['AAPL','AMZN'])
        sig['AAPL'] = [1,0,0,0,-1]
        sig['AMZN'] = [0,0,1,-1,0]
        algo = algos.SelectWhere(signal=sig)

        algo(s)
        self.assertEqual('AAPL' in s.context['LONG'],True)

    def cross(self,fast,slow):
        data = pd.DataFrame(index=fast.index)
        data['signal'] = fast - slow#data[fast] - data[slow]
        data['signal'] = np.where(data['signal']>0,1,data['signal'])
        data['signal'] = np.where(data['signal']<0,-1,data['signal'])

        data['signal'] = data['signal'] - data['signal'].shift(1)
        data['signal'] = np.where(data['signal']>0,1,data['signal'])
        data['signal'] = np.where(data['signal']<0,-1,data['signal'])
        return data['signal']

    def test_signal(self):
        data = pd.DataFrame(index=pd.date_range('2018-01-01', periods=10), columns=['AAPL', 'AMZN'])
        data['AAPL'] = [1.1,1.3,1.15,0.9,1.22,1.1,1.3,1.15,0.9,1.22]
        data['AMZN'] = [1.1, 1.3, 1.15, 0.9, 1.22, 1.1, 1.3, 1.15, 0.9, 1.22]

        sma2 = data['AMZN'].rolling(2).mean()

        print(data)

        sig = self.cross(data['AMZN'],sma2)
        print(sig)