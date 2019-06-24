import datetime as dt
import pandas as pd
import util as ut
import random
import numpy as np
import indicator
import RTLearner as rt
import marketsim
import matplotlib.pyplot as plt
import StrategyLearner as sl
import ManualStrategy as ms


if __name__ == "__main__":



    insample_args = dict(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)
    outsample_args = dict(symbol="JPM", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31), sv=100000)


    test_impact = [0,0.002,0.004,0.006,0.008,0.01,0.02,0.03]
    for impact in range(len(test_impact)):
        learner = sl.StrategyLearner(verbose=False, impact=test_impact[impact])  # constructorj
        learner.addEvidence(**insample_args)  # training phase
        df_trades_insample = learner.testPolicy(**insample_args)

        # port_val_outsample = \
        # marketsim.compute_portvals(data=df_trades, symbol=outsample_args['symbol'], commission=0.0, impact=test_impact[impact],
        #                            sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31))[0]
        port_val_insample = \
        marketsim.compute_portvals(data=df_trades_insample, symbol=insample_args['symbol'], commission=0.0, impact=test_impact[impact],
                                   sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31))[0]
        # benchmark_outsample = learner.benchmark(**outsample_args)
        benchmark_insample = learner.benchmark(**insample_args)
        port_val_normal_insample = port_val_insample / port_val_insample.iloc[0]
        benchmark_normal_insample = benchmark_insample / benchmark_insample[0]
        learner.val_plot(impact, port_val_normal_insample, benchmark_normal_insample, df_trades_insample, 'Strategy Learner: In Sample(impact='+str(test_impact[impact]) +')')
        print '===== Impact: ', test_impact[impact], '========='
        print 'Number of trade: ', len(df_trades_insample)
        print 'Final return: ', port_val_normal_insample[-1]/port_val_normal_insample[0] - 1
        # learner.val_plot(impact*2+1, port_val_normal_outsample, benchmark_normal_outsample, df_trades, 'Strategy Learner: Out Sample(impact='+str(test_impact[impact])+')')
    # plt.show()
