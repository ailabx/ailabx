from binance.spot import Spot

client = Spot()
# Get server timestamp
print(client.time())
# Get klines of BTCUSDT at 1m interval
data = client.klines("BTCUSDT", "1h")
print(len(data))
print(data)
