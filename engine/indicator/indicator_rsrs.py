import backtrader as bt
import numpy as np
import statsmodels.api as sm


class RSRS(bt.Indicator):
    lines = ('rsrs', 'R2')

    params = (('N', 18), ('value', 5))

    def __init__(self):
        self.high = self.data.high
        self.low = self.data.low

    def next(self):
        high_N = self.high.get(ago=0, size=self.p.N)
        low_N = self.low.get(ago=0, size=self.p.N)

        try:
            X = sm.add_constant(np.array(low_N))
            model = sm.OLS(np.array(high_N), X)
            results = model.fit()
            self.lines.rsrs[0] = results.params[1]
            self.lines.R2[0] = results.rsquared
        except:
            self.lines.rsrs[0] = 0


class RSRS_Norm(bt.Indicator):
    lines = ('rsrs_norm','rsrs_r2','beta_right')
    params = (('N', 18), ('M', 600))

    def __init__(self):
        self.rsrs = RSRS(self.data)
        self.lines.rsrs_norm = (self.rsrs - bt.ind.Average(self.rsrs, period=self.p.M))/bt.ind.StandardDeviation(self.rsrs, period= self.p.M)
        self.lines.rsrs_r2 = self.lines.rsrs_norm * self.rsrs.R2
        self.lines.beta_right = self.rsrs * self.lines.rsrs_r2