# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 11:32:57 2020

@author: Bran
"""



import yfinance as yf
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np

ticker = ["TSLA"]

ohlcv = yf.download(ticker,dt.date.today()-dt.timedelta(400),dt.datetime.today())


"""
MACD
(moving average convergence divergence)
"""


def MACD(DF,a=12,b=26,c=9):
    """calculates the MACD with periods a=fast,b=slow,c=signal"""
    df = DF.copy()
    df["MA_Fast"]=df["Adj Close"].ewm(span=a,min_periods=a).mean()
    df["MA_Slow"]=df["Adj Close"].ewm(span=b,min_periods=b).mean()
    df["MACD"]=df["MA_Fast"]-df["MA_Slow"]
    df["Signal"]=df["MACD"].ewm(span=c,min_periods=c).mean()
    #do not fill NaN for a tech. indicator
    df.dropna(inplace=True)
    return df



#visualizing the MACD
df = MACD(ohlcv)

fig, (ax0, ax1) = plt.subplots(nrows=2,ncols=1, sharex=True, sharey=False, figsize=(10, 6), gridspec_kw = {'height_ratios':[2.5, 1]})
df.iloc[-100:,4].plot(ax=ax0)
ax0.set(ylabel='Adj Close')

df.iloc[-100:,[-2,-1]].plot(ax=ax1)
ax1.set(xlabel='Date', ylabel='MACD/Signal')


fig.suptitle('Stock Price with MACD', fontsize=14, fontweight='bold')

"""
ATR
(average true range)
"""

def ATR(DF, n=20):
    """calculate both true range and average true range"""
    df = DF.copy()
    #take absolute differences
    df['H-L']=abs(df['High']-df['Low'])
    df['H-PC']=abs(df['High']-df['Adj Close'].shift(1))
    df['L-PC']=abs(df['Low']-df['Adj Close'].shift(1))
    #some prefer mean here
    df['TR']=df[['H-L','H-PC','L-PC']].max(axis=1,skipna=False)
    #ATR is rolling mean of TR, typically simple mean
    df['ATR'] = df['TR'].rolling(n).mean()
    #df['ATR'] = df['TR'].ewm(span=n,adjust=False,min_periods=n).mean()
    df.drop(['H-L','H-PC','L-PC'],axis=1, inplace=True)
    return df

#visualizing the ATR
df = ATR(ohlcv)
df.iloc[:,[-2,-1]].plot()


"""
Bollinger Bands
"""
def BollBnd(DF, n=20):
    """function to calculate Bollinger Band"""
    df = DF.copy()
    df["MA"] = df['Adj Close'].rolling(n).mean()
    #ddof=0 for standard deviation of the population, not sample
    df["BB_up"] = df["MA"] + 2*df['Adj Close'].rolling(n).std(ddof=0) 
    df["BB_dn"] = df["MA"] - 2*df['Adj Close'].rolling(n).std(ddof=0) 
    df["BB_width"] = df["BB_up"] - df["BB_dn"]
    df.dropna(inplace=True)
    return df

#Visualizing the Bollinger Band
fig2, ax2 = plt.subplots()
ax2.set(xlabel='Date')
ax2.set(title='Bolligner Band')
BollBnd(ohlcv).iloc[-100:,[-4,-3,-2]].plot(ax=ax2)
ax2.fill_between(BollBnd(ohlcv).index[-100:],BollBnd(ohlcv).iloc[-100:,-3], BollBnd(ohlcv).iloc[-100:,-2], alpha=.2)

"""
RSI
(relative strength index)
"""

def RSI(DF, n=14):
    """function to calculate RSI"""
    df = DF.copy()
    df['delta']=df['Adj Close'] - df['Adj Close'].shift(1)
    df['gain']=np.where(df['delta']>=0,df['delta'],0)
    df['loss']=np.where(df['delta']<0,abs(df['delta']),0)
    avg_gain = []
    avg_loss = []
    gain = df['gain'].tolist()
    loss = df['loss'].tolist()
    #first delta is NaN, so these indices are correct
    for i in range(len(df)):
        if i < n:
            avg_gain.append(np.NaN)
            avg_loss.append(np.NaN)
        elif i == n:
            avg_gain.append(df['gain'].rolling(n).mean().tolist()[n])
            avg_loss.append(df['loss'].rolling(n).mean().tolist()[n])
        elif i > n:
            avg_gain.append(((n-1)*avg_gain[i-1] + gain[i])/n)
            avg_loss.append(((n-1)*avg_loss[i-1] + loss[i])/n)
    df['avg_gain']=np.array(avg_gain)
    df['avg_loss']=np.array(avg_loss)
    df['RS'] = df['avg_gain']/df['avg_loss']
    df['RSI'] = 100 - (100/(1+df['RS']))
    return df


RSI(ohlcv)['RSI'].plot()
RSI(ohlcv)['Adj Close'].plot()




















