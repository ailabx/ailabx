# encoding:utf8
import pandas as pd
from loguru import logger

from engine.datafeed.expr.expr_mgr import ExprMgr
from engine.datafeed.datafeed_hdf5 import Hdf5DataFeed
from engine.config import DATA_DIR_HDF5_CACHE


class Dataloader:
    def __init__(self, symbols, names, fields, load_from_cache=False):
        self.expr = ExprMgr()
        self.feed = Hdf5DataFeed()
        self.symbols = symbols
        self.names = names
        self.fields = fields

        with pd.HDFStore(DATA_DIR_HDF5_CACHE.resolve()) as store:
            key = 'features'
            if load_from_cache and '/' + key in store.keys():  # 注意判断keys需要前面加“/”

                logger.info('从缓存中加载...')
                self.data = store[key]
            else:
                self.data = self.load_one_df()
                store[key] = self.data

    def load_one_df(self):
        dfs = self.load_dfs()
        all = pd.concat(dfs)
        all.sort_index(ascending=True, inplace=True)
        all.dropna(inplace=True)
        self.data = all
        return all

    def load_dfs(self, symbols=None, names=None, fields=None):
        if not symbols:
            symbols = self.symbols
        if not names:
            names = self.names
        if not fields:
            fields = self.fields

        dfs = []
        for code in symbols:
            # 直接在内存里加上字段，方便复用
            df = self.feed.get_df(code)
            for name, field in zip(names, fields):
                exp = self.expr.get_expression(field)
                # 这里可能返回多个序列
                se = exp.load(code)
                if type(se) is pd.Series:
                    df[name] = se
                if type(se) is tuple:
                    for i in range(len(se)):
                        df[name + '_' + se[i].name] = se[i]
            df['code'] = code
            dfs.append(df)

        return dfs


if __name__ == '__main__':
    names = []
    fields = []

    # fields += ['BBands($close)']
    # names += ['BBands']

    fields += ["RSRS($high,$low,18)"]
    names += ['RSRS']

    fields += ['Norm($RSRS_beta,600)']
    names += ['Norm_beta']

    # fields += ['OBV($close,$volume)']
    # names += ['obv']

    fields += ['Slope($close,20)']
    names += ['mom_slope']

    fields += ['KF($mom_slope)']
    names += ['kf_mom_slope']

    fields += ["Ref($close,-1)/$close - 1"]
    names += ['label']

    loader = Dataloader(['000300.SH'], names, fields, load_from_cache=True)
    print(loader.data)
