from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import pandas as pd

from random import randint

import backtrader as bt
from backtrader_rl.strategys import returnBasedStrategy
from backtrader_rl.utils import actionObserver,rewardObserver,cummulativeRewardObserver
from backtrader_rl.engines import  BTEngine
from backtrader_rl.adapters.gymAdapter import gymAdapter

# ================
# Defining constants
# ================

# the length of data points available to the agent at each step
LOOKBACK = 40


# ================
# Preparing test data
# ================

from pathlib import Path
root = Path().absolute()
file = "BNB_USDT_5m.csv"
df = pd.read_csv(Path(root,file),index_col=0)
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.set_index("timestamp",drop=True)
data = bt.feeds.PandasData(dataname=df)

engine = BTEngine(lookback = LOOKBACK)
engine.broker.set_cash(100)
engine.adddata(data)

# ================
# Defining the Strategy
# ================

# the strategy defines the reward schema
# the position based strategy uses the position PNL as a reward at each step 
engine.addstrategy(returnBasedStrategy)

# observeres allow us to peak into the actions taken by the agent over the episode
#engine.addobserver(actionObserver)
#engine.addobserver(rewardObserver)
#engine.addobserver(cummulativeRewardObserver)


# default backtrader observers also work just fine
#engine.addobserver(bt.observers.BuySell)
#engine.addobserver(bt.observers.Broker)
#engine.addobserver(bt.observers.Trades)


# ================
# use the openai gym environment
# ================

engine.reset()

terminated = False

rewards = []

while not terminated:
    engine.step(randint(0, 2))
    print(engine.broker.getvalue())
    observation, reward, terminated = engine.step(randint(0,2))
