
from app import app

from dash import Input, Output, State
import plotly.express as px

import pandas as pd
import datetime
import time
import requests
import json

from common import BASE_CURRENCIES
from common import COLORS

from data_manage import prepare_crypto_list
from data_manage import preapre_data_for_crypto_main_line_graph, prepare_data_for_fear_and_greed_index, preapre_data_for_rsi_indicator, preapre_data_for_ma_50_and_200_indicator, save_exchange_rates, get_from_cache_database


CRYPTO_CURRENCIES = prepare_crypto_list()


##### Main crypto graph section #####

default_start_time = datetime.datetime(2015, 1, 1)
default_end_time = datetime.datetime.now()
df_main_graph = preapre_data_for_crypto_main_line_graph(default_start_time, default_end_time, CRYPTO_CURRENCIES)

@app.callback(
    Output("crypto-graph", "figure"), 
    [Input("crypto-dropdown", "value"),
     Input('base-currency', 'value'),
     Input('start-date-picker', 'date'),
     Input('end-date-picker', 'date')]
)
def display_main_crypto_series(crypto_dropdown, base_currency, start_date, end_date):


    from dateutil import parser
    sent_start_time=parser.isoparse(start_date)
    sent_end_time=parser.isoparse(end_date)

    
    start_time_difference = sent_start_time - default_start_time
    start_time_difference = start_time_difference.days

    end_time_difference = sent_end_time - default_start_time
    end_time_difference = end_time_difference.days

    from forex_python.converter import CurrencyRates

    try:
        currency_rates = CurrencyRates()
        usd_rate = currency_rates.get_rate('USD', base_currency)
    except:
        date, usd_price, pln_price, eur_price, gbp_price, chf_price = get_from_cache_database(base_currency)
        usd_rate=1/usd_price

    df=df_main_graph.copy(deep=True)
    df=df[start_time_difference:end_time_difference]

    for currency in CRYPTO_CURRENCIES:
        df[currency]=df[currency].multiply(usd_rate)


    # df = pd.read_csv('saved_data/crypto-usd.csv')
    fig = px.line(df, x = 'date', y=crypto_dropdown,
                  labels={
                     "bitcoin": "Price",
                     "value": "Price",
                     "date": "Date"
                 })
    fig.layout.plot_bgcolor = COLORS['background']
    fig.layout.paper_bgcolor = COLORS['background']
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    return fig


alert_message=True


@app.callback(
    [Output('LED-display-usd', 'value'),
     Output('LED-display-pln', 'value'),
     Output('LED-display-eur', 'value'),
     Output('LED-display-gpb', 'value'),
     Output('LED-display-chf', 'value'),
     Output('alert', 'children'),
     Output('alert', 'color'),
     Output('alert', 'is_open')],
    [Input('base-currency', 'value')]
)
def get_exchange_rates(base_currency):

    from forex_python.converter import CurrencyRates

    try:
        currency_rates = CurrencyRates()
        usd_price = round(currency_rates.get_rate(base_currency, 'USD'),2)
        pln_price = round(currency_rates.get_rate(base_currency, 'PLN'),2)
        eur_price = round(currency_rates.get_rate(base_currency, 'EUR'),2)
        gbp_price = round(currency_rates.get_rate(base_currency, 'GBP'),2)
        chf_price = round(currency_rates.get_rate(base_currency, 'CHF'),2)

        if base_currency=="USD":
            save_exchange_rates(usd_price, pln_price, eur_price, gbp_price, chf_price)

        alert_message = "Everything ok"
        color="info"
        is_open=False

    except:

        date, usd_price, pln_price, eur_price, gbp_price, chf_price = get_from_cache_database(base_currency)

        alert_message = "Warning! Currency rates are out of date! (currency prices of the day {})".format(date)
        color="warning"
        is_open=True

    return usd_price, pln_price, eur_price, gbp_price, chf_price, alert_message, color, is_open



@app.callback(
    Output('table-header', 'children'),
    [Input('base-currency', 'value')]
)
def create_table_header(base_currency):
    return f'Ranking of 10 ten most popular cryptocurrencies in {base_currency}:'


@app.callback(
    [Output('crypto-table', 'columns'),
     Output('crypto-table', 'data')],
    [Input('base-currency', 'value')]
)
def create_ranking_table(base_currency):

    from forex_python.converter import CurrencyRates

    try:
        currency_rates = CurrencyRates()
        usd_rate = currency_rates.get_rate('USD', base_currency)
    except:
        date, usd_price, pln_price, eur_price, gbp_price, chf_price = get_from_cache_database(base_currency)
        usd_rate=1/usd_price

    coincapapi_url = 'http://api.coincap.io/v2/assets?limit=10'

    base_currency = BASE_CURRENCIES[base_currency]

    response = requests.request("GET", coincapapi_url)
    json_data = json.loads(response.text.encode('utf8'))
    assets = json_data["data"]
    df_assets = pd.DataFrame(assets)

    crypto_symbols = list(df_assets['symbol'])
    crypto_names = list(df_assets['id'])

    crypto_url_logo_names = []
    for index in range(len(crypto_names)):
        crypto_url_logo_names.append(crypto_names[index]+"-"+crypto_symbols[index].lower())

    markdown_urls = []

    for logo_name in crypto_url_logo_names:
        markdown_urls.append(f"[![Coin](https://cryptologos.cc/logos/{logo_name}-logo.svg?v=023#thumbnail)](https://cryptologos.cc/)")

    try:
        df = pd.DataFrame(  
        dict(
            [
                ("Pos", [pos+1 for pos in range(len(crypto_names))]),
                ("Logo", [url for url in markdown_urls]),
                ("Crypto Name", [crypto_name for crypto_name in list(df_assets['name'])]),
                ("Symbol", [symbol for symbol in crypto_symbols]),
                (f"Price[{base_currency}]", [round((float(price)*usd_rate),4) for price in list(df_assets['priceUsd'])]),
                ("Supply", [round(float(supply),2) for supply in list(df_assets['supply'])]),
                (f"MarketCap[{base_currency}]", [round((float(market_cap)*usd_rate),2) for market_cap in list(df_assets['marketCapUsd'])]),
                ("Change24h[%]", [round(float(change),2) for change in list(df_assets['changePercent24Hr'])]),
            ]
        )
        )
    except:
        df = pd.DataFrame(  
        dict(
            [
                ("Pos", [pos+1 for pos in range(len(crypto_names))]),
                ("Logo", [url for url in markdown_urls]),
                ("Crypto Name", [crypto_name for crypto_name in list(df_assets['name'])]),
                ("Symbol", [symbol for symbol in crypto_symbols]),
                (f"Price[{base_currency}]", [round((float(price)*usd_rate),4) for price in list(df_assets['priceUsd'])]),
                ("Supply", [round(float(supply),2) for supply in list(df_assets['supply'])]),
                (f"MarketCap[{base_currency}]", [round((float(market_cap)*usd_rate),2) for market_cap in list(df_assets['marketCapUsd'])]),
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
        {"id": f"Price[{base_currency}]", "name": f"Price[{base_currency}]"},
        {"id": "Supply", "name": "Supply"},
        {"id": f"MarketCap[{base_currency}]", "name": f"MarketCap[{base_currency}]"},
        {"id": "Change24h[%]", "name": "Change24h[%]"},
    ]

    return columns, data




##### Fear and greed index section #####

df_fng, df_short_fng = prepare_data_for_fear_and_greed_index()

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
def display_fng_series(time_range):

    if time_range=="Last Week":
        df_cut = df_fng[:6]
    elif time_range=="Last Month":
        df_cut = df_fng[:29]
    elif time_range=="Last Six Month":
        df_cut = df_fng[:179]
    else:
        df_cut = df_fng

    fig = px.line(df_cut, x = 'timestamp', y='value',
                  labels={
                     "value": "FNG value",
                     "timestamp": "Date"
                 })
    fig.layout.plot_bgcolor = COLORS['background']
    fig.layout.paper_bgcolor = COLORS['background']
    fig.update_xaxes(showgrid=False, zeroline=False, autorange="reversed")
    fig.update_yaxes(showgrid=False, zeroline=False)
    return fig





###### RSI indicator section #######

df_rsi = preapre_data_for_rsi_indicator()

@app.callback(
    Output("rsi-line-graph", "figure"), 
    Input("rsi-checklist", "value"))
def display_rsi_series(time_range):

    if time_range=="Last Day":
        df_cut = df_rsi[:25]
    elif time_range=="Last Week":
        df_cut = df_rsi[:169]
    elif time_range=="Last Two Weeks":
        df_cut = df_rsi[:337]
    else:
        df_cut = df_rsi

    fig = px.scatter(df_cut, x="timestamp", y="value", color="value", 
                color_continuous_scale=["red", "yellow", "green"], 
                title = "RSI Index for X:BTC-USD indicator",
                labels={
                     "value": "RSI value",
                     "timestamp": "Date"
                 })
    fig.layout.plot_bgcolor = COLORS['background']
    fig.layout.paper_bgcolor = COLORS['background']
    fig.update_traces(mode='markers+lines')
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



###### MA-50 and Ma-200 indicator section #######

df_ma50, df_ma200 = preapre_data_for_ma_50_and_200_indicator()

@app.callback(
    Output('ma-line-graph', 'figure'),
    [Input('ma-types', 'value'),
     Input('ma-window', 'value'),
     Input('ma-period', 'value')]
)
def display_ma_series(types, window, period):

    if window == "50 days":
        df_ma=df_ma50
    else:
        df_ma=df_ma200


    if period=="Last Day":
        df_ma_cut = df_ma[:25]
    elif period=="Last Week":
        df_ma_cut = df_ma[:169]
    elif period=="Last Two Weeks":
        df_ma_cut = df_ma[:337]
    else:
        df_ma_cut = df_ma

    ma_types=[]
    if "  Simple Moving Average (SMA)" in types:
        ma_types.append('SMA')
    if "  Exponential Moving Average (EMA)" in types:
        ma_types.append('EMA')
    ma_types.append('BTC price')

    fig = px.line(df_ma_cut, x = 'timestamp', y=ma_types, 
                  title = "Moving Averages Index for X:BTC-USD indicator",
                  labels={
                     "value": "BTC Price",
                     "timestamp": "Date"
                 })
    fig.layout.plot_bgcolor = COLORS['background']
    fig.layout.paper_bgcolor = COLORS['background']
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    return fig


@app.callback(
    Output("ma-collapse", "is_open"),
    [Input("ma-collapse-button", "n_clicks")],
    [State("ma-collapse", "is_open")],
)
def ma_toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open