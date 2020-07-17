# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 21:19:21 2020

@author: Bran
"""


import oandapyV20
import oandapyV20.endpoints.instruments as instruments
import oandapyV20.endpoints.pricing as pricing
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.trades as trades
import pandas as pd

#################initiating API connection#######################
my_token = ""
account_id = ""
client = oandapyV20.API(access_token=my_token,environment="practice")


##################get historical data ###########################
#granularity can be: seconds S5 - S30, minutes M1 - M30, hours H1 - H12, days D, weeks W or months M
params = {"count": 150,"granularity": "M5"} 
candles = instruments.InstrumentsCandles(instrument="USD_JPY",params=params)
client.request(candles)
#print(candles.response)

#from JSON to dataframe
ohlc_dict = candles.response["candles"]
ohlc = pd.DataFrame(ohlc_dict)
ohlc_df = ohlc.mid.dropna().apply(pd.Series)
ohlc_df["volume"] = ohlc["volume"]
ohlc_df.index = ohlc["time"]
#strings to numbers
ohlc_df = ohlc_df.apply(pd.to_numeric)


#####################streaming data#############################
#again, we won't work with streams
params = {"instruments": "USD_JPY"}
r = pricing.PricingInfo(accountID=account_id, params=params)
i=0
while i <=20:
    rv = client.request(r)
    print("Time=",rv["time"])
    print("bid=",rv["prices"][0]["closeoutBid"])
    print("ask=",rv["prices"][0]["closeoutAsk"])
    print("*******************")
    i+=1
    
####################interacting with account#####################   
#trading account details
r = accounts.AccountDetails(accountID=account_id)
client.request(r)
print(r.response)

#trading account summary
r = accounts.AccountSummary(accountID=account_id)
client.request(r)
print(r.response)



###################placing orders#################################
#simple hard coded orders:
data = {
        "order": {
        "price": "1.15",
        "stopLossOnFill": {
        "timeInForce": "GTC",
        "price": "1.01"
                          },
        "timeInForce": "FOK",
        "instrument": "USD_CAD",
        "units": "100",
        "type": "MARKET",
        "positionFill": "DEFAULT"
                }
        }
            
r = orders.OrderCreate(accountID=account_id, data=data)
client.request(r)

#more sophisticated way of placing an order:
def ATR(DF,n):
    "function to calculate True Range and Average True Range"
    df = DF.copy()
    df['H-L']=abs(df['h']-df['l'])
    df['H-PC']=abs(df['h']-df['c'].shift(1))
    df['L-PC']=abs(df['l']-df['c'].shift(1))
    df['TR']=df[['H-L','H-PC','L-PC']].max(axis=1,skipna=False)
    df['ATR'] = df['TR'].rolling(n).mean()
    #df['ATR'] = df['TR'].ewm(span=n,adjust=False,min_periods=n).mean()
    df2 = df.drop(['H-L','H-PC','L-PC'],axis=1)
    return round(df2["ATR"][-1],2)


def market_order(instrument,units,sl):
    """units can be positive or negative, stop loss (in pips) added/subtracted to price """
    params = {"instruments": instrument}
    r = pricing.PricingInfo(accountID=account_id, params=params)
    rv = client.request(r)
    #long
    if units > 0:
        price = float(rv["prices"][0]["closeoutAsk"])
        st_ls = price - sl
    #short
    else:
        price = float(rv["prices"][0]["closeoutBid"])
        st_ls = price + sl
    
    data = {
            "order": {
            "price": "",
            "stopLossOnFill": {
            "timeInForce": "GTC",
            "price": str(st_ls)
                              },
            "timeInForce": "FOK",
            "instrument": str(instrument),
            "units": str(units),
            "type": "MARKET",
            "positionFill": "DEFAULT"
                    }
            }
    return data

#place order
r = orders.OrderCreate(accountID=account_id, data=market_order("USD_JPY",100,30*ATR(ohlc_df,120)))
client.request(r)


#check trades
r = trades.OpenTrades(accountID=account_id)
client.request(r)
#client.request(r)['trades'][0]['currentUnits']
