from .portfolio import Portfolio
from empyrical import stats

class Performance(object):
    def __init__(self):
        pass

    def calc(self,df):
        print('计算绩效')
        df['equity'] = (df['returns'] + 1).cumprod()
        df['bench_equity'] = (df['bench_returns'] + 1).cumprod()

        self.period_return = df['equity'][-1] -1
        self.benchmark_return = df['bench_equity'][-1] -1

        self.trading_days = len(df) #交易天数
        self.annu_return = self.period_return * 252 /self.trading_days
        self.bench_annu_return = self.benchmark_return * 252 / self.trading_days

        # 波动率
        self.volatility = stats.annual_volatility(df['returns'])

        # 夏普比率
        self.sharpe = stats.sharpe_ratio(df['returns'])
        # 最大回撤
        self.max_drawdown = stats.max_drawdown(df['returns'].values)

        #信息比率
       # self.information = stats.information_ratio(df['returns'].values,df['benchmark_returns'].values)

        self.alpha,self.beta = stats.alpha_beta_aligned(df['returns'].values,df['bench_returns'].values)

        return {
            'returns':self.period_return,
            'annu_returns':self.annu_return,
            'bench_returns':self.benchmark_return,
            'bench_annu_returns':self.bench_annu_return,
            'trading_days':self.trading_days,
            'max_drawdown':self.max_drawdown,
            'volatility':self.volatility,
            'sharpe':self.sharpe,
            'alpha':self.alpha,
            'beta':self.beta
        }


class Backtest(object):
    def __init__(self):
        self.context = {}



    def run(self,handle_bar,datafeed):
        print('启动回测引擎...')
        self.datafeed = datafeed
        self.context['instruments'] = datafeed.instruments
        self.portfolio = Portfolio(indexes=datafeed.get_benchmark_index())

        done = False
        while not done:
            bars, done = datafeed.step()
            actions = handle_bar(bars, self.context)  # 调用策略函数
            self.portfolio.step(actions,bars)

        self.show_result()

    def show_result(self):
        df = self.portfolio.get_result_df().copy(deep=True)
        df['bench_returns'] = self.datafeed.get_benchmark_return()

        rets = Performance().calc(df)

        print(df.head())
        print(rets)

        df[['equity','bench_equity']].plot()
        import matplotlib.pyplot as plt
        plt.show()

#创建回测引擎实例M
M = Backtest()