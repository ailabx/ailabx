import unittest

from engine.models import StockRanker
from engine.datafeed.data_features import *
from datetime import datetime
from engine.datafeed.datasets import get_data

class TestStockTrainer(unittest.TestCase):
    def test_stock_trainer(self):
        start = datetime(2017, 1, 1)
        end = datetime(2017, 1, 31)
        features = ['return_0', 'return_4']
        df = feature_extractor('600519', features, start_date=start, end_date=end)
        df = auto_labeler(df, 'return', 5)
        print(df.head(10))

        df = df.dropna(axis=0,how='any',thresh=None)
        print(df.head(10))

        X = df[features]
        y = df['label'].astype('int')

        model = StockRanker('gbdt')
        X,y = get_data()
        model.train(X,y)
