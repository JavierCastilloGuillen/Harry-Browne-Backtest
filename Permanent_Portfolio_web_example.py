#%%
import pandas as pd
import zipline
import pickle
import pytz
import numpy as np
import csv
import os
from zipline.api import order, record, order_target_percent, symbol, schedule_function, date_rules, time_rules
import datetime as dt
from matplotlib import pyplot as plt, ticker, rc
import pandas_datareader as pdr
import pyfolio as pf
from SAMPLE_analysis import analyze, create_benchmark, process_performance
import warnings
warnings.filterwarnings('ignore')

##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################


#### ====== PHASE 1 DATA RETREIVAL, FILTERING AND PROCESSING ====== ####

# 1. Get the stocks to be used on backtest. For our example 4 ETF's and store them on data/bars_adj
# 2. Get Trading Calendar Days Running: trading_days.py MODIFY DATES according to your stock data!!
# 3. We will need it to index our market data
# 4. Formatting data to be read by ZIPLINE basic pandas here...
# 5. This function will create adjusted data on folder /data/csvs/daily
# 6. Modify your extension.py file to ingest data, generally located here C:\Users\YOURNAME\.zipline see sample on extension.py
#       6.1 See SAMPLE-FILE_extension.py 
#       6.2 On your extension.py you'll need to add your path and your trading dates
# 7. Once here, you're prepared to ingest the data to be used by running on your virtual environment prompt: $ zipline -b ingest custom-csvdir-bundle



# %% 
# 1. Get the stocks to be used on your backtest...

stocks = ['SPY', 'GLD', 'TLT', 'SHY' ]

'''
For the example and convenience for general users, we will retreive data from yahoo
Stock tickers where
SPY = S&P500 ETF for Stocks
GLD = Gold ETF for Gold
TLT = Long Term Bond ETF 
SHY = Short term Bond ETF for cash
'''

now = dt.datetime.now()
startyear = 2005
startmonth = 1 
startday = 1
start = dt.datetime(startyear, startmonth, startday)
a=0
for stock in stocks:
	try:
		a +=1
		df = pdr.get_data_yahoo(stock, start, now)
		print(f'Getting data {a}.....{stock}')
		df.to_csv(f'{stock}.csv')
	except Exception as e:
		print("No results found on "+stock)
		pass



#%%
# 3. We will need it to index our market data
# Read the trading_calendar obtained from trading_days.py... and array trading days for indexing
with open('trading_calendar.csv') as f:
    reader = csv.reader(f)
    data = list(reader)

arr = np.array(data)
trading_days = arr.ravel() 


#%%
# 4. Formatting data to be read by ZIPLINE
def format_bundle(indir, outdir):
       
    count = 0
    for f in os.listdir(indir): # For Production
        
        df = pd.read_csv('{}/{}'.format(indir, f))
        df = df.drop(columns=['Close'], axis=1)
        df = df.set_index(trading_days)
        df = df.reindex(trading_days)
        df.reset_index(inplace=True)
        df.rename(columns={'Date':'date',
                    'Open': 'open',
                    'High': 'high',
                    'Low': 'low',
                    'Adj Close': 'close',
                    'Volume': 'volume'
                    }, inplace=True)
        if not 'dividend' in df.columns:
            df['dividend'] = 0.0
        df['split'] = 1
        df = df[['date','open','high','low','close','volume','dividend', 'split']]
        # if you want to see... print(df.info())
        # if you want to see... print(df)        
        
        # Round the numbers in the dataframe
        df = df.round({'open':2,
                  'high':2,
                  'low':2,
                  'close':2,
                  'volume':1,
                  'dividend':2})
        df.to_csv('{}/{}'.format(outdir, f), index=False)

        count += 1
        
    return ('{} files was adjusted'.format(count))


#%%  
# 5. This function will create adjusted data on folder /data/csvs/daily
format_bundle('data/bars_adj', 'data/csvs/daily')

# Time to modify extension.py step 6

# Run on your virtual environment prompt: $ zipline -b ingest custom-csvdir-bundle




##########################################################################################
##########################################################################################
##########################################################################################

#### ====== PHASE 2 ALGORITHM LOGICS ====== ####

# 1. Define your context, initialize, handle_data if needed, read zipline documentation for more. ;)
#   1.1 Due weight strategy, ETF's weight = 25% of total portfolio size
#   1.2 Schedule function to trigger the rebalance function as you see, monthly to make it funnier for sample (Harry Browne Model adjust yearly)
#   1.3 Creating a benchmark (as sample on the code bear in mind SPY is one of the ETF's we hold in the portfolio ;) ) 
#   1.4 Rebalance function to readjust weights once schedule function is triggered.
#   1.5 Create a sector map for further analysis. Convenient for stocks.
# 2. Running the backtest SELECT CORRECT DATES and (read run_algorithm() docs, to go deeper on this) but basically we select the data source, 
#    dates, previous data (initialize), handle_data if needed, starting capital, etc. 




#%%
## Initializing...
def initialize(context):
    # Weights for Harry Browne permanent portfolio
    context.securities = {
        'GLD': 0.25, 
        'SHY': 0.25, 
        'SPY': 0.25, 
        'TLT': 0.25, 
    }
    
    # Schedule rebalance for once a month
    schedule_function(rebalance, date_rules.month_start(), time_rules.market_open())
    # Replace date_rules.month_start() for date_rules.year_start() to get real Harry Browne Hipotesys rebalance yearly


    # Define ticker or data to be used as benchmark
    context.set_benchmark(symbol('SPY'))


def rebalance(context, data):
    for sec, weight in context.securities.items():
        sym = symbol(sec)
        
        if data.can_trade(sym):
            # Rebalance weight in portfolio
            order_target_percent(sym, weight) 



#%%
## Running the backtest...
start = pd.Timestamp('2005-01-03', tz='utc')
end = pd.Timestamp('2021-06-25', tz='utc')
sect_map = {'SPY': 'Shares',
            'SHY': 'Cash/Short Term Bond', 
            'TLT': 'Long Term Bond', 
            'GLD': 'Gold'}
result = zipline.run_algorithm(
    start=start,
    end=end,  
    initialize=initialize, # Initialize variables
    capital_base=100000, # Capital to start the backtest
    data_frequency = 'daily',  # Data frequency
    bundle='custom-csvdir-bundle' ) # The bundle for data retreival

print("Backtest process is finished, ready to analysis.")


##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################

#### ====== PHASE 3 ANALYSIS ====== ####


# 1. On analysis.py we could define functions for the performance, bencmhark and analysis charts what we will require
#   1.1 As an example we will do it importing create_benchmark from analysis.py
#   1.2 The more you customise your system the more convenient to fullfill this analyisis file to clean the main code. 
# 2. Creating a benchmark to compare results. As said before SPY what we hold, but just as an example.



#%% 
# Create a benchmark file for Pyfolio using analysis.py
bench_df = pd.read_csv('/Users/javie/Desktop/Harry Browne Backtest/data/csvs/daily/SPY.csv' )
bench_df['return'] = bench_df.close.pct_change()
bench_df.to_csv('SPY.csv', columns=['date','return'], index=False)
# Create a benchmark dataframe from function coming from analysis.py
bench_series = create_benchmark('SPY')
result.index = result.index.normalize() # to set the time to 00:00:00
bench_series = bench_series[bench_series.index.isin(result.index)]
print('Benchmark File created')



#%%
# Extract DataFrames for metrics 
returns, positions, transactions = pf.utils.extract_rets_pos_txn_from_zipline(result)
# If you want to see.. print(returns, positions, transactions)
print('Metrics extracted')

#%%
# Call the analysis required from your analysis.py functions

# analyze(result, bench_series)
# pf.create_returns_tear_sheet(returns, 
#                             benchmark_rets= bench_series, 
#                             live_start_date='2019-1-1', 
#                             positions= positions, 
#                             transactions=transactions)
pf.create_full_tear_sheet(returns, 
                          benchmark_rets= bench_series, 
                          live_start_date='2019-1-1', 
                          positions= positions, 
                          transactions=transactions,
                          sector_mappings=sect_map)





#%%
# If needed, export to csv, prepare .xlsx, etc..
result.to_csv('result.csv')
# %%
