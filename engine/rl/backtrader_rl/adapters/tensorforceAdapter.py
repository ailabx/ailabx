from tensorforce import Environment
from numpy import infty

class tensorforceAdapter(Environment):

    def __init__(self,engine,**kwargs):
        super().__init__(**kwargs)
        self.engine = engine

    def states(self):
        return dict(type='float', min_value = 0, shape=self.engine.state_shape)

    def actions(self):
        return dict(type='int', num_values=len(self.engine.actions_mapping))

    def close(self):
        self.engine.close()

    def reset(self,options = {}):
        observation = self.engine.reset(seed = None,**options)
        return observation

    def execute(self, actions):
        observation, reward, self.terminated = self.engine.step(actions)
        return observation, self.terminated, reward

    def plot(self):
        return self.engine.plot()