import backtrader as bt
import numpy as np

class BaseStrategy(bt.Strategy):

    def __init__(self):
        self.action = 1
        self.reward = 0
        self._mapping = {"buy" : 2, "sell" : 0, "hold":1}

    def _set_action_mapping(self,mapping):
        self._mapping = mapping

    def _setAction(self,action):
        self.action = action

    def next(self):
        if len(self._mapping) == 2:
            if self.action == self._mapping["buy"]:
                # if current position is sell
                # then we are reversing the trade
                if self.position.size < 0:
                    self.buy(size = 2 * abs(self.position.size))
                elif self.position.size == 0:
                    self.buy()
            elif self.action == self._mapping["sell"]:
                # if current position is buy
                # then we are closing a trade
                if self.position.size > 0:
                    self.sell(size = 2 * abs(self.position.size))
                elif self.position.size == 0:
                    self.sell()  
            elif self.action == -1:
                pass      

        else:

            if self.action == self._mapping["buy"]:
                # if current position is sell
                # then we are closing a trade
                if self.position.size < 0:
                    self.close()
                elif self.position.size == 0:
                    self.buy()
            elif self.action == self._mapping["sell"]:
                # if current position is buy
                # then we are closing a trade
                if self.position.size > 0:
                    self.close()
                elif self.position.size == 0:
                    self.sell()  
            elif self.action == -1:
                pass      

    def _computeReward(self):
        try:
            reward = self.computeReward()
        except:
            reward = 0
        self.reward = reward
        return self.reward

class PositionBasedStrategy(BaseStrategy):

    def computeReward(self):
        if self.position.size == 0:
            return 0

        a = self.position.price
        b = self.datas[0].close[0]
        d = (b-a)/((b+a)/2)
        return d * 100 * (self.position.size/abs(self.position.size))

class returnBasedStrategy(BaseStrategy):

    def start(self):
        self.start_value = self.broker.get_value()

    def computeReward(self):

        return (self.broker.get_value()-self.start_value)/self.start_value * 100

class SharpRatioStrategy(BaseStrategy):

    params = (("riskfree_rate" , 0),)

    def computeReward(self):
        trades = list(list(self._trades.copy().values())[0].values())[0]
        filterd_trades = list(filter(lambda x : x.isclosed, trades))
        
        if len(filterd_trades) < 1:
            return 0

        ret = list(map(lambda x : ((x.pnl/x.price) * 100) - self.p.riskfree_rate, filterd_trades))

        if np.std(ret) == 0:
            return 0

        sharp_ratio = np.mean(ret)/np.std(ret)

        return sharp_ratio

class SortinoRatioStrategy(BaseStrategy):

    params = (("riskfree_rate" , 0),)

    def computeReward(self):
        trades = list(list(self._trades.copy().values())[0].values())[0]
        filterd_trades = list(filter(lambda x : x.isclosed, trades))
        
        if len(filterd_trades) < 1:
            return 0

        ret = list(map(lambda x : ((x.pnl/x.price) * 100) - self.p.riskfree_rate, filterd_trades))
        

        downside_ret = list(filter(lambda x : x < 0, ret))

        if len(downside_ret) < 1 or np.std(downside_ret) == 0:
            return 0

        sharp_ratio = np.mean(ret)/np.std(downside_ret)

        return sharp_ratio