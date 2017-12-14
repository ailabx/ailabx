## 量化回测系统之benchmark管理

### benchmark

投资结果如果也有考核的话，当然就是收益率的。但是收益率是相对的，比如说市场（大盘指数在一个周期跌了30%，那如果一个基金经理同期的业绩的-10%，那还算跑盈了大盘）。私募更多会看绝对收益率。更严格或者说对用户更合理的，应该是必须跑赢同期存款利率外加通胀（否则存银行就好了）。

所以做为一个量化系统，肯定需要一个benchmark做参照系。一般会取上证综指或沪深300指数。

在系统里，我们允许用户自己配置。

```
    code        name    change   preclose      close       high        low  \
0   000001    上证指数  -1.13   4527.396   4476.215   4572.391   4432.904
1   000002    Ａ股指数  -1.13   4744.093   4690.628   4791.534   4645.190
2   000003    Ｂ股指数  -2.15    403.694    395.018    405.795    392.173
3   000008    综合指数   0.79   3724.496   3753.906   3848.575   3695.817
4   000009   上证380  -2.79   7689.128   7474.305   7695.329   7398.911
5   000010   上证180  -1.13  10741.180  10619.610  10863.080  10529.900
6   000011    基金指数  -1.02   7033.291   6961.659   7058.856   6918.273
7   000012    国债指数   0.01    148.626    148.641    148.656    148.510
8   000016    上证50  -0.79   3308.454   3282.330   3370.025   3255.769
9   000017     新综指  -1.13   3826.013   3782.936   3864.307   3746.284
10  000300   沪深300  -1.37   4807.592   4741.861   4839.078   4703.567
11  399001    深证成指  -0.69  14809.424  14707.245  14979.810  14580.422
12  399002    深成指R  -0.69  17193.832  17075.202  17391.652  16927.959
13  399003    成份Ｂ指  -1.93   9027.079   8853.081   9013.194   8826.048
14  399004  深证100R  -1.79   5994.881   5887.414   6036.322   5832.431
15  399005    中小板指  -3.34   8935.338   8637.195   8953.813   8551.202
16  399006    创业板指  -2.17   2747.497   2687.974   2779.200   2650.425
17  399100   新 指 数  -2.77  10091.194   9811.256  10111.664   9718.085
18  399101    中小板综  -3.31  12792.057  12368.868  12800.453  12253.744
19  399106    深证综指  -2.76   2271.275   2208.561   2275.344   2187.897
20  399107    深证Ａ指  -2.77   2375.176   2309.466   2379.507   2287.784
21  399108    深证Ｂ指  -1.77   1398.244   1373.512   1397.996   1367.343
22  399333    中小板R  -3.34   9640.766   9319.085   9660.699   9226.304
23  399606    创业板R  -2.16   2828.251   2767.127   2861.040   2728.472
```
系统支持大部分的A股指数如上表。

在aiquant/engine/benchmark.py里新建类Benchmark

```
#初始化传入benchmark_code，比如000001为上证综指
#起止日期
class Benchmark(object):
    def __init__(self,benchmark_code,start_date,end_date):
        self.benchmark_code = benchmark_code
        self.start_date = start_date
        self.end_date = end_date
        #从服务器把benchmark的数据一次性加载到内存里
        self.load_benchmark_data()

    def load_benchmark_data(self):
        self.df_index_data = data_utils.get_prices_by_code(self.benchmark_code,self.start_date,self.end_date)
```

更新下取数据的函数,支持从指数表里读：
```
    #根据code和日期范围从表里取这个时间段的数据
def get_prices_by_code(code,start_date,end_date,index=False):
    if index:
        items = query_docs('index_prices', {'code': code, 'date': {'$gt': start_date,
                                                                       '$lt': end_date}})
    else:
        items = query_docs('stock_prices', {'code': code, 'date': {'$gt': start_date,
                                                                       '$lt': end_date}})
    return list(items)
```
    
这里有个小tip,股票股票存在停牌等事项，可能在某几天没有交易记录，所以交易日，从指数里取。

```
    #benchmark.py
    def get_trading_days(self):
        return list(self.df_index_data['date'])

    class MongodbHandler(DataHandler):
        ...
        def __init__(self,events,start_date,end_date,benchmark='000300'):
        
        self.benchmark = Benchmark(benchmark,start_date,end_date)
        self.trading_days = self.benchmark.get_trading_days()
```

### 自动化测试

对于一个计算型的系统，自动化单元测试是非常有必要的，因为很难通过观察去发现里边细小的错误。

通过系统加载的沪深300指数数据与网易财经的数据作对比，除了小数点上的区别，是对的。

```
import unittest
import queue
import math

from aiquant.engine.benchmark import Benchmark
from datetime import datetime

class TestBenchmark(unittest.TestCase):
    def setUp(self):
        events = queue.Queue()
        self.benchmark = Benchmark('000300',datetime(2016,7,1),datetime(2017,7,1))

    def testOnbar(self):
        data = self.benchmark.df_index_data

        #dataframe用iloc下标取行，各到是一个小的dataframe
        items = data.iloc[[0,1]].to_dict(orient='records')
        self.assertAlmostEqual(items[0]['close'],3154.20)
        self.assertLess(math.fabs(items[1]['open']-3136.39),0.01 )

```

