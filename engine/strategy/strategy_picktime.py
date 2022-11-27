import backtrader as bt
from .algos import *
from loguru import logger

from .strategy_base import StrategyBase


class StrategyPickTime(StrategyBase):
    params = (
        ('long', 252),
        ('short', 42),
    )

    def __init__(self):
        # bt.ind.EMA(self.data, period=self.p.ema_period)
        self.long = bt.ind.SMA(period=self.p.long)
        self.short = bt.ind.SMA(period=self.p.short)

    def next(self):
        if self.short[0] > self.long[0]:
            self.buy()
        else:
            self.close()
