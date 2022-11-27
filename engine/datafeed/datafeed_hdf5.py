# encoding:utf8
import datetime

import pandas as pd

from engine.common import Singleton
from engine.config import DATA_DIR_HDF5_ALL
from loguru import logger

@Singleton
class Hdf5DataFeed:
    def __init__(self, db_name='index.h5'):
        print(self.__class__.__name__, '初始化...')
        self.code_dfs = {}

    def get_df(self, code, db=None):
        if code in self.code_dfs.keys():
            return self.code_dfs[code]

        with pd.HDFStore(DATA_DIR_HDF5_ALL.resolve()) as store:
            logger.debug('从hdf5里读', code)
            df = store[code]
            df = df[['open', 'high', 'low', 'close', 'volume', 'code']]
        self.code_dfs[code] = df
        return df

    def get_one_df_by_codes(self, codes):
        dfs = [self.get_df(code) for code in codes]
        df_all = pd.concat(dfs, axis=0)
        df_all.dropna(inplace=True)
        df_all.sort_index(inplace=True)
        return df_all

    def get_returns_df(self, codes):
        df = self.get_one_df_by_codes(codes)
        all = pd.pivot_table(df, index='date', values='close', columns=['code'])
        returns_df = all.pct_change()
        returns_df.dropna(inplace=True)
        return returns_df

    def get_returns_df_ordered(self, codes):
        dfs = []
        for code in codes:
            df = self.get_df(code, cols=['close'])
            close = df['close']
            close.name = code
            dfs.append(close)
        all = pd.concat(dfs, axis=1)
        returns_df = all.pct_change()
        returns_df.dropna(inplace=True)
        return returns_df


if __name__ == '__main__':
    feed = Hdf5DataFeed()
    feed2 = Hdf5DataFeed()
    print(feed.get_df('399006.SZ'))
    df = feed.get_one_df_by_codes(['000300.SH', '000905.SH', 'SPX'])
    print(df)
