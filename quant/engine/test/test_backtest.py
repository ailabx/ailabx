
import unittest
import pandas as pd
from datetime import datetime
from quant.engine.portfolio import Broker,Strategy
from quant.engine.backtest import Backtest,EventType,BacktestRunner
from quant.engine import algos
from quant.engine.common.logging_utils import logger
from quant.engine.tools import quandl
import os
import numpy as np
from quant.engine.technical import cross

#context{'instruments':['instrument1',...]}

class TestBacktest(unittest.TestCase):
    def __test_ranker(self):
        pass

    def test_run_stras(self):
        params = {'start': '2017-03-01', 'end': '2018-01-31',
                  'universe': ['AAPL', 'AMZN'],
                  'stras': ['1', '2']
                  }
        BacktestRunner().run_backtests(params)

    def __test_run(self):
        path = os.path.abspath(os.path.join(os.getcwd(), "../../data"))
        feed = quandl.build_feed("WIKI", ['AAPL','AMZN'], 2017, 2017, path)
        data = quandl.get_close_from_feed(feed)
        #data = pd.DataFrame(index=pd.date_range('2018-01-01', periods=10), columns=['AAPL', 'AMZN'])
        #data['AAPL'] = [1.1,1.3,1.15,0.9,1.22,1.1,1.3,1.15,0.9,1.22]
        #data['AMZN'] = [1.1, 1.3, 1.15, 0.9, 1.22, 1.1, 1.3, 1.15, 0.9, 1.22]
        s = Strategy(data=data,algos=[
            algos.RunOnce(),
            #algos.PrintDate(),
            algos.SelectAll(),
            algos.WeighEqually(),
            algos.Rebalance()
        ])

        sig = pd.DataFrame(index=data.index,columns=data.columns)

        for symbol in list(data.columns):
            max_high = max(feed[symbol]['High'],20)
            #print('sma====',sma5)
            sig[symbol] = cross.cross_up(feed[symbol]['High'],max_high)

        print(sig)


        s2 = Strategy(data=data, algos=[
            algos.SelectWhere(signal=sig),
            algos.WeighEqually(),
            algos.Rebalance()
        ])

        engine = Backtest('买入并持有AAPL,AMZN',strategy=s,data=data.copy())
        engine2 = Backtest('海龟策略', strategy=s2, data=data.copy())

        runner = BacktestRunner()
        runner.run_backtests([engine,engine2])
        #engine.startegy.plot()
