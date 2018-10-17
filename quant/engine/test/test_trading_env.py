'''
@author: 魏佳斌
@license: (C) Copyright 2018-2025, ailabx.com.

@contact: 86820609@qq.com
@file: test_trading_env.py
@time: 2018-10-17 10:29
@desc:

'''
import unittest
from quant.engine.trading_env import TradingEnv
class TestTradingEnv(unittest.TestCase):
    def test_run_step(self):
        env = TradingEnv()