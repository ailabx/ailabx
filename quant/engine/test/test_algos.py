import unittest
import pandas as pd
import numpy as np
from quant.engine import algos
from quant.engine.trading_env import TradingEnv
from datetime import datetime

class TestAlgos(unittest.TestCase):
    def test_selectbyexpr(self):
        aapl = pd.DataFrame(index=pd.date_range('2018-01-01', periods=10), columns=['Open', 'High','Low','Close'])
        aapl['Close'] = [3,1,2,1,4,1.1,1.3,1.15,0.9,1.22]

        amzn = pd.DataFrame(index=pd.date_range('2018-01-01', periods=10), columns=['Open', 'High', 'Low', 'Close'])
        amzn['Close'] = [3,1,2,1,4, 1.1, 1.3, 1.15, 0.9, 1.22]

        all_data = {'AAPL':aapl,'AMZN':amzn}

        all_close = pd.DataFrame(index=pd.date_range('2018-01-01', periods=10), columns=['AAPL', 'AMZN'])
        all_close['AAPL'] = [3,1,2,1,4, 1.1, 1.3, 1.15, 0.9, 1.22]
        all_close['AMZN'] = [3,1,2,1,4, 1.1, 1.3, 1.15, 0.9, 1.22]

        long_expr = 'cross_up(ma(close,2),ma(close,4))'
        flat_expr = 'cross_down(ma(close,2),ma(close,4))'
        algo = algos.SelectByExpr(long_expr=long_expr,flat_expr=flat_expr)
        context = {
            'universe':['AAPL','AMZN'],
            'all_close':all_close,
            'all_data':all_data,
            'now': datetime(2018, 1, 5)
        }
        algo(context)
        print(context['sig'])
        self.assertEqual('AAPL' in context['LONG'], True)
        self.assertEqual('AMZN' in context['LONG'], True)

    def __test_selectwhere(self):
        data = pd.DataFrame(index=pd.date_range('2010-01-01', periods=5), columns=['AAPL', 'AMZN'])
        data['AAPL'] = 10
        data['AMZN'] = 20

        sig = pd.DataFrame(index=pd.date_range('2010-01-01',periods=5),columns=['AAPL','AMZN'])
        sig['AAPL'] = [1,0,0,0,-1]
        sig['AMZN'] = [0,0,1,-1,0]
        algo = algos.SelectWhere(signal=sig)
        context = {'now':datetime(2010,1,1)}
        algo(context)
        self.assertEqual('AAPL' in context['LONG'],True)


    def __cross(self,fast,slow):
        data = pd.DataFrame(index=fast.index)
        data['signal'] = fast - slow#data[fast] - data[slow]
        data['signal'] = np.where(data['signal']>0,1,data['signal'])
        data['signal'] = np.where(data['signal']<0,-1,data['signal'])

        data['signal'] = data['signal'] - data['signal'].shift(1)
        data['signal'] = np.where(data['signal']>0,1,data['signal'])
        data['signal'] = np.where(data['signal']<0,-1,data['signal'])
        return data['signal']

    def __test_signal(self):
        data = pd.DataFrame(index=pd.date_range('2018-01-01', periods=10), columns=['AAPL', 'AMZN'])
        data['AAPL'] = [1.1,1.3,1.15,0.9,1.22,1.1,1.3,1.15,0.9,1.22]
        data['AMZN'] = [1.1, 1.3, 1.15, 0.9, 1.22, 1.1, 1.3, 1.15, 0.9, 1.22]

        sma2 = data['AMZN'].rolling(2).mean()

        print(data)

        sig = self.cross(data['AMZN'],sma2)
        print(sig)