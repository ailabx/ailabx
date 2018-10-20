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
            if self.idx >= (len(self.df) - 1):
                return True
            self.idx += 1

        self.now = list(self.df.index)[self.idx]
        return False

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


    def long_cash(self,cash):
        if cash <= 0:
            logger.info('long_cash的现金需要>0')
            return
        price = self.get_item('price')
        delta_pos = int(cash / price)
        target_share = delta_pos + self.get_item('position')
        return self.adjust_to_target_share(target_share=target_share)


    def adjust_to_target_share(self,target_share):
        if target_share < 0:
            return

        price = self.get_item('price')
        delta_pos = target_share - self.get_item('position')
        commission = price * abs(delta_pos) * self.commission_rate

        self.set_item('position',target_share)
        self.set_item('commission',commission)

        if delta_pos == 0:
            logger.info('有交易信号，仓位无变化')
        else:
            action = '买入' if delta_pos > 0 else '卖出'
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

    def update(self):
        done = self.update_idx()
        for symbol, broker in self.brokers.items():
            broker.onbar()
        self.__update_datas()
        return done

    def step(self,context):
        # 先处理FLAT
        if "FLAT" in context.keys():
            flats = context['FLAT']
            del context['FLAT']#处理完成要清掉，否则下次循环这个还在，strategy是没有变化
            target_shares = {flat:0 for flat in flats}
            if len(target_shares):
                self.__handle_orders(target_shares,type_of_func='target_share')


        if 'weights' in context.keys():
            weights = context['weights']
            del context['weights'] #处理完成要清掉，否则下次循环这个还在，strategy是没有变化
            cash = self.get_item('cash') * 0.98
            moneys = {symbol:cash*weight for symbol,weight in weights.items()}
            self.__handle_orders(moneys,type_of_func='cash')

    def __handle_orders(self,symbol_dict,type_of_func='target_share'):
        for symbol,value in symbol_dict.items():
            if symbol in self.brokers.keys():
                func = self.brokers[symbol].adjust_to_target_share
                if type_of_func == 'cash':
                    func = self.brokers[symbol].long_cash
                delta_cash, commission = func(value)
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


