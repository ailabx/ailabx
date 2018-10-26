from pyalgotrade import strategy
from pyalgotrade import plotter
from pyalgotrade.tools import quandl
from pyalgotrade.feed import csvfeed
import datetime
from pyalgotrade.technical import ma


class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, quandlFeed, instrument):
        super(MyStrategy, self).__init__(feed)
        self.setUseAdjustedValues(True)
        self.__instrument = instrument
        self.__position = None
        self.__sma_5 = ma.SMA(feed[instrument].getPriceDataSeries(), 5)
        self.__sma_10 = ma.SMA(feed[instrument].getPriceDataSeries(), 10)

        # It is VERY important to add the the extra feed to the event dispatch loop before
        # running the strategy.
        self.getDispatcher().addSubject(quandlFeed)

        # Subscribe to events from the Quandl feed.
        quandlFeed.getNewValuesEvent().subscribe(self.onQuandlData)

    def onQuandlData(self, dateTime, values):
        self.info(values)

    def onBars(self, bars):
        if self.__sma_10[-1] is None:
            return

        bar = bars[self.__instrument]
        # If a position was not opened, check if we should enter a long position.
        if self.__position is None:
            if self.__sma_5[-1] > self.__sma_10[-1]:
                # Enter a buy market order for 10 shares. The order is good till canceled.
                self.__position = self.enterLong(self.__instrument, 10, True)
        # Check if we have to exit the position.
        elif self.__sma_5[-1] < self.__sma_10[-1] and not self.__position.exitActive():
            self.__position.exitMarket()


def main(plot):
    instruments = ["AAPL"]
    # Download GORO bars using WIKI source code.
    feed = quandl.build_feed("WIKI", instruments, 2006, 2006, ".")

    # Load Quandl CSV downloaded from http://www.quandl.com/OFDP-Open-Financial-Data-Project/GOLD_2-LBMA-Gold-Price-London-Fixings-P-M
    quandlFeed = csvfeed.Feed("Date", "%Y-%m-%d")
    quandlFeed.setDateRange(datetime.datetime(2006, 1, 1), datetime.datetime(2012, 12, 31))
    quandlFeed.addValuesFromCSV("WIKI-AAPL-2006-quandl.csv")

    myStrategy = MyStrategy(feed, quandlFeed, instruments[0])

    if plot:
        plt = plotter.StrategyPlotter(myStrategy, True, False, False)
        #plt.getOrCreateSubplot("quandl").addDataSeries("USD", quandlFeed["USD"])
        #plt.getOrCreateSubplot("quandl").addDataSeries("EUR", quandlFeed["EUR"])
        #plt.getOrCreateSubplot("quandl").addDataSeries("GBP", quandlFeed["GBP"])

    myStrategy.run()

    if plot:
        plt.plot()


if __name__ == "__main__":
    main(True)