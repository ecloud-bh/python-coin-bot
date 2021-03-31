from binance.client import Client
import talib as ta
import numpy as np
import time

class BinanceConnection:
    def __init__(self, file):
        self.connect(file)

    """ Creates Binance client """
    def connect(self, file):
        lines = [line.rstrip('\n') for line in open(file)]
        key = lines[0]
        secret = lines[1]
        self.client = Client(key, secret)

if __name__ == '__main__':
    filename = 'credentials.txt'
    connection = BinanceConnection(filename)

    symbol = 'DENTUSDT'
    interval = '1m'
    limit = 500

    while True:
        # 10 saniye bekliyoruz. Sürekli sorgu göndermeye gerek yok.
        time.sleep(2)

        try:
            klines = connection.client.get_klines(symbol=symbol, interval=interval, limit=limit)
        except Exception as exp:
            print(exp.status_code, flush=True)
            print(exp.message, flush=True)

        open = [float(entry[1]) for entry in klines]
        high = [float(entry[2]) for entry in klines]
        low = [float(entry[3]) for entry in klines]
        close = [float(entry[4]) for entry in klines]

        last_closing_price = close[-1]

        previous_closing_price = close[-2]

        print('anlık kapanış fiyatı', last_closing_price, ', bir önceki kapanış fiyatı', previous_closing_price)

        close_array = np.asarray(close)
        close_finished = close_array[:-1]

        macd, macdsignal, macdhist = ta.MACD(close_finished, fastperiod=12, slowperiod=26, signalperiod=9)
        rsi = ta.RSI(close_finished, timeperiod=14)

        if len(macd) > 0:
            last_macd = macd[-1]
            last_macd_signal = macdsignal[-1]

            previous_macd = macd[-2]
            previous_macd_signal = macdsignal[-2]

            rsi_last = rsi[-1]

            macd_cross_up = last_macd > last_macd_signal and previous_macd < previous_macd_signal

            if macd_cross_up and rsi_last > 40:
                print('al sinyali', flush=True)

                # mail atabilirsiniz, sms gönderebilirsiniz.

                # alım yapabilirsiniz (0.1 miktarında market ya da limit alım emri girebiliriz):

                # buy_order = connection.client.order_market_buy(
                #     symbol=symbol,
                #     quantity=0.1)
