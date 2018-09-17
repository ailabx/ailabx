import unittest
from quant.engine.tools import quandl
import os
class TestBroker(unittest.TestCase):
    def test_build(self):
        path = os.path.abspath(os.path.join(os.getcwd(), "../../data"))
        feed = quandl.build_feed("WIKI", ['AAPL','AMZN'], 2006, 2007, path)
        print(feed)
