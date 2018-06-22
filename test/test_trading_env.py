import unittest
from engine.data import CSVDataFeed
from engine.trading_env import Trader

class TestTradingEnv(unittest.TestCase):
    def __test_csv_datafeed(self):
        feed = CSVDataFeed(csv='../data/000001_index.csv')
        obv,done = feed.step()
        print(type(obv),obv['close'])

    def test_trading_sim(self):
        port = Trader(period=252)
        port.update_first_step(action=2)
        self.assertEqual(port.costs[0],0.0003)
        self.assertEqual(port.positions[0],1)
        self.assertEqual(port.navs[0],1)
        self.assertEqual(port.mkt_navs[0],1)
        self.assertEqual(port.actions[0],2)
        self.assertEqual(port.mkt_returns[0],0)

        port.step+=1

        port.update_step(2,ret=0.1)
        self.assertEqual(port.costs[1], 0)
        self.assertEqual(port.positions[1],1)
        self.assertEqual(port.mkt_navs[1], 1.1)
        self.assertEqual(port.navs[1],1.0997)
        self.assertEqual(port.mkt_returns[1], 0.1)

        port.step+=1
        port.update_step(0,ret=0.1)
        self.assertEqual(port.costs[2],0.0006)
        self.assertEqual(port.positions[2],-1)
        self.assertAlmostEqual(port.mkt_navs[2], 1.21)
        self.assertAlmostEqual(port.navs[2],1.0997*1.1 -0)

        port.step += 1
        port.update_step(0, ret=0.1)
        self.assertEqual(port.costs[3], 0)
        self.assertEqual(port.positions[3], -1)
        self.assertAlmostEqual(port.mkt_navs[3], 1.331)
        self.assertAlmostEqual(port.navs[3], 1.20967 * (1-0.1-0.0006))

