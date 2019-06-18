import pandas as pd
import numpy as np
import util
import datetime as dt
import marketsim
import matplotlib.pyplot as plt

# df_trades = tos.testPolicy(symbol = "AAPL", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000)


# Assume that we can predict the price exactly, in other words, we've already known wether the price will go up or down.

# To achive the optimal ending value, we have to make sure that before everytime price goes up, we buy(long), before everytime
# the price goes down, we sell.
class TheoreticallyOptimalStrategy():


    def testPolicy(self, symbol, sd, ed, sv):
        df_trades = pd.DataFrame({'Date':'','trade':''}, index=[])
        options = [1000, -1000, 0]
        symbols = []
        symbols.append(symbol)
        data = util.get_data(symbols = symbols, dates= pd.date_range(sd,ed))
        data = pd.DataFrame(data['JPM'])
        data_pct = data.pct_change()
        for i in range(1,len(data_pct)):

            change = data_pct.iloc[i][0]
            pre_date = data_pct.iloc[i-1].name
            holding = df_trades.trade.sum()
            if holding == 0:
                if change > 0:
                    trade = options[0]
                    df_trades = df_trades.append({'Date':pre_date, 'trade': trade}, ignore_index=True)
                else:
                    trade = options[1]
                    df_trades = df_trades.append({'Date':pre_date, 'trade': trade}, ignore_index=True)
            else:
                if change > 0 and holding < 0 :
                # buy 1000 shares, long 1000 shares
                    trade = options[0] + 1000
                    df_trades = df_trades.append({'Date':pre_date, 'trade': trade}, ignore_index=True)
                elif change < 0 and holding >0:
                # sell 1000 shares, short 1000 shares
                    trade = options[1] - 1000
                    df_trades = df_trades.append({'Date':pre_date, 'trade': trade}, ignore_index=True)
                else:
                    continue
        return df_trades

    def benchmark(self,symbol, sd, ed, sv):
        num_share = 1000
        price_data = util.get_data(symbols=[symbol], dates=pd.date_range(sd, ed))[symbol]
        port_val = price_data * num_share
        cash = price_data[0] * num_share
        port_val = (sv - cash) + port_val

        # normal_val = port_val / port_val[0]

        return port_val

if __name__ == "__main__":
    sd_insample = '2008-01-01'
    ed_insample = '2009-12-31'

    tos = TheoreticallyOptimalStrategy()
    df = tos.testPolicy('JPM',sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000)
    benchmark = tos.benchmark('JPM', sd = dt.datetime(2008,1,1), ed = dt.datetime(2009,12,31), sv = 100000)
    port_val = marketsim.compute_portvals(data = df, symbol='JPM', start_val = 100000, commission=0.0, impact=0.0, sd=sd_insample, ed=ed_insample)[0]


    print 'Cumulative return of the benchmark: '
    print benchmark[-1] / benchmark[0] - 1
    print 'Cumulative return of the portfolio: '
    print port_val[-1] / port_val[0] - 1
    print 'Stdev of daily returns of benchmark: '
    print benchmark.pct_change().std()
    print 'Stdev of daily returns of portfolio: '
    print port_val.pct_change().std()
    print 'Mean of daily returns of benchmark: '
    print benchmark.pct_change().mean()
    print 'Mean of daily returns of portfolio: '
    print port_val.pct_change().mean()


    port_val_normal = port_val/port_val.iloc[0]
    benchmark_normal = benchmark/benchmark[0]

    fig = plt.figure(1)

    plt.plot(port_val_normal, label = 'port_val')
    plt.plot(benchmark_normal, label = 'benchmark_val')
    plt.title('Optimal Strategy')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.xticks(rotation = 30)
    plt.legend(loc = 'best')


