import unittest
import pandas as pd
from quant.engine.backtest import Performance
from empyrical import stats

class TestPerformance(unittest.TestCase):
    def test_output(self):
        p = Performance()
        df = pd.DataFrame(index=pd.date_range('2010-01-01', periods=10), columns=['AAPL','AMZN'])
        df['AAPL'] = [0.1, 0.1, 0.1, -0.156, -0.1, 0.1, 0.1, 0.1, -0.11, -0.1]
        df['AMZN'] = [0.11, 0.1, 0.1, -0.156, -0.1, 0.1, 0.1, 0.1, -0.11, -0.1]
        ret = p.calc_performance(df)
        print(ret)


    def __test_returns(self):
        p = Performance()
        df = pd.DataFrame(index=pd.date_range('2010-01-01',periods=10),columns=['returns',])
        df['returns'] = [0.1,0.1,0.1,-0.156,-0.1,0.1,0.1,0.1,-0.11,-0.1]
        #print(df)
        r = df['returns']

        ret = p.calc_period_return(r)
        ret_annual = p.calc_annual_return(r)
        print(stats.cum_returns_final(r))

        #收益率
        self.assertEqual(ret,stats.cum_returns_final(r))
        self.assertEqual(ret_annual,stats.annual_return(r))

        #print('标准差-年化波动率',)
        #print(stats.annual_volatility(df['returns']))

        #波动率，夏普比
        self.assertEqual(p.calc_volatility(r),stats.annual_volatility(r))
        self.assertEqual(p.calc_sharpe(r), stats.sharpe_ratio(r))

        #self.assertEqual(p.calc_sortino(r),stats.annual_return(r))