from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread,pyqtSignal

import os
import pandas as pd
from ..engine.tools import quandl
from ..engine.portfolio import Strategy
from ..engine import algos
from ..engine.technical.cross import *
from ..engine.technical.indicators import *
from ..engine.backtest import Backtest,BacktestRunner
from ..engine.consts import ShowTypes
from datetime import datetime
import traceback
import yaml

from ..engine.consts import *

class JobMgr(object):
    def __init__(self,logic):
        self.logic = logic

        self.file = os.path.dirname(os.path.abspath(__file__)) + '/config/stras.yaml'
        if os.path.exists(self.file):
            with open(self.file) as f:
                self.stras = yaml.load(f)
        else:
            self.stras = self.get_raw_stras()
            self.dump_to_file(self.stras)

        self.logic.signal.emit({'event_type':EventType.on_stras_changed})

    def dump_to_file(self,stras):
        with open(self.file,'w') as f:
            yaml.dump(stras,f)
        self.logic.signal.emit({'event_type': EventType.on_stras_changed})

    def get_stra_by_id(self,id):
        for stra in self.stras:
            if id == stra['job_id']:
                return stra
        return None

    def remove_stra(self,id):
        stra = self.get_stra_by_id(id)
        if stra:
            self.stras.remove(stra)
        self.dump_to_file(self.stras)

    def update_sert_stra(self,stra):
        if self.get_stra_by_id(stra['job_id']) is not None:
            self.remove_stra(stra['job_id'])
        self.stras.append(stra)
        self.dump_to_file(self.stras)
        return True

    def get_raw_stras(self):
        self.stras = [{
            'job_id': '1',
            'name': '海龟策略',
            'desc': '海龟策略',
            'pick_symbols': {
                'market':ShowTypes.market_us,
                'type': ShowTypes.pick_symbol_fixed,
                'universe': ['AAPL', 'AMZN']
            },
            'pick_time': {
                'long': 'cross_up(close,rolling_max(high,20))',
                'flat': 'cross_down(close,rolling_min(low,20))',
            },
            'alloc_funds': ShowTypes.alloc_funds_cash_equally
        },

            {
                'job_id': '2',
                'name': '均线突破',
                'desc': '均线突破',
                'pick_symbols': {
                    'market':ShowTypes.market_btc,
                    'type': ShowTypes.pick_symbol_fixed,
                    'universe': ['AAPL', 'AMZN']
                },
                'pick_time': {
                    'long': 'cross_up(close,ma(close,10))',
                    'flat': 'cross_down(close,ma(close,20))',
                },
                'alloc_funds': ShowTypes.alloc_funds_cash_equally
            },

        ]
        return self.stras


class LogicMgr(QThread):
    signal = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.jobmgr = JobMgr(self)

    def __prepare_data(self,params):
        start_dt = datetime.strptime(params['start'], '%Y-%m-%d')
        end_dt = datetime.strptime(params['end'], '%Y-%m-%d')

        year = start_dt.year
        year_end = end_dt.year

        years = list(range(year, year_end + 1))

        cur_path = os.path.abspath(__file__)
        father_path = os.path.abspath(os.path.dirname(cur_path) + os.path.sep + ".")
        father_path = os.path.abspath(os.path.dirname(father_path) + os.path.sep + ".")

        path = os.path.abspath(father_path + "/data")
        self.feed = quandl.build_feed("WIKI", params['universe'], years[0], years[-1], path)
        data = quandl.get_close_from_feed(self.feed)

        self.data = data.loc[params['start']:params['end']]

    def parse_stra(self,stra):
        algo_list = []

        sig = pd.DataFrame(index=self.data.index, columns=self.data.columns)

        for symbol in list(self.data.columns):
            close = self.data[symbol]
            high = self.feed[symbol]['High']
            low = self.feed[symbol]['Low']
            sig_long = eval(stra['pick_time']['long'])
            sig_flat = eval(stra['pick_time']['flat'])
            sig[symbol] = sig_long + sig_flat

        algo_list.append(algos.SelectWhere(signal=sig))


        if stra['alloc_funds'] == ShowTypes.alloc_funds_cash_equally:
            algo_list.append(algos.WeighEqually())

        algo_list.append(algos.Rebalance())
        s = Strategy(data=self.data, algos=algo_list)
        e = Backtest(stra['name'], strategy=s, data=self.data.copy())
        return e

    def run_stras(self,params):
        self.tasks= []
        self.__prepare_data(params)

        #回测基准
        s = Strategy(data=self.data, algos=[
            algos.RunOnce(),
            algos.SelectAll(),
            algos.WeighEqually(),
            algos.Rebalance()
        ])
        self.tasks.append(Backtest('基准', strategy=s, data=self.data.copy()))


        for id in params['stras']:
            job = self.jobmgr.get_stra_by_id(id)
            if job is None:
                continue
            engine = self.parse_stra(job)
            self.tasks.append(engine)

        self.run()

    def run(self):
        runner = BacktestRunner()
        runner.events.reg_handler(self.on_events)
        runner.run_backtests(self.tasks)

    def on_events(self,data):
        try:
            #pass
            self.signal.emit(data)
        except:
            traceback.print_exc()

