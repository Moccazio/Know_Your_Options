def filter_by_moneyness(df, pct_cutoff=0.2):
    crit1 = (1-pct_cutoff)*df.Strike < df.Underlying
    crit2 = df.Underlying< (1+pct_cutoff)*df.Strike
    return (df.loc[crit1 & crit2].reset_index(drop=True))            

def know_your_options(ticker, option="Call"):
    import utils 
    import QuantLib as ql 
    import pandas as pd
    import yfinance as yf
    import numpy as np
    import matplotlib.pyplot as plt

    from pandas.tseries.offsets import BDay
    end = pd.datetime.today().date()
    start = end - 252 * BDay() * 1

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

        risk_free_rate = 0.001
        day_count = ql.Actual365Fixed()
        calendar = ql.UnitedStates()

        calculation_date = ql.Date.todaysDate()
        ql.Settings.instance().evaluationDate = calculation_date

        exercise = EuropeanExercise(ql.Date(expiration.day, expiration.month, expiration.year))
        payoff = PlainVanillaPayoff(ql.Option.Call, row["strike"])
        european_option = EuropeanOption(payoff,exercise)
        
        spot_handle = ql.QuoteHandle(ql.SimpleQuote(current_price))
        flat_ts = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date, risk_free_rate, day_count))
        dividend_yield = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date, dividend_rate, day_count))
        flat_vol_ts = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(calculation_date, calendar, row["impliedVolatility"], day_count))
        bsm_process = ql.BlackScholesMertonProcess(spot_handle, dividend_yield, flat_ts, flat_vol_ts)
            
        european_option.setPricingEngine(ql.AnalyticEuropeanEngine(bsm_process))

        return {"Underlying": current_price,
                "Ticker": ticker,
                "YTE": row["yte"],
                "DTE": row["dte"],
                "Strike": row["strike"],
                "Last": row["lastPrice"],
                "Bid": row["bid"],
                "Ask": row["ask"],
                "IV": row["impliedVolatility"],
                "NPV": european_option.NPV(),
                "Delta": european_option.delta(),
                "Gamma": european_option.gamma(),
                "Theta": european_option.theta() / 365,
                "AKA": row["contractSymbol"]}        
        
    def create_put(row):

        risk_free_rate = 0.001
        day_count = ql.Actual365Fixed()
        calendar = ql.UnitedStates()

        calculation_date = ql.Date.todaysDate()
        ql.Settings.instance().evaluationDate = calculation_date

        exercise = EuropeanExercise(ql.Date(expiration.day, expiration.month, expiration.year))
        payoff = PlainVanillaPayoff(ql.Option.Put, row["strike"])
        european_option = EuropeanOption(payoff,exercise)
        
        spot_handle = ql.QuoteHandle(ql.SimpleQuote(current_price))
        flat_ts = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date, risk_free_rate, day_count))
        dividend_yield = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date, dividend_rate, day_count))
        flat_vol_ts = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(calculation_date, calendar, row["impliedVolatility"], day_count))
        bsm_process = ql.BlackScholesMertonProcess(spot_handle, dividend_yield, flat_ts, flat_vol_ts)
            
        european_option.setPricingEngine(ql.AnalyticEuropeanEngine(bsm_process))

        return {"Underlying": current_price,
                "Ticker": ticker,
                "YTE": row["yte"],
                "DTE": row["dte"],
                "Strike": row["strike"],
                "Last": row["lastPrice"],
                "Bid": row["bid"],
                "Ask": row["ask"],
                "IV": row["impliedVolatility"],
                "NPV": european_option.NPV(),
                "Delta": european_option.delta(),
                "Gamma": european_option.gamma(),
                "Theta": european_option.theta() / 365,
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
            calls = calls.drop(columns = ['contractSize', 'currency', 'change', 'percentChange', 'lastTradeDate'])
            strike_price = calls["strike"]
            
            options = calls.apply(create_call, axis=1, result_type="expand")
            options_ = options_.append(options, ignore_index=True) 
    else:    
        
        tk = yf.Ticker(ticker)
        exps = tk.options
        
        for e in exps:
            opt = tk.option_chain(e)
            puts = pd.DataFrame().append(opt.calls)
            puts['expirationDate'] = e
            expiration =  pd.to_datetime(e) + datetime.timedelta(days = 1)
            puts['expirationDate'] = expiration
            puts['yte'] = (puts['expirationDate'] - datetime.datetime.today()).dt.days / 365
            puts['dte'] = (puts['expirationDate'] - datetime.datetime.today()).dt.days
            puts[['bid', 'ask', 'strike']] = puts[['bid', 'ask', 'strike']].apply(pd.to_numeric)
            puts = puts.drop(columns = ['contractSize', 'currency', 'change', 'percentChange', 'lastTradeDate'])
            strike_price = puts["strike"]
            
            options = puts.apply(create_put, axis=1, result_type="expand")
            options_ = options_.append(options, ignore_index=True) 
    return  options_