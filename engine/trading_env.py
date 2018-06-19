#按照openai GYM的api结构，实现一个通用的交易env，可以用于传统策略驱动的量化，也可以方便接入深度强化学习

import numpy as np
import pandas as pd

class DataFeed(object):
    def __init__(self):
        pass

class CSVDataFeed(DataFeed):
    def __init__(self,csv):
        data = pd.read_csv(csv)
        data.index =data['date'] #date,open,high,low,close,return
        data = data.sort_index()
        data['return'] = data['close']/data['close'].shift(1) - 1

        self.data = data
        print(self.data.head(),len(self.data))
        self.idx = 0

    def reset(self):
        self.idx = 0

    def step(self):
        obs = self.data.iloc[self.idx]#.as_matrix()
        self.idx += 1
        done = self.idx >= len(self.data)
        return obs, done

class Portfolio(object):
    def __init__(self,period,trading_cost=0.0003):
        self.trading_cost = trading_cost
        self.period = period #回测总期数
        self.step = 0

        self.actions = np.zeros(period)
        self.positions = np.zeros(period)

        self.mkt_returns = np.zeros(period)
        self.portfolio_returns = np.zeros(period)

        self.navs = np.ones(period)
        self.mkt_navs = np.ones(period)
        self.costs = np.zeros(period)
        self.trades = np.zeros(period)

    def reset(self):
        self.step = 0
        self.actions.fill(0)
        self.positions.fill(0)

        self.mkt_returns.fill(0)
        self.portfolio_returns.fill(0)

        self.navs.fill(1)
        self.mkt_navs.fill(1)
        self.costs.fill(0)
        self.trades.fill(0)

    def update_first_step(self,action,ret=0.0):
        if self.step != 0:
            return

        self.mkt_navs[0] = 1
        self.navs[0] = 1
        self.trades[0] = abs(action-1)

        self.mkt_returns[0] = 0
        self.portfolio_returns[0] = 0


        self.actions[0] = action
        self.positions[0]  = action - 1
        trade_count = abs(action-1)
        self.costs[0] = trade_count *self.trading_cost

        self.reward = 0


    def update_step(self,action,ret):
        if self.step == 0:
            return

        self.mkt_returns[self.step] = ret

        self.actions[self.step] = action
        self.mkt_navs[self.step] = self.mkt_navs[self.step - 1] * (1+ret)
        self.reward = self.positions[self.step-1] *ret - self.costs[self.step-1]
        self.portfolio_returns[self.step] = self.reward

        self.navs[self.step] = self.navs[self.step-1]*(1+self.reward)

        self.positions[self.step] = action - 1
        trade_count = abs(self.positions[self.step] - self.positions[self.step -1])
        self.trades[self.step] = trade_count
        self.costs[self.step] = trade_count * self.trading_cost


    def update(self,action,observations):

        ret = observations['return']
        if self.step == 0:
            self.update_first_step(action,ret)
        else:
            self.update_step(action,ret)

        info = {'reward': self.reward, 'nav': self.navs[self.step], 'costs': self.costs[self.step]}
        self.step += 1
        return self.reward,info

    def to_df(self):
        """returns internal state in new dataframe """
        cols = ['actions', 'navs', 'mkt_navs', 'mkt_returns', 'portfolio_returns',
                'positions', 'costs', 'trades']
        # pdb.set_trace()
        df = pd.DataFrame({'actions': self.actions,     #策略行动
                           'navs': self.navs,           #证券净值
                           'mkt_navs': self.mkt_navs,   #市场净值

                           'mkt_returns': self.mkt_returns,
                           'portfolio_returns': self.portfolio_returns,

                           'positions': self.positions,  # 证券仓位
                           'costs': self.costs,  # eod costs
                           'trades': self.trades},  # eod trade
                          columns=cols)

        print(self.step)

        return df



class TradingSim(object) :
  #单证券交易模拟器

    def __init__(self, steps, trading_cost_bps = 1e-3, time_cost_bps = 1e-4):
        # invariant for object life
        self.trading_cost_bps = trading_cost_bps
        self.time_cost_bps    = time_cost_bps
        self.steps            = steps
        # change every step
        self.step             = 0
        self.actions          = np.zeros(self.steps)
        self.navs             = np.ones(self.steps)
        self.mkt_nav         = np.ones(self.steps)
        self.strat_retrns     = np.ones(self.steps)
        self.positions            = np.zeros(self.steps)
        self.costs            = np.zeros(self.steps)
        self.trades           = np.zeros(self.steps)
        self.mkt_retrns       = np.zeros(self.steps)

    def reset(self):
        self.step = 0
        self.actions.fill(0)
        self.navs.fill(1)
        self.mkt_nav.fill(1)
        self.strat_retrns.fill(0)
        self.positions.fill(0)
        self.costs.fill(0)
        self.trades.fill(0)
        self.mkt_retrns.fill(0)


    def do_step(self, action, retrn):

        #上一期的持仓状态,如果当前step==0，则持仓为0，即未持仓
        old_position = 0.0 if self.step == 0 else self.positions[self.step - 1]

        #上一步的持仓净值及市场净值
        old_nav = 1.0 if self.step == 0 else self.navs[self.step - 1]
        mkt_nav = 1.0 if self.step == 0 else self.mkt_nav[self.step - 1]


        self.mkt_retrns[self.step] = retrn  #回报率
        self.actions[self.step] = action    #行动

        '''
        SHORT (0)
        FLAT (1)
        LONG (2)
        '''

        self.positions[self.step] = action - 1 #(0,1,2)-1 => (-1,0,1) 持仓状态：做多是1,坐空是-1,0是FLAT不变
        self.trades[self.step] = self.positions[self.step] - old_position
        #trades是否交易，比如指令给出位置是1，而上一期也是1，则无状态改变，不需要交易。这里取舍空间为[-2,2]，可以跨两态
        #比如坐空到坐多

        #交易成本率
        trade_costs_pct = abs(self.trades[self.step]) * self.trading_cost_bps
        self.costs[self.step] = trade_costs_pct + self.time_cost_bps

        #奖励 = 上期持仓状态*回报率 - 交易成本
        reward = ((old_position * retrn) - self.costs[self.step])
        self.strat_retrns[self.step] = reward

        if self.step != 0:
            self.navs[self.step] = old_nav * (1 + self.strat_retrns[self.step - 1])
            self.mkt_nav[self.step] = mkt_nav * (1 + self.mkt_retrns[self.step - 1])

        info = {'reward': reward, 'nav': self.navs[self.step], 'costs': self.costs[self.step]}

        self.step += 1
        print(reward,info)
        return reward, info


class TradingEnv(object):
    def __init__(self):
        self.datafeed = CSVDataFeed(csv='../data/000300_index.csv')
        self.portfolio = Portfolio(period=len(self.datafeed.data))

    def reset(self):
        self.datafeed.reset()
        self.portfolio.reset()

    def step(self, action,observation,done):
        reward, info = self.portfolio.update(action,observation)

        # info = { 'reward': self.reward, 'nav':self.nav, 'costs':costs }
        return observation, reward, done, info

    #运行策略入口
    def run_strategy(self, strategy):

        #先读第一步的数据
        done = False
        while not done:
            observation, done = self.datafeed.step()

            action = strategy(observation, self)  # 调用策略函数

            observation, reward, done, info = self.step(action,observation,done)

            if done:
                print('done!!')

        df = self.portfolio.to_df()
        df.index = self.datafeed.data.index
        return df

import random
def sample():
    return random.sample([0,1,2],1)[0]
import matplotlib.pyplot as plt
if __name__ == '__main__':
    randomtrader = lambda o, e: sample()  # retail trader
    buyandhold = lambda o, e: 2  # 买入并持用，策略是一个函数，这里用lambda的形式
    env = TradingEnv()
    df = env.run_strategy(randomtrader)
    print(df.tail())
    df[['navs','mkt_navs']].plot(grid=True)
    plt.show()
