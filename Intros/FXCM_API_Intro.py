# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 17:21:52 2020

@author: Bran
"""


import fxcmpy

#probably better to store in a txt file
token = ''
con = fxcmpy.fxcmpy(access_token = token, log_level = 'error', server='demo')
pair = 'EUR/USD'


#-----------get historical data------------------
data = con.get_candles(pair, period='m5', number=250)
"""periods can be m1, m5, m15 and m30, H1, H2, H3, H4, H6 and H8, D1, W1, M1"""



#-----------streaming data-------------------
#for real-time data
#we won't really use this
"for streaming data, we first need to subscribe to a currency pair"
con.subscribe_market_data('EUR/USD')
con.get_last_price('EUR/USD')
#last few prices
con.get_prices('EUR/USD')
con.unsubscribe_market_data('EUR/USD')



#----------trading account data---------------
con.get_accounts().T

con.get_open_positions().T
con.get_open_positions_summary().T

con.get_closed_positions()

con.get_orders() 

#orders
#simple orders
con.create_market_buy_order('EUR/USD', 10)
con.create_market_buy_order('USD/CAD', 10)
con.create_market_sell_order('USD/CAD', 20)
con.create_market_sell_order('EUR/USD', 10)

#better
#GTC=good till close
order = con.open_trade(symbol='USD/CAD', is_buy=True,
                       is_in_pips=True,
                       amount=10, time_in_force='GTC',
                       stop=-9, trailing_step =True,
                       order_type='AtMarket', limit=9)

#close an individual trade by id
#con.close_trade(trade_id=tradeId, amount=1000)
#better
con.close_all_for_symbol('USD/CAD')

#closing connection
con.close()
