# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 11:32:57 2020

@author: Bran
"""



import yfinance as yf
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
import pandas as pd
from stocktrends import Renko

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


"""
ADX
(average directional index)
"""



def ADX(DF,n=14):
    """function to calculate ADX"""
    df = DF.copy()
    df['TR'] = ATR(df,n)['TR'] #the period parameter of ATR function does not matter because period does not influence TR calculation
    df['DMplus']=np.where((df['High']-df['High'].shift(1))>(df['Low'].shift(1)-df['Low']),df['High']-df['High'].shift(1),0)
    df['DMplus']=np.where(df['DMplus']<0,0,df['DMplus'])
    df['DMminus']=np.where((df['Low'].shift(1)-df['Low'])>(df['High']-df['High'].shift(1)),df['Low'].shift(1)-df['Low'],0)
    df['DMminus']=np.where(df['DMminus']<0,0,df['DMminus'])
    TRn = []
    DMplusN = []
    DMminusN = []
    TR = df['TR'].tolist()
    DMplus = df['DMplus'].tolist()
    DMminus = df['DMminus'].tolist()
    #TR taken care of by ATR
    #DM+/- use smoothing formulas
    for i in range(len(df)):
        if i < n:
            TRn.append(np.NaN)
            DMplusN.append(np.NaN)
            DMminusN.append(np.NaN)
        elif i == n:
            TRn.append(df['TR'].rolling(n).sum().tolist()[n])
            DMplusN.append(df['DMplus'].rolling(n).sum().tolist()[n])
            DMminusN.append(df['DMminus'].rolling(n).sum().tolist()[n])
        elif i > n:
            TRn.append(TRn[i-1] - (TRn[i-1]/n) + TR[i])
            DMplusN.append(DMplusN[i-1] - (DMplusN[i-1]/n) + DMplus[i])
            DMminusN.append(DMminusN[i-1] - (DMminusN[i-1]/n) + DMminus[i])
    df['TRn'] = np.array(TRn)
    df['DMplusN'] = np.array(DMplusN)
    df['DMminusN'] = np.array(DMminusN)
    df['DIplusN']=100*(df['DMplusN']/df['TRn'])
    df['DIminusN']=100*(df['DMminusN']/df['TRn'])
    df['DIdiff']=abs(df['DIplusN']-df['DIminusN'])
    df['DIsum']=df['DIplusN']+df['DIminusN']
    df['DX']=100*(df['DIdiff']/df['DIsum'])
    ADX = []
    DX = df['DX'].tolist()
    #ADX is smoothed. Note it is a rolling of rolling. 
    for j in range(len(df)):
        if j < 2*n-1:
            ADX.append(np.NaN)
        elif j == 2*n-1:
            ADX.append(df['DX'][j-n+1:j+1].mean())
        elif j > 2*n-1:
            ADX.append(((n-1)*ADX[j-1] + DX[j])/n)
    df['ADX']=np.array(ADX)
    return df


"""
OBV
(on balance volume)
"""

def OBV(DF):
    """function to calculate On Balance Volume"""
    df = DF.copy()
    df['daily_ret'] = df['Adj Close'].pct_change()
    df['direction'] = np.where(df['daily_ret']>=0,1,-1)
    #fix first value getting -l direction
    df['direction'][0] = 0
    df['vol_adj'] = df['Volume'] * df['direction']
    df['obv'] = df['vol_adj'].cumsum()
    return df


"""
Simple Regression
(uses OLS from statsmodels)
"""


def slope(ser,n):
    """function to calculate the slope of regression line for n consecutive points on a plot"""
    ser = (ser - ser.min())/(ser.max() - ser.min())
    x = np.array(range(len(ser)))
    x = (x - x.min())/(x.max() - x.min())
    slopes = [i*0 for i in range(n-1)]
    for i in range(n,len(ser)+1):
        y_scaled = ser[i-n:i]
        x_scaled = x[i-n:i]
        x_scaled = sm.add_constant(x_scaled)
        model = sm.OLS(y_scaled,x_scaled)
        results = model.fit()
        slopes.append(results.params[-1])
    #the result will be a list of slopes given in degrees
    slope_angle = (np.rad2deg(np.arctan(np.array(slopes))))
    return np.array(slope_angle)



"""
Renko Chart 

"""

def renko_DF(DF):
    "function to convert ohlc data into renko bricks"
    df = DF.copy()
    df.reset_index(inplace=True)
    df = df.iloc[:,[0,1,2,3,5,6]]
    df.rename(columns = {"Date" : "date", "High" : "high","Low" : "low", "Open" : "open","Adj Close" : "close", "Volume" : "volume"}, inplace = True)
    df2 = Renko(df)
    df2.brick_size = round(ATR(DF,120)["ATR"][-1],0)
    renko_df = df2.get_ohlc_data() #if using older version of the library use get_bricks() instead
    return renko_df


renko_data = renko_DF(ohlcv)



