#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 10:41:09 2021

@author: abhirakshit
"""
import dash  #(version 1.12.0)
from dash.dependencies import Input, Output
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from pandas_datareader import data
from dash_table.Format import Format, Group
from datetime import datetime
from datetime import date
import dash_bootstrap_components as dbc
from datetime import timedelta, datetime
import pandas as pd
from dash_table.Format import Format, Scheme, Trim, Group
from dash_table import FormatTemplate
def basic_settings():

    numeric_columnlist = ["tradedVolume", "marketCap", "twoHundredDayAverage", "volume", "averageVolume", "averageDailyVolume10Day", 'dayHigh', 'dayLow']

    settings = dict(
        editable=True,              # allow editing of data inside all cells
        filter_action="native",     # allow filtering of data by user ('native') or not ('none')
        sort_action="native",       # enables data to be sorted per-column by user or not ('none')
        sort_mode="single",         # sort across 'multi' or 'single' columns
        row_selectable="multi",     # allow users to select 'multi' or 'single' rows
        row_deletable=False,         # choose if user can delete a row (True) or not (False)
        selected_columns=[],        # ids of columns that user selects
        selected_rows = [],
        page_action="native",       # all data is passed to the table up-front or not ('none')
        page_current=0,             # page number that user is on
        page_size=10,                # number of rows visible per page    
        )

    return numeric_columnlist, settings


def create_table(df, tablename, static_cols = ["ticker"], **kwargs):
    numeric_columnlist, settings = basic_settings()
    params = dict(
        id= tablename,
        columns=[
            {"name": i, "id": i, "deletable": False, "hideable": False}
            if i in static_cols
                else
            {"name": i, "id": i, "deletable": False, "type": "numeric", "hideable": True,
             "format": Format().group(True)}
            if i in numeric_columnlist            
            else {"name": i, "id": i, "hideable": True, "selectable": True}
            for i in df.columns
        ],
        data=df.to_dict('records'),  # the contents of the table
        fill_width = False
        )
    params.update(settings)
    params.update(kwargs)
    return params

def create_calendar(calidname, buttonidname, **kwargs):
    params = dict(id = calidname,
        min_date_allowed=date(1995, 8, 5),
        max_date_allowed=datetime.today(),
        start_date = datetime.today()-timedelta(10), 
        end_date = datetime.today(), 
        display_format='DD/MM/YYYY'
    )
    
    params.update(kwargs)
    cal = dcc.DatePickerRange(**params)
    but =  dbc.Button("Submit", id = buttonidname, className="mr-1")
    return  cal, but

def row1a():
    dd = dcc.Dropdown(
    options=[
        {'label': 'Market Cap', 'value': 'market_cap'},
        {'label': 'Traded Volume', 'value': 'traded_vol'},
        {'label': 'Latest price', 'value': 'price'}
    ],
    id = "property_dropdown",
        placeholder="Select Columns to be added",
    multi=True
)  
    cal, _ = create_calendar("trend_cal", "button")
    
    return dbc.Row([
        dbc.Col(html.Div(cal), width = 3),
        # dbc.Col(dbc.Button("Generate", id = "add_col", className="mr-1")),
        dbc.Col(html.Div(children = "dummy", style = {'display': 'none'}, id = "dummy_input")),
        dbc.Col(html.Div(style = {'display': 'none'}, id = "daily_data")),
        dbc.Col(dbc.Button("Update source", id = "load_mongo")),
        dbc.Col(html.Div(id = "load_mongo_status")),
        dbc.Col(html.Div())
        ])

def daily_chart():
    return dbc.Row([
        dbc.Col(html.Div(dcc.Graph(id = "daily_chart", figure = {}))),
        # dbc.Col(dbc.Button("Generate", id = "add_col", className="mr-1")),

        ])
def column_formatter(df, numeric_cols, percent_cols):

  percentage = FormatTemplate.percentage(2)
  numericformatter = Format(precision = 2, scheme=Scheme.fixed, group=',')

  column_dictlist = []

  for col in df.columns:
    if col in percent_cols:
      column_dictlist.append({"name": col, "id": col, 'type': 'numeric', 'format': percentage, "hideable": True})

    elif col in numeric_cols:
      column_dictlist.append({"name": col, "id": col, 'type': 'numeric', 'format': numericformatter, "hideable": True})

    else:
      column_dictlist.append({"name": col, "id": col})

  return column_dictlist

def row1b():
    all_cols = ['ticker', "Company_name", 'previousClose', 'regularMarketOpen', 'twoHundredDayAverage',
       'trailingAnnualDividendYield', 'payoutRatio', 'volume24Hr',
       'regularMarketDayHigh', 'navPrice', 'averageDailyVolume10Day',
       'totalAssets', 'regularMarketPreviousClose', 'fiftyDayAverage',
       'trailingAnnualDividendRate', 'open', 'toCurrency',
       'averageVolume10days', 'expireDate', 'yield', 'algorithm',
       'dividendRate', 'exDividendDate', 'beta', 'circulatingSupply',
       'startDate', 'regularMarketDayLow', 'priceHint', 'currency',
       'regularMarketVolume', 'lastMarket', 'maxSupply', 'openInterest',
       'marketCap', 'volumeAllCurrencies', 'strikePrice', 'averageVolume',
       'priceToSalesTrailing12Months', 'dayLow', 'ask', 'ytdReturn', 'askSize',
       'volume', 'fiftyTwoWeekHigh', 'forwardPE', 'maxAge', 'fromCurrency',
       'fiveYearAvgDividendYield', 'fiftyTwoWeekLow', 'bid', 'tradeable',
       'dividendYield', 'bidSize', 'dayHigh', 'last_update', 'trailingPE']
    
    numeric_columnlist, settings = basic_settings()
    numeric_columnlist = [col for col in all_cols if col not in ["ticker", "Company_name"]]
    df = pd.DataFrame(columns = all_cols)
    table_params = {"id": "all_table"}
    columns_dictlist = column_formatter(df, numeric_columnlist, ["pv"])
    table_params.update(settings)
    table_params.update(dict(columns = columns_dictlist))
    shown_columns = ["ticker", "Company_name","previousClose", "fiftyTwoWeekHigh", "marketCap", "volume", "beta" ]
    hidden_cols = [col for col in all_cols if col not in shown_columns]
    table_params.update(dict(hidden_columns = hidden_cols))
    t1 = dash_table.DataTable(**table_params)
    return t1

def row2a():
    optionlist = [{"label": i, "value": i} for i in ["Open", "High", "Low", "Close", "Adj Close", "Volume"]]
    dd = dcc.Dropdown(
    options= optionlist,
    id = "property_dropdown",
        value = "Close",
    multi=True
    )
    return dbc.Row([
        dbc.Col(dd, width = 6),
        dbc.Col(dbc.Button("Clear graph", id = "clear1"))
        ])

if __name__ == '__main__':
    t1 = row1b()