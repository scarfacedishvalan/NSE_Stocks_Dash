#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 18 20:10:50 2021

@author: abhirakshit
"""
import dash  #(version 1.12.0)
from dash.dependencies import Input, Output, State
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
import pandas as pd
import get_data
import plotly.graph_objects as go
import os

def add_callbacks(app):

    
    @app.callback(
        [Output("all_table", "data"), Output("load_mongo_status", "children")],
        [Input("load_mongo", "n_clicks")]
        )
    def update_from_mongo(n):
        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
        if "load_mongo" in changed_id:
            df_all = get_data.load_all_data()
            last_update_date = df_all["last_update"][0][:10]
            return [df_all.to_dict("records"), "Last update on " + last_update_date]
        
        return [dash.no_update, dash.no_update]
    # @app.callback(
    #     [Output("all_table", "data")],
    #     [Input("dummy_input", "children")]
    #     )
    # def load_data(dummy):
    #     df_all = get_data.read_all_data()
    #     return [df_all.to_dict("records")]
    
    
    
    @app.callback(
        [Output("daily_chart", "figure"), Output('all_table', "selected_rows")],
        [ Input('all_table', "derived_virtual_data"),
    Input('all_table', "derived_virtual_selected_rows"), Input("clear1", "n_clicks"),
    Input("property_dropdown", "value"), Input("trend_cal", "start_date"),
    Input("trend_cal", "end_date")],
    [State("daily_chart", "figure")]
        )
    def update_daily_graph(data1, rows, n, fieldlist, start_date, end_date, dict_of_fig):
        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
        if "clear1" in changed_id:
            return [{}, []]
    
        if data1 is None or rows is None or rows == [] or fieldlist == [] or fieldlist is None:
            return [dash.no_update, dash.no_update]
        params= dict(start = pd.to_datetime(start_date),
                  end = pd.to_datetime(end_date))   
        
        if not isinstance(fieldlist, list):
            field = fieldlist
        else:
            field = fieldlist[-1]

        row = rows[-1]
        fig = go.Figure(dict_of_fig)

        df_all = pd.DataFrame(data1)

        ticker = df_all["ticker"][row]
        df_daily = get_data.get_daily_data(ticker, **params)
        if field not in df_daily.columns:
            return [dash.no_update, dash.no_update]
    
        fig.add_trace(go.Scatter(x=df_daily.index, y=df_daily[field],
                mode='lines',
                name=ticker + ' ' + field))

        return [fig, dash.no_update]
            
            
    
    return app