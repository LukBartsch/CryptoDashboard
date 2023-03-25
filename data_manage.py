import os
import pandas as pd
import time
import requests
import json
import datetime

from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///exchange_rates_cache.sqlite', echo=False)
base = declarative_base()
db_session = sessionmaker(bind=engine)
session = db_session()


class ExchangeRates(base):

    __tablename__ = "exchange_rates"

    id = Column(Integer, primary_key=True)
    date = Column(String)
    USD = Column(Float)
    PLN = Column(Float)
    EUR = Column(Float)
    GBP = Column(Float)
    CHF = Column(Float)

    def __init__(self, id, date, USD, PLN, EUR, GBP, CHF):
        self.id = id
        self.date = date
        self.USD = USD
        self.PLN = PLN
        self.EUR = EUR
        self.GBP = GBP
        self.CHF = CHF

base.metadata.create_all(engine)


api_key_polygon = os.environ['api_key_polygon']


def prepare_crypto_list():

    coincapapi_url = 'http://api.coincap.io/v2/assets?limit=10'

    try:
        response = requests.request("GET", coincapapi_url)
        json_data = json.loads(response.text.encode('utf8'))
        assets = json_data["data"]
        df_assets = pd.DataFrame(assets)
        crypto_names = list(df_assets['id'])
    except:
        crypto_names = []

    return crypto_names


def preapre_data_for_crypto_main_line_graph(start_time, end_time, CRYPTO_CURRENCIES):

    unix_start_time = time.mktime(start_time.timetuple())*1000
    unix_end_time = time.mktime(end_time.timetuple())*1000

    try:
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

            if currency == 'bitcoin':
                df_main_graph=pd.DataFrame()
                df_main_graph['date']=df_temp['date']
                df_main_graph[currency]=df_temp[currency]
            else:
                df_main_graph=df_main_graph.merge(df_temp, on='date', how='left')
                df_main_graph = df_main_graph.drop(labels=["priceUsd", "time"], axis=1)

        # df_main_graph.to_csv('crypto-usd.csv', index=False)
    except:
        df_main_graph=pd.DataFrame()

    return df_main_graph



def prepare_data_for_fear_and_greed_index():

    from collections import OrderedDict

    fng_url = 'https://api.alternative.me/fng/?limit=365&date_format=us'
    
    try:
        response = requests.request("GET", fng_url)
        json_data = json.loads(response.text.encode('utf8'))
        data = json_data["data"]
        df_fng = pd.DataFrame(data)

        df_fng['value'] = pd.to_numeric(df_fng['value'], errors='coerce').fillna(0, downcast='infer')

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
    except:
        df_short_fng = pd.DataFrame()

    return df_fng, df_short_fng


def preapre_data_for_rsi_indicator():
    
    rsi_url = f'https://api.polygon.io/v1/indicators/rsi/X:BTCUSD?timespan=hour&window=14&series_type=close&expand_underlying=false&order=desc&limit=700&apiKey={api_key_polygon}'
    
    try:
        response = requests.request("GET", rsi_url)
        json_data = json.loads(response.text.encode('utf8'))
        data = json_data["results"]["values"]
        df_rsi = pd.DataFrame(data)
        df_rsi['timestamp'] = df_rsi['timestamp'].astype('datetime64[ms]')
    except:
        df_rsi = pd.DataFrame()

    return df_rsi


def preapre_data_for_ma_50_and_200_indicator():
    
    sma_url = f'https://api.polygon.io/v1/indicators/sma/X:BTCUSD?timespan=hour&window=50&series_type=close&order=desc&limit=700&apiKey={api_key_polygon}'
    ema_url = f'https://api.polygon.io/v1/indicators/ema/X:BTCUSD?timespan=hour&window=50&series_type=close&order=desc&limit=700&apiKey={api_key_polygon}'

    try:
        response = requests.request("GET", sma_url)
        json_data = json.loads(response.text.encode('utf8'))
        data = json_data["results"]["values"]
        df_sma = pd.DataFrame(data)

        response = requests.request("GET", ema_url)
        json_data = json.loads(response.text.encode('utf8'))
        data = json_data["results"]["values"]
        df_ema = pd.DataFrame(data)

        df_ma50=df_sma.merge(df_ema, on='timestamp', how='left')

        df_btc_price = prepare_btc_price_for_ma_indicator(df_ma50)

        df_ma50=df_ma50.merge(df_btc_price, on='timestamp', how='left')

        df_ma50['timestamp'] = df_ma50['timestamp'].astype('datetime64[ms]')
        # df['timestamp'] = df['timestamp'].apply(lambda x: datetime.datetime.fromtimestamp(x/1000.0))

        df_ma50 = df_ma50.rename(columns={"value_x":"SMA", "value_y":"EMA", "priceUsd":"BTC price"})

        df_ma200 = preapre_data_for_ma_200_indicator(df_btc_price)
    except:
        df_ma50 = pd.DataFrame()
        df_ma200 = pd.DataFrame()

    return df_ma50, df_ma200


def prepare_btc_price_for_ma_indicator(df_ma50):

    start_time=float(df_ma50["timestamp"].min())
    end_time=float(df_ma50["timestamp"].max())

    url_price_btc = f"http://api.coincap.io/v2/assets/bitcoin/history?interval=h1&start={start_time}&end={end_time}"

    try:
        response = requests.request("GET", url_price_btc)
        json_data = json.loads(response.text.encode('utf8'))
        data = json_data["data"]

        df_btc_price = pd.DataFrame(data)

        df_btc_price = df_btc_price.rename(columns={"time":"timestamp"})
        df_btc_price['priceUsd'] = df_btc_price['priceUsd'].astype(float)

    except:
        df_btc_price = pd.DataFrame()

    return df_btc_price


def preapre_data_for_ma_200_indicator(df_btc_price):
    
    sma200_url = f'https://api.polygon.io/v1/indicators/sma/X:BTCUSD?timespan=hour&window=180&series_type=close&order=desc&limit=700&apiKey={api_key_polygon}'
    ema200_url = f'https://api.polygon.io/v1/indicators/ema/X:BTCUSD?timespan=hour&window=180&series_type=close&order=desc&limit=700&apiKey={api_key_polygon}'

    try:

        response = requests.request("GET", sma200_url)
        json_data = json.loads(response.text.encode('utf8'))
        data = json_data["results"]["values"]
        df_sma200 = pd.DataFrame(data)

        response = requests.request("GET", ema200_url)
        json_data = json.loads(response.text.encode('utf8'))
        data = json_data["results"]["values"]
        df_ema200 = pd.DataFrame(data)

        df_ma200=df_sma200.merge(df_ema200, on='timestamp', how='left')

        df_ma200=df_ma200.merge(df_btc_price, on='timestamp', how='left')

        df_ma200['timestamp'] = df_ma200['timestamp'].astype('datetime64[ms]')

        df_ma200 = df_ma200.rename(columns={"value_x":"SMA", "value_y":"EMA", "priceUsd":"BTC price"})
    
    except:
        df_ma200 = pd.DataFrame()

    return df_ma200


def save_exchange_rates(usd_price, pln_price, eur_price, gbp_price, chf_price):

    existing_record = session.query(ExchangeRates).filter(ExchangeRates.date==str(datetime.date.today())).first()

    if not existing_record:
        data_record = ExchangeRates(None, datetime.date.today(), usd_price, pln_price, eur_price, gbp_price, chf_price)
        session.add(data_record)
        session.commit()


def check_cache_database():

    date="2023-03-25"
    usd_price = 1
    pln_price = 4.36
    eur_price = 0.93
    gbp_price = 0.82
    chf_price = 0.92

    existing_records = session.query(ExchangeRates).all()

    if not existing_records:
        data_record = ExchangeRates(None, date, usd_price, pln_price, eur_price, gbp_price, chf_price)
        session.add(data_record)
        session.commit()


def get_from_cache_database(base_currency):

    check_cache_database()

    last_record  = session.query(ExchangeRates).order_by(ExchangeRates.id.desc()).first()


    if base_currency == "PLN": base=float(last_record.PLN)
    elif base_currency == "EUR": base=float(last_record.EUR)
    elif base_currency == "GBP": base=float(last_record.GBP)
    elif base_currency == "CHF": base=float(last_record.CHF)
    else: base=float(last_record.USD)

    usd_price = round(float(last_record.USD)/base,2)
    pln_price = round(float(last_record.PLN)/base,2)
    eur_price = round(float(last_record.EUR)/base,2)
    gbp_price = round(float(last_record.GBP)/base,2)
    chf_price = round(float(last_record.CHF)/base,2)

    return last_record.date, usd_price, pln_price, eur_price, gbp_price, chf_price

