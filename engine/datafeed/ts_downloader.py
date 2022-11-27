# encoding:utf8
# 导入tushare
import pandas as pd
import tushare as ts

# 初始化pro接口
pro = ts.pro_api('854634d420c0b6aea2907030279da881519909692cf56e6f35c4718c')


def get_etf(code, offset=0, limit=600):
    # 拉取数据
    df = pro.fund_daily(**{
        "trade_date": "",
        "start_date": "",
        "end_date": "",
        "ts_code": code,
        "limit": limit,
        "offset": offset
    }, fields=[
        "ts_code",
        "trade_date",
        "open",
        "high",
        "low",
        "close",
        "vol"
    ])

    df.rename(columns={'trade_date': 'date', 'ts_code': 'code', 'vol': 'volume'}, inplace=True)
    df.set_index('date', inplace=True)
    # 拉取数据
    df_adj = pro.fund_adj(**{
        "ts_code": code,
        "trade_date": "",
        "start_date": "",
        "end_date": "",
        "offset": offset,
        "limit": limit
    }, fields=[
        "trade_date",
        "adj_factor"
    ])
    df_adj.rename(columns={'trade_date': 'date'}, inplace=True)
    df_adj.set_index('date', inplace=True)
    df = pd.concat([df, df_adj], axis=1)
    df.dropna(inplace=True)
    for col in ['open', 'high', 'low', 'close']:
        df[col] *= df['adj_factor']
    df.index = pd.to_datetime(df.index)
    df.sort_index(ascending=True, inplace=True)
    return df


def get_global_index(code):
    # 拉取数据
    df = pro.index_global(**{
        "ts_code": code,
        "trade_date": "",
        "start_date": "",
        "end_date": "",
        "limit": "",
        "offset": ""
    }, fields=[
        "ts_code",
        "trade_date",
        "open",
        "close",
        "high",
        "low",
        "vol"
    ])
    df.rename(columns={'ts_code': 'code', 'vol': 'volume', 'trade_date': 'date'}, inplace=True)
    df.set_index('date', inplace=True)

    df.index = pd.to_datetime(df.index)
    df.sort_index(ascending=True, inplace=True)
    return df


def get_index(code):
    # 拉取数据
    df = pro.index_daily(**{
        "ts_code": code,
        "trade_date": "",
        "start_date": "",
        "end_date": "",
        "limit": "",
        "offset": ""
    }, fields=[
        "ts_code",
        "trade_date",
        "close",
        "open",
        "high",
        "low",
        "vol",
    ])
    df.rename(columns={'ts_code': 'code', 'vol': 'volume', 'trade_date': 'date'}, inplace=True)
    df.set_index('date', inplace=True)

    df.index = pd.to_datetime(df.index)
    df.sort_index(ascending=True, inplace=True)
    return df


def download_symbols(symbols, b_index=False):
    for symbol in symbols:
        if not b_index:  # etf
            offset = 0
            df = get_etf(symbol, offset=offset)
            while(offset < 10000):
                offset += 600
                df_append = get_etf(symbol, offset=offset, limit=600)
                if df_append is None or len(df_append) == 0:
                    break
                print(df_append.tail())
                df = df.append(df_append)
            df.sort_index(ascending=True, inplace=True)

        else:
            if '.' in symbol:
                df = get_index(symbol)
            else:
                df = get_global_index(symbol)
        print(df)
        if df is None or len(df) == 0:
            print('error')
            continue
        with pd.HDFStore(DATA_DIR_HDF5_ALL.resolve()) as store:
            store[symbol] = df


if __name__ == '__main__':
    from engine.config import DATA_DIR_HDF5_ALL

    print(DATA_DIR_HDF5_ALL.resolve())

    symbols = ['000300.SH', '000905.SH', 'SPX', '399006.SZ']
    #download_symbols(symbols, b_index=True)

    etfs = ['510300.SH',  # 沪深300ETF
            '159949.SZ',  # 创业板50
            '510050.SH',  # 上证50ETF
            '159928.SZ',  # 中证消费ETF
            '510500.SH',  # 500ETF
            '159915.SZ',  # 创业板 ETF
            '512120.SH',  # 医药50ETF
            '159806.SZ',  # 新能车ETF
            '510880.SH',  # 红利ETF
            ]

    download_symbols(etfs, b_index=False)

    with pd.HDFStore(DATA_DIR_HDF5_ALL.resolve()) as store:
        print('读数据')
        print(store['510300.SH'])
