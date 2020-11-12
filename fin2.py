
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
import numpy as np
import seaborn as sns

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

def setPortfolio():
    
    mktEnv = MarketEnvironment()
    # strikes
    kl = 90
    ks = 110
    print(mktEnv)
    option_spread_ptf = Portfolio(name="Option Spread")
    print(option_spread_ptf)
      # 90-call
    vcl = PlainVanillaOption(mktEnv, K=kl, T='31-12-2021')
    print(vcl)
    
    vcs = PlainVanillaOption(mktEnv, K=ks, T='31-12-2021')
    print(vcs)

    # creation of bull-spread portfolio strategy   
    option_spread_ptf.add_instrument(vcl, 1)
    option_spread_ptf.add_instrument(vcs, -1)
    print(option_spread_ptf)
    
def calc_commission_rate(x):
    """ Return the commission rate based on the table:
    0-90% = 2%
    91-99% = 3%
    >= 100 = 4%
    """
    if x <= .90:
        return .02
    if x <= .99:
        return .03
    else:
        return .04

def monteCarlo():
    print("*** Monte-Carlo ***")  
    sns.set_style('whitegrid')
    avg = 1
    std_dev = .1
    num_reps = 500
    num_simulations = 1000

    pct_to_target = np.random.normal(avg, std_dev, num_reps).round(2)
    print(pct_to_target)
    
    sales_target_values = [75_000, 100_000, 200_000, 300_000, 400_000, 500_000]
    sales_target_prob = [.3, .3, .2, .1, .05, .05]
    sales_target = np.random.choice(sales_target_values, num_reps, p=sales_target_prob)
    print(sales_target)
    
    df = pd.DataFrame(index=range(num_reps), data={'Pct_To_Target': pct_to_target,
                                               'Sales_Target': sales_target})

    df['Sales'] = df['Pct_To_Target'] * df['Sales_Target']
    print(df)
    df['Commission_Rate'] = df['Pct_To_Target'].apply(calc_commission_rate)
    df['Commission_Amount'] = df['Commission_Rate'] * df['Sales']
    print(df)
    
    all_stats = []

# Loop through many simulations
    for i in range(num_simulations):

        # Choose random inputs for the sales targets and percent to target
        sales_target = np.random.choice(sales_target_values, num_reps, p=sales_target_prob)
        pct_to_target = np.random.normal(avg, std_dev, num_reps).round(2)
    
        # Build the dataframe based on the inputs and number of reps
        df = pd.DataFrame(index=range(num_reps), data={'Pct_To_Target': pct_to_target,
                                                       'Sales_Target': sales_target})
    
        # Back into the sales number using the percent to target rate
        df['Sales'] = df['Pct_To_Target'] * df['Sales_Target']
    
        # Determine the commissions rate and calculate it
        df['Commission_Rate'] = df['Pct_To_Target'].apply(calc_commission_rate)
        df['Commission_Amount'] = df['Commission_Rate'] * df['Sales']
    
        # We want to track sales,commission amounts and sales targets over all the simulations
        all_stats.append([df['Sales'].sum().round(0),
                          df['Commission_Amount'].sum().round(0),
                          df['Sales_Target'].sum().round(0)])
        
    results_df = pd.DataFrame.from_records(all_stats, columns=['Sales',
                                                           'Commission_Amount',
                                                           'Sales_Target'])
    results_df.describe().style.format('{:,}')
def main():
    print("*** Stock Price ***")
    getStockPrice()
    
if __name__ == "__main__":
    main()
    msft = fyf.Ticker("CRON")
    print(msft.info)
    test_matplot()
    setPortfolio()
    monteCarlo()