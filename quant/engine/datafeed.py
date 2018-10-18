'''
@author: 魏佳斌
@license: (C) Copyright 2018-2025, ailabx.com.

@contact: 86820609@qq.com
@file: datafeed.py
@time: 2018-10-17 10:50
@desc: 实现交易数据获取，这里考虑最简化用户环境，暂不使用数据库，直接按年保存至本地csv。

'''
from .common.logging_utils import logger
import os
import pandas as pd
import datetime
from .common import csv_utils

def download_csv(sourceCode, tableCode, begin, end, frequency, authToken):
    url = "http://www.quandl.com/api/v1/datasets/%s/%s.csv" % (sourceCode, tableCode)
    params = {
        "trim_start": begin.strftime("%Y-%m-%d"),
        "trim_end": end.strftime("%Y-%m-%d"),
        "collapse": frequency
    }
    if authToken is not None:
        params["auth_token"] = authToken

    return csv_utils.download_csv(url, params)

def download_daily_bars(sourceCode, tableCode, year, csvFile, authToken=None):
    """Download daily bars from Quandl for a given year.

    :param sourceCode: The dataset's source code.
    :type sourceCode: string.
    :param tableCode: The dataset's table code.
    :type tableCode: string.
    :param year: The year.
    :type year: int.
    :param csvFile: The path to the CSV file to write.
    :type csvFile: string.
    :param authToken: Optional. An authentication token needed if you're doing more than 50 calls per day.
    :type authToken: string.
    """

    bars = download_csv(sourceCode, tableCode, datetime.date(year, 1, 1), datetime.date(year, 12, 31), "daily", authToken)
    f = open(csvFile, "w")
    f.write(bars)
    f.close()



class DataFeed(object):
    def __init__(self,data_path,source='quandl'):
        self.data_path = data_path
        self.source = source

    def __fetch_data(self,code,year):
        fileName = os.path.join(self.data_path, "%s-%d-quandl.csv" % (code, year))
        if not os.path.exists(fileName):
            logger.info("Downloading %d to %s" % (year, fileName))
            if self.source == 'quandl':
                self.__fetch_from_quanl(code,year,fileName)

        df = pd.read_csv(fileName).copy()
        df.index = df['Date']
        return df

    def __fetch_from_quanl(self,code,year,file_name,authToken=None):
        download_daily_bars('WIKI', code, year, file_name, authToken)

    def download_or_get_data(self,codes,from_year,to_year,authToken=None):
        #目录是否存在，如果不存在，则创建
        if not os.path.exists(self.data_path):
            logger.info("Creating %s directory" % (self.data_path))
            os.mkdir(self.data_path)

        all = {}
        for code in codes:

            all_code = []
            for year in range(from_year, to_year + 1):
                all_code.append(self.__fetch_data(code,year))

            df_code = pd.concat(all_code, axis=0)
            all[code] = df_code.sort_index()

        self.data = all
        return all

    def get_close_from_feed(self):
        all_close = []
        for code in self.data.keys():
            se = self.data[code]['Adj. Close']
            se.name = code
            all_close.append(se)

        all = pd.concat(all_close, axis=1)
        return all