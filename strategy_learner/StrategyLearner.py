"""  		   	  			    		  		  		    	 		 		   		 		  
Template for implementing StrategyLearner  (c) 2016 Tucker Balch  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
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
  		   	  			    		  		  		    	 		 		   		 		  
import datetime as dt
import pandas as pd  		   	  			    		  		  		    	 		 		   		 		  
import util as ut

import random
# import DTLearner
import numpy as np
import indicator
import RTLearner as rt
import marketsim
import matplotlib.pyplot as plt
  		   	  			    		  		  		    	 		 		   		 		  
class StrategyLearner(object):  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    # constructor
    def author(self):
        return 'lzheng73'  #
    def __init__(self, verbose = False, impact=0.0):  		   	  			    		  		  		    	 		 		   		 		  
        self.verbose = verbose  		   	  			    		  		  		    	 		 		   		 		  
        self.impact = impact
        # self.predict = None
        self.learner = None

    # this method should create a QLearner, and train it for trading  		   	  			    		  		  		    	 		 		   		 		  
    def addEvidence(self, symbol, \
        sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,12,31), \
        sv = 100000):

        data = ut.get_data([symbol],pd.date_range(sd,ed))[symbol]
        price_indicator = indicator.bollinger(data)
        price_sma = price_indicator['Price/SMA']
        MACD = indicator.MACD(data)['MACD']
        # MACD = indicator.MACD(symbol, sd, ed)['Qstick']



        # calculate the feature & response for train, will do the same thing for test
        train_data = pd.DataFrame()



        train_data['Price/SMA'] = price_sma

        train_data['MACD'] = MACD

        train_data['upper_ratio'] = price_indicator['upper']/price_indicator['SMA']
        train_data['lower_ratio'] = price_indicator['SMA']/price_indicator['lower']
        train_data['return'] = price_indicator['price'].pct_change(5)

        # get X and Y
        data_arr = np.array(train_data.tail(-26))
        trainX = data_arr[:,0:-1]
        trainY = data_arr[:, -1]

        # scaler = StandardScaler()
        # scaler.fit(trainY)
        # trainY_transform = scaler.transform(trainY)

        self.learner = rt.RTLearner(leaf_size = 10, verbose = False)
        # self.learner.addEvidence(trainX,trainY_transform)
        trainY = (trainY-trainY.mean())/trainY.std()
        self.learner.addEvidence(trainX,trainY)



    # this method should use the existing policy and test it against new data
    def testPolicy(self, symbol, \
        sd=dt.datetime(2010,1,1), \
        ed=dt.datetime(2011,12,31), \
        sv = 100000):

        data = ut.get_data([symbol], pd.date_range(sd, ed))[symbol]

        price_indicator = indicator.bollinger(data)
        price_sma = price_indicator['Price/SMA']

        # MACD = indicator.MACD(symbol, sd, ed)['Qstick']

        MACD = indicator.MACD(data)['MACD']

        # calculate the feature & response for train, will do the same thing for test
        data_policy = pd.DataFrame()
        data_policy['Price/SMA'] = price_sma
        data_policy['MACD'] = MACD


        data_policy['upper_ratio'] = price_indicator['upper'] / price_indicator['SMA']
        data_policy['lower_ratio'] = price_indicator['lower'] / price_indicator['SMA']
        # data_policy['return'] = price_indicator['price'].pct_change(periods=1)
        # print data_policy.shape
        # print data_policy
        data_test = np.array(data_policy.tail(-26))


        predict = self.learner.query(data_test)
        date = data_policy.tail(-26).index

        # build the trade dataframe based on the


        df_trades = pd.DataFrame({'Date': '', 'trade': ''}, index=[])
        options = [1000, -1000, 0]
        symbols = []
        symbols.append(symbol)

        YBUY = 0.01
        YSELL = -0.001
        for i in range(1, len(predict)):
            change = predict[i]
            pre_date = date[i]
            holding = df_trades.trade.sum()
            if holding == 0:
                if change - self.impact > YBUY :
                    trade = options[0]
                    df_trades = df_trades.append({'Date': pre_date, 'trade': trade}, ignore_index=True)
                else:
                    trade = options[1]
                    df_trades = df_trades.append({'Date': pre_date, 'trade': trade}, ignore_index=True)
            else:
                if change - self.impact > YBUY and holding < 0:
                    # buy 1000 shares, long 1000 shares
                    trade = options[0] + 1000
                    df_trades = df_trades.append({'Date': pre_date, 'trade': trade}, ignore_index=True)
                elif change < YSELL and holding > 0:
                    # sell 1000 shares, short 1000 shares
                    trade = options[1] - 1000
                    df_trades = df_trades.append({'Date': pre_date, 'trade': trade}, ignore_index=True)
                else:
                    continue
        if self.verbose: print type(trades) # it better be a DataFrame!  		   	  			    		  		  		    	 		 		   		 		  
        if self.verbose: print trades  		   	  			    		  		  		    	 		 		   		 		  
        if self.verbose: print prices_all

        df_trades.set_index('Date',inplace=True)

        return df_trades

    def benchmark(self, symbol, sd, ed, sv):
        num_share = 1000
        price_data = ut.get_data(symbols=[symbol], dates=pd.date_range(sd, ed))[symbol]
        port_val = price_data * num_share
        cash = price_data[0] * num_share
        port_val = (sv - cash) + port_val
        return port_val

    def val_plot(self, num, df, benchmark, df_trade, title):
        plt.plot(df, label='port_val', color='black', linewidth=1)
        plt.plot(benchmark, label='benchmark_val', color='blue', linewidth=1)
        plt.title(title)
        xcoords = list(zip(list(df_trade.index), list(df_trade.values)))
        for xc in xcoords:
            if xc[1] < 0:
                plt.axvline(x=xc[0], color='red', linewidth=0.5)
            else:
                plt.axvline(x=xc[0], color='green', linewidth=0.5)
        plt.xticks(rotation=30)
        plt.legend(loc='best')
        plt.savefig('exp2_'+str(num)+'.png')
  		   	  			    		  		  		    	 		 		   		 		  
if __name__=="__main__":
    learner = StrategyLearner(verbose=False, impact=0.000)  # constructor

    # insample_args = dict(symbol="ML4T-220", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)
    # outsample_args = dict(symbol="ML4T-220", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31), sv=100000)

    # insample_args = dict(symbol="AAPL", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)
    # outsample_args = dict(symbol="AAPL", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31), sv=100000)
    #
    insample_args = dict(symbol="UNH", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)
    outsample_args = dict(symbol="UNH", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31), sv=100000)

    # insample_args = dict(symbol="SINE_FAST_NOISE", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)
    # outsample_args = dict(symbol="SINE_FAST_NOISE", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31),sv=100000)

    learner.addEvidence(**insample_args)  # training phase
    # learner.testPolicy()
    df_trades = learner.testPolicy(**outsample_args)  # testing phase
    df_trades_insample = learner.testPolicy(**insample_args)

    port_val_outsample = marketsim.compute_portvals(data = df_trades,  symbol=outsample_args['symbol'], commission=0.0, impact=0.0, sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31))[0]
    port_val_insample = marketsim.compute_portvals(data = df_trades_insample,  symbol=insample_args['symbol'], commission=0.0, impact=0.0, sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31))[0]

    benchmark_outsample = learner.benchmark(**outsample_args)

    benchmark_insample = learner.benchmark(**insample_args)

    port_val_normal_insample = port_val_insample / port_val_insample.iloc[0]
    port_val_normal_outsample = port_val_outsample / port_val_outsample.iloc[0]


    benchmark_normal_outsample = benchmark_outsample / benchmark_outsample[0]

    benchmark_normal_insample = benchmark_insample / benchmark_insample[0]



    fig = plt.figure(1)

    # print float(port_val_normal_insample)

    plt.plot(port_val_normal_insample, label='port_val')
    plt.plot(benchmark_normal_insample, label='benchmark_val')
    plt.title('in sample Strategy')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.xticks(rotation=30)
    plt.legend(loc='best')
    plt.show()

    fig2 = plt.figure(2)

    plt.plot(port_val_normal_outsample, label='port_val')
    plt.plot(benchmark_normal_outsample, label='benchmark_val')
    plt.title('out Strategy')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.xticks(rotation=30)
    plt.legend(loc='best')
    # print "One does not simply think up a strategy"
