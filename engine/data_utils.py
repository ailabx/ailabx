import pandas as pd


def to_backtrader_dataframe(df):
    df.index = pd.to_datetime(df.index)
    df['openinterest'] = 0
    df = df[['open', 'high', 'low', 'close', 'volume', 'openinterest']]
    return df
