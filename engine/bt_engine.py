# encoding:utf8
from datetime import datetime

import backtrader as bt

from engine.datafeed.datafeed_hdf5 import Hdf5DataFeed
from engine.datafeed.dataloader import Dataloader
from engine.datafeed.dataset import Dataset
from engine.strategy.strategy_base import StratgeyAlgoBase


class BacktraderEngine:
    def __init__(self, init_cash=1000000.0, benchmark='000300.SH', start=datetime(2010, 1, 1),
                 end=datetime.now().date()):
        self.init_cash = init_cash
        self.start = start
        self.end = end
        self.benchmark = benchmark
        self.extra = {}

        cerebro = bt.Cerebro()
        cerebro.broker.setcash(init_cash)

        # 设置手续费
        cerebro.broker.setcommission(0.0001)
        # 滑点：双边各 0.0001
        cerebro.broker.set_slippage_perc(perc=0.0001)

        self.cerebro = cerebro
        self.cerebro.addanalyzer(bt.analyzers.PyFolio, _name='_PyFolio')

        self.feed = Hdf5DataFeed()

    def add_extra(self, symbol, names, fields):
        self.extra[symbol] = self.loader.load_dfs([symbol], names, fields)[0]
        # print(self.extra)

    def add_features(self, symbols, names, fields, load_from_cache=False):
        # 1.添加数据集，即资产候选集
        for s in symbols:
            self.add_data(s)

        # 2.特征工程
        self.loader = Dataloader(symbols, names, fields, load_from_cache)
        self.features = self.loader.data

    def add_model(self, model, split_date, feature_names):
        self.dataset = Dataset(dataloader=self.loader, split_date=split_date, feature_names=feature_names)
        model.fit(self.dataset)
        self.features['pred_score'] = model.predict(self.dataset)
        print(self.features['pred_score'])

    def _init_analyzers(self):
        '''
        self.cerebro.addanalyzer(bt.analyzers.Returns, _name='_Returns')
        self.cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='_TradeAnalyzer')
        self.cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name='_AnnualReturn')
        self.cerebro.addanalyzer(bt.analyzers.SharpeRatio, riskfreerate=0.0, annualize=True, _name='_SharpeRatio')
        self.cerebro.addanalyzer(bt.analyzers.DrawDown, _name='_DrawDown')
         '''
        self.cerebro.addanalyzer(bt.analyzers.PyFolio, _name='_PyFolio')

    def add_data(self, code):
        # 加载数据
        df = self.feed.get_df(code)
        df = to_backtrader_dataframe(df)
        data = bt.feeds.PandasData(dataname=df, name=code, fromdate=self.start, todate=self.end)

        self.cerebro.adddata(data)
        self.cerebro.addobserver(bt.observers.Benchmark,
                                 data=data)
        self.cerebro.addobserver(bt.observers.TimeReturn)

    def run_algo_strategy(self, algo_list):
        self.cerebro.addstrategy(StratgeyAlgoBase, algo_list=algo_list, features=self.features, extra=self.extra)
        self.results = self.cerebro.run()

    def _bokeh_plot(self):
        from backtrader_plotting import Bokeh
        from backtrader_plotting.schemes import Tradimo
        plotconfig = {
            'id:ind#0': dict(
                subplot=True,
            ),
        }
        b = Bokeh(style='line', scheme=Tradimo(), plotconfig=plotconfig)
        self.cerebro.plot(b)

    def show_result_empyrical(self, returns):
        import empyrical

        print('累计收益：', round(empyrical.cum_returns_final(returns), 3))
        print('年化收益：', round(empyrical.annual_return(returns), 3))
        print('最大回撤：', round(empyrical.max_drawdown(returns), 3))
        print('夏普比', round(empyrical.sharpe_ratio(returns), 3))
        print('卡玛比', round(empyrical.calmar_ratio(returns), 3))
        print('omega', round(empyrical.omega_ratio(returns)), 3)

    def analysis(self, pyfolio=False):
        portfolio_stats = self.results[0].analyzers.getbyname('_PyFolio')
        returns, positions, transactions, _ = portfolio_stats.get_pf_items()
        returns.index = returns.index.tz_convert(None)
        self.show_result_empyrical(returns)

        if pyfolio:
            from pyfolio.tears import create_full_tear_sheet
            create_full_tear_sheet(returns, positions=positions, transactions=transactions)
        else:
            import quantstats
            df = self.feed.get_df(self.benchmark)
            df['rate'] = df['close'].pct_change()
            df = df[['rate']]
            quantstats.reports.html(returns, benchmark=df, download_filename='stats.html', output='stats.html',
                                    title='AI量化平台')
            import webbrowser
            webbrowser.open('stats.html')

        '''
        
        import pyfolio as pf
        pf.create_full_tear_sheet(
            returns,
            positions=positions,
            transactions=transactions)
        '''
        # self.cerebro.plot(volume=False)


from engine.data_utils import to_backtrader_dataframe
from engine.strategy.strategy_rotation import StrategyRotation
from engine.strategy.stragegy_buyhold import StratgeyBuyHold


# 策略选择类
class StFetcher(object):
    _STRATS = [StratgeyBuyHold, StrategyRotation]  # 注册策略

    def __new__(cls, *args, **kwargs):
        idx = kwargs.pop('idx')  # 策略索引

        obj = cls._STRATS[idx](*args, **kwargs)
        return obj


if __name__ == '__main__':
    # symbols = ['399006.SZ']
    symbols = ['399006.SZ', '000300.SH']
    symbols = ['510300.SH', '159915.SZ']
    symbols = [
        '510050.SH',  # 上证50ETF
        '159928.SZ',  # 中证消费ETF
        '510300.SH',  # 沪深300ETF
        '159915.SZ',  # 创业板50
        '512120.SH',  # 医药50ETF
        '159806.SZ',  # 新能车ETF
        '510880.SH',  # 红利ETF
    ]

    fields = []
    names = []
    feature_names = []

    fields += ['Slope($close,20)']
    names += ['mom_slope']
    feature_names += ['mom_slope']

    fields += ['KF($mom_slope)']
    names += ['kf_mom_slope']
    feature_names += ['kf_mom_slope']

    fields += ["Ref($close,-1)/$close - 1"]
    names += ['label']

    from engine.bt_engine import BacktraderEngine
    from datetime import datetime

    e = BacktraderEngine(init_cash=1000000, benchmark='399006.SZ', start=datetime(2014, 1, 1))
    e.add_features(symbols, names, fields, load_from_cache=True)

    from engine.ml.model import SklearnModel
    from sklearn.ensemble import RandomForestRegressor,AdaBoostRegressor,HistGradientBoostingRegressor

    e.add_model(SklearnModel(AdaBoostRegressor()), split_date='2020-01-01', feature_names=feature_names)

    RSRS_benchmark = '510300.SH'
    # e.add_extra(RSRS_benchmark, fields=['RSRS($high,$low,18)', '$RSRS_beta<0.8'], names=['RSRS', 'signal'])
    e.add_extra(RSRS_benchmark, fields=['RSRS($high,$low,18)', 'Norm($RSRS_beta,600)', '$Zscore<0.0'],
                names=['RSRS', 'Zscore', 'signal'])

    from engine.strategy.algos import SelectTopK, PickTime, WeightEqually

    e.run_algo_strategy([SelectTopK(K=1, order_by='pred_score', b_ascending=False), WeightEqually()])
    e.analysis(pyfolio=False)
