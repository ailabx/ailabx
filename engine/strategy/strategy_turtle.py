import backtrader as bt
from engine.strategy.strategy_base import StrategyBase


class TurtleTradingStrategy(StrategyBase):
    params = dict(
        N1=20,  # 唐奇安通道上轨的t
        N2=10,  # 唐奇安通道下轨的t
    )

    def __init__(self):
        self.order = None
        self.buy_count = 0  # 记录买入次数
        self.last_price = 0  # 记录买入价格
        # 准备第一个标的沪深300主力合约的close、high、low 行情数据
        self.close = self.datas[0].close
        self.high = self.datas[0].high
        self.low = self.datas[0].low
        # 计算唐奇安通道上轨：过去20日的最高价
        self.DonchianH = bt.ind.Highest(self.high(-1), period=self.p.N1, subplot=True)
        # 计算唐奇安通道下轨：过去10日的最低价
        self.DonchianL = bt.ind.Lowest(self.low(-1), period=self.p.N2, subplot=True)
        # 生成唐奇安通道上轨突破：close>DonchianH，取值为1.0；反之为 -1.0
        self.CrossoverH = bt.ind.CrossOver(self.close(0), self.DonchianH, subplot=False)
        # 生成唐奇安通道下轨突破:
        self.CrossoverL = bt.ind.CrossOver(self.close(0), self.DonchianL, subplot=False)
        # 计算 ATR
        self.TR = bt.ind.Max((self.high(0) - self.low(0)),  # 当日最高价-当日最低价
                             abs(self.high(0) - self.close(-1)),  # abs(当日最高价?前一日收盘价)
                             abs(self.low(0) - self.close(-1)))  # abs(当日最低价-前一日收盘价)
        self.ATR = bt.ind.SimpleMovingAverage(self.TR, period=self.p.N1, subplot=False)
        # 计算 ATR，直接调用 talib ，使用前需要安装 python3 -m pip install TA-Lib
        # self.ATR = bt.talib.ATR(self.high, self.low, self.close, timeperiod=self.p.N1, subplot=True)

    def next(self):
        # 如果还有订单在执行中，就不做新的仓位调整
        if self.order:
            return

            # 如果当前持有多单
        if self.position.size > 0:
            # 多单加仓:价格上涨了买入价的0.5的ATR且加仓次数少于等于3次
            if self.datas[0].close > self.last_price + 0.5 * self.ATR[0] and self.buy_count <= 4:
                print('if self.datas[0].close >self.last_price + 0.5*self.ATR[0] and self.buy_count <= 4:')
                print('self.buy_count', self.buy_count)
                # 计算建仓单位：self.ATR*期货合约乘数300*保证金比例0.1
                self.buy_unit = max((self.broker.getvalue() * 0.01) / self.ATR[0], 1)
                self.buy_unit = int(self.buy_unit)  # 交易单位为手
                # self.sizer.p.stake = self.buy_unit
                self.order = self.buy(size=self.buy_unit)
                self.last_price = self.position.price  # 获取买入价格
                self.buy_count = self.buy_count + 1
            # 多单止损：当价格回落2倍ATR时止损平仓
            elif self.datas[0].close < (self.last_price - 2 * self.ATR[0]):
                print('elif self.datas[0].close < (self.last_price - 2*self.ATR[0]):')
                self.order = self.sell(size=abs(self.position.size))
                self.buy_count = 0
            # 多单止盈：当价格突破10日最低点时止盈离场 平仓
            elif self.CrossoverL < 0:
                print('self.CrossoverL < 0')
                self.order = self.sell(size=abs(self.position.size))
                self.buy_count = 0

                # 如果当前持有空单

        else:  # 如果没有持仓，等待入场时机
            # 入场: 价格突破上轨线且空仓时，做多
            if self.CrossoverH > 0 and self.buy_count == 0:
                print('if self.CrossoverH > 0 and self.buy_count == 0:')
                # 计算建仓单位：self.ATR*期货合约乘数300*保证金比例0.1
                self.buy_unit = max((self.broker.getvalue() * 0.01) / self.ATR[0], 1)
                self.buy_unit = int(self.buy_unit)  # 交易单位为手
                self.order = self.buy(size=self.buy_unit)
                self.last_price = self.position.price  # 记录买入价格
                self.buy_count = 1  # 记录本次交易价格
            # 入场: 价格跌破下轨线且空仓时
            elif self.CrossoverL < 0 and self.buy_count == 0:
                print('self.CrossoverL < 0 and self.buy_count == 0')

