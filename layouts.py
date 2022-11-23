
from dash import html, dcc
import dash_daq as daq

from datetime import datetime, timedelta

# from common import COLORS
from common import BASE_CURRENCIES
from common import CRYPTO_CURRENCIES
from common import TODAY_DATE


layout = html.Div(className="main", children=[

    html.H1(
        children="Dash application for cryptocurrencies monitoring",
        className="main-header"
    ),

    html.Section(children=[
        html.Div(children=[
            html.Label(
                'Select base currency: ',
            ),
            dcc.Dropdown(
                id='base-currency',
                options=BASE_CURRENCIES,
                value='PLN'
            ),
        ],
            className='select-data higher-width'
        ),

        html.Div(children=[
            html.Label(
                'Select crypto: ',
            ),
            dcc.Dropdown(
                id='crypto-dropdown',
                options=CRYPTO_CURRENCIES,
                value='bitcoin',
                multi=True
            ),
        ],
            className='select-data higher-width'
        ),

        html.Div(children=[
            html.Label(
                'Select start date: ',
            ),
            html.Div(
                dcc.DatePickerSingle(
                    id='start-date-picker',
                    min_date_allowed=datetime(2015, 1, 1),
                    max_date_allowed=(datetime.today() - timedelta(days=7)),
                    date=datetime(2019, 1, 1),
                    initial_visible_month=datetime(2019, 1, 1)
                ),
            ),
        ],
            className='select-data small-width'
        ),

        html.Div(children=[
            html.Label(
                'Select end date: ',
            ),
            html.Div(
                dcc.DatePickerSingle(
                    id='end-date-picker',
                    min_date_allowed=datetime(2015, 1, 1),
                    max_date_allowed=TODAY_DATE,
                    date=TODAY_DATE,
                    initial_visible_month=TODAY_DATE,
                ),
            ),
        ],
            className='select-data small-width'
        )
    ],
        className='main-options'
    ),


    html.Section(
        dcc.Graph(
            id='crypto-graph',
        ),
        className='graph-container'
    ),



    html.Section(
        html.Div([
            daq.Gauge(
                id='fear_greed_index',
                color={"gradient":True,"ranges":{"red":[0,33],"yellow":[33,66],"green":[66,100]}},
                value=100,
                showCurrentValue=True,
                label='Fear and Greed Index ',
                max=100,
                min=0,
            )
        ])
    ),

])