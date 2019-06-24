import indicator
import marketsim
import pandas as pd
import numpy as np
import datetime as dt
import util
import matplotlib.pyplot as plt


class ManualStrategy():

    def benchmark(self,symbol, sd, ed, sv):
        num_share = 1000
        price_data = util.get_data(symbols=[symbol], dates=pd.date_range(sd, ed))[symbol]
        port_val = price_data * num_share
        cash = price_data[0] * num_share
        port_val = (sv - cash) + port_val
        return port_val


    def testPolicy_only_bands(self, symbol, sd, ed, sv):
        df_trades = pd.DataFrame({'Date':'','trade':''}, index=[])
        options = [1000, -1000, 0]
        symbols = []
        symbols.append(symbol)
        data = util.get_data(symbols = symbols, dates= pd.date_range(sd,ed))
        data = pd.DataFrame(data['JPM'])
        data_pct = data.pct_change()

        price_indicator, what = indicator.main(symbol, sd, ed)
        price_indicator['up_sale'] = price_indicator['upper']/price_indicator['price']
        price_indicator['down_buy'] = price_indicator['lower']/price_indicator['price']

        length = len(data)
        threshold = 1

        for i in range(20,length):
            sale_indicator = price_indicator['up_sale'].iloc[i]
            buy_indicator = price_indicator['down_buy'].iloc[i]


            date = data.iloc[i].name
            holding = df_trades.trade.sum()

            if holding == 0:
                if buy_indicator > threshold:
                    trade = options[0]
                    df_trades = df_trades.append({'Date':date, 'trade': trade}, ignore_index=True)
                elif sale_indicator < threshold:
                    trade = options[1]
                    df_trades = df_trades.append({'Date':date, 'trade': trade}, ignore_index=True)
                else:
                    continue
            else:
                if buy_indicator > threshold and holding < 0 :
                    # buy 1000 shares, long 1000 shares

                        trade = options[0] + 1000
                        df_trades = df_trades.append({'Date':date, 'trade': trade}, ignore_index=True)
                elif sale_indicator < threshold and holding >0:
                    # sell 1000 shares, short 1000 shares
                        trade = options[1] - 1000
                        df_trades = df_trades.append({'Date':date, 'trade': trade}, ignore_index=True)

                else:
                    continue
                    # continue
        return df_trades
    def testPolicy_nvi(self, symbol, sd, ed, sv):
        df_trades = pd.DataFrame({'Date':'','trade':''}, index=[])
        options = [1000, -1000, 0]
        symbols = []
        symbols.append(symbol)
        data = util.get_data(symbols = symbols, dates= pd.date_range(sd,ed))
        data = pd.DataFrame(data['JPM'])
        data_pct = data.pct_change()

        price_indicator, volume_indicator = indicator.main(symbol, sd, ed)
        price_indicator['up_sale'] = price_indicator['upper']/price_indicator['price']
        price_indicator['down_buy'] = price_indicator['lower']/price_indicator['price']
        volume_indicator['volume_indicator_pvi'] = volume_indicator['PVI'] / volume_indicator['es_PVI']
        volume_indicator['volume_indicator_nvi'] = volume_indicator['NVI'] / volume_indicator['es_NVI']


        # SMA_change = SMA.pct_change().shift(-5)
        # print price_indicator.head()
        # date_lst = data.index
        length = len(data)
        buy_threshold = 1
        sell_threshold = 1
        # depends on individual risk preference.


        # when buy_threshold = 0.6
        # sell_threshold = 0.3
        # performance is pretty good

        # the threshold depends on the volality
        for i in range(0,length):
            # print price_indicator['up_sale'].iloc[i]
            # sale_indicator = price_indicator['up_sale'].iloc[i]
            # buy_indicator = price_indicator['down_buy'].iloc[i]

            indicator_volume = volume_indicator['volume_indicator_pvi'] .iloc[i]
            # change = ratio.iloc[i][0]
            date = data.iloc[i].name
            # date = date_lst[i]
            holding = df_trades.trade.sum()

            if holding == 0:
                if indicator_volume <1:
                    trade = options[0]
                    df_trades = df_trades.append({'Date':date, 'trade': trade}, ignore_index=True)
                # elif sale_indicator > sell_threshold:
                #     trade = options[1]
                #     df_trades = df_trades.append({'Date':date, 'trade': trade}, ignore_index=True)
                else:
                    trade = options[1]
                    df_trades = df_trades.append({'Date':date, 'trade': trade}, ignore_index=True)
                    # continue
            else:
                if indicator_volume <1 and holding < 0:
                    # if buy_indicator > buy_threshold and holding < 0 :
                    # buy 1000 shares, long 1000 shares

                    trade = options[0] + 1000
                    df_trades = df_trades.append({'Date':date, 'trade': trade}, ignore_index=True)
                    # elif sale_indicator > sell_threshold and holding >0:
                    # # sell 1000 shares, short 1000 shares
                    #     trade = options[1] - 1000
                    #     df_trades = df_trades.append({'Date':date, 'trade': trade}, ignore_index=True)
                elif indicator_volume >1 and holding > 0:
                    # continue
                    trade = options[1] - 1000
                    df_trades = df_trades.append({'Date': date, 'trade': trade}, ignore_index=True)
                else:
                    continue
                    # continue
        return df_trades



    def testPolicy_Qstick(self, symbol, sd, ed, sv):
        df_trades = pd.DataFrame({'Date':'','trade':''}, index=[])
        options = [1000, -1000, 0]
        symbols = []
        symbols.append(symbol)
        data = util.get_data(symbols = symbols, dates= pd.date_range(sd,ed))
        data = pd.DataFrame(data[symbol])
        data_pct = data.pct_change()

        price_indicator, qstick = indicator.main(symbol, sd, ed)
        price_indicator['up_sale'] = price_indicator['upper']/price_indicator['price']
        price_indicator['down_buy'] = price_indicator['lower']/price_indicator['price']

        length = len(data)
        threshold = 0.8

        for i in range(20,length):
            sale_indicator = price_indicator['up_sale'].iloc[i]
            buy_indicator = price_indicator['down_buy'].iloc[i]

            indicator_qstick = qstick['Qstick'] .iloc[i]
            # change = ratio.iloc[i][0]
            date = data.iloc[i].name
            # date = date_lst[i]
            holding = df_trades.trade.sum()

            if holding == 0:
                if indicator_qstick < 0:
                    trade = options[0]
                    df_trades = df_trades.append({'Date':date, 'trade': trade}, ignore_index=True)
                elif indicator_qstick > 0:
                    trade = options[1]
                    df_trades = df_trades.append({'Date':date, 'trade': trade}, ignore_index=True)
                else:
                    continue
            else:

                # if indicator_volume > 1 and holding < 0:
                if buy_indicator > threshold and holding <0:
                    trade = options[0] + 1000
                    df_trades = df_trades.append({'Date': date, 'trade': trade}, ignore_index=True)
                elif sale_indicator < threshold and holding > 0:
                    trade = options[1] - 1000
                    df_trades = df_trades.append({'Date': date, 'trade': trade}, ignore_index=True)
                elif indicator_qstick < 0 and holding < 0:
                    # buy 1000 shares, long 1000 shares
                    trade = options[0] + 1000
                    df_trades = df_trades.append({'Date': date, 'trade': trade}, ignore_index=True)

                elif  indicator_qstick < 0 and holding < 0 :
                    # buy 1000 shares, long 1000 shares
                    trade = options[0] + 1000
                    df_trades = df_trades.append({'Date':date, 'trade': trade}, ignore_index=True)
                elif indicator_qstick > 0 and holding >0:
                    # sell 1000 shares, short 1000 shares
                    trade = options[1] - 1000
                    df_trades = df_trades.append({'Date':date, 'trade': trade}, ignore_index=True)
                else:
                    continue
        return df_trades


    def testPolicy(self, symbol, sd, ed, sv):
        df_trades = pd.DataFrame({'Date':'','trade':''}, index=[])
        options = [1000, -1000, 0]
        symbols = []
        symbols.append(symbol)
        data = util.get_data(symbols = symbols, dates= pd.date_range(sd,ed))
        data = pd.DataFrame(data[symbol])
        data_pct = data.pct_change()

        price_indicator, macd = indicator.main(symbol, sd, ed)
        price_indicator['up_sale'] = price_indicator['upper']/price_indicator['price']
        price_indicator['down_buy'] = price_indicator['lower']/price_indicator['price']

        length = len(data)
        threshold = 0.8

        for i in range(20,length):
            sale_indicator = price_indicator['up_sale'].iloc[i]
            buy_indicator = price_indicator['down_buy'].iloc[i]

            # indicator_qstick = qstick['Qstick'] .iloc[i]
            indicator_macd = macd[i]
            # change = ratio.iloc[i][0]
            date = data.iloc[i].name
            # date = date_lst[i]
            holding = df_trades.trade.sum()

            if holding == 0:
                if indicator_macd < 0:

                # if indicator_qstick < 0:
                    trade = options[0]
                    df_trades = df_trades.append({'Date':date, 'trade': trade}, ignore_index=True)
                # elif indicator_qstick > 0:
                elif indicator_macd < 0 :
                    trade = options[1]
                    df_trades = df_trades.append({'Date':date, 'trade': trade}, ignore_index=True)
                else:
                    continue
            else:

                # if indicator_volume > 1 and holding < 0:
                if buy_indicator > threshold and holding <0:
                    trade = options[0] + 1000
                    df_trades = df_trades.append({'Date': date, 'trade': trade}, ignore_index=True)
                elif sale_indicator < threshold and holding > 0:
                    trade = options[1] - 1000
                    df_trades = df_trades.append({'Date': date, 'trade': trade}, ignore_index=True)
                elif indicator_macd < 0 and holding < 0:

                # elif indicator_qstick < 0 and holding < 0:
                    # buy 1000 shares, long 1000 shares
                    trade = options[0] + 1000
                    df_trades = df_trades.append({'Date': date, 'trade': trade}, ignore_index=True)

                # elif  indicator_qstick < 0 and holding < 0 :
                elif indicator_macd < 0 and holding < 0:

                    # buy 1000 shares, long 1000 shares
                    trade = options[0] + 1000
                    df_trades = df_trades.append({'Date':date, 'trade': trade}, ignore_index=True)
                # elif indicator_qstick > 0 and holding >0:
                elif indicator_macd > 0 and holding > 0:

                    # sell 1000 shares, short 1000 shares
                    trade = options[1] - 1000
                    df_trades = df_trades.append({'Date':date, 'trade': trade}, ignore_index=True)
                else:
                    continue
        df_trades.set_index('Date', inplace=True)

        return df_trades

    def testPolicy_Qstick_alone(self, symbol, sd, ed, sv):
        df_trades = pd.DataFrame({'Date': '', 'trade': ''}, index=[])
        options = [1000, -1000, 0]
        symbols = []
        symbols.append(symbol)
        data = util.get_data(symbols=symbols, dates=pd.date_range(sd, ed))
        data = pd.DataFrame(data[symbol])
        data_pct = data.pct_change()

        price_indicator, qstick = indicator.main(symbol, sd, ed)
        price_indicator['up_sale'] = price_indicator['upper'] / price_indicator['price']
        price_indicator['down_buy'] = price_indicator['lower'] / price_indicator['price']

        length = len(data)


        for i in range(20, length):
            sale_indicator = price_indicator['up_sale'].iloc[i]
            buy_indicator = price_indicator['down_buy'].iloc[i]

            indicator_qstick = qstick['Qstick'].iloc[i]
            # change = ratio.iloc[i][0]
            date = data.iloc[i].name
            # date = date_lst[i]
            holding = df_trades.trade.sum()

            if holding == 0:
                if indicator_qstick < 0:
                    trade = options[0]
                    df_trades = df_trades.append({'Date': date, 'trade': trade}, ignore_index=True)
                elif indicator_qstick > 0:
                    trade = options[1]
                    df_trades = df_trades.append({'Date': date, 'trade': trade}, ignore_index=True)
                else:
                    continue
            else:

                if indicator_qstick < 0 and holding < 0:
                    # buy 1000 shares, long 1000 shares
                    trade = options[0] + 1000
                    df_trades = df_trades.append({'Date': date, 'trade': trade}, ignore_index=True)
                elif indicator_qstick > 0 and holding > 0:
                    # sell 1000 shares, short 1000 shares
                    trade = options[1] - 1000
                    df_trades = df_trades.append({'Date': date, 'trade': trade}, ignore_index=True)

                else:
                    continue

        return df_trades




    def benchmark(self,symbol, sd, ed, sv):
        num_share = 1000
        price_data = util.get_data(symbols=[symbol], dates=pd.date_range(sd, ed))[symbol]
        port_val = price_data * num_share
        cash = price_data[0] * num_share
        port_val = (sv - cash) + port_val
        return port_val





if __name__ == "__main__":

    tos = ManualStrategy()
    sd_insample = '2008-01-01'
    ed_insample = '2009-12-31'
    sd = ' 2010-01-01'
    ed = '2011-12-31'
    symbol = 'JPM'

    df_both_in = tos.testPolicy(symbol,sd=sd_insample, ed=ed_insample, sv = 100000)
    # df_Qstick = tos.testPolicy_Qstick_alone(symbol,sd=sd_insample, ed=ed_insample, sv = 100000)
    # df_bands = tos.testPolicy_only_bands(symbol,sd=sd_insample, ed=ed_insample, sv = 100000)
    benchmark = tos.benchmark(symbol, sd=sd_insample, ed=ed_insample, sv = 100000)
    benchmark_out = tos.benchmark(symbol, sd=sd, ed=ed, sv = 100000)


    df_both_out = tos.testPolicy(symbol,sd=sd, ed=ed, sv = 100000)



    port_val_both_in = marketsim.compute_portvals(data = df_both_in,sd=sd_insample, ed=ed_insample, symbol=symbol, commission=0, impact=0)[0]
    port_val_both_out = marketsim.compute_portvals(data = df_both_out,sd=sd, ed=ed, symbol=symbol, commission=0, impact=0)[0]



    print 'Cumulative return of the in: '
    print port_val_both_in[-1] / port_val_both_in[0] - 1
    print 'Cumulative return of the out: '
    print port_val_both_out[-1] / port_val_both_out[0] - 1
    print 'Stdev of daily returns of in: '
    print port_val_both_in.pct_change().std()
    print 'Stdev of daily returns of out: '
    print port_val_both_out.pct_change().std()
    print 'Mean of daily returns of in: '
    print port_val_both_in.pct_change().mean()
    print 'Mean of daily returns of out: '
    print port_val_both_out.pct_change().mean()


    port_val_both_normal = port_val_both_in/port_val_both_in.iloc[0]
    # port_val_bands_normal = port_val_bands/port_val_bands.iloc[0]
    # port_val_Qstick_normal = port_val_Qstick/port_val_Qstick.iloc[0]
    port_val_both_out = port_val_both_out/port_val_both_out.iloc[0]


    benchmark_normal = benchmark/benchmark[0]
    benchmark_normal_out = benchmark_out/benchmark_out[0]


    tos.val_plot(2,port_val_both_normal,benchmark_normal, df_both_in, 'Bollinger Bands(threshold = 1) & Qstick')
    tos.val_plot(2,port_val_both_out, benchmark_normal_out, df_both_out, 'Out Sample')








