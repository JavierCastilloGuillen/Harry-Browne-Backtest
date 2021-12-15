
Make sure you create an specific virtual environment for zipline, pyfolio and their dependencies. They might generate conflict if not done it this way.

The program has the Permanent_Portfolio_web_example.py which is the main file, trading_days.py which is needed to generate the trading dates.

Then two SAMPLE files. as a way to understand better the step by step described on Permanent_Portfolio_web_example.py

The Permanent_Portfolio_web_example.py has 3 steps described during the process
Program splited into cells #%% to make easier on step by step.

##  PHASE 1 DATA RETREIVAL, FILTERING AND PROCESSING 

-  Get the stocks to be used on backtest. For our example 4 ETF's and store them on data/bars_adj
-  Get Trading Calendar Days Running: trading_days.py MODIFY DATES according to your stock data!!
-  We will need it to index our market data
-  Formatting data to be read by ZIPLINE basic pandas here...
-  This function will create adjusted data on folder /data/csvs/daily
-  Modify your extension.py file to ingest data, generally located here C:\Users\YOURNAME\\.zipline see sample on extension.py
-  See SAMPLE-FILE_extension.py 
-  On your extension.py you'll need to add your path and your trading dates
-  Once here, you're prepared to ingest the data to be used by running on your virtual environment prompt: $ zipline -b ingest custom-csvdir-bundle


## PHASE 2 ALGORITHM LOGICS 

- Define your context, initialize, handle_data if needed, read zipline documentation for more. ;)
- Due weight strategy, ETF's weight = 25% of total portfolio size
- Schedule function to trigger the rebalance function as you see, monthly to make it funnier for sample (Harry Browne Model adjust yearly)
- Creating a benchmark (as sample on the code bear in mind SPY is one of the ETF's we hold in the portfolio ;) ) 
- Rebalance function to readjust weights once schedule function is triggered.
- Create a sector map for further analysis. Convenient for stocks.
- Running the backtest SELECT CORRECT DATES and (read run_algorithm() docs, to go deeper on this) but basically we select the data source, dates, previous data (initialize), handle_data if needed, starting capital, etc. 



## PHASE 3 ANALYTICS 

- On analysis.py we could define functions for the performance, bencmhark and analysis charts what we will require
- As an example we will do it importing create_benchmark from analysis.py
- The more you customise your system the more convenient to fullfill this analyisis file to clean the main code. 
- Creating a benchmark to compare results. As said before SPY what we hold, but just as an example.


### IS CONVENIENT TO READ:

Read the documentation for more information: https://zipline.ml4trading.io/

Problems with ingesting data:https://zipline.ml4trading.io/bundles.html
