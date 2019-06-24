import numpy as np
import pandas as pd
from util import get_data
import matplotlib.pyplot as plt

# create 3 indicator that i think is predictive to future stock price.

'''
The three indicators I choose are:
    1. Bollinger bands
    2. Simple moving average
    
    use bar chart to visualize volume.
'''

WINDOW_SIZE = 10


def author():
    return 'lzheng73'  #

def SMA(data):
    # Set default window size to 20
    data_normal = data/data.iloc[0]
    sma = data.rolling(window = WINDOW_SIZE).mean()
    ratio = data/sma - 1
    return data_normal, sma, ratio

def bollinger(data):
    df = pd.DataFrame()
    std_data = data.rolling(window = WINDOW_SIZE).std()
    data_normal, sma, ratio = SMA(data)
    bands_down = sma - 2*std_data
    bands_up = sma + 2*std_data
    sma_normal = sma/sma.iloc[WINDOW_SIZE]
    bands_up_normal = bands_up/bands_up.iloc[WINDOW_SIZE]
    bands_down_normal = bands_down/bands_down.iloc[WINDOW_SIZE]

    df['price_normal'] = data_normal
    df['SMA_normal'] = sma_normal
    df['SMA'] = sma
    df['lower_normal'] = bands_down_normal
    df['upper_normal'] = bands_up_normal
    df['Price/SMA'] = ratio
    df['price'] = data
    df['upper'] = bands_up
    df['lower'] = bands_down

    return df


def MACD(data):
    # df = pd.DataFrame()

    # open = get_data([symbol], pd.date_range(sd, ed), colname='Open')[symbol]
    # close = get_data([symbol], pd.date_range(sd, ed), colname='Close')[symbol]

    df = pd.DataFrame()
    # open = get_data([symbol], pd.date_range(sd, ed), colname='Open')[symbol]
    # close = get_data([symbol], pd.date_range(sd, ed), colname='Close')[symbol]
    # df['Open'] = open
    # df['Close'] = close
    # df['Close_EWM'] = df['Close'].ewm(alpha=0.05,min_periods=12).mean()
    #
    # df['Qstick'] = (df['Close_EWM'] - df['Open']).ewm(alpha=0.05, min_periods=20).mean()

    df['26_EMA'] = data.ewm(alpha=0.01,min_periods=26).mean()
    df['12_EMA'] = data.ewm(alpha=0.05,min_periods=12).mean()
    df['signal'] = data.ewm(alpha=0.01,min_periods=9).mean()
    df['MACD'] = (df['12_EMA'] - df['26_EMA']) / df['signal']

    return df


def main(symbol, sd, ed):
    data = get_data([symbol],pd.date_range(sd, ed))[symbol]
    # volumn_indicator = PVI_NVI(symbol, sd, ed)
    price_indicator = bollinger(data)
    macd = MACD(data)['MACD']
    # q_stick = CQ(symbol, sd,ed)
    return  price_indicator, macd

if __name__ == '__main__':
    price_indicator,  q_stick = main('JPM','2008-01-01','2009-12-31')
    # price_indicator_normal = price_indicator[['price_normal','lower_normal','upper_normal','SMA_normal','ratio']]
    price_indicator_normal = price_indicator[['price_normal','lower_normal','upper_normal','SMA_normal','Price/SMA']]


    ax_qstick = q_stick['Qstick'].plot(title = "Tushar Chande's QStick Indicator")
    ax_qstick.set_xlabel('Qstick indicator')
    ax_qstick.set_ylabel('Date')

    ax_price_normal = price_indicator_normal.plot(title = 'Normalized Bollinger Bands & SMA')
    ax_price_normal.set_xlabel('Date')
    ax_price_normal.set_ylabel('Normalized Price')


    ax_bollinger = price_indicator[['price','lower','upper','SMA']].plot(title = 'Bollinger Bands')
    ax_bollinger.set_xlabel('Date')
    ax_bollinger.set_ylabel('Price')

