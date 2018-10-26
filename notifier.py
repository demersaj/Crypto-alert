import json
import time
import schedule
import binanceKeys
import os

from pync import Notifier
from binance.client import Client

#connect to Binance API
binance_client = Client(binanceKeys.apiKey, binanceKeys.secretKey)

def job():

    config = None

    with open ("config.json") as file:
        config = json.load(file)

    for market in config.get("markets"):

        if market["active"] is False:
            continue

        symbol = market["name"]
        max_price = market["max"]
        min_price = market["min"]
        ticker = binance_client.get_symbol_ticker(symbol=symbol)
        price = float(ticker.get("price"))

        if price > max_price or price < min_price:
            Notifier.notify(message="{} is currently ${}".format(symbol, price),
                            title='Crypto Alert!',
                            appIcon='https://i.imgur.com/yqsHQIL.png',
                            open='https://www.binance.com/en/trade/BTC_USDT')

            Notifier.remove(os.getpid())
            Notifier.list(os.getpid())

# scheduling
schedule.every().minute.do(job)

print("Initiated")

while True:
    schedule.run_pending()
    time.sleep(1)

