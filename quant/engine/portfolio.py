import numpy as np
import pandas as pd
from .common.logging_utils import logger
from .algos import AlgoStack

class BrokerBase(object):
    def update_idx(self):
        if self.idx is None:
            self.idx = 0
        else:
            self.idx += 1
        self.now = list(self.df.index)[self.idx]

    def get_item(self,column,idx=None):
        if idx is None:
            idx = self.idx
        return self.df.iloc[idx, self.df.columns.get_loc(column)]
    def set_item(self,column,value,idx=None):
        if idx is None:
            idx = self.idx
        self.df.iloc[idx, self.df.columns.get_loc(column)] = value

class Broker(BrokerBase):
    def __init__(self,name,prices,strategy=None):
        self.name = name
        self.prices = prices
        self.strategy = strategy
        self.df = pd.DataFrame(index=prices.index,columns=['price','position','commission'])
        self.df['price'] = prices
        self.df['code'] = name
        self.df['position'] = None
        self.df['commission'] = None

        self.idx = None
        self.__last_position = None
        self.__last_commission = None


    def __update_datas(self):
        self.set_item('commission',0.0)
        if self.idx == 0:
            self.set_item('position',0)
        else:
            self.set_item('position', self.get_item('position',idx=self.idx - 1))


    def onbar(self):
        self.update_idx()
        self.__update_datas()

    def flat(self):
        share_to_sell = self.get_item('position')
        if share_to_sell == 0:
            return

        price = self.get_item('price')
        amount = share_to_sell * price

        self.set_item('position', 0)
        commission = amount*0.0008
        self.set_item('commission', commission )

        date = list(self.df.index)[self.idx]
        logger.info('{} - 以{}的价格，卖出:{}：{}股'.format(date,price,self.name,share_to_sell))

        if self.strategy:
            self.strategy.update_cash_commission(-amount,commission)

    def adjust(self,target_value):
        if target_value <= 0:
            return

        price = self.get_item('price')
        target_shares = int(target_value / price)

        delta_pos = target_shares - self.get_item('position')
        commssion = price * abs(delta_pos) * 0.0008
        self.set_item('position',target_shares)
        self.set_item('commission',commssion)
        action = '买入' if delta_pos else '卖出'
        date = list(self.df.index)[self.idx]
        logger.info('{} - 以{}的价格，{}{}：{}股'.format(date,price, action,self.name, abs(delta_pos)))

        if self.strategy:
            self.strategy.update_cash_commission(delta_pos*price,commssion)

class Strategy(BrokerBase):
    def __init__(self,data,algos=[],init_cash=100000.0):
        self.data = data
        self.stack = AlgoStack(*algos)
        self.init_cash = init_cash
        self.brokers = {}
        for col in data.columns:
            self.brokers[col] = Broker(name=col,prices=data[col],strategy=self)

        self.context = {'universe':data.columns,
                        'total':init_cash,'cash':init_cash,
                        'max_hold':10 #最大持仓数，默认为10支
                        }
        self.df = pd.DataFrame(index=data.index,columns=['total','cash','commission'])
        self.df['total'] = None
        self.df['cash'] =  None
        self.df['commission'] = None

        self.idx = None
        self.now = None

    def __calc_current_total(self):
        total = self.get_item('cash')
        for symbol,broker in self.brokers.items():
            total += broker.get_item('position') * broker.get_item('price')
        return total

    def __update_datas(self):
        self.set_item('commission',0.0)
        if self.idx == 0:
            self.set_item('cash',self.init_cash)
            self.set_item('total', self.init_cash)
        else:
            self.set_item('cash', self.get_item('cash',idx=self.idx - 1))
            self.set_item('total', self.__calc_current_total())

    def onbar(self):
        self.update_idx()
        for symbol, broker in self.brokers.items():
            broker.onbar()

        self.__update_datas()
        #执行模块化的算法
        self.stack(self)

    def rebalance(self,weights):
        cash = self.get_item('cash') * 0.99
        if 'FLAT' in self.context:
            flats = self.context['FLAT']
            for symbol in flats:
                if symbol in self.brokers.keys():
                    self.brokers[symbol].flat()

        for symbol,weight in weights.items():
            if symbol in self.brokers.keys():
                #调整至目标市值
                self.brokers[symbol].adjust(cash * weight)

    #提供给broker交易之后调用的
    def update_cash_commission(self,delta_cash,delta_commission):
        self.set_item('cash',self.get_item('cash') - delta_cash - delta_commission)
        self.set_item('commission',self.get_item('commission')+delta_commission)
        self.set_item('total',self.get_item('total') - delta_commission)


    #取组合收益率
    def get_returns(self):
        self.df['returns']= self.df['total']/self.df['total'].shift(1) - 1
        return self.df['returns']

    def get_equity(self):
        returns = self.get_returns()
        self.df['equity'] = (self.df['returns']+1).cumprod()
        #print(self.df['equity'])
        se = self.df['equity']
        return se

    def get_reports(self):
        dfs = []
        for name,broker in self.brokers.items():
            broker.df['trade'] = broker.df['position'] - broker.df['position'].shift(1).fillna(0)
            dfs.append(broker.df)
        all = pd.concat(dfs)
        return all


