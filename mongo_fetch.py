#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 28 10:09:11 2021

@author: abhirakshit
"""

import pandas as pd
from yahoofinancials import YahooFinancials
from joblib import Parallel, delayed
from datetime import datetime
import pymongo


class MongoConnect():
    def __init__(self, collection_name, dbname):
        self.client = pymongo.MongoClient("mongodb+srv://abhrksht:Redwing@cluster0.lqb3j.mongodb.net/stocks_key_stats?retryWrites=true&w=majority")
        self.db = self.client[dbname]
        self.collection = self.db[collection_name]
    


        
    def fetch_all_df(self):
        sum_cols = ['previousClose', 'regularMarketOpen', 'twoHundredDayAverage', 'trailingAnnualDividendYield', 
                    'payoutRatio', 'volume24Hr', 'regularMarketDayHigh', 'navPrice', 
                    'averageDailyVolume10Day', 'totalAssets', 'regularMarketPreviousClose', 
                    'fiftyDayAverage', 'trailingAnnualDividendRate', 'open', 'toCurrency', 
                    'averageVolume10days', 'expireDate', 'yield', 'algorithm', 'dividendRate', 
                    'exDividendDate', 'beta', 'circulatingSupply', 'startDate', 
                    'regularMarketDayLow', 'priceHint', 'currency', 'regularMarketVolume', 
                    'lastMarket', 'maxSupply', 'openInterest', 'marketCap', 'volumeAllCurrencies', 
                    'strikePrice', 'averageVolume', 'priceToSalesTrailing12Months', 'dayLow', 
                    'ask', 'ytdReturn', 'askSize', 'volume', 'fiftyTwoWeekHigh', 'forwardPE', 
                    'maxAge', 'fromCurrency', 'fiveYearAvgDividendYield', 'fiftyTwoWeekLow', 
                    'bid', 'tradeable', 'dividendYield', 'bidSize', 'dayHigh', 'last_update']
        df = pd.DataFrame(columns = ["ticker"] + sum_cols)
        query = { "index": { "$regex": '[a-z]*.NS' } }
        res = self.collection.find(query)
        for x in res:
            ticker = x["index"]
            d1 = x["data"]
            d1.update({"ticker": ticker})
            df = df.append(d1, ignore_index=True)
        return df

    def create_index(self, index):
        res = self.collection.find_one({"index":index})
        if res is None:
            self.collection.insert_one({"index": index,"data":{}})
            return self
        else:
            return self
        
    def find_details(self, ticker):
        res = self.collection.find_one({"index":ticker})
        if res is None:
            return {}
        return res["data"]
    
    
    def get_all_tickers(self):
        d1 = self.find_details("all_tickers_available")
        return pd.DataFrame(d1)["ticker"].tolist()

    def update_company_names(self, df_names):
        self.create_index("company_names")
        self.collection.update_many({"index": "company_names"}, 
                                        { "$set": { "data": df_names.to_dict("records")}})
    
    
    def load_company_names(self):
        data_dict = self.find_details("company_names")
        df_names = pd.DataFrame(data_dict)
        return df_names

    def get_updated_tickerlist(self):
        tickers = [ticker for ticker in self.collection.distinct(key = "index") if ticker != "all_tickers_available"]
        return tickers


if __name__ == '__main__':
    mgdb = MongoConnect("stocks_monitoring", "stocks_key_stats")
    query = { "index": { "$regex": '[a-z]*.NS' } }
    # df = mgdb.fetch_all_df()
    df_names = pd.read_csv("static/NSE_tickers_YF.csv")
    mgdb.update_company_names(df_names)
    
