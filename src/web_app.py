'''
Import Statements
'''
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import numpy as np
import pandas as pd
from downloader import Downloader
import yfinance as yf
from datetime import datetime

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Loads preliminary data
ticker1name = 'AAPL' ; ticker2name = 'MSFT'
ticker3name = 'GOOG' ; ticker4name = 'AMZN'
ticker1 = yf.Ticker('AAPL')
ticker1hist = ticker1.history(period='max')
ticker2 = yf.Ticker('MSFT')
ticker2hist = ticker2.history(period='max')
ticker3 = yf.Ticker('GOOG')
ticker3hist = ticker3.history(period='max')
ticker4 = yf.Ticker('AMZN')
ticker4hist = ticker4.history(period='max')

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H3(children='Multi-Security Analysis'),
    html.Div([
        html.P('Enter tickers:'),
        dcc.Input(id = 'ticker1Input', value='AAPL', type='text'),
        dcc.Input(id='ticker2Input', value='MSFT', type='text'),
        dcc.Input(id='ticker3Input', value='GOOG', type='text'),
        dcc.Input(id='ticker4Input', value='AMZN', type='text'),
        html.Button('Update', id='update-tickers', n_clicks=0)

    ]),
    html.Div([
        html.Span('Display Type:'),
        dcc.Dropdown(
            id='graph1Leftdisplaydropdown',
            options=[
                {'label': 'Security Price', 'value': 'price'},
                {'label': 'Security Return', 'value': 'return'}
            ],
            value='price'
        ),
        html.Span('Start Date (YYYY-MM-DD):'),
        dcc.Input(id = 'start1Input', value='2000-01-01', type='text'),
        html.Span('End Date (YYYY-MM-DD):'),
        dcc.Input(id = 'end1Input', value=datetime.today().strftime('%Y-%m-%d'), type='text')
    ]),
    html.Div([
        html.H4('<Chart 1>'),
        dcc.Graph(id='graph1Left', figure={
            'data': [
                {'x': ticker1hist.index, 'y': ticker1hist.Close, 'type': 'line', 'name': ticker1name},
                {'x': ticker2hist.index, 'y': ticker2hist.Close, 'type': 'line', 'name': ticker2name},
                {'x': ticker3hist.index, 'y': ticker3hist.Close, 'type': 'line', 'name': ticker3name},
                {'x': ticker4hist.index, 'y': ticker4hist.Close, 'type': 'line', 'name': ticker4name}
            ],
            'layout': {
                'title': 'price Comparison'
            }
        })
    ]),
    html.Div([
        html.H3(children='Financial Statements'),
        html.Div([
            html.P('Enter GAAP Parameter')

        ])
    ])
])

@app.callback(
    Output(component_id='graph1Left', component_property='figure'),
    [Input(component_id='update-tickers', component_property='n_clicks')],
    [State(component_id='ticker1Input', component_property='value'),
    State(component_id='ticker2Input', component_property='value'),
    State(component_id='ticker3Input', component_property='value'),
    State(component_id='ticker4Input', component_property='value'),
    State(component_id='graph1Leftdisplaydropdown', component_property='value'),
    State(component_id='start1Input', component_property='value'),
    State(component_id='end1Input', component_property='value')]
)
def update_figure1(n_clicks, ticker1name, ticker2name, ticker3name, ticker4name, dropdown1, start1, end1):

    ticker1 = yf.Ticker(ticker1name)
    ticker1hist = ticker1.history(start=start1, end=end1)
    ticker2 = yf.Ticker(ticker2name)
    ticker2hist = ticker2.history(start=start1, end=end1)
    ticker3 = yf.Ticker(ticker3name)
    ticker3hist = ticker3.history(start=start1, end=end1)
    ticker4 = yf.Ticker(ticker4name)
    ticker4hist = ticker4.history(start=start1, end=end1)

    if dropdown1 == 'return':
        y1 = ticker1hist.Close / ticker1hist.Close[0]
        y2 = ticker2hist.Close / ticker2hist.Close[0]
        y3 = ticker3hist.Close / ticker3hist.Close[0]
        y4 = ticker4hist.Close / ticker4hist.Close[0]
    else:
        y1 = ticker1hist.Close ; y2 = ticker2hist.Close
        y3 = ticker3hist.Close ; y4 = ticker4hist.Close

    chart_dict = {
        'data': [
            {'x': ticker1hist.index, 'y': y1, 'type': 'line', 'name': ticker1name},
            {'x': ticker2hist.index, 'y': y2, 'type': 'line', 'name': ticker2name},
            {'x': ticker3hist.index, 'y': y3, 'type': 'line', 'name': ticker3name},
            {'x': ticker4hist.index, 'y': y4, 'type': 'line', 'name': ticker4name}
        ],
        'layout': {
            'title': '{} Comparison'.format(str(dropdown1))
        }
    }

    return chart_dict


if __name__ == '__main__':
    app.run_server(debug=True)
