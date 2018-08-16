from engine.backtest import M,SymbolRanker
from engine.datafeed import D
import unittest
from datetime import datetime

#context{'instruments':['instrument1',...]}

def handle_bar(bars,context):
    print('========================')
    #print(bars)
    #所有股票买入并持有
    actions = {'LONG':['600519']}
    return actions

class TestBacktest(unittest.TestCase):
    def test_ranker(self):
        instruments = ['600519', '000858','rank_return_0/rank_return_5']
        features = ['rank_pe_0']
        start = datetime(2017, 1, 1)
        end = datetime(2018, 1, 30)
        features_name = [feature.replace('/','_') for feature in features]
        dfs = D.load_datas(instruments, start, end,features=features)
        #df = dfs['600519']
        #df = df.dropna(axis=0, how='any', thresh=None)
        print(dfs.tail())

        ranker = SymbolRanker()
        train,test = ranker.split_datasets(dfs[features_name],dfs['label'])
        print(len(train[0]),len(test[0]))

        print(train[0].tail())
        print(train[1].tail())

        ranker.train(train[0][features_name],train[1].astype('int'))

    def __test_run(self):

        instruments = ['600519', '000858']
        features = ['return_0', 'return_4']
        start = datetime(2017, 1, 1)
        end = datetime(2017, 1, 30)

        D.load_data_with_features(instruments,features,start,end)

        M.run(handle_bar,D)