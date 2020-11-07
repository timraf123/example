
###############################################################################
#                          1. Importing Libraries                             #
###############################################################################

import datetime
import matplotlib.pyplot as plt
import yfinance as fyf
import pandas as pd
import json
import demjson
import sys
from pandas_datareader import data as pdr
fyf.pdr_override() 
from pyblackscholesanalytics.market.market import MarketEnvironment
from pyblackscholesanalytics.portfolio.portfolio import Portfolio
from pyblackscholesanalytics.options.options import PlainVanillaOption
from pyblackscholesanalytics.plotter.plotter import PortfolioPlotter


def get_time_parameter(option, kind='date'):
    # date time-parameter
    if kind == 'date':

        # valuation date of the option
        emission_date = option.get_t()

        # emission/expiration date of the option
        expiration_date = option.get_T()

        # time-parameter as a date-range of 5 valuation dates between t and T-10d
        time_parameter = pd.date_range(start=emission_date,
                                       end=expiration_date - pd.Timedelta(days=20),
                                       periods=5)

    # time-to-maturity time parameter    
    else:

        # time-parameter as a list of times-to-maturity
        time_parameter = [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]

    return time_parameter

def readTickers():
    tickers = []
    df = pd.read_csv('C:\options.csv')
   
    for ind in df.index: 
        tickers.append( df['Ticker'][ind])
          
    print(tickers)
        
    return tickers
    
def getTickers(tickers):
 
    start = datetime.datetime(2018, 1, 1)
    end   = datetime.datetime(2020, 10, 9)
    data = pdr.get_data_yahoo(tickers, start = start, end = end)
    return data

def getStockPrice():
    
    rd = readTickers()
    prices = getTickers(rd)
    print (prices)

def main():
    print("*** Stock Price ***")
    getStockPrice()
if __name__ == "__main__":
    main()
    msft = fyf.Ticker("CRON")
    print(msft.info)
    market_env = MarketEnvironment()
    print(market_env)
  