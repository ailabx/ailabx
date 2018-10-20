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
from .common.logging_utils import logger

class TradingEnv(object):
    def __init__(self,strategy,feed,init_cash=100000.0):
        self.feed = feed
        self.strategy = strategy
        self.init_cash = init_cash
        self.all_close = feed.get_close_from_feed()

        self.portfolio = Portfolio(data=self.all_close,init_cash=init_cash)
        self.__init_env()

    def get_statistics(self):
        df,all = self.portfolio.statistics()
        #print(df)
        period_returns = df['equity'][-1] - 1
        num_years = self.context['len'] / 252
        annual_returns = (1 + period_returns) ** (1 / num_years) - 1
        return {
            'period_returns':period_returns,
            'annual_returns':annual_returns,
            'equity':df['equity'],
            'returns':df['returns']
        }

    def plot(self):
        import matplotlib.pyplot as plt
        import matplotlib
        ret = self.get_statistics()
        ret['equity'].plot(title='买入并持有：净值曲线', legend=True, grid=True)

        from pylab import mpl
        mpl.rcParams['font.sans-serif'] = ['FangSong']  # 指定默认字体
        mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
        plt.show()

    def __init_env(self):
        self.context = {'universe': self.all_close.columns,
                        'total': self.init_cash,
                        'cash': self.init_cash,
                        'all_close':self.all_close,
                        'all_data':self.feed.data,
                        'max_hold': 10,  # 最大持仓数，默认为10支
                        'idx': -1,
                        'now': None,
                        'len':len(self.all_close)
                        }
        logger.info('回测日期从{}到{},一共{}期'.format(self.all_close.index[0],self.all_close.index[-1],len(self.all_close)))


    def __update_env(self):
        self.context['idx'] = self.portfolio.idx
        self.context['now'] = self.portfolio.now
        self.context['bar'] = self.all_close.iloc[self.context['idx']]

    def run_strategy(self):
        done = False
        observation = None
        while not done:
            observation,reward,done,info = self.run_step()
        logger.info('回测成功完成！')

    #环境运行一步
    def run_step(self):
        '''
        :param actions: 交易指令 {LONG:['AAPL',],FLAT:['BTC']}表示买入AAPL,卖出BTC
        :return: observation,reward,done,info
        '''
        #target_shares = {'BTC':0,'AAPL':100}
        from datetime import datetime
        #print(type(self.context['now']),self.context['now'])
        #if self.context['now'] == '2006-03-01':
            #print('ok')

        done = self.portfolio.update()
        self.__update_env()
        # 这里strategy会修改env.context
        self.strategy(self.context)
        self.portfolio.step(self.context)


        observation = None
        reward = None
        info = None
        return observation,reward,done,info
