import gym

from engine.rl.clock import Clock


class FinanceEnv(gym.Env):
    def __init__(self,
                 action_scheme: ActionScheme,
                 reward_scheme: RewardScheme,
                 observer: Observer,
                 stopper: Stopper,
                 informer: Informer,
                 renderer: Renderer,
                 ):

        self.action_scheme = action_scheme
        self.reward_scheme = reward_scheme
        self.observer = observer
        self.stopper = stopper
        self.informer = informer
        self.renderer = renderer

        # 就是游标管理
        self.clock = Clock()

        super(FinanceEnv, self).__init__()

    def step(self, action):
        # 行动计划 执行动作
        self.action_scheme.perform(self, action)
        # 观察者 反馈动作执行后的状态
        obs = self.observer.observe(self)
        # 激励计划得到reward
        reward = self.reward_scheme.reward(self)
        # stopper决定任务是否结束
        done = self.stopper.stop(self)
        # infomer是给出信息
        info = self.informer.info(self)

        self.clock.increment()

        return obs, reward, done, info

