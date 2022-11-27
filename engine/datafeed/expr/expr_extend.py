import numpy as np

from engine.datafeed.expr.ops import PairOperator, Rolling
import pandas as pd
import statsmodels.api as sm


class RSRS(PairOperator):
    def __init__(self, feature_left, feature_right, N):
        self.N = N
        #self.M = M
        super(RSRS, self).__init__(feature_left, feature_right)

    def _load_internal(self, instrument):
        series_left = self.feature_left.load(instrument)
        series_right = self.feature_right.load(instrument)

        slope = []
        R2 = []
        # 计算斜率值
        n = self.N
        for i in range(len(series_left)):
            if i < (self.N - 1):
                slope.append(pd.NA)
                R2.append(pd.NA)
            else:
                x = series_right[i - n + 1:i + 1]
                # iloc左闭右开
                x = sm.add_constant(x)
                y = series_left.iloc[i - n + 1:i + 1]
                regr = sm.OLS(y, x)
                res = regr.fit()
                beta = round(res.params[1], 2)  # 斜率指标
                slope.append(beta)
                R2.append(res.rsquared)

        betas = pd.Series(slope, index=series_left.index)
        betas.name = 'beta'
        r2 = pd.Series(R2, index=series_left.index)
        r2.name = 'r2'
        return betas, r2


class Norm(Rolling):
    def __init__(self, feature, N):
        super(Norm, self).__init__(feature, N, "slope")

    def _load_internal(self, instrument):
        # 因子标准化
        def get_zscore(sub_series):
            mean = np.mean(sub_series)
            std = np.std(sub_series)
            return (sub_series[-1] - mean) / std

        series = self.feature.load(instrument)
        series = series.fillna(0.0)
        result = series.rolling(self.N, min_periods=100).apply(get_zscore)
        series = pd.Series(result, index=series.index)
        return series
