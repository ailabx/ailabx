## 量化回测系统的设计

### 背景介绍

在智能投顾（投资为目的）的大体系里，回测系统是一个必要的存在。因为无论是基本面，技术面，或者其他策略，都需要在回测系统里验证想法。

这是任何一个其他行业不具备的优势。我们可以不必真的经历一个周期，等待漫长的时间，浪费大量的时间甚至是真金白银去寻一个结果。

市场上，尤其的python领域里的回测框架已经很多了。rqalpha, zipline,pyalgotrade等等，还有很多小的平台，和可编程的量化社区，比如ricequant,joinquant等。

有没必要自己弄一个，仁者见仁吧。

自己实现一个回测系统至少有如下好处：

1，深度理解系统的运行，比如收益率，夏普比，风险是如何计算的，交易成本是如何计算的等等。

2，数据来源的整合。可以最优化整合自己的数据源吧。

3，可以与自己的其他框架深度整合，比如要实现自动参数优化，因子学习。

### 系统设计

回测过程，本身并不复杂，其实使用pandas直接就可以完成，不使用循环处理每天数据。当然这是对于简单的策略，比如当5日均线上穿收盘价格时，买入，反之卖出这样的一个策略。用pandas的DataFrame会相当的简洁且易于理解。

但对于较复杂的逻辑，对于投资组合的管理，需要分析当下的各种财务数据，甚至宏观经济，舆情数据，那这种方式就心有余而力不足了。

所以，我们都会按交易周期去遍历，比如按日K线。模拟真实场景，去发现交易信号，产生订单，并执行交易。

业内通行的做法是“事件驱动”。这个很好理解，事件驱动有利于系统解耦合。对于上游组件，比如策略发现交易信号，就产生一个“信号事件”即可。至于谁应该响应并处理，以及处理结果，都不管。每个模块各司其职。另一个好处就是好扩展，无论是扩展事件类型，还是有更多模型需要响应已有的事件。

### 系统实现

我们实现的系统叫aiquant，传统quant，主要是根据自己的经验，想法去实现策略。这很考验策略所有者的能力，眼界，和系统或者说量化的关系不那么大，也就是说，系统与量化不是最重要的，重要的反倒是策略的想法与经验。

我们的目的就是要把选因子，或者调参这种事情，应该交给人工智能。这才是真正的智能投顾。所以我们叫aiquant。

aiquant包下有engine包，我们在aiquant/engine/backtest.py里实现我们回测系统主类Backtest。

```
class Backtest(object):
    #构造backtest引擎时，传入策略类（在init后续实例化，因为需要把context传递给它。）
    #bars是数据管理单元
    #另外两个参数是回测的时间范围
    def __init__(self,strategy_cls,bars,start_date=None,end_date=None):
        #事件处理器
        self.events = queue.Queue()
        self.bars = bars
        
    #主系统入口,每次loop，都会让bars触发新的bar事件，即有一个新bar到达
    def run(self):
        while self.bars.update_bars():
            #可能有多事件，要处理完，如果队列暂时是空的，不处理
            while True:
                #队列为空则消息循环结束
                try:
                    event = self.events.get(False)
                except queue.Empty:
                    break
                else:
                   self.handle_event(event)
        
     def handle_event(self,event):
         pass
    
```
这里用到了一个数据管理类bars,在aiquant/engine/data.py里实现。

```
class DataHandler(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def update_bars(self):
        #更新周期的bar，比如加一根k线，表示当期收盘了
        raise NotImplementedError("没有实现update_bars()")
```

在data.py里我们继承DataHandler并实现它，这里我们先实现一个简单的本地csv文件作为数据源的版本。

```
 '''
events:事件，onbar会触发事件
csv_dir，csv文件所在目录
symbol_list是需要加载的symbol列表，比如['680008',xxxx]
'''
class CSVDataHandler(DataHandler):
    def __init__(self,events,csv_dir,symbol_list):
        pass
    
    def update_bars(self):
    """
    把symbol_list里的symbol最近一个bar装入
        """
        pass
```
