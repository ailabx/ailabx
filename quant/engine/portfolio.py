'''
@author: 魏佳斌
@license: (C) Copyright 2018-2025, ailabx.com.

@contact: 86820609@qq.com
@file: portfolio.py
@time: 2018-10-08 15:07重构
@desc: Portfolio负责记录整个投资组合的明细，而SymbolBroker记录了单支证券的具体信息

'''

import pandas as pd
from .common.logging_utils import logger

'''
SymbolBroker和Portfolio的基类，实现一些通用功能
'''
class BrokerBase(object):
    def update_idx(self):
        '''
        更新序列游标，以及now时间索引。初始值是None
        :return:
        '''
        if self.idx is None:
            self.idx = 0
        else:
            self.idx += 1
        self.now = list(self.df.index)[self.idx]

    def get_item(self,column,idx=None):
        '''
        :param column: dataframe的列名
        :param idx: 取某一行，默认idx是当前行，可以自行指定
        :return:
        '''
        if idx is None:
            idx = self.idx
        return self.df.iloc[idx, self.df.columns.get_loc(column)]

    def set_item(self,column,value,idx=None):
        '''
        :param column: dataframe的列名
        :param value: 新的值
        :param idx:
        :return:
        '''
        if idx is None:
            idx = self.idx
        self.df.iloc[idx, self.df.columns.get_loc(column)] = value

class SymbolBroker(BrokerBase):
    def __init__(self,code,prices,commission_rate=0.0008):
        '''

        :param code: 证券代码
        :param prices: pd.Series类型，证券的收盘价
        '''
        self.code = code
        self.prices = prices
        self.commission_rate = commission_rate
        self.df = pd.DataFrame(index=prices.index,columns=['price','position','commission'])
        self.df['price'] = prices
        self.df['code'] = code
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
        return self.adjust_to_target_shares(target_shares=0)

    def adjust_to_target_shares(self,target_shares):
        if target_shares < 0:
            return

        price = self.get_item('price')
        delta_pos = target_shares - self.get_item('position')
        commission = price * abs(delta_pos) * self.commission_rate

        self.set_item('position',target_shares)
        self.set_item('commission',commission)

        action = '买入' if delta_pos else '卖出'
        logger.info('{} - 以{}的价格，{}{}：{}股'.format(self.now,price, action,self.code, abs(delta_pos)))

        # 这里有一个问题，就是cash可能不够，这就需要在Portfolio计算买入份额时检查。
        return -delta_pos*price,commission

class Portfolio(BrokerBase):
    def __init__(self,data,init_cash=100000.0):
        self.data = data
        self.init_cash = init_cash
        self.brokers = {}
        for col in data.columns:
            self.brokers[col] = SymbolBroker(code=col,prices=data[col])

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

    def step(self,target_shares={}):
        self.update_idx()
        for symbol, broker in self.brokers.items():
            broker.onbar()
        self.__update_datas()

        self.__rebalance(target_shares)

        #idx是先移动，所以要减1
        done = self.idx >= (len(self.data) - 1)
        return done

    def __rebalance(self,target_shares):
        for symbol,share in target_shares.items():
            if symbol in self.brokers.keys():
                delta_cash, commission = self.brokers[symbol].adjust_to_target_shares(share)
                self.__update_cash_commission(delta_cash,commission)

    def __update_cash_commission(self,delta_cash,delta_commission):
        self.set_item('cash',self.get_item('cash') + delta_cash - delta_commission)
        self.set_item('commission',self.get_item('commission')+delta_commission)
        self.set_item('total',self.get_item('total') - delta_commission)


    def statistics(self):
        self.df['returns'] = self.df['total'] / self.df['total'].shift(1) - 1
        self.df['equity'] = (self.df['returns'] + 1).cumprod()

        dfs = []
        for name, broker in self.brokers.items():
            broker.df['trade'] = broker.df['position'] - broker.df['position'].shift(1).fillna(0)
            dfs.append(broker.df)
        all = pd.concat(dfs)

        return self.df,all


