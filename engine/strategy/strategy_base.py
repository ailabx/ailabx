# encoding: utf8
import backtrader as bt
from loguru import logger
import pandas as pd


class StrategyBase(bt.Strategy):
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        logger.info('%s, %s' % (dt.isoformat(), txt))

    # 取当前的日期
    def get_current_dt(self):
        return self.datas[0].datetime.date(0).strftime('%Y-%m-%d')

    # 取当前持仓的data列表
    def get_current_holding_datas(self):
        holdings = []
        for data in self.datas:
            if self.getposition(data).size > 0:
                holdings.append(data)
        return holdings

    # 打印订单日志
    def notify_order(self, order):

        return

        order_status = ['Created', 'Submitted', 'Accepted', 'Partial',
                        'Completed', 'Canceled', 'Expired', 'Margin', 'Rejected']
        # 未被处理的订单
        if order.status in [order.Submitted, order.Accepted]:
            return
            self.log('未处理订单：订单号:%.0f, 标的: %s, 状态状态: %s' % (order.ref,
                                                           order.data._name,
                                                           order_status[order.status]))
            return
        # 已经处理的订单
        if order.status in [order.Partial, order.Completed]:
            return
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, 状态: %s, 订单号:%.0f, 标的: %s, 数量: %.2f, 价格: %.2f, 成本: %.2f, 手续费 %.2f' %
                    (order_status[order.status],  # 订单状态
                     order.ref,  # 订单编号
                     order.data._name,  # 股票名称
                     order.executed.size,  # 成交量
                     order.executed.price,  # 成交价
                     order.executed.value,  # 成交额
                     order.executed.comm))  # 佣金
            else:  # Sell
                self.log(
                    'SELL EXECUTED, status: %s, ref:%.0f, name: %s, Size: %.2f, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order_status[order.status],
                     order.ref,
                     order.data._name,
                     order.executed.size,
                     order.executed.price,
                     order.executed.value,
                     order.executed.comm))

        elif order.status in [order.Canceled, order.Margin, order.Rejected, order.Expired]:
            # order.Margin资金不足，订单无法成交
            # 订单未完成
            self.log('未完成订单，订单号:%.0f, 标的 : %s, 订单状态: %s' % (
                order.ref, order.data._name, order_status[order.status]))

        self.order = None

    def notify_trade(self, trade):
        logger.debug('trade......', trade.status)
        # 交易刚打开时
        if trade.justopened:
            self.log('开仓, 标的: %s, 股数: %.2f,价格: %.2f' % (
                trade.getdataname(), trade.size, trade.price))
        # 交易结束
        elif trade.isclosed:
            self.log('平仓, 标的: %s, GROSS %.2f, NET %.2f, 手续费 %.2f' % (
                trade.getdataname(), trade.pnl, trade.pnlcomm, trade.commission))
        # 更新交易状态
        else:
            self.log('交易更新, 标的: %s, 仓位: %.2f,价格: %.2f' % (
                trade.getdataname(), trade.size, trade.price))


class StratgeyAlgoBase(StrategyBase):
    def __init__(self, algo_list=None, features=None, extra=None):
        self.algos = algo_list
        self.features = features
        self.extra = extra

    def next(self):
        context = {
            'strategy': self,
            'features': self.features,
            'extra': self.extra
        }

        for algo in self.algos:
            if algo(context) is True:  # 如果algo返回True,直接不运行，本次不调仓
                return


class StrategyAdjustTable(StrategyBase):
    def __init__(self, weight_table):
        self.table = weight_table
        self.trade_dates = pd.to_datetime(self.table.index.unique()).tolist()

    def next(self):
        dt = self.datas[0].datetime.date(0)  # 获取当前的回测时间点
        # 如果是调仓日，则进行调仓操作
        if dt in self.trade_dates:
            dt_weight = self.table[self.table.index == dt]
            codes = dt_weight['code'].tolist()
            for code in codes:
                w = dt_weight.query(f"code=='{code}'")['weight'].iloc[0]  # 提取持仓权重
                data = self.getdatabyname(code)
                order = self.order_target_percent(data=data, target=w * 0.99)  # 为减少可用资金不足的情况，留 5% 的现金做备用
