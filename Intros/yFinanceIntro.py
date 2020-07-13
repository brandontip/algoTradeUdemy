# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 21:38:31 2020

@author: Bran
"""


import datetime as dt
import yfinance as yf
import pandas as pd

stocks = ["AMZN", "MSFT", "INTC", "GOOG", "INFY.NS"]
#30 days ago 
start =  dt.datetime.today()-dt.timedelta(30)
end = dt.datetime.today()

#empty data frame
cl_price = pd.DataFrame()
#empty dictionary
ohlcv_data = {}

#this creates a dataframe with close prices for each ticker
#for ticker in stocks:
#   cl_price[ticker] = yf.download(ticker, start, end,)["Adj Close"]   

for ticker in stocks:
    ohlcv_data[ticker] = yf.download(ticker, start, end,)    


ohlcv_data["MSFT"]

