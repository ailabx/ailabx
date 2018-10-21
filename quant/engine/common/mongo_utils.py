import pymongo

class MongoMgr(object):
    def __init__(self,db_name='astock'):
        self.mongo_connect = pymongo.MongoClient('47.94.133.21', 27017)[db_name]
        #self.mongo_connect.authenticate('', '')

    # 添加文档或文档集合
    def insert_doc_or_docs(self,table_name, doc_or_docs):
        try:
            self.mongo_connect[table_name].insert(doc_or_docs, continue_on_error=True)
        except pymongo.errors.DuplicateKeyError:
            pass

    # 文档查询,返回是结果的cursor，可以直接遍历，或list(cur)转成列表，一次读出
    def query_docs(self,table_name, query, filter=None, page=None, page_size=None, sort=None, sort_dir=pymongo.DESCENDING):
        items = self.mongo_connect[table_name].find(query, filter)
        if sort:
            items = items.sort(sort, sort_dir)

        if page is not None and page_size:
            items = items.skip(page * page_size).limit(page_size)
        return items

    # 给指定表的指定列加索引
    def ensure_index(self,table_name, col):
        self.mongo_connect[table_name].ensure_index(col)

    # 查看索引
    def show_index(self,table_name):
        return self.mongo_connect[table_name].index_information()

    def query_count(self,table_name, query):
        count = self.mongo_connect[table_name].count(query)
        return count

    def update_batch(self,table_name, query, data):
        self.mongo_connect[table_name].update(query, {'$set': data}, multi=True)

mongo = MongoMgr()

if __name__ == '__main__':
    docs = [
        {'_id': 8, 'data': 88},
        {'_id': 9, 'data': 99},
        {'_id': 36, 'data': 3366}
    ]
    mongo.insert_doc_or_docs('test_table',docs)
    mongo.insert_doc_or_docs('test_table',{'_id':'ok2','msg':'hello mongo'})

    items = mongo.query_docs('test_table',{})
    for item in items:
        print(item)

    mongo.ensure_index('test_table','data')
    print(mongo.show_index('test_table'))


