# PythonTradingBot
There are two scripts, one is a stock trading bot that connects to the Alpaca API,
the other in a crypto trading bot which connects to python-binance.
Both have the following strategy:
  BUY when the price rises above the (open) moving average(10).
  SHORT/SELL when the price dips below the 10 open moving average.

Although the Alpaca API has been easy to use, it limits accounts with
a balance of less than $25k from making more than 4 day trades per every five business
days due toe the Pattern Day Trading restrictions.
Another issue is that not all stocks are shortable and even if you trade a stock that is shortable,
users with an account balance of less than $2k are not allowed to short stocks.
