import pandas as pd
pd.options.display.float_format = '{:,.8f}'.format
def filter_by_moneyness(df, pct_cutoff=0.2):
    crit1 = (1-pct_cutoff)*df.Strike < df.Underlying
    crit2 = df.Underlying< (1+pct_cutoff)*df.Strike
    return (df.loc[crit1 & crit2].reset_index(drop=True))            

def know_your_options(ticker, option="Call"):
    import datetime
    import re
    import utils 
    import QuantLib as ql 
    import pandas as pd
    import yfinance as yf
    import numpy as np
    import matplotlib.pyplot as plt
    from yahoo_fin.stock_info import get_quote_table

    import warnings
    plt.style.use('dark_background')
    warnings.simplefilter(action='ignore', category=FutureWarning)
                
    info = get_quote_table(ticker)
    current_price = info["Quote Price"]
    yield_re = re.compile(r"\((?P<value>(\d+\.\d+))%\)")
    try:
        dividend_rate = float(yield_re.search(info["Forward Dividend & Yield"])["value"])
    except (KeyError, ValueError, TypeError):
        dividend_rate = 0.0      
        
    def create_call(row):
    
        calculation_date = ql.Date.todaysDate()
        ql.Settings.instance().evaluationDate = calculation_date

        risk_free_rate = 0.001
        day_count = ql.Actual365Fixed()
        settlement = calculation_date
        calendar = ql.UnitedStates()

        exercise = ql.AmericanExercise(settlement, ql.Date(expiration.day, expiration.month, expiration.year))
        payoff = ql.PlainVanillaPayoff(ql.Option.Call, row["strike"])
        american_option = ql.VanillaOption(payoff,exercise)
        
        spot_handle = ql.QuoteHandle(ql.SimpleQuote(current_price))
        flat_ts = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date, risk_free_rate, day_count))
        dividend_yield = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date, dividend_rate, day_count))
        flat_vol_ts = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(calculation_date, calendar, row["impliedVolatility"], day_count))
        bsm_process = ql.BlackScholesMertonProcess(spot_handle, dividend_yield, flat_ts, flat_vol_ts)
            
        american_option.setPricingEngine(ql.FdBlackScholesVanillaEngine(bsm_process, 100, 100))

        return {"Underlying": current_price,
                "Ticker": ticker,
                "Type": row["type"],
                "Expiration": row['expirationDate'],
                "YTE": row["yte"],
                "DTE": row["dte"],
                "Strike": row["strike"],
                "Last": row["lastPrice"],
                "Bid": row["bid"],
                "Ask": row["ask"],
                "Midpoint": (row['bid'] + row['ask']) / 2,
                "Spread": row['ask'] - row['bid'],
                "IV": row["impliedVolatility"],  
                "NPV": american_option.NPV(),
                "Delta": american_option.delta(),
                "Gamma": american_option.gamma(),
                "Theta": american_option.theta() / 365,
                "AKA": row["contractSymbol"]}        
        
    def create_put(row):

        calculation_date = ql.Date.todaysDate()
        ql.Settings.instance().evaluationDate = calculation_date

        risk_free_rate = 0.001
        day_count = ql.Actual365Fixed()
        settlement = calculation_date
        calendar = ql.UnitedStates()
        
        exercise = ql.AmericanExercise(settlement, ql.Date(expiration.day, expiration.month, expiration.year))
        payoff = ql.PlainVanillaPayoff(ql.Option.Put, row["strike"])
        american_option = ql.VanillaOption(payoff,exercise)
        
        spot_handle = ql.QuoteHandle(ql.SimpleQuote(current_price))
        flat_ts = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date, risk_free_rate, day_count))
        dividend_yield = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date, dividend_rate, day_count))
        flat_vol_ts = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(calculation_date, calendar, row["impliedVolatility"], day_count))
        bsm_process = ql.BlackScholesMertonProcess(spot_handle, dividend_yield, flat_ts, flat_vol_ts)
            
        american_option.setPricingEngine(ql.FdBlackScholesVanillaEngine(bsm_process, 100, 100))
        

        return {"Underlying": current_price,
                "Ticker": ticker,
                "Type": row["type"],
                "Expiration": row['expirationDate'],
                "YTE": row["yte"],
                "DTE": row["dte"],
                "Strike": row["strike"],
                "Last": row["lastPrice"],
                "Bid": row["bid"],
                "Ask": row["ask"],
                "Midpoint": (row['bid'] + row['ask']) / 2,
                "Spread": row['ask'] - row['bid'],
                "IV": row["impliedVolatility"],  
                "NPV": american_option.NPV(),
                "Delta": american_option.delta(),
                "Gamma": american_option.gamma(),
                "Theta": american_option.theta() / 365,
                "AKA": row["contractSymbol"]}                  
        
    options_= pd.DataFrame()       
    
    if option == "Call":
        
        tk = yf.Ticker(ticker)
        exps = tk.options
        
        for e in exps:
            opt = tk.option_chain(e)
            calls = pd.DataFrame().append(opt.calls)
            calls['expirationDate'] = e
            expiration =  pd.to_datetime(e) + datetime.timedelta(days = 1)
            calls['expirationDate'] = expiration
            calls['yte'] = (calls['expirationDate'] - datetime.datetime.today()).dt.days / 365
            calls['dte'] = (calls['expirationDate'] - datetime.datetime.today()).dt.days
            calls[['bid', 'ask', 'strike']] = calls[['bid', 'ask', 'strike']].apply(pd.to_numeric)
            calls['type'] = "Call"
            calls = calls.drop(columns = ['contractSize', 'currency', 'change', 'percentChange', 'lastTradeDate'])
            options = calls.apply(create_call, axis=1, result_type="expand")
            options_ = options_.append(options, ignore_index=True) 
    else:    
        
        tk = yf.Ticker(ticker)
        exps = tk.options
        
        for e in exps:
            opt = tk.option_chain(e)
            puts = pd.DataFrame().append(opt.puts)
            puts['expirationDate'] = e
            expiration =  pd.to_datetime(e) + datetime.timedelta(days = 1)
            puts['expirationDate'] = expiration
            puts['yte'] = (puts['expirationDate'] - datetime.datetime.today()).dt.days / 365
            puts['dte'] = (puts['expirationDate'] - datetime.datetime.today()).dt.days
            puts[['bid', 'ask', 'strike']] = puts[['bid', 'ask', 'strike']].apply(pd.to_numeric)
            puts['type'] = "Put"
            puts = puts.drop(columns = ['contractSize', 'currency', 'change', 'percentChange', 'lastTradeDate'])
            options = puts.apply(create_put, axis=1, result_type="expand")
            options_ = options_.append(options, ignore_index=True) 
    return  options_

data_c = know_your_options("AAPL", option="Call")
data_p = know_your_options("AAPL", option="Put")
data = pd.DataFrame().append(data_c).append(data_p)


def save_sp500_tickers():
    import bs4 as bs
    from bs4 import BeautifulSoup
    import requests
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'html')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        if not '.' in ticker:
            tickers.append(ticker.replace('\n',''))    
    return tickers
symbols = save_sp500_tickers()

def _get_option_data(symbols):
    
    symbol_count = len(symbols)
    N = symbol_count
    missing_symbols = []
    _merged = []
    for i, sym in enumerate(symbols, start=1):
        if not pd.isnull(sym):
            try:
                data_c = know_your_options(sym, option="Call")
                data_p = know_your_options(sym, option="Put")
                data = pd.DataFrame().append(data_c).append(data_p)
                fbm_data = filter_by_moneyness(data)
                fbm_data.to_csv("data/"+sym+".csv")
                
            except Exception as e:
                print(e, sym)
                missing_symbols.append(sym)
            N -= 1
            pct_total_left = (N / symbol_count)
            print('{}..[done] | {} of {} symbols collected | {:>.2%}'.format(\
                                                            sym, i, symbol_count, pct_total_left))
    return missing_symbols