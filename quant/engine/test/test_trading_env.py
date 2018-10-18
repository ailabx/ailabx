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
        feed.download_or_get_data(['AAPL', 'AMZN'], 2006, 2006)
        env = TradingEnv(feed)
        buy_and_hold = Strategy([
            RunOnce(),
            PrintBar(),
            SelectAll(),
            WeighEqually(),
        ])
        env.run_strategy(strategy=buy_and_hold)