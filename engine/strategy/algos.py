# encoding: utf8
from loguru import logger
import pandas as pd
import abc


class RunOnce:
    def __init__(self):
        self.done = False

    def __call__(self, context):
        done = self.done
        self.done = True
        return done


class RunPeriod:

    def __call__(self, target):
        # get last date
        now = target['strategy'].datetime.date(0)
        last_date = target['strategy'].datetime.date(-1)
        date_to_compare = last_date
        now = pd.Timestamp(now)
        date_to_compare = pd.Timestamp(date_to_compare)

        result = self.compare_dates(now, date_to_compare)

        return result

    @abc.abstractmethod
    def compare_dates(self, now, date_to_compare):
        raise (NotImplementedError("RunPeriod Algo is an abstract class!"))


# https://github.com/pmorissette/bt/blob/master/bt/algos.py
class RunQuarterly(RunPeriod):

    def compare_dates(self, now, date_to_compare):
        if now.quarter != date_to_compare.quarter:
            return False
        return True


import backtrader as bt


class AddIndicators:
    def __call__(self, stra):
        for data in stra.datas:
            roc = bt.ind.RateOfChange(data, period=20)
            stra.inds[data] = {'mom': roc}


class SelectAll:
    def __call__(self, context):
        stra = context['strategy']
        context['selected'] = list(stra.datas)
        return False


class SelectBySignal:
    def __init__(self, buy_col='buy', sell_col='sell'):
        self.buy_col = buy_col
        self.sell_col = sell_col

    def __call__(self, context):
        stra = context['strategy']
        features = context['features']

        to_buy = []
        to_sell = []
        holding = []

        curr_date = stra.get_current_dt()
        if curr_date not in features.index:
            logger.error('日期不存在{}'.format(curr_date))
            return True

        bar = features.loc[curr_date]
        if type(bar) is pd.Series:
            bar = bar.to_frame().T

        for row_index, row in bar.iterrows():
            # print(row_index, row)
            symbol = row['code']
            data = stra.getdatabyname(symbol)

            if row[self.buy_col]:
                to_buy.append(data)
            if row[self.sell_col]:
                to_sell.append(data)

            if data in stra.get_current_holding_datas():
                holding.append(data)

        new_hold = list(set(to_buy + holding))
        for data in to_sell:
            if data in new_hold:
                new_hold.remove(data)

        context['selected'] = new_hold


def get_current_bar(context):
    stra = context['strategy']
    features = context['features']

    curr_date = stra.get_current_dt()
    if curr_date not in features.index:
        logger.error('日期不存在{}'.format(curr_date))
        return None

    bar = features.loc[curr_date]
    if type(bar) is pd.Series:
        bar = bar.to_frame().T
    return bar


class SelectTopK:
    def __init__(self, K=1, order_by='order_by', b_ascending=False):
        self.K = K
        self.order_by = order_by
        self.b_ascending = b_ascending

    def __call__(self, context):
        stra = context['strategy']
        features = context['features']

        if self.order_by not in features.columns:
            logger.error('排序字段{}未计算'.format(self.order_by))
            return

        bar = get_current_bar(context)
        if bar is None:
            logger.error('取不到bar')
            return True
        bar.sort_values(self.order_by, ascending=self.b_ascending, inplace=True)

        selected = []
        pre_selected = None
        if 'selected' in context:
            pre_selected = context['selected']
            del context['selected']

        # 当前全候选集
        # 按顺序往下选K个
        for code in list(bar.code):
            if pre_selected:
                if code in pre_selected:
                    selected.append(code)
            else:
                selected.append(code)
            if len(selected) >= self.K:
                break
        context['selected'] = selected


class PickTime:
    def __init__(self, benchmark='000300.SH', signal='signal'):
        self.benchmark = benchmark
        #self.buy = self.buy
        self.signal = signal

    def __call__(self, context):
        stra = context['strategy']
        extra = context['extra']
        df = extra[self.benchmark]

        if self.signal not in df.columns:
            logger.error('择时信号不存在')
            return True

        curr_date = stra.get_current_dt()
        if curr_date not in df.index:
            logger.error('日期不存在{}'.format(curr_date))
            return None

        bar = df.loc[curr_date]
        if type(bar) is pd.Series:
            bar = bar.to_frame().T

        if bar[self.signal][0]:
            logger.info('择时信号显示，平仓所有。')
            context['selected'] = []



class WeightEqually:
    def __init__(self):
        pass

    def __call__(self, context):
        selected = context["selected"]
        stra = context['strategy']

        # 若有持仓，但未入选，则平仓
        curr_holdings = stra.get_current_holding_datas()

        for data_holding in curr_holdings:
            # logger.info('已持仓：' + data_holding._name)
            if data_holding._name not in selected:
                stra.close(data_holding)

        N = len(selected)
        if N > 0:
            weight = 1 / N
            for data in selected:
                stra.order_target_percent(data, weight * 0.98)

        return False


class WeightFix:
    def __init__(self, weights):
        self.weights = weights

    def __call__(self, context):
        selected = context["selected"]
        stra = context['strategy']
        N = len(selected)
        if N != len(self.weights):
            logger.error('标的个数与权重个数不等')
            return True

        for data, w in zip(selected, self.weights):
            stra.order_target_percent(data, w)
        return False


from .algo_utils import *


class WeightRP:
    def __init__(self, returns_df, method=None, half=False):
        self.returns_df = returns_df
        self.method = method
        self.half = half

    def __call__(self, context):
        N = 240

        def get_train_set(change_time, df):
            """返回训练样本数据"""
            # change_time: 调仓时间
            change_time = pd.to_datetime(change_time)
            df = df.loc[df.index < change_time]
            df = df.iloc[-N:]  # 每个调仓前240个交易日
            return df

        selected = context["selected"]  # select算子返回的需要分配仓位的 data集合
        stra = context['strategy']

        dt = stra.get_current_dt()
        # print(dt)
        sub_df = get_train_set(dt, self.returns_df)

        one_cov_matrix = None
        if self.half:
            one_cov_matrix = calculate_half_cov_matrix(sub_df)
        else:
            one_cov_matrix = np.matrix(sub_df.cov() * N)

        # 1.计算协方差： 取调仓日 前N=240个交易日数据， one_cov_matrix = returns_df.cov()*240，return np.matrix(one_cov_matrix)

        # 2.计算RP权重
        weights = None
        if self.method and self.method == 'pca':
            weights = calculate_portfolio_weight(one_cov_matrix, risk_budget_objective=pca_risk_parity)
        else:
            weights = calculate_portfolio_weight(one_cov_matrix, risk_budget_objective=naive_risk_parity)
        # print(weights)

        # 按动量 加减分

        K = 10
        new_weights = []
        for data, w in zip(selected, weights):
            mom = stra.inds[data]['mom'][0]
            if mom >= 0.08:
                new_weights.append(w * K)
            elif mom < -0.0:
                new_weights.append(w / K)
            else:
                new_weights.append(w)

        new_weights = [w / sum(new_weights) for w in new_weights]
        print(weights, new_weights)

        for data, w in zip(selected, new_weights):
            stra.order_target_percent(data, w * 0.95)


def run_algos(context, algo_list):
    for algo in algo_list:
        if algo(context) is True:  # 如果algo返回True,直接不运行，本次不调仓
            return

    if 'selected' in context:
        del context['selected']
