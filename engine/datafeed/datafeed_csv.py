# encoding:utf8
import os
import pandas as pd
from loguru import logger
from engine.config import DATA_DIR_CSV


class CSVDatafeed:
    _instance = None

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kw)
        return cls._instance

    def __init__(self):
        self.code_dfs = {}

    def add_data(self, code, csv_file=None):
        if not csv_file:
            csv_file = DATA_DIR_CSV.joinpath('{}.csv'.format(code))

        if not os.path.exists(csv_file):
            logger.error('{}csv文件不存在！'.format(code))
            return

        df = pd.read_csv(csv_file)
        if len(df) == 0:
            logger.error('{}没有数据！'.format(code))
            return

        for col in ['date']:
            if col not in df.columns:
                logger.error('{}字段{}不存在！'.format(code, col))
                return

        df['code'] = code
        df['date'] = df['date'].apply(lambda x: str(x))
        df.sort_values(by='date', inplace=True)

        df['rate'] = df['close'].pct_change()
        df['equity'] = (df['rate'] + 1).cumprod()
        df.set_index('date', inplace=True)

        self.code_dfs[code] = df
        return df

    def get_df(self, instrument):
        if instrument in self.code_dfs.keys():
            df = self.code_dfs[instrument]
            return df
        else:
            logger.info('{}未加载，现在加载，'.format(instrument))
            df = self.add_data(instrument)
            return df

    def get_all_df(self):
        df_all = pd.concat(self.code_dfs.values(), axis=0)
        df_all.dropna(inplace=True)
        #df_all.index = df_all['date']
        df_all.sort_index(inplace=True)

        return df_all


# 这里是全局变量
feed = CSVDatafeed()

if __name__ == '__main__':
    from engine.datafeed.expr import ExprMgr

    expr = ExprMgr()
    expr.init()

    code = '000300.Sh'
    df = feed.get_df(code)

    fields = []
    names = []

    fields += ["Corr($close/Ref($close,1), Log($volume/Ref($volume, 1)+1), 30)"]
    names += ["CORR30"]
    fields += ["Corr($close/Ref($close,1), Log($volume/Ref($volume, 1)+1), 60)"]
    names += ["CORR60"]

    fields += ["Std($close, 30)/$close"]
    names += ["STD30"]
    fields += ["Corr($close, Log($volume+1), 5)"]
    names += ["CORR5"]

    # fields += ["Resi($close, 10)/$close"]
    # names += ["RESI10"]
    # fields += ["Resi($close, 5)/$close"]
    # names += ["RESI5"]

    fields += ["Std($close, 5)/$close"]
    names += ["STD5"]
    fields += ["Std($close, 20)/$close"]
    names += ["STD20"]
    fields += ["Std($close, 60)/$close"]
    names += ["STD60"]

    fields += ["Ref($low, 0)/$close"]
    names += ["LOW0"]

    fields += [
        "Std(Abs($close/Ref($close, 1)-1)*$volume, 30)/(Mean(Abs($close/Ref($close, 1)-1)*$volume, 30)+1e-12)"
    ]
    names += ['WVMA30']

    fields += ["Ref($close, 5)/$close"]
    names += ["ROC5"]

    fields += ["(2*$close-$high-$low)/$open"]
    names += ['KSFT']

    fields += ["($close-Min($low, 5))/(Max($high, 5)-Min($low, 5)+1e-12)"]
    names += ["RSV5"]

    fields += ["($high-$low)/$open"]
    names += ['KLEN']

    for name, field in zip(names, fields):
        exp = expr.get_expression(field)
        se = exp.load(code)
        df[name] = se

    print(df)
    from alphalens.utils import get_clean_factor_and_forward_returns

    # 将tears.py中的get_values()函数改为to_numpy()
    ret = get_clean_factor_and_forward_returns(df[['rate']], close)
    from alphalens.tears import create_full_tear_sheet

    create_full_tear_sheet(ret, long_short=False)
