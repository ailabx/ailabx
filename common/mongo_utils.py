import pymongo


def get_db(ip='127.0.0.1', port=27017):
    '''
    uri = "mongodb://{username}:{password}@{host}:{port}/?authMechanism=MONGODB-CR".format(
        username='read',
        password='read',
        host='ip',
        port=2020,
        # db_name='datalake'
    )
    '''

    db = pymongo.MongoClient(ip, port)['datalake']
    #db.authenticate('write', 'write')
    return db


def write_df(tb_name, df, db='datalake', drop_tb_if_exist=False):
    db = get_db()
    if drop_tb_if_exist:
        if tb_name in db.list_collection_names():
            db.drop_collection(tb_name)
    try:
        if len(df) == 0:
            print('长度为零')
        else:
            docs = df.to_dict(orient='records')
            get_db()[tb_name].insert_many(docs)
    except pymongo.errors.BulkWriteError as e:
        print(e)


def update_dict(tb_name, dict_data, key='ts_code', upsert=True):
    db = get_db()
    db[tb_name].update_one({key: dict_data[key]}, {'$set': dict_data}, upsert=upsert)


def get_etf_list(found_date=None, cols=['ts_code']):
    query = {'market': 'E', 'invest_type': {'$nin': ['货币型']}}
    if found_date:
        query['found_date'] = {'$lte': found_date}

    filter = {
        '_id': 0
    }
    if cols:
        for col in cols:
            filter[col] = 1

    items = get_db()['basic'].find(query, filter)
    items = list(items)
    return items


def get_fund_list(found_date=None, cols=['ts_code']):
    query = {'market': 'O', 'invest_type': {'$nin': ['货币型']}, 'name': {'$regex': '^(?!.*[I,E|C|定|个月|半年])'}}
    if found_date:
        query['found_date'] = {'$lte': found_date}

    filter = {
        '_id': 0
    }
    if cols:
        for col in cols:
            filter[col] = 1

    items = get_db()['basic'].find(query, filter)
    items = list(items)
    return items


if __name__ == '__main__':
    funds = get_fund_list('20180104', cols=['ts_code', 'name'])
    print(len(funds))
    print(funds)
