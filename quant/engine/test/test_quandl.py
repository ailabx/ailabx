import unittest
from quant.engine.datafeed import DataFeed

import os
class TestBroker(unittest.TestCase):
    def test_build(self):
        path = os.path.abspath(os.path.join(os.getcwd(), "../../data"))
        feed = DataFeed(data_path=path).download_or_get_data(['AAPL','AMZN'], 2006, 2007)
        self.assertEqual(len(feed),2)

        for code,bars in feed.items():
            print(bars.head())

        #close = quandl.get_close_from_feed(feed)
        #print(close.head())
