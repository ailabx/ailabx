import tushare as ts
from engine.common.mongo_utils import mongo

def build_astock_index_quotes(index_code):
    start = '2010-01-01'
    end = '2017-12-31'
    df = ts.get_h_data(index_code, start=start, end=end, index=True)
    df['date'] = df.index
    df['code'] = index_code + '_index'
    df['_id'] = df['code'] + '_' + df['date'].apply(lambda x: str(x).replace(' 00:00:00', ''))
    mongo.insert_doc_or_docs('astock_daily_quotes', df.to_dict(orient='records'))


def build_astock_quotes():
    start = '2010-01-01'
    end = '2017-12-31'
    codes = ['601318','600519','600036','000333','000651',
             '601166','600016','600887','601328','600276','000858',
             '600030','002415','601288','600104','600000','601668','601398','000002','600900']

    for code in codes:
        print('当前采集:{}'.format(code))
        df = ts.get_h_data(code, start=start,end=end,drop_factor=False,autype=None)
        df['date'] = df.index
        df['code'] =  code
        df['_id'] = code + '_' + df['date'].apply(lambda x:str(x).replace(' 00:00:00',''))
        mongo.insert_doc_or_docs('astock_daily_quotes',df.to_dict(orient='records'))

if __name__ == '__main__':
    #build_astock_quotes()
    build_astock_index_quotes('000300')