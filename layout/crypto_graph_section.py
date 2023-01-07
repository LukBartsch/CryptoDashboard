from dash import html, dcc

from datetime import datetime, timedelta

from common import BASE_CURRENCIES
from common import TODAY_DATE
from callbacks import CRYPTO_CURRENCIES


main_crypto_title = (

    html.H1(
        children="Dash application for cryptocurrencies monitoring",
        className="main-header"
    )
)


crypto_and_date_section = (

    html.Section(children=[
        html.Div(children=[
            html.Label(
                'Select base currency: ',
            ),
            dcc.Dropdown(
                id='base-currency',
                options=list(BASE_CURRENCIES.keys()),
                value='USD'
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
    )
)

crypto_graph = (
    html.Section(
        dcc.Graph(
            id='crypto-graph',
        ),
        className='graph-container'
    )
)