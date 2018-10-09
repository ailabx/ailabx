import unittest
import pandas as pd
import datetime

from quant.engine.portfolio import SymbolBroker,Portfolio
from quant.engine.algos import PrintDate

class TestPortfolio(unittest.TestCase):
    def __test_broker(self):

        data = pd.DataFrame(index=pd.date_range('2018-01-01',periods=10),columns=['AAPL','AMZN'],data=10)
        broker = SymbolBroker(code='AAPL',prices=data['AAPL'])

        #测试初始化
        print(broker.df)
        self.assertEqual(len(broker.df['price']),10)
        self.assertEqual(broker.code,'AAPL')

        #测试onbar
        broker.onbar()
        self.assertEqual(broker.now,datetime.datetime(2018,1,1))
        cash,commission = broker.adjust_to_target_shares(10)
        self.assertEqual(broker.idx,0)
        self.assertEqual(cash,-100)
        self.assertEqual(commission,100*0.0008)
        self.assertEqual(broker.get_item('position'),10)

        #print(broker.df)
        broker.onbar()
        cash, commission = broker.adjust_to_target_shares(100)
        self.assertEqual(broker.idx,1)
        self.assertEqual(cash, -900)
        self.assertEqual(commission, 900 * 0.0008)
        self.assertEqual(broker.now, datetime.datetime(2018, 1, 2))
        self.assertEqual(broker.get_item('position'), 100)
        print(broker.df)

        broker.onbar()
        cash, commission = broker.flat()
        self.assertEqual(broker.get_item('position'), 0)
        self.assertEqual(cash, 1000)
        self.assertEqual(commission, 1000 * 0.0008)
        self.assertEqual(broker.get_item('commission'), 100*broker.get_item('price')*0.0008)
        print(broker.df)

        broker.df['code'] = 'AAPL'
        broker.df['trade'] = broker.df['position'] - broker.df['position'].shift(1).fillna(0)
        print(broker.df)

    def test_portfolio(self):
        data = pd.DataFrame(index=pd.date_range('2018-01-01', periods=10), columns=['AAPL', 'AMZN'], data=10)
        s = Portfolio(data=data)
        self.assertEqual(len(s.brokers),2)

        s.step()
        s.step()
        s.step({'AAPL':10,'AMZN':10})
        s.step()
        done = False
        while not done:
            done = s.step()

        df,all = s.statistics()
        print(df)
        print(all)

    def __test_calc_returns(self):
        data = pd.DataFrame(index=pd.date_range('2018-01-01', periods=5), columns=['AAPL', 'AMZN'], data=10)
        s = Strategy(data=data, algos=[PrintDate()])
        s.df['total'] = [10.1,11.3,12.7,13.6,15.8]

        returns = s.get_returns()
        print(returns)
        self.assertEqual(15.8/13.6-1,returns[-1])

    def __test_get_reports(self):
        data = pd.DataFrame(index=pd.date_range('2018-01-01', periods=5), columns=['AAPL', 'AMZN'], data=10)
        s = Strategy(data=data, algos=[PrintDate()])
        s.df['total'] = [10.1, 11.3, 12.7, 13.6, 15.8]

        reports = s.get_reports()
        print(reports)



