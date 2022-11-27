import pandas as pd
import time
# 声明ccxt第三方包， 通过pip install ccxt 可以进行安装
#ccxt 的github地址为： https://github.com/ccxt/ccxt
import ccxt
import os
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option("display.max_rows", 500000)   #设置最大行数，根据需要更改

# 初始化币安交易所对象
exchange = ccxt.binance()
# 请求的candles个数
limit = 5000000

# 当前时间
current_time =int( time.time()//60 * 60 * 1000) # 毫秒
print(current_time)

# 获取请求开始的时间
since_time = current_time - limit * 60 * 1000


since = exchange.parse8601('2020-01-01T00:00:00Z')
#exchange.fetch_ohlcv('BTC/USDT', '1d', since, 3)
# 'BTC/USDT' 比特币对美元的交易对，或者ETH/USD 以太坊对美元的交易对.
data = exchange.fetch_ohlcv(symbol='BTC/USDT', since=since, timeframe='1h')
df = pd.DataFrame(data)
df = df.rename(columns={0: 'open_time', 1: 'open', 2: 'high', 3: 'low', 4: 'close', 5: 'volume'})
# 时间转换成北京时间
df['open_time'] = pd.to_datetime(df['open_time'], unit='ms') + pd.Timedelta(hours=8)

# 设置index
df = df.set_index('open_time', drop=True)

# 保存成csv文件
#df.to_csv('binance_data.csv') # comma seperate Value
print(df)
df.to_csv('b_1h.csv')
