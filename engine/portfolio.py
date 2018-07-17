import numpy as np
import pandas as pd

#单支证券的管理
class Trader(object):
    def __init__(self,indexes):
        self.idx = -1 #step会把这个下标从0开始
        self.trading_cost = 0.0003
        self.df = pd.DataFrame(index=indexes)
        self.df['position'] = 0
        self.df['close'] = 0.0
        self.df['share'] = 0
        self.df['commission'] = 0.0

    def get_commission(self):
        return self.df['commission'][self.idx]

    def get_market_value(self):
        return self.df['share'][self.idx]*self.df['close'][self.idx]

    def __async(self,bar):
        idx = self.idx
        if idx > 0:
            self.df.iloc[idx] = self.df.iloc[idx-1]

        self.df.iloc[self.idx,self.df.columns.get_loc('commission')] = 0.0
        self.df.iloc[self.idx,self.df.columns.get_loc('close')] = bar['close']

    def flat(self,bar):
        if self.df['position'][self.idx] == 0:
            return

        last_share = self.df['share'][self.idx -1]
        self.df.iloc[self.idx,self.df.columns.get_loc('share')] = 0
        self.df.iloc[self.idx,self.df.columns.get_loc('position')] = 0
        value = last_share * bar['close']
        self.df.iloc[self.idx,self.df.columns.get_loc('commission')] = value*self.trading_cost

        #cash增量
        return value*(1-self.trading_cost)

    def step(self,bar):
        self.idx += 1
        self.__async(bar)

    def long_or_short(self,share,position,bar):
        #做多或空,需要前一期持仓状态为空仓
        last_pos = self.df['position'][self.idx - 1] if self.idx > 0 else 0
        if last_pos != 0:
            return 0 #已持仓，直接返回0

        df = self.df

        df.iloc[self.idx,df.columns.get_loc('share')] = share
        df.iloc[self.idx,df.columns.get_loc('position')] = position
        value = share*bar['close']
        df.iloc[self.idx,df.columns.get_loc('commission')]= value*self.trading_cost

        #cash减量
        cash = value*(1+self.trading_cost)
        return cash


class Portfolio(object):
    def __init__(self,indexes,init_cash=100000.0):
        self.init_cash = init_cash
        self.traders = {}
        self.df_portfolio = pd.DataFrame(index=indexes)

        self.df_portfolio['total'] = 0.0
        self.df_portfolio['cash'] = 0.0
        self.df_portfolio['commission'] = 0.0
        self.df_portfolio['symbols_value'] = 0.0

        df = self.df_portfolio

        df.iloc[0,df.columns.get_loc('cash')] = init_cash
        df.iloc[0,df.columns.get_loc('total')] = init_cash
        self.idx = -1

        self.traders = {'600519':Trader(indexes=indexes)}

    def __get_trader(self,symbol):
        if symbol in self.traders.keys():
            return self.traders[symbol]
        else:
            return None

    def __alloc_cash(self,symbols):
        if len(symbols) <= 0:return

        cash = self.df_portfolio['cash'][self.idx]
        ten_percent = cash / 10.0
        per_symbol = cash / len(symbols)

        #if per_symbol > ten_percent:
            #per_symbol =  ten_percent

        return per_symbol

    def __calc_share(self,bar,cash):
        share = cash / bar['close']
        #if share < 100:
        #    return 0
        return int(share)

    def step(self,orders,bars):
        self.idx += 1
        for symbol in self.traders.keys():
            trader = self.__get_trader(symbol)
            if trader:
                trader.step(bars[symbol])

        #当期收盘，订单其实是下期开盘价成交
        self.__sync_yesterday_data()

        #1,先处理平仓订单
        if 'FLAT' in orders.keys():
            flat_symbols = orders['FLAT']
            for symbol in flat_symbols:
                trader = self.__get_trader(symbol)
                if trader:
                    self.df_portfolio['cash'][self.idx] += trader.flat(bars[symbol])



        #2，处理多仓订单
        if 'LONG' in orders.keys():
            symbols = orders['LONG']
            cash = self.__alloc_cash(symbols)
            for symbol in symbols:
                trader = self.__get_trader(symbol)
                if trader:
                    share = self.__calc_share(bars[symbol],cash)
                    if share == 0:
                        print('symbol:{},cash:{}不够一手！'.format(symbol,str(cash)))
                        continue
                    self.df_portfolio.iloc[self.idx,self.df_portfolio.columns.get_loc('cash')] -= trader.long_or_short(share,1,bars[symbol])

        #3,更新组合市值
        self.__update_total_value()

    def __update_total_value(self):
        comission = 0.0
        symbols_value = 0.0
        for symbol in self.traders.keys():
            trader = self.__get_trader(symbol)
            if trader:
                comission += trader.get_commission()
                symbols_value += trader.get_market_value()

        self.df_portfolio['commission'][self.idx] = comission
        cash = self.df_portfolio['cash'][self.idx]
        self.df_portfolio.iloc[self.idx,self.df_portfolio.columns.get_loc("symbols_value")] = symbols_value
        self.df_portfolio.iloc[self.idx,self.df_portfolio.columns.get_loc('total')] = symbols_value + cash


    def __sync_yesterday_data(self):
        #当前是首期，不需要同步上期
        if self.idx <= 0:
            return
        self.df_portfolio.iloc[self.idx] = self.df_portfolio.iloc[self.idx - 1]

    def get_result_df(self):
        df = self.df_portfolio
        df['returns'] = df['total'] / df['total'].shift(1) - 1
        return df
