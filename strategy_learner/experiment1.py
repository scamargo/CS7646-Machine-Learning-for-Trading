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


def val_plot(num, df, benchmark, df_trade, title):
    # plt.plot()
    # plt.figure(num)
    plt.plot(df, label='port_val', color='black', linewidth=1)
    plt.plot(benchmark, label='benchmark_val', color='blue', linewidth=1)
    plt.title(title)

    xcoords = list(zip(list(df_trade.index), list(df_trade.values)))
    # print xcoords
    for xc in xcoords:
        if xc[1] < 0:
            plt.axvline(x=xc[0], color='red', linewidth=0.5)
        else:
            plt.axvline(x=xc[0], color='green', linewidth=0.5)
    plt.xticks(rotation=30)
    plt.legend(loc='best')
    plt.savefig('exp1_',str(num)+'.png')

if __name__ == "__main__":

    #
    # # insample_args = dict(symbol="ML4T-220", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)
    # # outsample_args = dict(symbol="ML4T-220", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31), sv=100000)
    #
    # # insample_args = dict(symbol="AAPL", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)
    # # outsample_args = dict(symbol="AAPL", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31), sv=100000)

    insample_args = dict(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)
    outsample_args = dict(symbol="JPM", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31), sv=100000)

    # # insample_args = dict(symbol="SINE_FAST_NOISE", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)
    # # outsample_args = dict(symbol="SINE_FAST_NOISE", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31),sv=100000)
    learner = sl.StrategyLearner(verbose=False, impact=0.000)  # constructorj
    learner.addEvidence(**insample_args)  # training phase
    df_trades = learner.testPolicy(**outsample_args)  # testing phase
    df_trades_insample = learner.testPolicy(**insample_args)

    port_val_outsample = \
    marketsim.compute_portvals(data=df_trades, symbol=outsample_args['symbol'], commission=0.0, impact=0.0,
                               sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31))[0]
    port_val_insample = \
    marketsim.compute_portvals(data=df_trades_insample, symbol=insample_args['symbol'], commission=0.0, impact=0.0,
                               sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31))[0]
    benchmark_outsample = learner.benchmark(**outsample_args)
    benchmark_insample = learner.benchmark(**insample_args)
    port_val_normal_insample = port_val_insample / port_val_insample.iloc[0]
    port_val_normal_outsample = port_val_outsample / port_val_outsample.iloc[0]
    benchmark_normal_outsample = benchmark_outsample / benchmark_outsample[0]
    benchmark_normal_insample = benchmark_insample / benchmark_insample[0]
    val_plot(1, port_val_normal_insample, benchmark_normal_insample, df_trades_insample, 'Strategy Learner: In Sample')
    val_plot(2, port_val_normal_outsample, benchmark_normal_outsample, df_trades, 'Strategy Learner: Out Sample')

    # ===============Manual Strategy============
    tos = ms.ManualStrategy()

    df_both_in = tos.testPolicy(**insample_args)
    benchmark = tos.benchmark(**insample_args)
    benchmark_out = tos.benchmark(**outsample_args)

    df_both_out = tos.testPolicy(**outsample_args)

    port_val_both_in = \
    marketsim.compute_portvals(data=df_both_in, symbol=insample_args['symbol'], commission=0.0, impact=0.0,
                               sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31))[0]
    port_val_both_out = marketsim.compute_portvals(data = df_both_out ,symbol=outsample_args['symbol'], commission=0.0, impact=0.0,
                               sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31))[0]

    port_val_both_normal = port_val_both_in / port_val_both_in.iloc[0]
    port_val_both_out = port_val_both_out / port_val_both_out.iloc[0]

    benchmark_normal = benchmark / benchmark[0]
    benchmark_normal_out = benchmark_out / benchmark_out[0]
    val_plot(3, port_val_both_normal, benchmark_normal, df_both_in, 'Manual Strategy: In Sample')
    val_plot(4, port_val_both_out, benchmark_normal_out, df_both_out, 'Manual Strategy: Out Sample')
    # plt.show()