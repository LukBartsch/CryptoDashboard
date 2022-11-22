
import pandas as pd
import datetime
import time
import requests
import json

from common import CRYPTO_CURRENCIES


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