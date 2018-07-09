
class Backtest(object):
    def __init__(self):
        self.context = {}


    def run(self,handle_bar,datafeed):
        print('启动回测引擎...')
        self.context['instruments'] = datafeed.instruments

        done = False
        while not done:
            bars, done = datafeed.step()
            action = handle_bar(bars, self.context)  # 调用策略函数

#创建回测引擎实例M
M = Backtest()