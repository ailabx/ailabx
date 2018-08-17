from .common.mongo_utils import mongo
import pandas as pd
import re
import talib
import numpy as np
import requests
import json
from datetime import datetime
from .feature_parser import FeatureCalc
import datetime as dt



class DataFeed(object):
    def __init__(self):
        self.idx = 0
        self.calc = FeatureCalc()

    def get_benchmark_index(self):
        return self.df_benchmark.index

    def get_benchmark_return(self):
        return self.df_benchmark['return_0']

    #往前走一步，如果超过范围返回done
    def step(self):
        bars = {}
        for instrument in self.all_dfs.keys():
            bars[instrument] = self.all_dfs[instrument].iloc[self.idx]
        self.idx += 1
        done = self.idx >= len(self.all_dfs[self.benchmark])
        return bars, done


    def auto_label(self,df,hold_days=5):
        return_hold = 'return_hold'
        df[return_hold] = (df['close'].shift(-hold_days) / df['close'] - 1)

        label_name = return_hold
        df = df.dropna(axis=0, how='any', thresh=None)
        df['label'] = df[return_hold]*100 + 10 #[0,20]
        df['label'] = df['label'].apply(lambda x:int(x))
        return df

    #通过url,json方式从服务器获取数据,并做好排序等预处理
    def fetch_data(self,url):
        json_data = requests.get(url).json()
        if json_data['err_code'] != 0:
            print('fetch_data出错:{}-{}'.format(url,json_data['msg']))
            return None

        data = json.loads(json_data['data'])
        df = pd.DataFrame(data)

        if 'date' in df.columns:
            df.index = df['date']+ ' ' + df['code']
            df.sort_index(inplace=True)

        elif 'EndDate' in df.columns:
            df.index = df['EndDate']
            df.sort_index(inplace=True)
        return df

    def func_by_date(self,group):
        print(group)
        if self.features:
            group = self.calc.calc_by_eval(group,self.features,self.calc.extra_basic_features(self.features),rank_flag=True)
        return group

    def func_by_code_after_rank(self,group):
        group = self.calc.calc_by_eval(group,self.features,self.calc.extra_basic_features(self.features))
        return group

    def func_by_code(self,group,args):
        #print(group)
        #这里按code分组了，直接使用date作为index，这样才可以reindex
        group.index = group['date']
        #考虑到停牌的情况，需要index reindex一样
        if len(group) < len(self.df_benchmark):
            print('有停牌数据...')
            group = group.reindex(self.df_benchmark['date'],method='ffill')

        #把基本面数据eps,bps取回来，整合进去
        code = group['code'][0]
        df_data = self.fundamentals(code,args[0],args[1])
        df_data = df_data.reindex(group.index,method='ffill')
        group = group.join(df_data)
        #print('join之后',group)

        #计算pe/pb
        group['pe']=group['close']/group['EPS']
        group['pb'] = group['close']/group['NAPS']

        # 计算其他特征，比如amount_5,close_10
        if self.features:
            group = self.calc.calc_basic_features(group,self.features)

        group = self.auto_label(group,hold_days=5)

        #各组的index要不同，所以加上code
        #group.index = group['date'] + '_' + group['code']
        #print(group)
        return group

    def load_benchmark(self,code,start_date, end_date):
        # 加载benchmark
        url = 'http://ailabx.com/kensho/quotes?code={}&start={}&end={}&index=true'.format(
            code,
            start_date.strftime('%Y%m%d'),
            end_date.strftime('%Y%m%d')
        )
        df_benchmark = self.fetch_data(url)
        return df_benchmark

    #加载所有instruments的数据,放在一个dataframe里
    def load_datas(self,instruments,start_date, end_date,features=None, benchmark='000300'):
        self.features = features

        self.df_benchmark = self.load_benchmark(benchmark,start_date,end_date)

        codes = ','.join(instruments)
        url = 'http://ailabx.com/kensho/quotes?code={}&start={}&end={}'.format(
            codes,
            start_date.strftime('%Y%m%d'),
            end_date.strftime('%Y%m%d')
        )

        df = self.fetch_data(url)
        # todo :
        #这里可以分批——按code每次100支，即100*3年*252=7条左右获取，然后append在一起再运算
        #本地缓存，直接使用hdf5
        df.reset_index(drop=True,inplace=True)
        df = df.groupby(df['code']).apply(self.func_by_code,[start_date,end_date])
        df.reset_index(drop=True,inplace=True)
        df.index = df['date']+'_'+df['code']
        print('groupby之后============》',df.index)

        df.reset_index(drop=True, inplace=True)
        df = df.groupby(df['date'],as_index=False).apply(self.func_by_date)
        df = df.groupby(df['code'],as_index=False).apply(self.func_by_code_after_rank)
        df.index = df['date']
        df.sort_index(inplace=True)
        return df

    def instruments(self,start_date,end_date):
        url = 'http://www.ailabx.com/kensho/instruments?&start={}&end={}'.format(
            start_date.strftime('%Y%m%d'),
            end_date.strftime('%Y%m%d')
        )

        json_data = requests.get(url).json()
        data = json.loads(json_data['data'])
        df = pd.DataFrame(data)
        return list(df['code'])

    def fundamentals(self,code,start_date,end_date):
        start_date -= dt.timedelta(days=90)
        url = 'http://www.ailabx.com/kensho/maindata?code={}&start={}&end={}'.format(
            code,
            start_date.strftime('%Y%m%d'),
            end_date.strftime('%Y%m%d')
        )
        df = self.fetch_data(url)
        del df['code'],df['EndDate']
        return df

D = DataFeed()