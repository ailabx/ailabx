## 量化交易系统之数据管理器

### MongodbDataHandler

本来打算先写一个简单的，基于csv文件的数据管理器，考虑到真实应用，还是直接连接数据库吧。这里我们使用mongodb,使用mysql等关系数据库也是一样的。我们主要使用pandas的Dataframe作用数据结构。

### 具体实现

在aiquant/engine/data.py下，继承自抽象基类DataHandler，需要实现update_bars函数。

```
class MongodbHandler(DataHandler):
#events是事件管理器
#start,end是起止日期
#benchmark是回测的参考标的，一般是指数，比如上证综指或沪深300指数
    def __init__(self,events,start_date,end_date,benchmark='000300'):
    #交易日列表，这个需要从指数里取，在这里最好从banchmark里取，因为普通股票有存在停牌的可能，在某几个交易日无交易数据
        self.trading_days = []
        #我们的投资组合空间，只加载这里的数据，如果为空，则全部加载
        self.universe = []
        
        #handler内部数据结构
        self.symbol_bars_list = {}#这是{symbol:[]}
        self.symbol_latest_bars = {}#这是最近一天的{symbol:bar}
        
    def update_bars(self):
        #这里查出当天的universe里的列表[{},{}]
        daily_datas = data_utils.get_prices_by_date(self.dt_current,self.universe)

        #当天的数据，保存到两个内存数据结构里，方便strategy调用
        for data in daily_datas:
            code = data['code']
            if code not in self.symbol_bars.keys():
                self.symbol_bars[code] = []
            self.symbol_bars_list[code].append(data)
            self.symbol_latest_bars[code] = data
        
        #发生onbar事件，并返回True
        self.events.put(BarEvent())
        return True
```
在aiquant/data/data_utils.py里实现数据查询函数

```
#查询某个交易日下，codes指定的证券的k线
def get_prices_by_date(date,codes):
    items = query_docs('prices', {'code':{'$in':codes}, 'date': date})
    return list(items)

#返回格式如下：
                 _id        amount  close    code  com_code       date   high  \
0  000001_2017-12-05  2.301868e+09  13.30  000001         3 2017-12-05  13.49   
1  000002_2017-12-05  1.747241e+09  31.03  000002         6 2017-12-05  31.48   

    low   open       volume  
0  13.1  13.15  172368132.0  
1  30.2  30.60   56430201.0  

#查询这个日期周期内的k线数据
def get_prices_by_code(code,start_date,end_date):
    items = query_docs('price_no_restore', {'code': code, 'date': {'$gt': start_date,
                                                                       '$lt': end_date}})
    
#返回如下格式：
             _id       amount  close    code  com_code       date   high  \
0   000001_2016-06-29  319908690.0   8.69  000001         3 2016-06-29   8.69   
1   000001_2016-06-28  289122214.0   8.63  000001         3 2016-06-28   8.64   
2   000001_2016-06-27  280044073.0   8.61  000001         3 2016-06-27   8.64   
3   000001_2016-06-24  367771054.0   8.57  000001         3 2016-06-24   8.70   
4   000001_2016-06-23  290490407.0   8.66  000001         3 2016-06-23   8.70   
5   000001_2016-06-22  413947369.0   8.73  000001         3 2016-06-22   8.73   
6   000001_2016-06-21  327940703.0   8.61  000001         3 2016-06-21   8.65   
7   000001_2016-06-20  232205298.0   8.60  000001         3 2016-06-20   8.60   
8   000001_2016-06-17  270236698.0   8.58  000001         3 2016-06-17   8.61   
9   000001_2016-06-16  331192445.0   8.57  000001         3 2016-06-16   8.60   
10  000001_2016-06-15  394033686.0  10.44  000001         3 2016-06-15  10.48   
11  000001_2016-06-14  283578297.0  10.40  000001         3 2016-06-14  10.41 
```

上面还有提到一个BarEvent()，定义在aiquant/engine/event.py里
```
class Event(object):
    pass

#只有一个type，就是告知相关方，有一个新的bar到达，本身事件不传递数据结构，需要用到数据可以到DataHandler里去取。
class BarEvent(Event):
    def __init__(self):
        self.type = 'BAR'
```

关于作者：魏佳斌，互联网产品/技术总监，北京大学光华管理学院（MBA）,特许金融分析师（CFA），资深产品经理/码农。偏爱python，深度关注互联网趋势，人工智能，AI金融量化。致力于使用最前沿的认知技术去理解这个复杂的世界。
扫描下方二维码，关注：AI量化实验室（ailabx），了解AI量化最前沿技术、资讯。
