from abc import ABC

import gym
import numpy as np
from gym import spaces


class FinanceEnv(gym.Env, ABC):
    def __init__(self, symbols, df_features, df_returns, initial_amount=1000000):
        super(FinanceEnv, self).__init__()
        # 正则化，和=1，长度就是组合里的证券数量
        self.action_space = spaces.Box(low=0, high=1, shape=(len(symbols),))
        self.observation_space = spaces.Box(
            low=-np.inf,
            high=np.inf,
            shape=(len(symbols), len(df_features.columns)), dtype=np.float64
        )
        #print(self.observation_space)
        self.dates = list(df_features.index)
        self.df_features = df_features
        self.df_returns = df_returns
        self.initial_amount = initial_amount
        self.portfolio_value = initial_amount
        self.index = 0

    def reset(self):
        self.index = 0
        self.portfolio_value = self.initial_amount
        df = self.df_features.loc[self.dates[0]]
        print(df.values.shape)
        return df.values

    def step(self, actions):
        done = False
        if self.index >= len(self.dates) - 1:
            done = True
            print(self.reward)
            return self.state, self.reward, done, {}

        self.index += 1

        weights = self.softmax_normalization(actions)
        df_return = np.array(self.df_returns.loc[self.dates[self.index]]['return'])
        port_return = sum(df_return * np.array(weights))
        self.portfolio_value = self.portfolio_value * (1 + port_return)

        df = self.df_features.loc[self.dates[self.index], :]

        self.state = df.values
        self.reward = self.portfolio_value * 1.0

        return self.state, self.reward, done, {}

    def softmax_normalization(self, actions):
        numerator = np.exp(actions)
        denominator = np.sum(np.exp(actions))
        softmax_output = numerator / denominator
        return softmax_output


if __name__ == '__main__':
    from stable_baselines3.common.env_checker import check_env
    from stable_baselines3 import A2C
    from engine.datafeed.dataloader import Dataloader

    symbols = ['399006.SZ', '000300.SH']
    names = []
    fields = []

    features = []
    fields += ['Slope($close,20)']
    names += ['mom_slope']
    features += ['mom_slope']

    fields += ['KF($mom_slope)']
    names += ['kf_mom_slope']
    features += ['kf_mom_slope']

    fields += ["$close/Ref($close,1) - 1"]
    names += ['return']

    loader = Dataloader(symbols, names, fields, load_from_cache=True)
    data = loader.data
    data = data[data.index > '2010-06-02']
    df_features = data[names]
    df_return = data[['return']]
    print(df_features)
    env = FinanceEnv(symbols, df_features, df_return)
    # check_env(env)
    model = A2C("MlpPolicy", env)
    model.learn(total_timesteps=100000)
