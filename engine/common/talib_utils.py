import talib
import numpy as np

class TalibHelper(object):
    #简单移动平均
    def MA(self,se,period):
        return talib.MA(np.array(se), timeperiod=period)
    #指数移动平均
    def EMA(self,se,peroid):
        return talib.EMA(np.array(se),timeperiod=peroid)
    #MACD
    def MACD(self,se,fast=6,slow=12,signal=9):
        macd, signal, hist = talib.MACD(np.array(se),fastperiod=fast, slowperiod=slow, signalperiod=signal)
        return macd,signal,hist

    #RSI
    def RSI(self,se,period):
        return talib.RSI(np.array(se), timeperiod=period)

    #动量
    def MOM(self,se,period):
        return talib.MOM(np.array(se), timeperiod=5)


if __name__ == '__main__':
    pass