import bitmex 
import time, requests, json
import pandas as pd
import numpy as np
import datetime
from time import sleep


test_api_key = ''
test_api_secret = ''

client = bitmex.bitmex(test = True, api_key = test_api_key, 
                       api_secret = test_api_secret)

#define buy and sell functions
def buy(s, qty, leverage):
  client.Order.Order_new(symbol=s, ordType='Market', orderQty= qty).result()
  #update leverage
  client.Position.Position_updateLeverage(symbol=s, leverage=leverage).result()
  print(" *****BUYING ", s, "*****")
  print(datetime.datetime.now(), "\n")

def sell(s, qty, leverage):
  client.Order.Order_new(symbol=s, ordType = 'Market', orderQty =-qty).result()
  #update leverage
  client.Position.Position_updateLeverage(symbol=s, leverage=leverage).result()
  print(" *****SELLING ", s, "*****")
  print(datetime.datetime.now(), "\n")

#function to get open positions
def get_pos(s):
    global pos 
    pos = client.Position.Position_get(filter=json.dumps({'symbol': s})).result()[0][0]

#function to get moving average and latest price
def get_MA(time_frame, count, s):
    past_prices = client.Trade.Trade_getBucketed(binSize = time_frame, count = count, 
                                             symbol = s, reverse = True).result()[0]
    df = pd.DataFrame(past_prices)
    df = df.drop(columns=['trades','volume','vwap','lastSize','turnover',
                      'homeNotional', 'foreignNotional'])
    df_close = df['close']
    global moving_average 
    moving_average = np.mean(df_close)
    global latest_price
    latest_price = df_close[0]
    global difference 
    difference = (latest_price/300)

def trade(s, qty, leverage, time_frame, count):
      get_pos(s)
      get_MA(time_frame, count, s)
      print(datetime.datetime.now())
      print("\n",s)
      print("Price:           ", latest_price)
      print("Moving average : ", moving_average)
      if (pos['isOpen']):
        if ((pos['currentQty']>0) and ((latest_price + difference) < moving_average)):
          sell(s, qty, leverage)
          sell(s, qty, leverage)
        elif((pos['currentQty']<0) and ((latest_price - difference) > moving_average)):
          buy(s, qty, leverage)
          buy(s, qty, leverage)

      elif((not (pos['isOpen'])) and ((latest_price + difference) < moving_average)):
        sell(s, qty, leverage)
      elif((not (pos['isOpen'])) and ((latest_price - difference) > moving_average)):
        buy(s, qty, leverage)

 
while True:
    trade('FILUSDT', 1000, 2, '1d', 40)
    #trade('ETHXBT', 1, 1, '1d', 140)
    trade('XBTUSDT', 1000, 1, '1d', 90)
    trade('ETHUSDT', 1000, 1, '1d', 60)
    trade('DOTUSDT', 1000, 1, '1d', 50)
    trade('LTCUSDT', 1000, 1, '1d', 60)
    trade('BCHUSDT', 1000, 1, '1d', 60)
    time.sleep(86400)
