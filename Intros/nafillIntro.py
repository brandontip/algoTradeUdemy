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
cl_price.fillna(method='bfill')
#backfill can work along rows too (default axis is 0)
#cl_price.fillna(method='bfill',axis=1)

#if you want the changes to be permanent, use inplace=True
#cl_price.fillna(method='bfill', inplace=True)

#dropna will delete rows or columns with NaN

daily_return= cl_price.pct_change()