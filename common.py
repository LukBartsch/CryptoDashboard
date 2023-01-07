import requests
import json
from datetime import datetime
import pandas as pd

BASE_CURRENCIES = {'USD': '$', 'PLN': 'zł', 'EUR': '€', 'GBP': '£', 'CHF': '₣'}


coincapapi_url = 'http://api.coincap.io/v2/assets?limit=10'
response = requests.request("GET", coincapapi_url)
json_data = json.loads(response.text.encode('utf8'))
assets = json_data["data"]
df_assets = pd.DataFrame(assets)
crypto_names = list(df_assets['id'])

CRYPTO_CURRENCIES = crypto_names

TODAY_DATE = datetime.today().strftime('%Y-%m-%d')

COLORS = {
    'background': '#111111',
    'text': '#7FDBFF'
}

api_key_polygon = 'IKAQmrb2sLnT0DbQvACRlG2OXg8Cbpa8'