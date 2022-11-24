
from dash import Input, Output, State
import plotly.express as px

import pandas as pd
import datetime
import time
import requests
import json

from common import CRYPTO_CURRENCIES
from common import COLORS

from app import app


start_time = datetime.datetime(2015, 1, 1)
end_time = datetime.datetime.now()

unix_start_time = time.mktime(start_time.timetuple())*1000
unix_end_time = time.mktime(end_time.timetuple())*1000


currency = 'bitcoin'



for currency in CRYPTO_CURRENCIES:

    url = f"http://api.coincap.io/v2/assets/{currency}/history?interval=d1&start={unix_start_time}&end={unix_end_time}"

    payload = {}
    headers= {}

    response = requests.request("GET", url, headers=headers, data = payload)
    json_data = json.loads(response.text.encode('utf8'))
    data = json_data["data"]

    df_temp = pd.DataFrame(data)
    df_temp[currency] = pd.to_numeric(df_temp['priceUsd'], errors='coerce').fillna(0, downcast='infer')
    df_temp['date'] = pd.to_datetime(df_temp['date'], dayfirst=False, utc=False, format='%Y-%m-%d')
    # df_temp.to_csv('bitcoin-usd.csv', index=False)

    if currency == 'bitcoin':
        df=pd.DataFrame()
        # df['time']=df_temp['time']
        df['date']=df_temp['date']
        df[currency]=df_temp[currency]
    else:
        df=df.merge(df_temp, on='date', how='left')
        # df['date_'+currency]=df_temp['new_date']
        # df[currency]=df_temp[currency]

df.to_csv('saved_data/crypto-usd.csv', index=False)




from collections import OrderedDict
table_data = OrderedDict(
    [
        ("Time", ["Now", "Yesterday", "Week ago", "Month ago", "Year ago"]),
        ("Label", ["Extreme Fear", "Fear", "Neutral", "Greed", "Extreme Greed"]),
        ("Value", [18, 30, 50, 71, 93]),
    ]
)
df_table_data = pd.DataFrame(table_data)



@app.callback(
    Output("crypto-graph", "figure"), 
    Input("crypto-dropdown", "value"))
def display_time_series(crypto_dropdown):
    df = pd.read_csv('saved_data/crypto-usd.csv')
    fig = px.line(df, x = 'date', y=crypto_dropdown)
    fig.layout.plot_bgcolor = COLORS['background']
    fig.layout.paper_bgcolor = COLORS['background']
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    return fig





@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open