#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 10:42:53 2021

@author: abhirakshit
"""
import numpy as np
from datetime import datetime, date, timedelta
# Import data libraries
import yfinance as yf
import pandas as pd
import plotly.express as px
import pandas_datareader as web
from pandas_datareader import data
from mongo_fetch import MongoConnect
import os

from yahoofinancials import YahooFinancials
import yfinance as yf

def get_daily_data(ticker, **kwargs):
    params = dict(start = date.today()-timedelta(10),
                  end = date.today(),
                  tickers = ticker,
                  progress = False
        )
    params.update(kwargs)
    return yf.download(**params)

def plot_daily_returns(df, **kwargs):
    params = dict(
        data_frame = df,
        y = "Close"
        )
    params.update(kwargs)
    return px.line(**params)
    
def get_company_properties(tickerlist, propertylist):
    df = pd.DataFrame(columns = ["symbol"])
    df["symbol"] = [ticker.replace(".NS", "") for ticker in tickerlist]
    df["symbol_yf"] = df["symbol"].apply(lambda x: x.replace(".NS", ""))
    yahoo_financials = YahooFinancials(tickerlist)
    if "market_cap" in propertylist:
        d1 = yahoo_financials.get_market_cap()
        market_caplist = []
        for ticker in df['symbol_yf']:
            try:
                market_caplist.append(list(web.get_quote_yahoo(ticker)['marketCap'])[0])
            except:
                market_caplist.append(np.nan)
        df['market_cap'] = market_caplist
    
    if "price" in propertylist:
        d1 = yahoo_financials.get_current_price()
        df['price'] = df['symbol_yf'].map(d1)
    
    if "traded_vol" in propertylist:
        d1 = yahoo_financials.get_current_volume()
        df['traded_vol'] = df['symbol_yf'].map(d1)
    
    df = df.drop("symbol_yf", axis = "columns")

    return df
    
def load_all_data():
    mgdb = MongoConnect("stocks_monitoring", "stocks_key_stats")
    df_all = mgdb.fetch_all_df()
    df_names = mgdb.load_company_names()
    df_all = df_names.set_index("ticker").join(df_all.set_index("ticker")).reset_index()
    return df_all

def read_all_data():
    path = os.path.join("static", "Key_Stats.csv")
    name_path = os.path.join("static", "NSE_tickers_YF.csv")
    df_names = pd.read_csv(name_path)
    df_all = pd.read_csv(path)
    df_all = df_names.set_index("ticker").join(df_all.set_index("ticker")).reset_index()
    return df_all


if __name__ == '__main__':
    # df = pd.read_excel("static/Qty_top100_test.xlsx")
    # df = pd.DataFrame(df, columns = ["Rank",	"symbol",	"Company_Name"])
    # tickerlist = list(df["symbol"])[0:5]
    df_all = load_all_data()
    # df_all.to_csv(r"static/Key_Stats.csv", index = False)

    # mcap = web.get_quote_yahoo("PNB.NS")['marketCap']
    # df_all = load_all_data()
    # df = get_daily_data("IDEA.NS")
    # df = load_all_data()
    