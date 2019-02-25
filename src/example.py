#
# An example from :
# https://www.datacamp.com/community/tutorials/lstm-python-stock-market
#
#
from pandas_datareader import data
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import urllib.request, json
import os
import numpy as np
import tensorflow as tf
# This code has been tested with TensorFlow 1.6
from sklearn.preprocessing import MinMaxScaler

def main():
    load_ticker('AAL')
    #test_quandl()
    return
    df = load_data()
    explore_data(df)
    plot(df)

def explore_data(df):
    # Sort DataFrame by date
    df = df.sort_values('Date')

    # Double check the result
    print(df.head())

def plot(df):
    plt.figure(figsize = (18,9))
    plt.plot(range(df.shape[0]),(df['Low']+df['High'])/2.0)
    plt.xticks(range(0,df.shape[0],500),df['Date'].loc[::500],rotation=45)
    plt.xlabel('Date',fontsize=18)
    plt.ylabel('Mid Price',fontsize=18)
    plt.show()


def test_quandl():
    import quandl
    df = quandl.get("WIKI/AAL",start_date="1971-10-01", end_date="2012-01-01")
    df.to_csv("aal.csv")

def load_ticker(ticker):

    import pandas_datareader as pdr
    import datetime
    file_to_save = 'stock_market_data-%s.csv'%ticker
    if not os.path.exists(file_to_save):
        print("Starting to download ticker data: %s" % ticker)
        finance_data_df = pdr.get_data_yahoo(ticker,
                              start =datetime.datetime(1970, 10, 1),
                              end=datetime.datetime(2019, 2, 21))
        finance_data_df.to_csv(file_to_save)
        print("file saved: %s" % file_to_save)
    else:
        print("file already downloaded")


def load_data():

    data_source = 'alphavantage' # alphavantage or kaggle
    api_key = 'JGFC2XLKMVREG5IC'
    ticker = "AAL"
    # Save data to this file
    file_to_save = 'stock_market_data-%s.csv'%ticker
    if data_source == 'alphavantage':
        # ====================== Loading Data from Alpha Vantage ==================================
        # American Airlines stock market prices

        # JSON file with all the stock market data for AAL from the last 20 years
        url_string = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=%s&outputsize=full&apikey=%s"%(ticker,api_key)


        # If you haven't already saved data,
        # Go ahead and grab the data from the url
        # And store date, low, high, volume, close, open values to a Pandas DataFrame
        if not os.path.exists(file_to_save):
            with urllib.request.urlopen(url_string) as url:
                data = json.loads(url.read().decode())
                # extract stock market data
                data = data['Time Series (Daily)']
                df = pd.DataFrame(columns=['Date','Low','High','Close','Open'])
                for k,v in data.items():
                    date = dt.datetime.strptime(k, '%Y-%m-%d')
                    data_row = [date.date(),float(v['3. low']),float(v['2. high']),
                                float(v['4. close']),float(v['1. open'])]
                    df.loc[-1,:] = data_row
                    df.index = df.index + 1
            print('Data saved to : %s'%file_to_save)
            df.to_csv(file_to_save)

        # If the data is already there, just load it from the CSV
        else:
            print('File already exists. Loading data from CSV')
            df = pd.read_csv(file_to_save)

    else:

        # ====================== Loading Data from Kaggle ==================================
        # You will be using HP's data. Feel free to experiment with other data.
        # But while doing so, be careful to have a large enough dataset and also pay attention to the data normalization
        df = pd.read_csv(os.path.join('Stocks','hpq.us.txt'), delimiter=',', usecols=['Date','Open','High','Low','Close'])
        print('Loaded data from the Kaggle repository')
    return df

if __name__ == '__main__':
    main()