"""MC1-P2: Optimize a portfolio.  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		   	  			    		  		  		    	 		 		   		 		  
Atlanta, Georgia 30332  		   	  			    		  		  		    	 		 		   		 		  
All Rights Reserved  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
Template code for CS 4646/7646  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
Georgia Tech asserts copyright ownership of this template and all derivative  		   	  			    		  		  		    	 		 		   		 		  
works, including solutions to the projects assigned in this course. Students  		   	  			    		  		  		    	 		 		   		 		  
and other users of this template code are advised not to share it with others  		   	  			    		  		  		    	 		 		   		 		  
or to make it available on publicly viewable websites including repositories  		   	  			    		  		  		    	 		 		   		 		  
such as github and gitlab.  This copyright statement should not be removed  		   	  			    		  		  		    	 		 		   		 		  
or edited.  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
We do grant permission to share solutions privately with non-students such  		   	  			    		  		  		    	 		 		   		 		  
as potential employers. However, sharing with other current or future  		   	  			    		  		  		    	 		 		   		 		  
students of CS 7646 is prohibited and subject to being investigated as a  		   	  			    		  		  		    	 		 		   		 		  
GT honor code violation.  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
-----do not edit anything above this line---  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
Student Name: Tucker Balch (replace with your name)  		   	  			    		  		  		    	 		 		   		 		  
GT User ID: tb34 (replace with your User ID)  		   	  			    		  		  		    	 		 		   		 		  
GT ID: 900897987 (replace with your GT ID)  		   	  			    		  		  		    	 		 		   		 		  
"""  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
import pandas as pd  		   	  			    		  		  		    	 		 		   		 		  
import matplotlib.pyplot as plt  		   	  			    		  		  		    	 		 		   		 		  
import numpy as np  		   	  			    		  		  		    	 		 		   		 		  
import datetime as dt  		   	  			    		  		  		    	 		 		   		 		  
from util import get_data, plot_data
import scipy.optimize as spo



# This is the function that will be tested by the autograder  		   	  			    		  		  		    	 		 		   		 		  
# The student must update this code to properly implement the functionality  		   	  			    		  		  		    	 		 		   		 		  
def optimize_portfolio(sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,1,1), \
    syms=['GOOG','AAPL','GLD','XOM'], gen_plot=False):

    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)  		   	  			    		  		  		    	 		 		   		 		  
    prices_all = get_data(syms, dates)  # automatically adds SPY  		   	  			    		  		  		    	 		 		   		 		  
    prices = prices_all[syms]  # only portfolio symbols  		   	  			    		  		  		    	 		 		   		 		  
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later  		   	  			    		  		  		    	 		 		   		 		  
    prices_SPY_norm = prices_SPY/prices_SPY[0]
    # find the allocations for the optimal portfolio  		   	  			    		  		  		    	 		 		   		 		  
    # note that the values here ARE NOT meant to be correct for a test case 
    def f(allocs):
        cr, adr, sddr,port_val_norm = get_metric(allocs, prices)
        Y = -adr / sddr
        return Y
    
    def con(x):
        return sum(x) - 1
    
    constraint = {'type':'eq','fun':con}

    allocs = np.ones(len(syms))/len(syms) 
    bound = tuple([(0,1) for i in range(len(allocs))])
    max_reslut = spo.minimize(f, allocs, method='SLSQP', options={'disp':True}, bounds = bound,constraints = constraint)
    allocation = max_reslut.x
    sr = max_reslut.fun
    cr, adr, sddr,port_val_norm = get_metric(allocation,prices)
    
    if gen_plot:
        df_temp = pd.concat([port_val_norm, prices_SPY_norm],keys = ['Portfolio', 'SPY'], axis=1)
        ax = df_temp.plot(title = 'Daily portfolio value and SPY')
        ax.set_xlabel("Date")
        ax.set_ylabel("Normolized price")
        pass
    
    return allocation, cr, adr, sddr, sr

def get_metric(allocs, prices):
        allocs_amount = allocs

        share_per_stock = allocs_amount / prices.iloc[0]
        price_matrix = np.matrix(prices)
        portfolio_value = np.array(np.dot(price_matrix, share_per_stock.T))
        port_val = portfolio_value.reshape((1, len(prices)))[0, :]

        # Get portfolio statistics (note: std_daily_ret = volatility)
        # add code here to compute stats
        cr = (port_val[-1] - 1.0) / 1.0
        port_val = pd.Series(port_val, index=prices.index)
        port_val_norm = port_val/ port_val[0]
#        prices['port_val'] = port_val
#        prices['port_norm'] = prices['port_val'] / sv
        daily_pct_change = port_val.pct_change()[1:]
        adr = daily_pct_change.mean()
        sddr = daily_pct_change.std()
        
        return cr, adr, sddr, port_val_norm






		   	  			    		  		  		    	 		 		   		 		  
def test_code():  		   	  			    		  		  		    	 		 		   		 		  
    # This function WILL NOT be called by the auto grader  		   	  			    		  		  		    	 		 		   		 		  
    # Do not assume that any variables defined here are available to your function/code  		   	  			    		  		  		    	 		 		   		 		  
    # It is only here to help you set up and test your code  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    # Define input parameters  		   	  			    		  		  		    	 		 		   		 		  
    # Note that ALL of these values will be set to different values by  		   	  			    		  		  		    	 		 		   		 		  
    # the autograder!  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    start_date = dt.datetime(2008,06,01)  		   	  			    		  		  		    	 		 		   		 		  
    end_date = dt.datetime(2009,06,01)  		   	  			    		  		  		    	 		 		   		 		  
    symbols = ['IBM', 'X', 'GLD', 'JPM']  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  

    allocations, sr ,cr, adr, sddr= optimize_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        gen_plot = False)
    for i in allocations:
        print(i)
    # Print statistics  		   	  			    		  		  		    	 		 		   		 		  
    print "Start Date:", start_date  		   	  			    		  		  		    	 		 		   		 		  
    print "End Date:", end_date  		   	  			    		  		  		    	 		 		   		 		  
    print "Symbols:", symbols  		   	  			    		  		  		    	 		 		   		 		  
    print "Allocations:", ["%.6f" % a for a in allocations]  		   	  			    		  		  		    	 		 		   		 		  
    print "Sharpe Ratio:", sr 		   	      		  		  		    	 		 		   		 		  
    print "Volatility (stdev of daily returns):", sddr
    print "Average Daily Return:", adr
    print "Cumulative Return:", cr
  		   	  			    		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		   	  			    		  		  		    	 		 		   		 		  
    # This code WILL NOT be called by the auto grader  		   	  			    		  		  		    	 		 		   		 		  
    # Do not assume that it will be called  		   	  			    		  		  		    	 		 		   		 		  
    test_code()  		   	  			    		  		  		    	 		 		   		 		  
