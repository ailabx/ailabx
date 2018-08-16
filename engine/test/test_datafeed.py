import unittest
from ..datafeed import *
from datetime import datetime

class TestDataFeed(unittest.TestCase):

    def __test_fetch_data(self):
        start_date = datetime(2010,1,1)
        end_date = datetime(2011,1,1)
        url = 'http://ailabx.com/kensho/quotes?code={}&start={}&end={}'.format(
            '600838,600519,000002',
            start_date.strftime('%Y%m%d'),
            end_date.strftime('%Y%m%d')
        )
        df = D.fetch_data(url)
        print(df.head())

        #加载maindata基本面数据
        url = 'http://www.ailabx.com/kensho/maindata?code={}&start={}&end={}'.format(
            '600519',
            start_date.strftime('%Y%m%d'),
            end_date.strftime('%Y%m%d')
        )
        df = D.fetch_data(url)
        print(df)

    def __test_load_benchmark(self):
        start_date = datetime(2010, 12, 29)
        end_date = datetime(2016, 1, 1)
        df = D.load_benchmark('000300', start_date, end_date)
        print(df.head())

    def test_load_datas(self):
        start_date = datetime(2016, 7, 15)
        end_date = datetime(2016, 9, 1)
        features = ['open_0/close_0','rank_return_1','rank_return_0','rank_return_0/rank_return_1']
        df = D.load_datas(['600519','600838','000002','000008'],start_date,end_date,features=features)
        print(df.head())

    def __test_instruments(self):
        start = datetime(2010, 1, 1)
        end = datetime(2017, 7, 19)
        instruments = D.instruments(start,end)
        print(len(instruments),instruments[:10])


    def __test_fundamentals(self):
        start = datetime(2016, 1, 1)
        end = datetime(2017, 1, 1)

        df = D.fundamentals('600519',start,end)
        print(df)

    def __test_fundamentals_quotes(self):
        start = datetime(2016, 1, 1)
        end = datetime(2017, 1, 1)

        df = D.fundamentals('600519', start, end)
        #print(df)

        df_quotes = D._load_data('600519',start,end)
        print(df_quotes)
