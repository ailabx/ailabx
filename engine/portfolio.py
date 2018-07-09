import numpy as np
class Trader(object):
    def __init__(self,period):
        self.idx = 0
        self.trading_cost = 0.0003
        self.actions = np.zeros(period)
        self.positions =np.zeros(period)
        self.prices = np.zeros(period)
    #单支证券的处理
    def step(self,action,bar):
        last_position = self.positions[self.idx-1] if self.idx > 0 else 0

        self.actions[self.idx] = action #记录当期的action,0：做空,1：平仓,2：做多
        self.positions[self.idx] = action - 1#执行指令后的仓位状态：-1：做空,0：未持仓,1：做多。
        self.prices[self.idx] = bar['close'] #记录当期收盘价

        trade_count = abs(self.positions[self.idx] - last_position)
        self.trades[self.idx] = trade_count #持仓如果有变化，则会发生交易费用，可以从做空到多，需要交易2次的成本
        self.costs[self.idx] = trade_count * self.trading_cost


class Portfolio(object):
    def __init__(self,peroid,init_cash=100000.0):
        self.init_cash = init_cash
        self.traders = {}
        self.cashs = np.zeros(peroid)
        self.cashs[0] = self.init_cash

    def step(self,actions,bars):
        for instru in actions.keys():
            bar = bars[instru]
            self.traders[instru].step(actions[instru],bar,self._calc_share(bar))

    def _calc_share(self,bar):
        current_cash= 0.0
        pass