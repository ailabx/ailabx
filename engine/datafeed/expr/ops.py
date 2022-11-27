# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.


from __future__ import division
from __future__ import print_function

import numpy as np
import pandas as pd
# import talib as ta

from typing import Union, List, Type
from scipy.stats import percentileofscore

from .base import Expression, ExpressionOps, Feature

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


#################### Element-Wise Operator ####################


class ElemOperator(ExpressionOps):
    """Element-wise Operator

    Parameters
    ----------
    feature : Expression
        feature instance

    Returns
    ----------
    Expression
        feature operation output
    """

    def __init__(self, feature):
        self.feature = feature

    def __str__(self):
        return "{}({})".format(type(self).__name__, self.feature)

    def get_longest_back_rolling(self):
        return self.feature.get_longest_back_rolling()

    def get_extended_window_size(self):
        return self.feature.get_extended_window_size()


class NpElemOperator(ElemOperator):
    """Numpy Element-wise Operator

    Parameters
    ----------
    feature : Expression
        feature instance
    func : str
        numpy feature operation method

    Returns
    ----------
    Expression
        feature operation output
    """

    def __init__(self, feature, func):
        self.func = func
        super(NpElemOperator, self).__init__(feature)

    def _load_internal(self, instrument):
        series = self.feature.load(instrument)
        return getattr(np, self.func)(series)


class Abs(NpElemOperator):
    """Feature Absolute Value

    Parameters
    ----------
    feature : Expression
        feature instance

    Returns
    ----------
    Expression
        a feature instance with absolute output
    """

    def __init__(self, feature):
        super(Abs, self).__init__(feature, "abs")


class Sign(NpElemOperator):
    """Feature Sign

    Parameters
    ----------
    feature : Expression
        feature instance

    Returns
    ----------
    Expression
        a feature instance with sign
    """

    def __init__(self, feature):
        super(Sign, self).__init__(feature, "sign")

    # def _load_internal(self, instrument, start_index, end_index, freq):
    def _load_internal(self, instrument):  # todo: 修改于11.15, 这里几个参数没有用
        """
        To avoid error raised by bool type input, we transform the data into float32.
        """
        series = self.feature.load(instrument)
        # TODO:  More precision types should be configurable
        series = series.astype(np.float32)
        return getattr(np, self.func)(series)


class Log(NpElemOperator):
    """Feature Log

    Parameters
    ----------
    feature : Expression
        feature instance

    Returns
    ----------
    Expression
        a feature instance with log
    """

    def __init__(self, feature):
        super(Log, self).__init__(feature, "log")


class Power(NpElemOperator):
    """Feature Power

    Parameters
    ----------
    feature : Expression
        feature instance

    Returns
    ----------
    Expression
        a feature instance with power
    """

    def __init__(self, feature, exponent):
        super(Power, self).__init__(feature, "power")
        self.exponent = exponent

    def __str__(self):
        return "{}({},{})".format(type(self).__name__, self.feature, self.exponent)

    def _load_internal(self, instrument):
        series = self.feature.load(instrument)
        return getattr(np, self.func)(series, self.exponent)


class Mask(NpElemOperator):
    """Feature Mask

    Parameters
    ----------
    feature : Expression
        feature instance
    instrument : str
        instrument mask

    Returns
    ----------
    Expression
        a feature instance with masked instrument
    """

    def __init__(self, feature, instrument):
        super(Mask, self).__init__(feature, "mask")
        self.instrument = instrument

    def __str__(self):
        return "{}({},{})".format(type(self).__name__, self.feature, self.instrument.lower())

    def _load_internal(self, instrument):
        return self.feature.load(self.instrument)


class Not(NpElemOperator):
    """Not Operator

    Parameters
    ----------
    feature_left : Expression
        feature instance
    feature_right : Expression
        feature instance

    Returns
    ----------
    Feature:
        feature elementwise not output
    """

    def __init__(self, feature):
        super(Not, self).__init__(feature, "bitwise_not")


#################### Pair-Wise Operator ####################
class PairOperator(ExpressionOps):
    """Pair-wise operator

    Parameters
    ----------
    feature_left : Expression
        feature instance or numeric value
    feature_right : Expression
        feature instance or numeric value
    func : str
        operator function

    Returns
    ----------
    Feature:
        two features' operation output
    """

    def __init__(self, feature_left, feature_right):
        self.feature_left = feature_left
        self.feature_right = feature_right

    def __str__(self):
        return "{}({},{})".format(type(self).__name__, self.feature_left, self.feature_right)

    def get_longest_back_rolling(self):
        if isinstance(self.feature_left, Expression):
            left_br = self.feature_left.get_longest_back_rolling()
        else:
            left_br = 0

        if isinstance(self.feature_right, Expression):
            right_br = self.feature_right.get_longest_back_rolling()
        else:
            right_br = 0
        return max(left_br, right_br)

    def get_extended_window_size(self):
        if isinstance(self.feature_left, Expression):
            ll, lr = self.feature_left.get_extended_window_size()
        else:
            ll, lr = 0, 0

        if isinstance(self.feature_right, Expression):
            rl, rr = self.feature_right.get_extended_window_size()
        else:
            rl, rr = 0, 0
        return max(ll, rl), max(lr, rr)


class NpPairOperator(PairOperator):
    """Numpy Pair-wise operator

    Parameters
    ----------
    feature_left : Expression
        feature instance or numeric value
    feature_right : Expression
        feature instance or numeric value
    func : str
        operator function

    Returns
    ----------
    Feature:
        two features' operation output
    """

    def __init__(self, feature_left, feature_right, func):
        self.func = func
        super(NpPairOperator, self).__init__(feature_left, feature_right)

    def _load_internal(self, instrument):
        assert any(
            [isinstance(self.feature_left, Expression), self.feature_right, Expression]
        ), "at least one of two inputs is Expression instance"
        if isinstance(self.feature_left, Expression):
            series_left = self.feature_left.load(instrument)
        else:
            series_left = self.feature_left  # numeric value
        if isinstance(self.feature_right, Expression):
            series_right = self.feature_right.load(instrument)
        else:
            series_right = self.feature_right
        check_length = isinstance(series_left, (np.ndarray, pd.Series)) and isinstance(
            series_right, (np.ndarray, pd.Series)
        )
        if check_length:
            warning_info = (
                f"Loading {instrument}: {str(self)}; np.{self.func}(series_left, series_right), "
                f"The length of series_left and series_right is different: ({len(series_left)}, {len(series_right)}), "
                f"series_left is {str(self.feature_left)}, series_right is {str(self.feature_left)}. Please check the data"
            )
        else:
            warning_info = (
                f"Loading {instrument}: {str(self)}; np.{self.func}(series_left, series_right), "
                f"series_left is {str(self.feature_left)}, series_right is {str(self.feature_left)}. Please check the data"
            )
        try:
            res = getattr(np, self.func)(series_left, series_right)
        except ValueError as e:
            logger.error(warning_info)
            raise ValueError(f"{str(e)}. \n\t{warning_info}")
        else:
            if check_length and len(series_left) != len(series_right):
                logger.warning(warning_info)
        return res


class Add(NpPairOperator):
    """Add Operator

    Parameters
    ----------
    feature_left : Expression
        feature instance
    feature_right : Expression
        feature instance

    Returns
    ----------
    Feature:
        two features' sum
    """

    def __init__(self, feature_left, feature_right):
        super(Add, self).__init__(feature_left, feature_right, "add")


class Sub(NpPairOperator):
    """Subtract Operator

    Parameters
    ----------
    feature_left : Expression
        feature instance
    feature_right : Expression
        feature instance

    Returns
    ----------
    Feature:
        two features' subtraction
    """

    def __init__(self, feature_left, feature_right):
        super(Sub, self).__init__(feature_left, feature_right, "subtract")


class Mul(NpPairOperator):
    """Multiply Operator

    Parameters
    ----------
    feature_left : Expression
        feature instance
    feature_right : Expression
        feature instance

    Returns
    ----------
    Feature:
        two features' product
    """

    def __init__(self, feature_left, feature_right):
        super(Mul, self).__init__(feature_left, feature_right, "multiply")


class Div(NpPairOperator):
    """Division Operator

    Parameters
    ----------
    feature_left : Expression
        feature instance
    feature_right : Expression
        feature instance

    Returns
    ----------
    Feature:
        two features' division
    """

    def __init__(self, feature_left, feature_right):
        super(Div, self).__init__(feature_left, feature_right, "divide")


class Greater(NpPairOperator):
    """Greater Operator

    Parameters
    ----------
    feature_left : Expression
        feature instance
    feature_right : Expression
        feature instance

    Returns
    ----------
    Feature:
        greater elements taken from the input two features
    """

    def __init__(self, feature_left, feature_right):
        super(Greater, self).__init__(feature_left, feature_right, "maximum")


class Less(NpPairOperator):
    """Less Operator

    Parameters
    ----------
    feature_left : Expression
        feature instance
    feature_right : Expression
        feature instance

    Returns
    ----------
    Feature:
        smaller elements taken from the input two features
    """

    def __init__(self, feature_left, feature_right):
        super(Less, self).__init__(feature_left, feature_right, "minimum")


class Gt(NpPairOperator):
    """Greater Than Operator

    Parameters
    ----------
    feature_left : Expression
        feature instance
    feature_right : Expression
        feature instance

    Returns
    ----------
    Feature:
        bool series indicate `left > right`
    """

    def __init__(self, feature_left, feature_right):
        super(Gt, self).__init__(feature_left, feature_right, "greater")


class Ge(NpPairOperator):
    """Greater Equal Than Operator

    Parameters
    ----------
    feature_left : Expression
        feature instance
    feature_right : Expression
        feature instance

    Returns
    ----------
    Feature:
        bool series indicate `left >= right`
    """

    def __init__(self, feature_left, feature_right):
        super(Ge, self).__init__(feature_left, feature_right, "greater_equal")


class Lt(NpPairOperator):
    """Less Than Operator

    Parameters
    ----------
    feature_left : Expression
        feature instance
    feature_right : Expression
        feature instance

    Returns
    ----------
    Feature:
        bool series indicate `left < right`
    """

    def __init__(self, feature_left, feature_right):
        super(Lt, self).__init__(feature_left, feature_right, "less")


class Le(NpPairOperator):
    """Less Equal Than Operator

    Parameters
    ----------
    feature_left : Expression
        feature instance
    feature_right : Expression
        feature instance

    Returns
    ----------
    Feature:
        bool series indicate `left <= right`
    """

    def __init__(self, feature_left, feature_right):
        super(Le, self).__init__(feature_left, feature_right, "less_equal")


class Eq(NpPairOperator):
    """Equal Operator

    Parameters
    ----------
    feature_left : Expression
        feature instance
    feature_right : Expression
        feature instance

    Returns
    ----------
    Feature:
        bool series indicate `left == right`
    """

    def __init__(self, feature_left, feature_right):
        super(Eq, self).__init__(feature_left, feature_right, "equal")


class Ne(NpPairOperator):
    """Not Equal Operator

    Parameters
    ----------
    feature_left : Expression
        feature instance
    feature_right : Expression
        feature instance

    Returns
    ----------
    Feature:
        bool series indicate `left != right`
    """

    def __init__(self, feature_left, feature_right):
        super(Ne, self).__init__(feature_left, feature_right, "not_equal")


class And(NpPairOperator):
    """And Operator

    Parameters
    ----------
    feature_left : Expression
        feature instance
    feature_right : Expression
        feature instance

    Returns
    ----------
    Feature:
        two features' row by row & output
    """

    def __init__(self, feature_left, feature_right):
        super(And, self).__init__(feature_left, feature_right, "bitwise_and")


class Or(NpPairOperator):
    """Or Operator

    Parameters
    ----------
    feature_left : Expression
        feature instance
    feature_right : Expression
        feature instance

    Returns
    ----------
    Feature:
        two features' row by row | outputs
    """

    def __init__(self, feature_left, feature_right):
        super(Or, self).__init__(feature_left, feature_right, "bitwise_or")


#################### Triple-wise Operator ####################
class If(ExpressionOps):
    """If Operator

    Parameters
    ----------
    condition : Expression
        feature instance with bool values as condition
    feature_left : Expression
        feature instance
    feature_right : Expression
        feature instance
    """

    def __init__(self, condition, feature_left, feature_right):
        self.condition = condition
        self.feature_left = feature_left
        self.feature_right = feature_right

    def __str__(self):
        return "If({},{},{})".format(self.condition, self.feature_left, self.feature_right)

    def _load_internal(self, instrument):
        series_cond = self.condition.load(instrument)
        if isinstance(self.feature_left, Expression):
            series_left = self.feature_left.load(instrument)
        else:
            series_left = self.feature_left
        if isinstance(self.feature_right, Expression):
            series_right = self.feature_right.load(instrument)
        else:
            series_right = self.feature_right
        series = pd.Series(np.where(series_cond, series_left, series_right), index=series_cond.index)
        return series

    def get_longest_back_rolling(self):
        if isinstance(self.feature_left, Expression):
            left_br = self.feature_left.get_longest_back_rolling()
        else:
            left_br = 0

        if isinstance(self.feature_right, Expression):
            right_br = self.feature_right.get_longest_back_rolling()
        else:
            right_br = 0

        if isinstance(self.condition, Expression):
            c_br = self.condition.get_longest_back_rolling()
        else:
            c_br = 0
        return max(left_br, right_br, c_br)

    def get_extended_window_size(self):
        if isinstance(self.feature_left, Expression):
            ll, lr = self.feature_left.get_extended_window_size()
        else:
            ll, lr = 0, 0

        if isinstance(self.feature_right, Expression):
            rl, rr = self.feature_right.get_extended_window_size()
        else:
            rl, rr = 0, 0

        if isinstance(self.condition, Expression):
            cl, cr = self.condition.get_extended_window_size()
        else:
            cl, cr = 0, 0
        return max(ll, rl, cl), max(lr, rr, cr)


#################### Rolling ####################
# NOTE: methods like `rolling.mean` are optimized with cython,
# and are super faster than `rolling.apply(np.mean)`


class Rolling(ExpressionOps):
    """Rolling Operator

    Parameters
    ----------
    feature : Expression
        feature instance
    N : int
        rolling window size
    func : str
        rolling method

    Returns
    ----------
    Expression
        rolling outputs
    """

    def __init__(self, feature, N, func):
        self.feature = feature
        self.N = N
        self.func = func

    def __str__(self):
        return "{}({},{})".format(type(self).__name__, self.feature, self.N)

    def _load_internal(self, instrument):
        series = self.feature.load(instrument)
        # NOTE: remove all null check,
        # now it's user's responsibility to decide whether use features in null days
        # isnull = series.isnull() # NOTE: isnull = NaN, inf is not null
        if self.N == 0:
            series = getattr(series.expanding(min_periods=1), self.func)()
        elif 0 < self.N < 1:
            series = series.ewm(alpha=self.N, min_periods=1).mean()
        else:
            series = getattr(series.rolling(self.N, min_periods=1), self.func)()
            # series.iloc[:self.N-1] = np.nan
        # series[isnull] = np.nan
        return series

    def get_longest_back_rolling(self):
        if self.N == 0:
            return np.inf
        if 0 < self.N < 1:
            return int(np.log(1e-6) / np.log(1 - self.N))  # (1 - N)**window == 1e-6
        return self.feature.get_longest_back_rolling() + self.N - 1

    def get_extended_window_size(self):
        if self.N == 0:
            # FIXME: How to make this accurate and efficiently? Or  should we
            # remove such support for N == 0?
            logger.warning("The Rolling(ATTR, 0) will not be accurately calculated")
            return self.feature.get_extended_window_size()
        elif 0 < self.N < 1:
            lft_etd, rght_etd = self.feature.get_extended_window_size()
            size = int(np.log(1e-6) / np.log(1 - self.N))
            lft_etd = max(lft_etd + size - 1, lft_etd)
            return lft_etd, rght_etd
        else:
            lft_etd, rght_etd = self.feature.get_extended_window_size()
            lft_etd = max(lft_etd + self.N - 1, lft_etd)
            return lft_etd, rght_etd


class Ref(Rolling):
    """Feature Reference

    Parameters
    ----------
    feature : Expression
        feature instance
    N : int
        N = 0, retrieve the first data; N > 0, retrieve data of N periods ago; N < 0, future data

    Returns
    ----------
    Expression
        a feature instance with target reference
    """

    def __init__(self, feature, N):
        super(Ref, self).__init__(feature, N, "ref")

    def _load_internal(self, instrument):
        series = self.feature.load(instrument)
        # N = 0, return first day
        if series.empty:
            return series  # Pandas bug, see: https://github.com/pandas-dev/pandas/issues/21049
        elif self.N == 0:
            series = pd.Series(series.iloc[0], index=series.index)
        else:
            series = series.shift(self.N)  # copy
        return series

    def get_longest_back_rolling(self):
        if self.N == 0:
            return np.inf
        return self.feature.get_longest_back_rolling() + self.N

    def get_extended_window_size(self):
        if self.N == 0:
            logger.warning("The Ref(ATTR, 0) will not be accurately calculated")
            return self.feature.get_extended_window_size()
        else:
            lft_etd, rght_etd = self.feature.get_extended_window_size()
            lft_etd = max(lft_etd + self.N, lft_etd)
            rght_etd = max(rght_etd - self.N, rght_etd)
            return lft_etd, rght_etd


class Mean(Rolling):
    """Rolling Mean (MA)

    Parameters
    ----------
    feature : Expression
        feature instance
    N : int
        rolling window size

    Returns
    ----------
    Expression
        a feature instance with rolling average
    """

    def __init__(self, feature, N):
        super(Mean, self).__init__(feature, N, "mean")


class Sum(Rolling):
    """Rolling Sum

    Parameters
    ----------
    feature : Expression
        feature instance
    N : int
        rolling window size

    Returns
    ----------
    Expression
        a feature instance with rolling sum
    """

    def __init__(self, feature, N):
        super(Sum, self).__init__(feature, N, "sum")


class Std(Rolling):
    """Rolling Std

    Parameters
    ----------
    feature : Expression
        feature instance
    N : int
        rolling window size

    Returns
    ----------
    Expression
        a feature instance with rolling std
    """

    def __init__(self, feature, N):
        super(Std, self).__init__(feature, N, "std")


class Var(Rolling):
    """Rolling Variance

    Parameters
    ----------
    feature : Expression
        feature instance
    N : int
        rolling window size

    Returns
    ----------
    Expression
        a feature instance with rolling variance
    """

    def __init__(self, feature, N):
        super(Var, self).__init__(feature, N, "var")


class Skew(Rolling):
    """Rolling Skewness

    Parameters
    ----------
    feature : Expression
        feature instance
    N : int
        rolling window size

    Returns
    ----------
    Expression
        a feature instance with rolling skewness
    """

    def __init__(self, feature, N):
        if N != 0 and N < 3:
            raise ValueError("The rolling window size of Skewness operation should >= 3")
        super(Skew, self).__init__(feature, N, "skew")


class Kurt(Rolling):
    """Rolling Kurtosis

    Parameters
    ----------
    feature : Expression
        feature instance
    N : int
        rolling window size

    Returns
    ----------
    Expression
        a feature instance with rolling kurtosis
    """

    def __init__(self, feature, N):
        if N != 0 and N < 4:
            raise ValueError("The rolling window size of Kurtosis operation should >= 5")
        super(Kurt, self).__init__(feature, N, "kurt")


class Max(Rolling):
    """Rolling Max

    Parameters
    ----------
    feature : Expression
        feature instance
    N : int
        rolling window size

    Returns
    ----------
    Expression
        a feature instance with rolling max
    """

    def __init__(self, feature, N):
        super(Max, self).__init__(feature, N, "max")


class IdxMax(Rolling):
    """Rolling Max Index

    Parameters
    ----------
    feature : Expression
        feature instance
    N : int
        rolling window size

    Returns
    ----------
    Expression
        a feature instance with rolling max index
    """

    def __init__(self, feature, N):
        super(IdxMax, self).__init__(feature, N, "idxmax")

    def _load_internal(self, instrument):
        series = self.feature.load(instrument)
        if self.N == 0:
            series = series.expanding(min_periods=1).apply(lambda x: x.argmax() + 1, raw=True)
        else:
            series = series.rolling(self.N, min_periods=1).apply(lambda x: x.argmax() + 1, raw=True)
        return series


class Min(Rolling):
    """Rolling Min

    Parameters
    ----------
    feature : Expression
        feature instance
    N : int
        rolling window size

    Returns
    ----------
    Expression
        a feature instance with rolling min
    """

    def __init__(self, feature, N):
        super(Min, self).__init__(feature, N, "min")


class IdxMin(Rolling):
    """Rolling Min Index

    Parameters
    ----------
    feature : Expression
        feature instance
    N : int
        rolling window size

    Returns
    ----------
    Expression
        a feature instance with rolling min index
    """

    def __init__(self, feature, N):
        super(IdxMin, self).__init__(feature, N, "idxmin")

    def _load_internal(self, instrument):
        series = self.feature.load(instrument)
        if self.N == 0:
            series = series.expanding(min_periods=1).apply(lambda x: x.argmin() + 1, raw=True)
        else:
            series = series.rolling(self.N, min_periods=1).apply(lambda x: x.argmin() + 1, raw=True)
        return series


class Quantile(Rolling):
    """Rolling Quantile

    Parameters
    ----------
    feature : Expression
        feature instance
    N : int
        rolling window size

    Returns
    ----------
    Expression
        a feature instance with rolling quantile
    """

    def __init__(self, feature, N, qscore):
        super(Quantile, self).__init__(feature, N, "quantile")
        self.qscore = qscore

    def __str__(self):
        return "{}({},{},{})".format(type(self).__name__, self.feature, self.N, self.qscore)

    def _load_internal(self, instrument):
        series = self.feature.load(instrument)
        if self.N == 0:
            series = series.expanding(min_periods=1).quantile(self.qscore)
        else:
            series = series.rolling(self.N, min_periods=1).quantile(self.qscore)
        return series


class Med(Rolling):
    """Rolling Median

    Parameters
    ----------
    feature : Expression
        feature instance
    N : int
        rolling window size

    Returns
    ----------
    Expression
        a feature instance with rolling median
    """

    def __init__(self, feature, N):
        super(Med, self).__init__(feature, N, "median")


class Mad(Rolling):
    """Rolling Mean Absolute Deviation

    Parameters
    ----------
    feature : Expression
        feature instance
    N : int
        rolling window size

    Returns
    ----------
    Expression
        a feature instance with rolling mean absolute deviation
    """

    def __init__(self, feature, N):
        super(Mad, self).__init__(feature, N, "mad")

    def _load_internal(self, instrument):
        series = self.feature.load(instrument)

        # TODO: implement in Cython

        def mad(x):
            x1 = x[~np.isnan(x)]
            return np.mean(np.abs(x1 - x1.mean()))

        if self.N == 0:
            series = series.expanding(min_periods=1).apply(mad, raw=True)
        else:
            series = series.rolling(self.N, min_periods=1).apply(mad, raw=True)
        return series


class Rank(Rolling):
    """Rolling Rank (Percentile)

    Parameters
    ----------
    feature : Expression
        feature instance
    N : int
        rolling window size

    Returns
    ----------
    Expression
        a feature instance with rolling rank
    """

    def __init__(self, feature, N):
        super(Rank, self).__init__(feature, N, "rank")

    def _load_internal(self, instrument):
        series = self.feature.load(instrument)

        # TODO: implement in Cython

        def rank(x):
            if np.isnan(x[-1]):
                return np.nan
            x1 = x[~np.isnan(x)]
            if x1.shape[0] == 0:
                return np.nan
            return percentileofscore(x1, x1[-1]) / len(x1)

        if self.N == 0:
            series = series.expanding(min_periods=1).apply(rank, raw=True)
        else:
            series = series.rolling(self.N, min_periods=1).apply(rank, raw=True)
        return series


class Count(Rolling):
    """Rolling Count

    Parameters
    ----------
    feature : Expression
        feature instance
    N : int
        rolling window size

    Returns
    ----------
    Expression
        a feature instance with rolling count of number of non-NaN elements
    """

    def __init__(self, feature, N):
        super(Count, self).__init__(feature, N, "count")


class Delta(Rolling):
    """Rolling Delta

    Parameters
    ----------
    feature : Expression
        feature instance
    N : int
        rolling window size

    Returns
    ----------
    Expression
        a feature instance with end minus start in rolling window
    """

    def __init__(self, feature, N):
        super(Delta, self).__init__(feature, N, "delta")

    def _load_internal(self, instrument):
        series = self.feature.load(instrument)
        if self.N == 0:
            series = series - series.iloc[0]
        else:
            series = series - series.shift(self.N)
        return series


# TODO:
# support pair-wise rolling like `Slope(A, B, N)`
class Slope(Rolling):
    """Rolling Slope

    Parameters
    ----------
    feature : Expression
        feature instance
    N : int
        rolling window size

    Returns
    ----------
    Expression
        a feature instance with linear regression slope of given window
    """

    def __init__(self, feature, N):
        super(Slope, self).__init__(feature, N, "slope")

    def _load_internal(self, instrument):
        def calc_slope(x):
            x = x / x[0]  # 这里做了一个“归一化”
            slope = np.polyfit(range(len(x)), x, 1)[0]
            return slope

        series = self.feature.load(instrument)
        result = series.rolling(self.N, min_periods=2).apply(calc_slope)
        series = pd.Series(result, index=series.index)
        return series


from pykalman import KalmanFilter

class KF(Rolling):

    def __init__(self, feature, damping=1, N=1):
        super(KF, self).__init__(feature, N, "kalman")
        self.damping = damping

    def _load_internal(self, instrument):
        series = self.feature.load(instrument)
        series = series.fillna(0.0)
        observation_covariance = 0.15
        initial_value_guess = 1
        transition_matrix = 1
        transition_covariance = 0.1

        kf = KalmanFilter(transition_matrices=[1],
                          observation_matrices=[1],
                          initial_state_mean=0,
                          initial_state_covariance=1,
                          observation_covariance=1,
                          transition_covariance=.01)
        pre, _ = kf.smooth(np.array(series))
        pre = pre.flatten()
        series = pd.Series(pre, index=series.index)
        return series


class Rsquare(Rolling):
    """Rolling R-value Square

    Parameters
    ----------
    feature : Expression
        feature instance
    N : int
        rolling window size

    Returns
    ----------
    Expression
        a feature instance with linear regression r-value square of given window
    """

    def __init__(self, feature, N):
        super(Rsquare, self).__init__(feature, N, "rsquare")

    def _load_internal(self, instrument):
        _series = self.feature.load(instrument)
        if self.N == 0:
            series = pd.Series(expanding_rsquare(_series.values), index=_series.index)
        else:
            series = pd.Series(rolling_rsquare(_series.values, self.N), index=_series.index)
            series.loc[np.isclose(_series.rolling(self.N, min_periods=1).std(), 0, atol=2e-05)] = np.nan
        return series


class Resi(Rolling):
    """Rolling Regression Residuals

    Parameters
    ----------
    feature : Expression
        feature instance
    N : int
        rolling window size

    Returns
    ----------
    Expression
        a feature instance with regression residuals of given window
    """

    def __init__(self, feature, N):
        super(Resi, self).__init__(feature, N, "resi")

    def _load_internal(self, instrument):
        series = self.feature.load(instrument)
        if self.N == 0:
            series = pd.Series(expanding_resi(series.values), index=series.index)
        else:
            series = pd.Series(rolling_resi(series.values, self.N), index=series.index)
        return series


class WMA(Rolling):
    """Rolling WMA

    Parameters
    ----------
    feature : Expression
        feature instance
    N : int
        rolling window size

    Returns
    ----------
    Expression
        a feature instance with weighted moving average output
    """

    def __init__(self, feature, N):
        super(WMA, self).__init__(feature, N, "wma")

    def _load_internal(self, instrument):
        series = self.feature.load(instrument)

        # TODO: implement in Cython

        def weighted_mean(x):
            w = np.arange(len(x))
            w = w / w.sum()
            return np.nanmean(w * x)

        if self.N == 0:
            series = series.expanding(min_periods=1).apply(weighted_mean, raw=True)
        else:
            series = series.rolling(self.N, min_periods=1).apply(weighted_mean, raw=True)
        return series


class EMA(Rolling):
    """Rolling Exponential Mean (EMA)

    Parameters
    ----------
    feature : Expression
        feature instance
    N : int, float
        rolling window size

    Returns
    ----------
    Expression
        a feature instance with regression r-value square of given window
    """

    def __init__(self, feature, N):
        super(EMA, self).__init__(feature, N, "ema")

    def _load_internal(self, instrument):
        series = self.feature.load(instrument)

        def exp_weighted_mean(x):
            a = 1 - 2 / (1 + len(x))
            w = a ** np.arange(len(x))[::-1]
            w /= w.sum()
            return np.nansum(w * x)

        if self.N == 0:
            series = series.expanding(min_periods=1).apply(exp_weighted_mean, raw=True)
        elif 0 < self.N < 1:
            series = series.ewm(alpha=self.N, min_periods=1).mean()
        else:
            series = series.ewm(span=self.N, min_periods=1).mean()
        return series


class CustomOps(Expression):

    def __init__(self, feature, name=None):
        self.feature = feature
        if name:
            self._name = name
        else:
            self._name = type(self).__name__

    def __str__(self):
        return self._name

    def get_longest_back_rolling(self):
        return 0

    def get_extended_window_size(self):
        return 0, 0


class QCut(CustomOps):
    def __init__(self, feature, N):
        self.N = N
        super(QCut, self).__init__(feature)

    def _load_internal(self, instrument):
        series = self.feature.load(instrument)
        quantiles = [step / 100 for step in range(0, 100, int(100 / self.N))]
        if len(quantiles) <= self.N:
            quantiles.append(1)

        labels = pd.qcut(series, quantiles, labels=range(0, self.N)).astype('float')

        return pd.Series(labels, index=series.index)


import talib as ta


class MACD(Rolling):
    def __init__(self, feature, M=26, N=12, O=9):
        self.M = 12
        self.N = 26
        self.O = 9
        super(MACD, self).__init__(feature, self.N, '')

    def _load_internal(self, instrument):
        series = self.feature.load(instrument)
        macd, signal, hist = ta.MACD(series.values, self.M, self.N, self.O)
        return pd.Series(macd, index=series.index)


class BBands(Rolling):
    def __init__(self, feature, M=20, N=2):
        self.M = M
        self.N = N
        super(BBands, self).__init__(feature, self.N, '')

    def _load_internal(self, instrument):
        series = self.feature.load(instrument)
        upper, middle, lower = ta.BBANDS(
            series.values,
            timeperiod=self.M,
            # number of non-biased standard deviations from the mean
            nbdevup=self.N,
            nbdevdn=self.N,
            # Moving average type: simple moving average here
            matype=0)

        upper = pd.Series(upper, index=series.index)
        upper.name = 'up'
        lower = pd.Series(lower, index=series.index)
        lower.name = 'down'
        return upper, lower

        return pd.Series(upper, index=series.index)


class BBands_up(Rolling):
    def __init__(self, feature, N=20):
        self.N = N
        super(BBands_up, self).__init__(feature, self.N, '')

    def _load_internal(self, instrument):
        series = self.feature.load(instrument)
        upper, middle, lower = ta.BBANDS(
            series.values,
            timeperiod=self.N,
            # number of non-biased standard deviations from the mean
            nbdevup=2,
            nbdevdn=2,
            # Moving average type: simple moving average here
            matype=0)

        upper = pd.Series(upper, index=series.index)
        upper.name = 'bbands_up'
        lower = pd.Series(lower, index=series.index)
        lower.name = 'bbands_lower'
        return upper, lower


class BBands_down(Rolling):
    def __init__(self, feature, N=20):
        self.N = N
        super(BBands_down, self).__init__(feature, self.N, '')

    def _load_internal(self, instrument):
        series = self.feature.load(instrument)
        upper, middle, down = ta.BBANDS(
            series.values,
            timeperiod=self.N,
            # number of non-biased standard deviations from the mean
            nbdevup=2,
            nbdevdn=2,
            # Moving average type: simple moving average here
            matype=0)

        return pd.Series(down, index=series.index)


class Return(Rolling):
    def __init__(self, feature, N=20):
        self.N = N
        super(Return, self).__init__(feature, self.N, '')

    def _load_internal(self, instrument):
        series = self.feature.load(instrument)
        se = series / series.shift(self.N) - 1

        ret = pd.Series(se, index=series.index)
        return ret


#################### Pair-Wise Rolling ####################
class PairRolling(ExpressionOps):
    """Pair Rolling Operator

    Parameters
    ----------
    feature_left : Expression
        feature instance
    feature_right : Expression
        feature instance
    N : int
        rolling window size

    Returns
    ----------
    Expression
        a feature instance with rolling output of two input features
    """

    def __init__(self, feature_left, feature_right, N, func):
        self.feature_left = feature_left
        self.feature_right = feature_right
        self.N = N
        self.func = func

    def __str__(self):
        return "{}({},{},{})".format(type(self).__name__, self.feature_left, self.feature_right, self.N)

    def _load_internal(self, instrument):
        series_left = self.feature_left.load(instrument)
        series_right = self.feature_right.load(instrument)
        if self.N == 0:
            series = getattr(series_left.expanding(min_periods=1), self.func)(series_right)
        else:
            series = getattr(series_left.rolling(self.N, min_periods=1), self.func)(series_right)
        return series

    def get_longest_back_rolling(self):
        if self.N == 0:
            return np.inf
        return (
                max(self.feature_left.get_longest_back_rolling(), self.feature_right.get_longest_back_rolling())
                + self.N
                - 1
        )

    def get_extended_window_size(self):
        if self.N == 0:
            logger.warning(
                "The PairRolling(ATTR, 0) will not be accurately calculated"
            )
            return self.feature.get_extended_window_size()
        else:
            ll, lr = self.feature_left.get_extended_window_size()
            rl, rr = self.feature_right.get_extended_window_size()
            return max(ll, rl) + self.N - 1, max(lr, rr)


class Corr(PairRolling):
    """Rolling Correlation

    Parameters
    ----------
    feature_left : Expression
        feature instance
    feature_right : Expression
        feature instance
    N : int
        rolling window size

    Returns
    ----------
    Expression
        a feature instance with rolling correlation of two input features
    """

    def __init__(self, feature_left, feature_right, N):
        super(Corr, self).__init__(feature_left, feature_right, N, "corr")

    def _load_internal(self, instrument):
        res: pd.Series = super(Corr, self)._load_internal(instrument)

        # NOTE: Load uses MemCache, so calling load again will not cause performance degradation
        series_left = self.feature_left.load(instrument)
        series_right = self.feature_right.load(instrument)
        res.loc[
            np.isclose(series_left.rolling(self.N, min_periods=1).std(), 0, atol=2e-05)
            | np.isclose(series_right.rolling(self.N, min_periods=1).std(), 0, atol=2e-05)
            ] = np.nan
        return res


class Cov(PairRolling):
    """Rolling Covariance

    Parameters
    ----------
    feature_left : Expression
        feature instance
    feature_right : Expression
        feature instance
    N : int
        rolling window size

    Returns
    ----------
    Expression
        a feature instance with rolling max of two input features
    """

    def __init__(self, feature_left, feature_right, N):
        super(Cov, self).__init__(feature_left, feature_right, N, "cov")


import statsmodels.api as sm



class RSRS_old(PairOperator):
    def __init__(self, feature_left, feature_right, N, M):
        self.N = N
        self.M = M
        super(RSRS_old, self).__init__(feature_left, feature_right)

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


class OBV(PairOperator):
    def __init__(self, feature_left, feature_right):
        self.feature_left = feature_left
        self.feature_right = feature_right

    def _load_internal(self, instrument):
        series_left = self.feature_left.load(instrument)
        series_right = self.feature_right.load(instrument)

        obv = ta.OBV(series_left, series_right)
        se = pd.Series(obv, index=series_left.index)
        return se


from engine.datafeed.expr.expr_extend import *
OpsList = [
    Norm,
    KF,
    OBV,
    QCut,
    BBands,
    BBands_up,
    BBands_down,
    MACD,
    Return,
    RSRS,
    Ref,
    Max,
    Min,
    Sum,
    Mean,
    Std,
    Var,
    Skew,
    Kurt,
    Med,
    Mad,
    Slope,
    Rsquare,
    Resi,
    Rank,
    Quantile,
    Count,
    EMA,
    WMA,
    Corr,
    Cov,
    Delta,
    Abs,
    Sign,
    Log,
    Power,
    Add,
    Sub,
    Mul,
    Div,
    Greater,
    Less,
    And,
    Or,
    Not,
    Gt,
    Ge,
    Lt,
    Le,
    Eq,
    Ne,
    Mask,
    IdxMax,
    IdxMin,
    If,
    Feature,
]


class OpsWrapper:
    """Ops Wrapper"""

    def __init__(self):
        self._ops = {}

    def reset(self):
        self._ops = {}

    def register(self, ops_list: List[Union[Type[ExpressionOps], dict]]):
        """register operator

        Parameters
        ----------
        ops_list : List[Union[Type[ExpressionOps], dict]]
            - if type(ops_list) is List[Type[ExpressionOps]], each element of ops_list represents the operator class, which should be the subclass of `ExpressionOps`.
            - if type(ops_list) is List[dict], each element of ops_list represents the config of operator, which has the following format:
                {
                    "class": class_name,
                    "module_path": path,
                }
                Note: `class` should be the class name of operator, `module_path` should be a python module or path of file.
        """
        for _operator in ops_list:
            if isinstance(_operator, dict):
                _ops_class, _ = get_callable_kwargs(_operator)
            else:
                _ops_class = _operator

            if not issubclass(_ops_class, Expression):
                raise TypeError("operator must be subclass of ExpressionOps, not {}".format(_ops_class))

            if _ops_class.__name__ in self._ops:
                logger.warning(
                    "The custom operator [{}] will override the qlib default definition".format(_ops_class.__name__)
                )
            self._ops[_ops_class.__name__] = _ops_class

    def __getattr__(self, key):
        if key not in self._ops:
            raise AttributeError("The operator [{0}] is not registered".format(key))
        return self._ops[key]


Operators = OpsWrapper()


def register_all_ops(C=None):
    """register all operator"""
    Operators.reset()
    Operators.register(OpsList)

    if C:
        if getattr(C, "custom_ops", None) is not None:
            Operators.register(C.custom_ops)
            logger.debug("register custom operator {}".format(C.custom_ops))
