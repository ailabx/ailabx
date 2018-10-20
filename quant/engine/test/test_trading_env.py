'''
@author: 魏佳斌
@license: (C) Copyright 2018-2025, ailabx.com.

@contact: 86820609@qq.com
@file: test_trading_env.py
@time: 2018-10-17 10:29
@desc:

'''
import unittest,os
from quant.engine.trading_env import TradingEnv
from quant.engine.datafeed import DataFeed
from quant.engine.algos import *


class TestTradingEnv(unittest.TestCase):
    def test_run_step(self):
        path = os.path.abspath(os.path.join(os.getcwd(), "../../data"))
        feed = DataFeed(data_path=path)
        feed.download_or_get_data(['AAPL',], 2006, 2006)

        buy_and_hold = Strategy([
            RunOnce(),
            PrintBar(),
            SelectAll(),
            WeighEqually(),
        ])

        long_expr = 'cross_up(ma(close,5),ma(close,10))'
        flat_expr = 'cross_down(ma(close,5),ma(close,10))'
        ma_cross = Strategy([
            SelectByExpr(long_expr=long_expr,flat_expr=flat_expr),
            WeighEqually(),
        ])

        env_benchmark = TradingEnv(strategy=buy_and_hold,feed=feed)
        env_benchmark.run_strategy()

        print('回测结果：')
        ret = env_benchmark.get_statistics()
        print('收益率:{},年化收益率:{}'.format(ret['period_returns'],ret['annual_returns']))

        env_benchmark.plot()

