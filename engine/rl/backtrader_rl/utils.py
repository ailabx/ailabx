import backtrader as bt

class minPeriodIndicator(bt.Indicator):
    lines = ("state",)
    params = (('period',5),)
    plotinfo = dict(plot = False,
                    subplot=False)
                    
    def __init__(self) -> None:
        self.addminperiod(self.params.period+1)

class rewardObserver(bt.Observer):
    alias = ("reward",)
    lines = ("rewards",)
    plotinfo = dict(plot=True,
                    subplot=True,
                    plotname = "Reward")

    def next(self):
        self.lines.rewards[0] = self._owner.reward

class cummulativeRewardObserver(bt.Observer):
    alias = ("cummulativeReward",)
    lines = ("cummulativeRewards",)
    plotinfo = dict(plot=True,
                    subplot=True,
                    plotname = "Cumulative Reward")

    def next(self):
        if len(self.lines.cummulativeRewards) == 1:
            self.lines.cummulativeRewards[0] = self._owner.reward
        else:
            self.lines.cummulativeRewards[0] = self.lines.cummulativeRewards[-1] + self._owner.reward

class RewardAnalyzer(bt.Analyzer):

    def __init__(self):
        self.cummulative_reward = 0
        self.reward_history = []

    def next(self):
        self.reward_history.append(self.strategy.reward)
        self.cummulative_reward += self.strategy.reward

    def get_analysis(self):
        return dict(cummulative_reward = self.cummulative_reward, reward_history = self.reward_history)

class actionObserver(bt.Observer):
    alias = ("action",)
    lines = ("actions",)
    
    plotinfo = dict(plot=True,
                    subplot=True,
                    plotname = "Action Space",
                    plotyticks=(0,1,2),
                    plothlines = (0,1,2))

    def next(self):
        self.lines.actions[0] = self._owner.action
