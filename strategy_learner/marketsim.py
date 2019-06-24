"""MC2-P1: Market simulator.  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
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
import numpy as np  		   	  			    		  		  		    	 		 		   		 		  
import datetime as dt  		   	  			    		  		  		    	 		 		   		 		  
import os  		   	  			    		  		  		    	 		 		   		 		  
from util import get_data, plot_data  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
def compute_portvals(data, symbol, sd, ed, start_val = 100000, commission=0, impact=0):
    # this is the function the autograder will call to test your code  		   	  			    		  		  		    	 		 		   		 		  
    # NOTE: orders_file may be a string, or it may be a file object. Your  		   	  			    		  		  		    	 		 		   		 		  
    # code should work correctly with either input
    # TODO: Your code here
    start_date = sd
    end_date = ed
    portvals_lst = []
    price = get_data([symbol],pd.date_range(start_date, end_date))
    date_trade = price.index

    current_status = pd.DataFrame({'symbol':'','shares':''}, index = [])
    order_date = [pd.to_datetime(i) for i in list(data.index)]

    for i in date_trade:
        if i in order_date:

            # print 'true'
            # i = str(i.strftime('%Y-%m-%d'))
            # print i
            # i = pd.to_datetime(i)
            order = data.loc[i]
            # order = data[data['Date'] == i]
            # print 'test',order

            for order_index in range(len(order)):
                daily_order = order.iloc[order_index]
                # date = daily_order[0]

                date = i

                symbol = symbol
                action = ['BUY' if daily_order>0 else 'SELL'][0]

                # print action

                shares = abs(daily_order)

                current_symbol = list(current_status['symbol'])
                order_stock_price = get_data([symbol], pd.date_range(date, date))[symbol][0]
                impact_fee = order_stock_price * impact * shares
                delta = order_stock_price * shares
                start_val -= (impact_fee + commission )

                if symbol in current_symbol:
                    if action == 'BUY':
                        start_val -= delta
                        current_status.loc[current_status['symbol'] == symbol, 'shares'] += shares
                    else:
                        start_val += delta
                        current_status.loc[current_status['symbol'] == symbol, 'shares'] -= shares
                else:
                    if action == 'BUY':
                        start_val -= delta
                        current_status = current_status.append({'symbol': symbol, 'shares': shares}, ignore_index=True)
                    else:
                        start_val += delta
                        current_status = current_status.append({'symbol': symbol, 'shares': -shares}, ignore_index=True)

                current_symbol = list(current_status['symbol'])
                adj_price = np.array(get_data(current_symbol , pd.date_range(date, date))[current_symbol].iloc[0])
                portvals = (adj_price * np.array(current_status['shares'])).sum()
                final_portval = start_val + portvals
            portvals_lst.append(final_portval)

        else:
            # i = str(i.strftime('%Y-%m-%d'))
            current_symbol = list(current_status['symbol'])
            adj_price = np.array(price[current_symbol].loc[i])
            portvals = (adj_price * np.array(current_status['shares'])).sum()
            final_portval = start_val + portvals
            portvals_lst.append(final_portval)

    rv = pd.DataFrame(index=date_trade, data=portvals_lst)
    return rv  		   	  			    		  		  		    	 		 		   		 		  

def author():
    return 'lzheng73'
    # replace tb34 with your Georgia Tech username.
def test_code():  		   	  			    		  		  		    	 		 		   		 		  

  		   	  			    		  		  		    	 		 		   		 		  
    of = "orders/orders-01.csv"
    sv = 1000000  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    # Process orders
    portvals = compute_portvals(orders_file = of, start_val = sv,commission=0, impact=0)
    last_index = len(portvals) -1
    start_date = portvals.index[0]
    end_date = portvals.index[len(portvals)-1]

    daily_return =  portvals[0].pct_change()



    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [(portvals[0][last_index]/portvals[0][0])-1,daily_return.mean(),daily_return.std(),1.5]
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [0.2,0.01,0.02,1.5]
  		   	  			    		  		  		    	 		 		   		 		  
    # Compare portfolio against $SPX  		   	  			    		  		  		    	 		 		   		 		  
    print "Date Range: {} to {}".format(start_date, end_date)  		   	  			    		  		  		    	 		 		   		 		  
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    print "Sharpe Ratio of SPY : {}".format(sharpe_ratio_SPY)
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    print "Cumulative Return of SPY : {}".format(cum_ret_SPY)
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)  		   	  			    		  		  		    	 		 		   		 		  
    print "Standard Deviation of SPY : {}".format(std_daily_ret_SPY)
    print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)  		   	  			    		  		  		    	 		 		   		 		  
    print "Average Daily Return of SPY : {}".format(avg_daily_ret_SPY)
    print "Final Portfolio Value: {}".format(portvals[0][-1])
  		   	  			    		  		  		    	 		 		   		 		  
# if __name__ == "__main__":
#     test_code()
