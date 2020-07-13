# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 11:23:50 2020

@author: Bran
"""
import datetime as dt
import pandas as pd
from yahoofinancials import YahooFinancials

all_tickers = ["AAPL", "MSFT", "CSCO", "AMZN", "INTC"]

close_prices = pd.DataFrame()

#we need the date to be in string format for yahoofinancials
end_date = (dt.date.today()).strftime('%Y-%m-%d')
beg_date = (dt.date.today()-dt.timedelta(100)).strftime('%Y-%m-%d')

for ticker in all_tickers:
    yahoo_financials = YahooFinancials(ticker)
    #the lowest granular possible is daily
    json_obj = yahoo_financials.get_historical_price_data(beg_date, end_date, "daily")
    #note that json_obj is a dictionary, in a format called JSON
    #JSON is a nested dictionary
    ohlv = json_obj[ticker]['prices']
    #the following line works because ohlv is a list of dictionaries 
    #with all of the same keys
    temp = pd.DataFrame(ohlv)[["formatted_date", "adjclose"]]
    temp.set_index("formatted_date", inplace=True)
    temp.dropna(inplace=True)
    close_prices[ticker] = temp["adjclose"]
    
    