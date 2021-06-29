#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 18 18:08:55 2021

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
import layout_components as lc
from callbacks import add_callbacks

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP]) # this was introduced in Dash version 1.12.0
app.layout = html.Div([html.H1("Stocks Monitoring"),
                       lc.row1a(),
                       html.Br(),
                       lc.row1b(),
                       html.Br(),
                       lc.row2a(),
                       html.Br(),
                       lc.daily_chart()
                       ])
app = add_callbacks(app)



if __name__ == '__main__':
    app.run_server(debug=True, port = 8052)