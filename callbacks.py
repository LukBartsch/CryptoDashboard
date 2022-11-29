
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


api_key_taapi = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbHVlIjoiNjM4MzdjYzRmYzVhOGFkZmVjOThmYzkwIiwiaWF0IjoxNjY5NTYxNTYzLCJleHAiOjMzMTc0MDI1NTYzfQ.bTCaTJl_t4geJvNSeC8Cc9kTnfNflXND06p_PE8aFyY'



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




###### Preapre data for RSI indicator #######

api_key_polygon = 'IKAQmrb2sLnT0DbQvACRlG2OXg8Cbpa8'

rsi_url = f'https://api.polygon.io/v1/indicators/rsi/AAPL?timespan=day&adjusted=true&window=14&series_type=close&order=desc&apiKey={api_key_polygon}&limit=365'
response = requests.request("GET", rsi_url)
json_data = json.loads(response.text.encode('utf8'))
data = json_data["results"]["values"]
df_rsi = pd.DataFrame(data)

df_rsi['timestamp'] = df_rsi['timestamp'].astype('datetime64[ms]')






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
    Output('table-header', 'children'),
    [Input('base-currency', 'value')]
)
def create_table_header(base_currency):
    return f'Ranking ten most popular cryptocurrencies'




@app.callback(
    [Output('currency-table', 'columns'),
     Output('currency-table', 'data')],
    [Input('crypto-dropdown', 'value')]
)
def create_table(currencies):

    # df = pd.read_csv('saved_data/crypto-usd.csv')
    # limit_to_five = df[-5:]

    # columns = [{'name': 'Crypto', 'id': 'currency'}]
    # date_columns = [
    #     {'name': 1, 'id': 2}
    #     for data in limit_to_five['date']]
    # columns.extend(date_columns)

    # rows = []
    # for currency in currencies:
    #     single_row = {
    #         'currency': currency
    #     }
    #     for rate, date in zip(limit_to_five['currency'], date_columns):
    #         date_column = date['id']
    #         try:
    #             single_row[date_column] = 1 / rate[currency]
    #         except KeyError:
    #             single_row[date_column] = 1
    #     rows.append(single_row)


    coincapapi_url = 'http://api.coincap.io/v2/assets?limit=10'

    response = requests.request("GET", coincapapi_url)
    json_data = json.loads(response.text.encode('utf8'))
    assets = json_data["data"]
    df_assets = pd.DataFrame(assets)



    crypto_symbols = list(df_assets['symbol'])
    crypto_names = list(df_assets['id'])

    crypto_url_logo_names = []
    for index in range(len(crypto_names)):
        crypto_url_logo_names.append(crypto_names[index]+"-"+crypto_symbols[index].lower())

    # print(crypto_symbols)
    # print(crypto_url_logo_names)

    markdown_urls = []

    for logo_name in crypto_url_logo_names:
        markdown_urls.append(f"[![Coin](https://cryptologos.cc/logos/{logo_name}-logo.svg?v=023#thumbnail)](https://cryptologos.cc/)")

    # print(markdown_urls)

    
    # crypto_logo = f"[![{symbol}](https://cryptologos.cc/logos/{crypto_name}-logo.svg?v=023#thumbnail)](https://cryptologos.cc/)"

    df = pd.DataFrame(
    dict(
        [
            ("Pos", [pos+1 for pos in range(len(crypto_names))]),
            ("Logo", [url for url in markdown_urls]),
            ("Crypto Name", [crypto_name for crypto_name in list(df_assets['name'])]),
            ("Symbol", [symbol for symbol in crypto_symbols]),
            ("Price", [price for price in list(df_assets['priceUsd'])]),
            ("Change24h[%]", [change for change in list(df_assets['changePercent24Hr'])]),
        ]
    )
    )


    data=df.to_dict("records")
    columns=[
        {"id": "Pos", "name": "Pos"},
        {"id": "Logo", "name": "Logo", "presentation": "markdown"},
        {"id": "Crypto Name", "name": "Crypto Name"},
        {"id": "Symbol", "name": "Symbol"},
        {"id": "Price", "name": "Price"},
        {"id": "Change24h[%]", "name": "Change24h[%]"},
    ]



    # df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')

    # print(df)

    # data = df.to_dict('records')
    # columns = [{"name": i, "id": i} for i in df.columns]


    # print(data)
    # print(columns)

    return columns, data




@app.callback(
    Output("fng-collapse", "is_open"),
    [Input("fng-collapse-button", "n_clicks")],
    [State("fng-collapse", "is_open")],
)
def fng_toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open



@app.callback(
    Output("fng-line-graph", "figure"), 
    Input("fng-checklist", "value"))
def display_new_series(time_range):

    if time_range=="Last Week":
        df_cut = df_fng[:6]
    elif time_range=="Last Month":
        df_cut = df_fng[:29]
    elif time_range=="Last Six Month":
        df_cut = df_fng[:179]
    else:
        df_cut = df_fng

    fig = px.line(df_cut, x = 'timestamp', y='value')
    fig.layout.plot_bgcolor = COLORS['background']
    fig.layout.paper_bgcolor = COLORS['background']
    fig.update_xaxes(showgrid=False, zeroline=False, autorange="reversed")
    fig.update_yaxes(showgrid=False, zeroline=False)
    return fig





@app.callback(
    Output("rsi-line-graph", "figure"), 
    Input("rsi-checklist", "value"))
def display_rsi_series(time_range):

    if time_range=="Last Week":
        df_cut = df_rsi[:6]
    elif time_range=="Last Month":
        df_cut = df_rsi[:29]
    elif time_range=="Last Six Month":
        df_cut = df_rsi[:179]
    else:
        df_cut = df_rsi

    fig = px.scatter(df_cut, x="timestamp", y="value", color="value", 
                color_continuous_scale=["red", "yellow", "green"], title = "Example of RSI for AAPL indicator")
    fig.layout.plot_bgcolor = COLORS['background']
    fig.layout.paper_bgcolor = COLORS['background']
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    return fig


@app.callback(
    Output("rsi-collapse", "is_open"),
    [Input("rsi-collapse-button", "n_clicks")],
    [State("rsi-collapse", "is_open")],
)
def rsi_toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open