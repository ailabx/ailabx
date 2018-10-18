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
    def __init__(self,feed,init_cash=100000.0):
        self.feed = feed
        self.all_close = feed.get_close_from_feed()
        self.context = {'universe': self.all_close.columns,
                        'total': init_cash, 'cash': init_cash,
                        'max_hold': 10,  # 最大持仓数，默认为10支
                        'idx':-1,
                        'now':None
                        }

        self.portfolio = Portfolio(data=self.all_close,init_cash=init_cash)

    def __update_env(self):
        self.context['idx'] = self.portfolio.idx
        self.context['now'] = self.portfolio.now

    def run_strategy(self,strategy):
        done = False
        observation = None
        while not done:
            done = self.portfolio.update()
            self.__update_env()
            #这里strategy会修改env.context
            strategy(self)
            observation,reward,info = self.run_step()

    #环境运行一步
    def run_step(self):
        '''
        :param actions: 交易指令 {LONG:['AAPL',],FLAT:['BTC']}表示买入AAPL,卖出BTC
        :return: observation,reward,done,info
        '''
        #target_shares = {'BTC':0,'AAPL':100}

        self.portfolio.step(self.context)


        observation = None
        reward = None
        info = None
        return observation,reward,info

    def weights_to_shares(self,weights):
        weights = {'AAPL':0.5,'AMZN':0.5}
        shares = {}
        cash = self.portfolio.get_item('cash')
        for k,v in weights.items():
            shares[k] = cash*v
