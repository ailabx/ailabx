# encoding:utf8
import backtrader as bt
from .algos import *
from loguru import logger
from engine.strategy.strategy_base import StrategyBase


class StratgeyAlgo(StrategyBase):
    def __init__(self, algos, algos_init=None):
        self.inds = {}
        if algos_init:
            for algo in algos_init:
                algo(self)

        self.algos = algos

    def next(self):
        context = {
            'strategy': self
        }
        run_algos(context, self.algos)
