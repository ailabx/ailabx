from ..common import csv_utils
from ..common import dt
import datetime,os
import pandas as pd
from ..common.logging_utils import logger
# http://www.quandl.com/help/api
from ..common import csv_utils


def download_weekly_bars(sourceCode, tableCode, year, csvFile, authToken=None):
    """Download weekly bars from Quandl for a given year.

    :param sourceCode: The dataset's source code.
    :type sourceCode: string.
    :param tableCode: The dataset's table code.
    :type tableCode: string.
    :param year: The year.
    :type year: int.
    :param csvFile: The path to the CSV file to write.
    :type csvFile: string.
    :param authToken: Optional. An authentication token needed if you're doing more than 50 calls per day.
    :type authToken: string.
    """

    begin = dt.get_first_monday(year) - datetime.timedelta(days=1)  # Start on a sunday
    end = dt.get_last_monday(year) - datetime.timedelta(days=1)  # Start on a sunday
    bars = download_csv(sourceCode, tableCode, begin, end, "weekly", authToken)
    f = open(csvFile, "w")
    f.write(bars)
    f.close()

def build_feed(sourceCode, tableCodes, fromYear, toYear, storage, frequency='DAY', timezone=None,
               skipErrors=False, authToken=None, columnNames={}, forceDownload=False,
               skipMalformedBars=False
               ):
    """Build and load a :class:`pyalgotrade.barfeed.quandlfeed.Feed` using CSV files downloaded from Quandl.
    CSV files are downloaded if they haven't been downloaded before.

    :param sourceCode: The dataset source code.
    :type sourceCode: string.
    :param tableCodes: The dataset table codes.
    :type tableCodes: list.
    :param fromYear: The first year.
    :type fromYear: int.
    :param toYear: The last year.
    :type toYear: int.
    :param storage: The path were the files will be loaded from, or downloaded to.
    :type storage: string.
    :param frequency: The frequency of the bars. Only **pyalgotrade.bar.Frequency.DAY** or **pyalgotrade.bar.Frequency.WEEK**
        are supported.
    :param timezone: The default timezone to use to localize bars. Check :mod:`pyalgotrade.marketsession`.
    :type timezone: A pytz timezone.
    :param skipErrors: True to keep on loading/downloading files in case of errors.
    :type skipErrors: boolean.
    :param authToken: Optional. An authentication token needed if you're doing more than 50 calls per day.
    :type authToken: string.
    :param columnNames: Optional. A dictionary to map column names. Valid key values are:

        * datetime
        * open
        * high
        * low
        * close
        * volume
        * adj_close

    :type columnNames: dict.
    :param skipMalformedBars: True to skip errors while parsing bars.
    :type skipMalformedBars: boolean.

    :rtype: :class:`pyalgotrade.barfeed.quandlfeed.Feed`.
    """

    #logger = pyalgotrade.logger.getLogger("quandl")
    #ret = quandlfeed.Feed(frequency, timezone)

    # Additional column names.
    #for col, name in six.iteritems(columnNames):
    #    ret.setColumnName(col, name)

    if not os.path.exists(storage):
        logger.info("Creating %s directory" % (storage))
        os.mkdir(storage)
    all = {}
    for tableCode in tableCodes:

        all_code = []
        for year in range(fromYear, toYear+1):

            fileName = os.path.join(storage, "%s-%s-%d-quandl.csv" % (sourceCode, tableCode, year))
            if not os.path.exists(fileName) or forceDownload:
                logger.info("Downloading %s %d to %s" % (tableCode, year, fileName))
                try:
                    if frequency == 'DAY':
                        download_daily_bars(sourceCode, tableCode, year, fileName, authToken)
                    else:
                        assert frequency == 'WEEK', "Invalid frequency"
                        download_weekly_bars(sourceCode, tableCode, year, fileName, authToken)
                except Exception as e:
                    if skipErrors:
                        logger.error(str(e))
                        continue
                    else:
                        raise e
            df = pd.read_csv(fileName).copy()
            #print(df.head())
            df.index = df['Date']
            #df.sort_index(inplace=True)
            #item = df['Adj. Close']
            #item.name = tableCode
            #print(item.head())

            all_code.append(df)

        df_code = pd.concat(all_code,axis=0)
        all[tableCode]=df_code.sort_index()

    #for data in all:
    #    logger.info('序列长度：'+str(len(data)))
    #all_df = pd.concat(all,axis=1)

    #ret.addBarsFromCSV(tableCode, fileName, skipMalformedBars=skipMalformedBars)
    return all




