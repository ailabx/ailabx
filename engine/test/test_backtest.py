from engine.backtest import M
from engine.datafeed import D
import unittest
from datetime import datetime

def handle_bar(bars,context):
    print('========================')
    print(bars)

class TestBacktest(unittest.TestCase):
    def test_run(self):

        instruments = ['600519', '000858']
        features = ['return_0', 'return_4']
        start = datetime(2017, 1, 1)
        end = datetime(2017, 1, 30)

        D.load_data_with_features(instruments,features,start,end)

        M.run(handle_bar,D)