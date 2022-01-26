#!pip install alpaca_trade_api
import alpaca_trade_api as tradeapi
import numpy as np
import time  #for timestamps in New York time
from alpaca_trade_api.rest import REST, TimeFrame
import logging
from time import sleep
import datetime  #for timestamps in local time

api_key = #enter API key here
api_secret = #enter API secret here
base_url = 'https://paper-api.alpaca.markets'

#select which stock to trade and how many units
s = 'TSLA'    
q = 1       

api = tradeapi.REST(api_key, api_secret, base_url, api_version = 'v2')

clock = api.get_clock()


def buy():           #Function to buy stock at market price
        print("\nLOCAL TIME: ", local_time)
        print("***BUYING***\n")
        api.submit_order(
                 symbol=s,
        qty=q,
        side='buy',
        type='market',
        time_in_force='gtc')
   

def sell():          #Function to sell stock, doesn't return anything
    print("\nLOCAL TIME: ", local_time)
    print("***SELLING***\n")
    api.submit_order(
        symbol=s,
        qty=q,
        side='sell',
        type='market',
        time_in_force='gtc')
  

def wait_for_market_open():   #Returns nothing, sleeps until markets open
    if not clock.is_open:
        time_to_open = (clock.next_open - clock.timestamp).total_seconds()
        print("MARKET NOT YET OPEN")
        print("NY TIME: ", clock.timestamp)
        print("NEXT OPEN: ", clock.next_open)
        print("LOCAL TIME: ", local_time, '\n')
        sleep(round(time_to_open))
  

while (True):
    local_time = datetime.datetime.now()

    open_pos = api.list_positions()

    wait_for_market_open() #check if market is open
    
    #get historical prices
    stock_df = api.get_barset(s, '15Min', limit=10).df
    stock_df.columns = stock_df.columns.droplevel(0)

    #calculate moving average
    open_list = stock_df['open']
    ma_10 = np.mean(open_list)
    latest_price = open_list[9]

    print("\nMA: ", ma_10)
    print("Latest Price: ", latest_price)
    print("LOCAL TIME:", local_time)

    #implement trading strategy
    if (open_pos):
      for stock in open_pos:
        if ((stock.side == 'long') and ((latest_price+0.01) < ma_10)):
          sell()
          sell()
        elif((stock.side == 'short') and ((latest_price - 0.01) > ma_10)):
          buy()
          buy()

    elif((not open_pos) and ((latest_price + 0.50) < ma_10)):
      sell()
    elif((not open_pos) and ((latest_price - 0.50) > ma_10)):
      buy()
    
    time.sleep(900)
