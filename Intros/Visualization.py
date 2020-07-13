# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 19:59:46 2020

@author: Bran
"""


import pandas as pd
import yfinance as yf
import datetime as dt
import matplotlib.pyplot as plt



tickers = ["TSLA", "IBM", "INTC", "AMD"]

close_prices =pd.DataFrame()
start = dt.datetime.today() - dt.timedelta(3650)
end = dt.datetime.today()



for ticker in tickers:
    close_prices[ticker] = yf.download(ticker,start,end)["Adj Close"]
    
    
close_prices.fillna(method='bfill', inplace=True)


daily_return = close_prices.pct_change()

#plot all columns of dataframe superimposed
close_prices.plot()

close_standardized =  (close_prices - close_prices.mean())/close_prices.std()
close_standardized.plot()

#plotting each column separately
fig, ax = plt.subplots()
plt.style.use('seaborn')
ax.set(title='Mean Tech Stock Daily Return', xlabel='Stock', ylabel = 'Daily Return')
plt.bar(daily_return.columns,daily_return.mean())

#visualization without pandas

