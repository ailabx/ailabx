from pyalgotrade import strategy
from pyalgotrade.technical import ma
from pyalgotrade.technical import cross

class AIStrategy(strategy.BacktestingStrategy):
    def __init__(self,feed,instrument,params):
        super(AIStrategy,self).__init__(feed)
        self._instrument =  instrument
        self.feed = feed
        self.params = params

        self.setUseAdjustedValues(True)
        self.__position = None
        self.__prices = feed[instrument].getPriceDataSeries()
        self.__sma = ma.SMA(self.__prices, params['sma_period'])

    def onBars(self, bars):
        if self.__position is None:
            shares = int(self.getBroker().getCash() * 0.9 / bars[self._instrument].getPrice())
            # Enter a buy market order. The order is good till canceled.
            self.__position = self.enterLong(self._instrument, shares, True)
            #if cross.cross_above(self.__prices,self.__sma)>0:
            #    print('cross_above')
        print('onBars')
        print(len(self.__prices),self.__prices[-1])

class SMACrossOver(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, smaPeriod):
        super(SMACrossOver, self).__init__(feed)
        self.__instrument = instrument
        self.__position = None
        # We'll use adjusted close values instead of regular close values.
        self.setUseAdjustedValues(True)
        self.__prices = feed[instrument].getPriceDataSeries()
        self.__sma = ma.SMA(self.__prices, smaPeriod)

    def getSMA(self):
        return self.__sma

    def onEnterCanceled(self, position):
        self.__position = None

    def onExitOk(self, position):
        self.__position = None

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        self.__position.exitMarket()

    def onBars(self, bars):
        import logging
        logging.info(bars[self.__instrument].getPrice())
        # If a position was not opened, check if we should enter a long position.
        if self.__position is None:
            if cross.cross_above(self.__prices, self.__sma) > 0:
                shares = int(self.getBroker().getCash() * 0.9 / bars[self.__instrument].getPrice())
                # Enter a buy market order. The order is good till canceled.
                self.__position = self.enterLong(self.__instrument, shares, True)
        # Check if we have to exit the position.
        elif not self.__position.exitActive() and cross.cross_below(self.__prices, self.__sma) > 0:
            self.__position.exitMarket()

from pyalgotrade import plotter
from pyalgotrade.barfeed import quandlfeed
from pyalgotrade.stratanalyzer import returns,sharpe
#import sma_crossover
import os

# Load the bar feed from the CSV file
def run_strategy(params=None):
    ax = params['ax']
    instrument = 'AMZN'
    feed = quandl.build_feed("WIKI", ['AMZN'], 2011, 2013, "d:/devgit/ailabx/data")
    strategy = AIStrategy(feed, instrument, {'sma_period': 5})

    strategy.attachAnalyzer(returns.Returns())
    sharpe_ratio = sharpe.SharpeRatio()
    strategy.attachAnalyzer(sharpe_ratio)

    # if plot:
    plt = plotter.StrategyPlotter(strategy, True, False, True)
    # plt.getInstrumentSubplot(instrument).addDataSeries("sma", strategy.getSMA())

    strategy.run()
    strategy.info("Final portfolio value: $%.2f" % strategy.getResult())
    print("Sharpe ratio: %.2f" % sharpe_ratio.getSharpeRatio(0.05))

    plt.plot()


from pyalgotrade.tools import quandl
if __name__ == '__main__':
    run_strategy()