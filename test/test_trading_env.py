import unittest
from engine.trading_env import CSVDataFeed,TradingSim

class TestTradingEnv(unittest.TestCase):
    def test_csv_datafeed(self):
        feed = CSVDataFeed(csv='../data/000001_index.csv')
        obv,done = feed.step()
        print(type(obv),obv['close'])

    def test_trading_sim(self):
        sim = TradingSim(steps=252)
        sim.do_step(action=2,retrn=0.1)