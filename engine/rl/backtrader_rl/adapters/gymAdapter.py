import gym
from gym import spaces
from numpy import infty

class gymAdapter(gym.Env):

    def __init__(self,engine,**kwargs):
        super().__init__(**kwargs)
        self.engine = engine
        self.action_space = spaces.Discrete(3)
        self.engine.action_mapping = {"buy" : 2, "sell" : 0, "hold":1}
        self.observation_space = spaces.Box(low = 0,high = infty, shape = self.engine.state_shape)
        print(self.observation_space.shape)

    def step(self,action):
        observation, reward, self.terminated = self.engine.step(action)
        truncated = False
        info = {}
        return observation, reward, self.terminated, truncated, info

    def reset(self,seed = None, options = {}):
        observation = self.engine.reset(seed = seed,**options)
        info = {}
        return observation

    def render(self):
        if self.terminated:
            self.engine.plot()

    def close(self):
        self.engine.close()
