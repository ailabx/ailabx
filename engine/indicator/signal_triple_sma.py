import backtrader as bt


# 自定义信号指标
class SignalTripleSMA(bt.Indicator):
    lines = ('signal',)  # 声明 signal 线，交易信号放在 signal line 上
    params = dict(
        short_period=5,
        median_period=20,
        long_period=60)

    def __init__(self):
        self.s_ma = bt.ind.SMA(period=self.p.short_period)
        self.m_ma = bt.ind.SMA(period=self.p.median_period)
        self.l_ma = bt.ind.SMA(period=self.p.long_period)

        # 短期均线在中期均线上方，且中期均线也在长期均线上方，三线多头排列，取值为1；反之，取值为0
        self.signal1 = bt.And(self.m_ma > self.l_ma, self.s_ma > self.m_ma)
        # 求上面 self.signal1 的环比增量，可以判断得到第一次同时满足上述条件的时间，第一次满足条件为1，其余条件为0
        self.buy_signal = bt.If((self.signal1 - self.signal1(-1)) > 0, 1, 0)
        # 短期均线下穿长期均线时，取值为1；反之取值为0
        self.sell_signal = bt.ind.CrossDown(self.s_ma, self.m_ma)
        # 将买卖信号合并成一个信号
        self.lines.signal = bt.Sum(self.buy_signal, self.sell_signal * (-1))
