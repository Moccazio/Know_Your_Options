import datetime
import re
import pandas as pd
import QuantLib as ql
import pandas as pd
import numpy as np
import yfinance as yf
from yahoo_fin.stock_info import get_quote_table

def option_data(ticker):
    
    opt_sym = yf.Ticker(ticker)
    info = get_quote_table(ticker)
    current_price = info["Quote Price"]
    yield_re = re.compile(r"\((?P<value>(\d+\.\d+))%\)")
    try:
        dividend_yield = float(
            yield_re.search(info["Forward Dividend & Yield"])["value"]
        )
    except (KeyError, ValueError, TypeError):
        dividend_yield = 0.0
    exps = opt_sym.options
    options_ = pd.DataFrame()
    def create_option(row):
        volatility = ql.BlackConstantVol(
            today,
            ql.UnitedStates(),
            row["volatility"],
            ql.Business252()
        )
        option = ql.VanillaOption(
            ql.PlainVanillaPayoff(ql.Option.Call, row["strike"]),
            exercise
        )
        process = ql.BlackScholesMertonProcess(
            ql.QuoteHandle(underlying),
            ql.YieldTermStructureHandle(dividendYield),
            ql.YieldTermStructureHandle(riskFreeRate),
            ql.BlackVolTermStructureHandle(volatility),
        )
        # Calculate it out from the last price
        imp_vol = option.impliedVolatility(row["lastPrice"], process)
        implied_volatility = ql.BlackConstantVol(
            today,
            ql.UnitedStates(),
            imp_vol,
            ql.Business252()
        )
        process = ql.BlackScholesMertonProcess(
            ql.QuoteHandle(underlying),
            ql.YieldTermStructureHandle(dividendYield),
            ql.YieldTermStructureHandle(riskFreeRate),
            ql.BlackVolTermStructureHandle(implied_volatility),
        )
        option.setPricingEngine(
            ql.FdBlackScholesVanillaEngine(process, 1000, 1000)
        )
        return {
            "Name": row["contractSymbol"],
            "Strike": row["strike"],
            "Last": row["lastPrice"],
            "Bid": row["bid"],
            "Ask": row["ask"],
            "NPV": option.NPV(),
            "Delta": option.delta(),
            "Gamma": option.gamma(),
            "Theta": option.theta() / 365,
            "Volatility": imp_vol * 100
        }
        options = calls.apply(create_option, axis=1, result_type="expand")
        
    for e in exps:
        expiration = pd.to_datetime(e) + datetime.timedelta(days = 1)
        opt = opt_sym.option_chain(e)   
        calls = pd.DataFrame().append(opt.calls).append(opt.puts)
        # Setup instruments for Black-Scholes pricing
        today = ql.Date.todaysDate()
        underlying = ql.SimpleQuote(current_price)
        exercise = ql.AmericanExercise(
            today,
        ql.Date(expiration.day, expiration.month, expiration.year))
        dividendYield = ql.FlatForward(
            today, dividend_yield, ql.Actual360()
        )
        riskFreeRate = ql.FlatForward(today, 0.0008913, ql.Actual360())
        # Filter down to only OTM strikes
        calls = calls[calls["strike"] >= current_price * 1.025]
        calls = calls[calls["strike"] <= current_price * 1.10]
        # Parse out implied volatility
        calls = calls.assign(
        volatility=calls["impliedVolatility"],
        )
        options = calls.apply(create_option, axis=1, result_type="expand")
        options_ = options_.append(options, ignore_index=True) 
    return options_