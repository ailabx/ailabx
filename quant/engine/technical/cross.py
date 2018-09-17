import numpy as np
import pandas as pd

def ma(se,n):
    ma_n = se.rolling(n).mean()
    print(ma_n)
    return ma_n

def cross(fast, slow):
    data = pd.DataFrame(index=fast.index)
    data['signal'] = fast - slow  # data[fast] - data[slow]
    data['signal'] = np.where(data['signal'] > 0, 1, data['signal'])
    data['signal'] = np.where(data['signal'] < 0, -1, data['signal'])

    data['signal'] = data['signal'] - data['signal'].shift(1)
    data['signal'] = np.where(data['signal'] > 0, 1, data['signal'])
    data['signal'] = np.where(data['signal'] < 0, -1, data['signal'])
    return data['signal']


def cross_up(fast, slow):
    data = pd.DataFrame(index=fast.index)
    data['signal'] = fast - slow  # data[fast] - data[slow]
    data['signal'] = np.where(data['signal'] > 0, 1, data['signal'])
    data['signal'] = np.where(data['signal'] < 0, -1, data['signal'])

    data['signal'] = data['signal'] - data['signal'].shift(1)
    data['signal'] = np.where(data['signal'] > 0, 1, 0)
    #data['signal'] = np.where(data['signal'] < 0, -1, data['signal'])
    return data['signal']

def cross_down(fast, slow):
    data = pd.DataFrame(index=fast.index)
    data['signal'] = fast - slow  # data[fast] - data[slow]
    data['signal'] = np.where(data['signal'] > 0, 1, data['signal'])
    data['signal'] = np.where(data['signal'] < 0, -1, data['signal'])

    data['signal'] = data['signal'] - data['signal'].shift(1)
    #data['signal'] = np.where(data['signal'] > 0, 1, data['signal'])
    data['signal'] = np.where(data['signal'] < 0, -1,0)
    return data['signal']