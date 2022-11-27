from engine.datafeed.datafeed_csv import feed
from engine.bt_engine import BacktraderEngine
from engine.strategy.stragegy_algo import StratgeyAlgo
from engine.strategy.algos import *
from datetime import datetime
from engine.datafeed.datafeed_arctic import ArcticDataFeed

if __name__ == '__main__':
    codes = ['159928.SZ', '510050.SH', '512010.SH', '513100.SH', '518880.SH', '511220.SH', '511010.SH',
             '161716.SZ']
    # weights = [0.03, 0.06, 0.08, 0.05, 0.1, 0.32, 0.26, 0.09]
    returns_df = ArcticDataFeed().get_returns_df_ordered(codes)
    #print(returns_df)

    end = datetime(2020, 12, 31)
    e = BacktraderEngine(start=datetime(2016, 1, 1))
    for code in codes:
        e.add_arctic_data(code)

    algos = [
        #RunOnce(),
        RunQuarterly(),
        SelectAll(),
        #WeightFix(weights)
        WeightRP(returns_df=returns_df, method='pca', half=True)
    ]

    e.cerebro.addstrategy(StratgeyAlgo, algos=algos, algos_init=[AddIndicators()])
    e.run()
    e.analysis()
