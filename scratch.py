import os
import pandas as pd

def symbol_to_path(symbol, base_dir="data"):
    return os.path.join(base_dir,"{}.csv".format(str(symbol)))

def get_data(symbols, dates):
    df = pd.DataFrame(index=dates)
    if 'SPY' not in symbols:
        symbols.insert(0, 'SPY')
    # join data for each symbol in symbols
    for symbol in symbols:
        df_temp = pd.read_csv(symbol_to_path(symbol),index_col='Date',
            parse_dates=True, usecols=['Date','Adj Close'],na_values=['nan'])
        df_temp = df_temp.rename(columns={'Adj Close': symbol})
        df = df.join(df_temp)
        if symbol == 'SPY':
            df = df.dropna(subset=["SPY"])
    return df

def test_run():
    my_dates = pd.date_range("2010-01-01","2010-12-31")
    my_symbols = ['GOOG','IBM','GLD']
    df = get_data(my_symbols, my_dates)

    print(df[['GOOG','GLD']])

if __name__ == "__main__":
    test_run()
    


