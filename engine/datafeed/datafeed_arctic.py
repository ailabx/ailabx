# encoding:utf8
import datetime

from arctic import Arctic, CHUNK_STORE
import pandas as pd


class ArcticDataFeed:
    def __init__(self, db_name='etf_quotes'):
        self.code_dfs = {}
        a = Arctic('localhost')
        a.initialize_library(db_name, lib_type=CHUNK_STORE)
        self.lib = a[db_name]

    def get_df(self, code, cols=None):
        if code in self.code_dfs.keys():
            return self.code_dfs[code]
        df = self.lib.read(code)
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
            df = self.get_df(code,cols=['close'])
            close = df['close']
            close.name = code
            dfs.append(close)
        all = pd.concat(dfs, axis=1)
        returns_df = all.pct_change()
        returns_df.dropna(inplace=True)
        return returns_df



if __name__ == '__main__':
    codes = ['159928.SZ', '510050.SH', '512010.SH', '513100.SH', '518880.SH', '511220.SH', '511010.SH',
             '161716.SZ']
    #df = ArcticDataFeed().get_df('562310.SH')
    df = ArcticDataFeed().get_returns_df(codes)
    print(df)

    df = ArcticDataFeed().get_returns_df_ordered(codes)
    print(df)



    import matplotlib.pyplot as plt
    import seaborn as sns
    from matplotlib import style


    # style.use('fivethirtyeight')
    # style.use('ggplot')
    sns.set_style("whitegrid")
    sns.set(palette="muted")
    #plt.plot(data, label=data.name, alpha=.6)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    # sns.color_palette("hls", 12)
    # sns.set(style ='darkgrid',palette ='deep')
    #fig, axes = plt.subplots(1, 1, figsize=(18, 6))


    #data = df['2009-01-01':]
    data = data / data.iloc[0] * 100  # 统一缩放到100为基点
    data.plot()
    plt.legend()
    plt.show()
