# encoding:utf8
import math
import random


# 状态空间
import numpy as np


class observation_space:
    def __init__(self, n):
        self.shape = (n,)


# 动作空间
class action_space:
    def __init__(self, n):
        self.n = n

    def seed(self, seed):
        pass

    def sample(self):
        return random.randint(0, self.n - 1)


class FinanceEnv:
    def __init__(self, symbols, features, df_features, lags=4, action_count=2,  min_performance=0.85):
        self.symbols = symbols
        self.features = features
        self.df_features = df_features

        self.observation_space = observation_space(lags)
        self.lags = lags # 滞后多少行
        self.min_performance = min_performance

        self.action_space = action_space(action_count)  # 动作维度
        #self.min_accuracy = min_accuracy  # 最低准确率

    def _get_state(self):
        state = self.df_features[self.features].iloc[
                self.index - self.lags:self.index]
        return state.values

    def seed(self, seed):
        random.seed(seed)
        np.random.seed(seed)

    def reset(self):
        self.treward = 0
        self.accuracy = 0
        self.performance = 1
        self.index = self.lags
        state = self.df_features[self.features].iloc[self.index -
                                               self.lags:self.index]
        return state.values

    def step(self, action):
        # 根据传入的动作，计算奖励reward
        correct = action == self.df_features['label'].iloc[self.index]
        ret = self.df_features['return'].iloc[self.index] #* self.leverage
        reward_1 = 1 if correct else 0
        reward_2 = abs(ret) if correct else -abs(ret)
        factor = 1 if correct else -1
        self.treward += reward_1
        self.index += 1
        self.accuracy = self.treward / (self.index - self.lags)
        self.performance *= math.exp(reward_2)
        if self.index >= len(self.df_features):
            done = True
        elif reward_1 == 1:
            done = False
        elif (self.performance < self.min_performance and
              self.index > self.lags + 5):
            done = True
        else:
            done = False
        state = self._get_state()
        info = {}
        return state, reward_1 + reward_2 * 5, done, info


if __name__ == '__main__':
    from engine.datafeed.dataloader import Dataloader
    from engine.model.dql_agent import DQLAgent

    names = []
    fields = []
    features = []
    symbols = ['000300.SH']

    fields += ['$close']
    names += ['close']

    fields += ['$close/Ref($close,1)-1']
    names += ['return']

    fields += ['If($return>0,1,0)']
    names += ['label']

    features += ['close']

    all = Dataloader().load_one_df(symbols, names, fields)
    print(all)
    env = FinanceEnv(symbols, features, all)
    print(env.reset(), env.reset().shape)
    a = env.action_space.sample()
    print(a)
    state, reward, done, info = env.step(a)
    print('state', state)
    print(reward, done, info)
    agent = DQLAgent(env=env, finish=True)
    agent.learn(1000)
