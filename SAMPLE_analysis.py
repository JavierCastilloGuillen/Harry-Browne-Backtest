import pandas as pd
import pyfolio as pf
import pickle
 
def create_benchmark(fname):
    bench = pd.read_csv('{}.csv'.format(fname), index_col='date', parse_dates=True, date_parser=lambda col: pd.to_datetime(col, utc=True))
    bench_series = pd.Series(bench['return'].values, index=bench.index)
    bench_series.rename(fname, inplace=True)
    return bench_series

def process_performance(fname):
    perf = pd.read_pickle('{}.pickle'.format(fname))
    perf.to_csv('{}.csv'.format(fname))
    perf.index = perf.index.normalize()
    return perf

def analyze(perfdata, benchdata):
    returns, positions, transactions = pf.utils.extract_rets_pos_txn_from_zipline(perfdata)
    #pf.create_.... choose the method to call
