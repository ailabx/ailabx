import talib

def rolling_max(se,n):
    max_n = se.rolling(n).max()
    return max_n

def rolling_min(se,n):
    min_n = se.rolling(n).min()
    return min_n

def ma(se,n):
    ma_n = se.rolling(n).mean()
    return ma_n

def ema(se,n):
    ema_n = talib.EMA(se,n)
    return ema_n

def macd(se,fast=12,slow=26,signal=9):
    macd_n, macd_sig, macd_hist = talib.MACD(se,fast,slow,signal)
    return macd_n,macd_sig,macd_hist

def rsi(se,n):
    rsi_n = talib.RSI(se,n)
    return rsi_n

def obv(se,volume,n):
    obv_n = talib.OBV(se, volume)
    return obv_n

def mom(se,n):
    mom_n = talib.MOM(se,timeperiod=n)
    return mom_n

def bbands(se,n):
    upper, middle, lower = talib.BBANDS(
        se.values,
        timeperiod=n,
        # number of non-biased standard deviations from the mean
        nbdevup=2,
        nbdevdn=2,
        # Moving average type: simple moving average here
        matype=0)
    return upper,middle,lower
