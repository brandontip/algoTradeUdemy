# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 12:03:45 2020

@author: Bran
"""


#alphavantage doesn't rely on yahoofinance
#-------------------IMPORTANT------------------------------
#however, the free trial limits to 5 ticker calls per minute

# it can provide data in either JSON or .csv

#typically is usually stored 'backwards', hence we use iloc -1

from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import time 

myKey='NLVE5M5QN0X68ZB3'

#extract data for a single ticker
#ts = TimeSeries(key=myKey, output_format='pandas')
#data = ts.get_daily(symbol='EURUSD', outputsize='full')[0]
#make sure the order coincides before renaming
#data.columns = ['open', 'high', 'low', 'close', 'volume']
#data = data.iloc[::-1]


# for multiple tickers
# you need the ticker names for alphavantage, usually the same as yahoo

#we will need to use the time module to get around 5 call limit
all_tickers = ['AAPL', 'MSFT', 'CSCO', 'AMZN', 'GOOG', 'FB']
close_prices = pd.DataFrame()
api_call_count = 0
start_time = time.time()
for ticker in all_tickers:    
    ts = TimeSeries(key=myKey, output_format='pandas')
    data = ts.get_intraday(symbol=ticker,interval='1min', outputsize='full')[0]
    api_call_count+=1
    data.columns = ['open', 'high', 'low', 'close', 'volume']
    data = data.iloc[::-1]
    close_prices[ticker] = data["close"]
    if api_call_count==5:
        api_call_count = 0
        time.sleep(60-(time.time()-start_time))
        start_time = time.time()

