from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread,pyqtSignal

import os
import pandas as pd
from ..engine.tools import quandl
from ..engine.portfolio import Strategy
from ..engine import algos
from ..engine.technical.cross import *
from ..engine.backtest import Backtest,BacktestRunner
from datetime import datetime
import traceback

from ..engine.consts import *

class ThreadWorker(QThread):
    signal = pyqtSignal()
    def __init__(self,func=None):
        super().__init__()
        self.func =  func

    def run(self):
        # 进行任务操作
        if self.func:
            self.func()
        i = 0
        while i < 10:
            self.signal.emit()  # 发射信号
            i += 1


class LogicMgr(QThread):
    signal = pyqtSignal(dict)

    def run(self):

        params = {'start':'2017-03-01','end':'2018-01-31',
                  'universe':['AAPL','AMZN'],
                  'long':'cross_up(close,ma(close,15))',
                  'flat':'cross_down(close,ma(close,20))'
                  }
        start_dt = datetime.strptime(params['start'],'%Y-%m-%d')
        end_dt = datetime.strptime(params['end'],'%Y-%m-%d')

        year = start_dt.year
        year_end = end_dt.year

        years = list(range(year,year_end+1))

        cur_path = os.path.abspath(__file__)
        father_path = os.path.abspath(os.path.dirname(cur_path) + os.path.sep + ".")
        father_path = os.path.abspath(os.path.dirname(father_path) + os.path.sep + ".")

        path = os.path.abspath(father_path+"/data")
        feed = quandl.build_feed("WIKI", params['universe'], years[0], years[-1], path)
        data = quandl.get_close_from_feed(feed)

        data = data.loc[params['start']:params['end']]

        s = Strategy(data=data, algos=[
            algos.RunOnce(),
            algos.SelectAll(),
            algos.WeighEqually(),
            algos.Rebalance()
        ])

        sig = pd.DataFrame(index=data.index, columns=data.columns)


        for symbol in list(data.columns):
            close = data[symbol]
            sig_long = eval(params['long'])
            sig_flat = eval(params['flat'])
            sig[symbol] = sig_long+sig_flat

        print(sig)

        s2 = Strategy(data=data, algos=[
            algos.SelectWhere(signal=sig),
            algos.WeighEqually(),
            algos.Rebalance()
        ])

        engine = Backtest('买入并持有AAPL,AMZN', strategy=s, data=data.copy())
        engine2 = Backtest('价格突破10日均线信号突破', strategy=s2, data=data.copy())

        runner = BacktestRunner()
        runner.events.reg_handler(self.on_events)
        runner.run_backtests([engine, engine2])

    def on_events(self,data):
        print('data',data)
        try:
            #pass
            self.signal.emit(data)
        except:
            traceback.print_exc()
