import pandas as pd
# 导入tushare
import tushare as ts

# 初始化pro接口
pro = ts.pro_api('854634d420c0b6aea2907030279da881519909692cf56e6f35c4718c')


def get_etf_quotes(code, date_start="", offset=0, limit=800):
    # 拉取数据
    df = pro.fund_daily(**{
        "trade_date": "",
        "start_date": "{}".format(date_start),
        "end_date": "",
        "ts_code": "{}".format(code),
        "limit": limit,
        "offset": offset
    }, fields=[
        "ts_code",
        "trade_date",
        "open",
        "high",
        "low",
        "close",
        "vol",
        # "amount"
    ])
    df.dropna(inplace=True)
    if len(df) == 0:
        return None
    return df


def get_all_quotes(code):
    offset = 0
    df = get_etf_quotes(code, offset=0)
    print(df)
    all = [df]
    while (df is not None):
        print('===========================offset====================', offset)
        offset += 800
        df = get_etf_quotes(code, offset=offset)
        all.append(df)

    df_all = pd.concat(all)
    df_all.dropna(inplace=True)
    df_all.set_index('trade_date', inplace=True)
    return df_all


def get_etf_adj(code, date_start='', offset=0, limit=800):
    # 拉取数据
    df_adj = pro.fund_adj(**{
        "ts_code": "{}".format(code),
        "trade_date": "",
        "start_date": "{}".format(date_start),
        "end_date": "",
        "offset": offset,
        "limit": limit
    }, fields=[
        # "ts_code",
        "trade_date",
        "adj_factor"
    ])
    if len(df_adj) == 0:
        return None
    return df_adj


def get_all_adj(code):
    offset = 0
    df = get_etf_adj(code, offset=0)
    print(df)
    all = [df]
    while (df is not None):
        print('===========================offset====================', offset)
        offset += 800
        df = get_etf_adj(code, offset=offset)
        all.append(df)

    df_all = pd.concat(all)
    df_all.dropna(inplace=True)
    df_all.set_index('trade_date', inplace=True)
    return df_all


if __name__ == '__main__':

    from common.mongo_utils import get_db
    import pandas as pd

    items = get_db()['basic_etfs'].find({},{'_id':0, 'ts_code':1})
    codes = pd.DataFrame(list(items))
    codes = list(codes['ts_code'])
    print(codes)
    for i, code in enumerate(codes):
        print(i,i/len(codes),code)
        #code = code
        df_adj = get_all_adj(code)
        df_quotes = get_all_quotes(code)
        all = pd.concat([df_quotes, df_adj], axis=1)
        all.dropna(inplace=True)
        all['date'] = all.index
        all.rename(columns={'vol': 'volume', 'ts_code': 'code', 'adj_factor': 'factor'}, inplace=True)
        for col in ['open', 'high', 'low', 'close']:
            all[col] = all[col] * all['factor']
        all.set_index('date', inplace=True)
        all.index = pd.to_datetime(all.index)
        print(all)

        from common.arctic_utils import get_store, write_df

        lib = get_store('etf_quotes')
        if code in lib.list_symbols():
            lib.delete(code)
        write_df(lib, code, all, chunk_size='M')
        df = lib.read(code)
        print(df)


