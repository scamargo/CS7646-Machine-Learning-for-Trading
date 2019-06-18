"""Analyze a portfolio.

Copyright 2017, Georgia Tech Research Corporation
Atlanta, Georgia 30332-0415
All Rights Reserved
"""

import pandas as pd
import numpy as np
import datetime as dt
from util import get_data, plot_data

# This is the function that will be tested by the autograder
# The student must update this code to properly implement the functionality
def assess_portfolio(sd = dt.datetime(2008,1,1), ed = dt.datetime(2009,1,1), \
    syms = ['GOOG','AAPL','GLD','XOM'], \
    allocs=[0.1,0.2,0.3,0.4], \
#   sv: starting values; rfr: risk fress rate; sf:yearly sampling frequency...
    sv=1000000.0, rfr=0.0, sf=252.0, \
    gen_plot=True):

    sv = float(sv)
    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later

    # Get daily portfolio value  ad
#    port_val = prices_SPY # add code here to compute daily portfolio values
    
    
    
    allocs_array = np.array(allocs)


    allocs_amount = allocs_array*sv
    share_per_stock = allocs_amount/prices.iloc[0]
    price_matrix = np.matrix(prices)
    portfolio_value = np.array(np.dot(price_matrix,share_per_stock.T))
    port_val = portfolio_value.reshape((1,len(prices)))[0,:]
    
    # Get portfolio statistics (note: std_daily_ret = volatility)
    # add code here to compute stats
    cr = (port_val[-1] - sv)/ sv
    ev = port_val[-1]
    port_val = pd.Series(port_val,index = prices.index)
    prices['port_val'] = port_val
    prices['port_norm'] = prices['port_val']/sv
    daily_pct_change = port_val.pct_change()[1:]
    adr = daily_pct_change.mean()
    sddr = daily_pct_change.std()
    sr = adr/sddr
    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        # add code to plot here
        df_temp = pd.concat([prices['port_norm'], prices_SPY/prices_SPY[0]], keys=['Portfolio', 'SPY'], axis=1)
        ax = df_temp.plot(title = 'Daily portfolio value and SPY')
        ax.set_xlabel("Date")
        ax.set_ylabel("Normolized price")
        pass

    # Add code here to properly compute end value
    
    return cr, adr, sddr, sr, ev

def test_code():
   # This code WILL NOT be tested by the auto grader
   # It is only here to help you set up and test your code

   # Define input parameters
   # Note that ALL of these values will be set to different values by
   # the autograder!
   start_date = dt.datetime(2009,1,1)
   end_date = dt.datetime(2010,1,1)
   symbols = ['GOOG', 'AAPL', 'GLD', 'XOM','ADM','AEE']
   allocations = [0.2, 0.1, 0.2, 0.1, 0.4, 0.2]
   start_val = 1000000
   risk_free_rate = 0.0
   sample_freq = 252

   # Assess the portfolio
   cr, adr, sddr, sr, ev = assess_portfolio(sd = start_date, ed = end_date,\
       syms = symbols, \
       allocs = allocations,\
       sv = start_val, \
       gen_plot = False)


   # print statistics
   print "Start Date:", start_date
   print "End Date:", end_date
   print "Symbols:", symbols
   print "Allocations:", allocations
   print "Sharpe Ratio:", sr
   print "Volatility (stdev of daily returns):", sddr
   print "Average Daily Return:", adr
   print "Cumulative Return:", cr

if __name__ == "__main__":
   test_code()
