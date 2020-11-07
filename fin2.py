
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
import matplotlib.pyplot as plt

def time_values(option, kind='date'):
 
    if kind == 'date':

        stardate = option.get_t()
        expire = option.get_T()

        # time-parameter as a date-range of 5 valuation dates between t and T-10d
        time_values = pd.date_range(start=stardate,
                                       end=expire - pd.Timedelta(days=20),
                                       periods=5)

    else:

        time_values = [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]

    return time_values

def test_matplot():
    labels = ['G1', 'G2', 'G3', 'G4', 'G5']
    men_means = [20, 35, 30, 35, 27]
    women_means = [25, 32, 34, 20, 25]
    men_std = [2, 3, 4, 1, 2]
    women_std = [3, 5, 2, 3, 3]
    width = 0.35       # the width of the bars: can also be len(x) sequence
    
    fig, ax = plt.subplots()
    
    ax.bar(labels, men_means, width, yerr=men_std, label='Men')
    ax.bar(labels, women_means, width, yerr=women_std, bottom=men_means,
           label='Women')
    
    ax.set_ylabel('Scores')
    ax.set_title('Scores by group and gender')
    ax.legend()
    
    plt.show()

def readTickers():
    tickers = []
    df = pd.read_csv('C:\options.csv')
   
    for ind in df.index: 
        tickers.append( df['Ticker'][ind])
          
    print(tickers)
        
    return tickers
    
def getTickers(tickers):
 
    start = datetime.datetime(2018, 1, 1)
    enddate   = datetime.datetime(2020, 10, 9)
    data = pdr.get_data_yahoo(tickers, start = start, end = enddate)
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
    test_matplot()
  