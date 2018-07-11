from .portfolio import Portfolio

class Backtest(object):
    def __init__(self):
        self.context = {}



    def run(self,handle_bar,datafeed):
        print('启动回测引擎...')
        self.context['instruments'] = datafeed.instruments
        self.portfolio = Portfolio(indexes=datafeed.get_benchmark_index())

        done = False
        while not done:
            bars, done = datafeed.step()
            actions = handle_bar(bars, self.context)  # 调用策略函数
            self.portfolio.step(actions,bars)


        df = self.portfolio.get_result_df()
        print(df)
        df['equity'].plot()
        import matplotlib.pyplot as plt
        plt.show()

#创建回测引擎实例M
M = Backtest()