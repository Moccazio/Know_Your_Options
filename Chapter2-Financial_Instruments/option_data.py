import datetime
import re
import pandas as pd
import QuantLib as ql
import pandas as pd
import numpy as np
import yfinance as yf
from yahoo_fin.stock_info import get_quote_table

def filter_by_moneyness(df, pct_cutoff=0.2):
    crit1 = (1-pct_cutoff)*df.Strike < df.Underlying_Price
    crit2 = df.Underlying_Price < (1+pct_cutoff)*df.Strike
    return (df.loc[crit1 & crit2].reset_index(drop=True))

def options_chain(symbol):
    info = get_quote_table(symbol)
    current_price = info["Quote Price"]
    tk = yf.Ticker(symbol)
    exps = tk.options
    options = pd.DataFrame()
    for e in exps:
        opt = tk.option_chain(e)
        opt = pd.DataFrame().append(opt.calls).append(opt.puts)
        opt['expirationDate'] = e
        options = options.append(opt, ignore_index=True)
    options['expirationDate'] = pd.to_datetime(options['expirationDate']) + datetime.timedelta(days = 1)
    options['yte'] = (options['expirationDate'] - datetime.datetime.today()).dt.days / 365
    options['dte'] = (options['expirationDate'] - datetime.datetime.today()).dt.days
    options['CALL'] = options['contractSymbol'].str[4:].apply(
        lambda x: "C" in x)
    options[['bid', 'ask', 'strike']] = options[['bid', 'ask', 'strike']].apply(pd.to_numeric)
    options['midpoint'] = (options['bid'] + options['ask']) / 2 
    options['spread'] =  (options['ask'] - options['bid'])
    options['spread_pct'] = (options['ask'] - options['bid'])/options['ask'] 
    options['Underlying'] = current_price 
    options = options.drop(columns = ['contractSize', 'currency', 'change', 'percentChange', 'lastTradeDate'])
    return pd.DataFrame({
            "Underlying": current_price,
            "Ticker": symbol,
            "Expiry": options["expirationDate"],
            "YTE": options["yte"],
            "DTE": options["dte"],
            "Call": options["CALL"],
            "IV": options["impliedVolatility"],        
            "Strike": options["strike"],
            "Last": options["lastPrice"],
            "Bid": options["bid"],
            "Ask": options["ask"],
            "Midpoint": options['midpoint'],
            "Spread": options['spread'],
            "Spread_Pct": options['spread_pct'],
            "AKA": options["contractSymbol"]})

from yahoo_fin.stock_info import tickers_sp500

tickers =  tickers_sp500()[0:50]


def _get_option_data(symbols):
    
    symbol_count = len(symbols)
    N = symbol_count
    missing_symbols = []
    _merged = []
    for i, sym in enumerate(symbols, start=1):
        if not pd.isnull(sym):
            try:
                data_ = option_data(sym)
                _merged.append(data_)
                
            except Exception as e:
                print(e, sym)
                missing_symbols.append(sym)
            N -= 1
            pct_total_left = (N / symbol_count)
            print('{}..[done] | {} of {} tickers collected | {:>.2%}'.format(\
                                                            sym, i, symbol_count, pct_total_left))
    option_df = pd.concat(_merged, axis=0) 
    print(missing_symbols)
    return option_df

_df = _get_option_data(tickers)