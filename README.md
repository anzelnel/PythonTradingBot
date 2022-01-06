# PythonTradingBot
Automated trading using Alpaca API


Strategy: 
Trade Bitcoin/USD and Etherium/USD according to the 10-day moving average. 
When the price of th crypto crosses the MA in a bullish direction, the current position should be closed, 
the crypto should be bought and kept until the price crosses the MA again.
Once the price crosses the MA in a bearish directon, the crypto should be shorted and the position should 
be held until the price crosses the MA again.
