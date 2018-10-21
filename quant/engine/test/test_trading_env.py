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
        ],name='买入并持有-基准策略')

        long_expr = 'cross_up(ma(close,5),ma(close,10))'
        flat_expr = 'cross_down(ma(close,5),ma(close,10))'
        ma_cross = Strategy([
            SelectByExpr(long_expr=long_expr,flat_expr=flat_expr),
            WeighEqually(),
        ],name='均线交叉策略')

        env_benchmark = TradingEnv(strategy=buy_and_hold,feed=feed)
        env_benchmark.run_strategy()

        env = TradingEnv(strategy=ma_cross,feed=feed)
        env.run_strategy()

        bench_stats = env_benchmark.get_statistics()
        stra_stats = env.get_statistics()

        stats = [bench_stats,stra_stats]

        from quant.engine.trading_env import EnvUtils

        utils =EnvUtils(stats=stats)
        utils.show_stats()

