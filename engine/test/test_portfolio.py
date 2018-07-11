import unittest
from engine.portfolio import Trader,Portfolio

class TestPortfolio(unittest.TestCase):
    def test_portfolio(self):
        port = Portfolio(indexes=['2018-01-01','2018-01-02','2018-01-03'])
        print(port.df_portfolio)

        status = {'LONG':['600519']}
        bars = {'600519':{'close':28.88}}
        port.step(status,bars)
        port.step(status,bars)

        print(port.df_portfolio)


    def __test_trader(self):
        trader = Trader(indexes=['2018-01-01','2018-01-02','2018-01-03'])
        print(trader.df)

        #第0期，做多1手，收盘价为28.88
        bar = {'close': 28.88}
        trader.step(bar)
        cash = trader.long_or_short(100,1,bar)
        self.assertEqual(cash,2888*(1+0.0003))

        #移动第1期
        bar ={'close':31.88}
        trader.step(bar)
        print(trader.df)

        #第2期平仓
        trader.step({'close':36.88})
        cash = trader.flat({'close':36.88})
        print(trader.df)
        self.assertAlmostEqual(cash,3688*(1-0.0003))
        self.assertAlmostEqual(trader.get_commission(),3688*0.0003)