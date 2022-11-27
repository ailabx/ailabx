import gym
import numpy as np
from gym import spaces
from stable_baselines3 import A2C


class FinanceEnv(gym.Env):
    metadata = {"render.modes": ["human"]}

    def __init__(self):
        super(FinanceEnv, self).__init__()
        # 定义动作与状态空间，都是gym.spaces 对象
        # 例：使用离散空间:
        N_DISCRETE_ACTIONS = 2
        self.action_space = spaces.Discrete(N_DISCRETE_ACTIONS)
        # Example for using image as input (channel-first; channel-last also works):

        #N_CHANNELS = 3
        rows = 28
        cols = 28
        self.observation_space = spaces.Box(low=0, high=255,
                                            shape=(rows,), dtype=np.uint8)

    def step(self, action):
        observation = self.observation_space.sample()
        reward = 1.0
        done = True
        info = {}
        return observation, reward, done, info

    def reset(self):
        observation = self.observation_space.sample()
        #print(observation)
        return observation  # reward, done, info can't be included

    def render(self, mode="human"):
        pass

    def close(self):
        pass


if __name__ == '__main__':
    from stable_baselines3.common.env_checker import check_env

    env = FinanceEnv()
    check_env(env)
    model = A2C("MlpPolicy", env).learn(total_timesteps=1000)
