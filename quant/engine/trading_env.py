'''
@author: 魏佳斌
@license: (C) Copyright 2018-2025, ailabx.com.

@contact: 86820609@qq.com
@file: trading_env.py
@time: 2018-10-08 17:17
@desc: 交易环境，可以支持：普通回测，机器学习/深度学习，深度强化学习的训练与回测，最终可支持
实盘交易

'''

from .portfolio import Portfolio

class TradingEnv(object):
    def __init__(self,data,init_cash=100000.0):
        self.context = {'universe': data.columns,
                        'total': init_cash, 'cash': init_cash,
                        'max_hold': 10  # 最大持仓数，默认为10支
                        }

        self.portfolio = Portfolio(data=data,init_cash=init_cash)

    def run_strategy(self,strategy):
        done = False
        observation = None
        while not done:
            actions = strategy(self)
            observation,reward,done,info = self.run_step(actions)

    #环境运行一步
    def run_step(self,actions):
        '''
        :param actions: 交易指令 {LONG:['AAPL',],FLAT:['BTC']}表示买入AAPL,卖出BTC
        :return: observation,reward,done,info
        '''
        target_shares = {'BTC':0,'AAPL':100}
        return self.portfolio.step(target_shares)