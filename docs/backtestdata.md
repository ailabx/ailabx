## 量化回测引擎之DataHandler实现

还是在aiquant/engine/data.py下，继承DataHandler。

有几个关键点：
1，事件管理器，update_bars之后会触发onbar事件。

2，起止日期：回测周期

3，benchmark:参考标的，是某一个指数

4,universe需要重点说明，如果传入一个str型，代表取这个指数的成份股，比如000300是沪深300，如果传入list型，则代表一个股票池，一般是自己的自选股池。为None入代表沪深股票全集

5，针对benchmark指数的trading_days作循环。

6，每一个bar,会把数据缓存在symbol_bars_list，symbol_latest_bars里，前者是{'code':[bars(时间正序)]}，后者是{'code':bar}

7,沿着trading_day从起始时间开始，往终止时间。
```
class MongodbHandler(DataHandler):
    def __init__(self,events,start_date,end_date,benchmark='000300',universe='000300'):

        #如果universe是一个字符串，则代表指数，如果是[]，代表一个集合，为空则为全集
        if type(universe) is str:
            self.universe = list(pd.DataFrame(data_utils.get_index_components(universe))['code'])
        elif type(universe) is list:
            self.universe = universe
        else:
            self.universe = []

        self.events = events

        self.benchmark = Benchmark(benchmark,start_date,end_date)
        self.trading_days = self.benchmark.get_trading_days()

        self.update_index = 0

        self.symbol_bars_list = {}#这是{symbol:[]}
        self.symbol_latest_bars = {}#这是最近一天的{symbol:bar}


```

更新数据并触发onbar事件：

```
#这个函数向服务器请求新的bar，然后出发onbar事件，表示新一期收盘
    def update_bars(self):
        if self.update_index > (len(self.trading_days) -1):
            return False

        self.dt_current = self.trading_days[self.update_index]
        self.update_index += 1

        #这里查出当天的universe里的列表[{},{}]
        daily_datas = data_utils.get_prices_by_date(self.dt_current,self.universe)
        for data in daily_datas:
            code = data['code']
            if code not in self.symbol_bars_list.keys():
                self.symbol_bars_list[code] = []
            self.symbol_bars_list[code].append(data)
            self.symbol_latest_bars[code] = data

        self.symbol_latest_bars['date'] = self.dt_current
        self.events.put(BarEvent())
        return True
```

在数据预加载之后，提供接口供调用：
```
#取某symbol的最近N个bar，比如计算5日均线
    def get_latest_bars(self, symbol, N=1):
        try:
            bars_list = self.symbol_bars_list[symbol]
        except KeyError:
            print("symbol：%s没有被加载，请检查universe配置。"%(symbol))
        else:
            return bars_list[-N:]
```

至此，一个基于mongo数据库的数据管理器就搞定 了，只需要配置起始时间，就会每天从服务器读取k线数据并缓存在内存中供回测使用。而且这种方式，有效规避使用未来数据的问题。因为在当天收盘之前，是取不到后面的数据。

