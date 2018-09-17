import unittest
import pandas as pd
import datetime

from quant.engine.portfolio import Broker,Strategy
from quant.engine.algos import PrintDate

class TestBroker(unittest.TestCase):
    def test_broker(self):

        data = pd.DataFrame(index=pd.date_range('2018-01-01',periods=10),columns=['AAPL','AMZN'],data=10)
        broker = Broker(name='AAPL',prices=data['AAPL'])

        #测试初始化
        #print(broker.df)
        self.assertEqual(len(broker.df['price']),10)
        self.assertEqual(broker.name,'AAPL')

        #测试onbar
        broker.onbar()
        self.assertEqual(broker.now,datetime.datetime(2018,1,1))
        broker.adjust(100)
        self.assertEqual(broker.idx,0)
        self.assertEqual(broker.get_item('position'),10)

        #print(broker.df)
        broker.onbar()
        broker.adjust(1000)
        self.assertEqual(broker.idx,1)
        self.assertEqual(broker.now, datetime.datetime(2018, 1, 2))
        self.assertEqual(broker.get_item('position'), 100)
        print(broker.df)

        broker.onbar()
        broker.flat()
        self.assertEqual(broker.get_item('position'), 0)
        self.assertEqual(broker.get_item('commission'), 100*broker.get_item('price')*0.0008)
        print(broker.df)

        broker.df['code'] = 'AAPL'
        broker.df['trade'] = broker.df['position'] - broker.df['position'].shift(1).fillna(0)
        print(broker.df)

    def test_brokers(self):
        data = pd.DataFrame(index=pd.date_range('2018-01-01', periods=10), columns=['AAPL', 'AMZN'], data=10)
        s = Strategy(data=data,algos=[PrintDate()])
        self.assertEqual(len(s.brokers),2)

        s.onbar()
        s.onbar()
        s.rebalance({'AAPL':0.5,'AMZN':0.5})
        s.onbar()
        #print(s.df)
        #for symbol,broker in s.brokers.items():
            #print(broker.df)

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



