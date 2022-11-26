
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



##### Prepare data for main line charts with crypto #####################################

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






##### Prepare data for fear and greed index #####################################

from collections import OrderedDict

fng_url = 'https://api.alternative.me/fng/?limit=365&date_format=us'
response = requests.request("GET", fng_url)
json_data = json.loads(response.text.encode('utf8'))
data = json_data["data"]
df_fng = pd.DataFrame(data)

df_fng_temp = df_fng.loc[[0,1,6,29,364]]

labels_list = [label for label in df_fng_temp['value_classification']]
values_list = [value for value in df_fng_temp['value']]

fng_table_data = OrderedDict(
    [
        ("Time", ["Now", "Yesterday", "Week ago", "Month ago", "Year ago"]),
        ("Label", labels_list),
        ("Value", values_list),
    ]
)
df_short_fng = pd.DataFrame(fng_table_data)





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



@app.callback(
    Output("fng-line-graph", "figure"), 
    Input("checklist", "value"))
def display_new_series(time_range):

    

    if time_range=="Last Week":
        df_cut = df_fng[:6]
    elif time_range=="Last Month":
        df_cut = df_fng[:29]
    else:
        df_cut = df_fng

    fig = px.line(df_cut, x = 'timestamp', y='value')
    fig.layout.plot_bgcolor = COLORS['background']
    fig.layout.paper_bgcolor = COLORS['background']
    fig.update_xaxes(showgrid=False, zeroline=False, autorange="reversed")
    fig.update_yaxes(showgrid=False, zeroline=False)
    return fig