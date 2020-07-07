# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 16:12:01 2020

@author: Bran
"""


import datetime as dt
import yfinance as yf
import pandas as pd

stocks = ["AMZN", "MSFT", "GOOG", "FB"]
start =  dt.datetime.today()-dt.timedelta(3650)
end = dt.datetime.today()

#empty data frame
cl_price = pd.DataFrame()
#empty dictionary
ohlcv_data = {}



for ticker in stocks:
    cl_price[ticker] = yf.download(ticker, start, end,)["Adj Close"] 



#filling NaN values
#fill with 0
#cl_price.fillna(0)
#fill with different values
#cl_price.fillna({"FB":0, "GOOG":1})
#backfill
#cl_price.fillna(method='bfill')
#backfill can work along rows too (default axis is 0)
#cl_price.fillna(method='bfill',axis=1)

#if you want the changes to be permanent, use inplace=True
cl_price.fillna(method='bfill', inplace=True)

#dropna will delete rows or columns with NaN



#some basic statistics
daily_return= cl_price.pct_change()
daily_return.mean()
daily_return.std()



#basic rollings

#first 19 entries will be NaN
daily_return.rolling(window=20).mean()
daily_return.rolling(window=20).std()

daily_return.rolling(window=20, min_periods=1).mean()

#exponential weigh puts more weight on recent values
aily_return.ewm(span=20,min_periods=20).mean()
daily_return.ewm(span=20,min_periods=20).std()



