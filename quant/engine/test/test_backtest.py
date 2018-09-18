
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
        instruments = ['600519', '000858','rank_return_0/rank_return_5']
        features = ['rank_pe_0']
        start = datetime(2017, 1, 1)
        end = datetime(2018, 1, 30)
        features_name = [feature.replace('/','_') for feature in features]
        dfs = D.load_datas(instruments, start, end,features=features)
        #df = dfs['600519']
        #df = df.dropna(axis=0, how='any', thresh=None)
        print(dfs.tail())

        ranker = SymbolRanker()
        train,test = ranker.split_datasets(dfs[features_name],dfs['label'])
        print(len(train[0]),len(test[0]))

        print(train[0].tail())
        print(train[1].tail())

        ranker.train(train[0][features_name],train[1].astype('int'))

    def onfinished(self,s):
        logger.info('回测任务完成！')
        df = s.backtests[0].get_reports()
        df['date'] = df.index
        print(df)
        groups = df.groupby(df['date'])
        for name,group in groups:
            item = group[group['trade']>0]
            if len(item):
                print('交易：',item)
        #df.groupby(df[])
        #logger.info(s.get_returns())
    def onbar(self,s):
        pass
        #logger.info('--------------------onbar')


    def test_run(self):
        path = os.path.abspath(os.path.join(os.getcwd(), "../../data"))
        data = quandl.build_feed("WIKI", ['AAPL','AMZN'], 2017, 2017, path)
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
            sma5 = data[symbol].rolling(10).mean()
            print('sma====',sma5)
            sig[symbol] = cross.cross(data[symbol],sma5)

        print(sig)


        s2 = Strategy(data=data, algos=[
            algos.SelectWhere(signal=sig),
            algos.WeighEqually(),
            algos.Rebalance()
        ])

        engine = Backtest('买入并持有AAPL,AMZN',strategy=s,data=data.copy())
        engine2 = Backtest('价格突破10日均线信号突破', strategy=s2, data=data.copy())

        runner = BacktestRunner()
        runner.run_backtests([engine,engine2])
        #engine.startegy.plot()
