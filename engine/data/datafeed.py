import pandas as pd

class DataFeed(object):
    def __init__(self):
        pass

class CSVDataFeed(DataFeed):
    def __init__(self,csv):
        data = pd.read_csv(csv)
        data.index =data['date'] #date,open,high,low,close,return
        data = data.sort_index()
        data['return'] = data['close']/data['close'].shift(1) - 1

        self.data = data
        print(self.data.head(),len(self.data))
        self.idx = 0

    def get_date_range(self):
        return self.data.index[0],self.data.index[-1]

    def reset(self):
        self.idx = 0

    def step(self):
        obs = self.data.iloc[self.idx]#.as_matrix()
        self.idx += 1
        done = self.idx >= len(self.data)
        return obs, done