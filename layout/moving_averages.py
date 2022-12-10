from dash import html, dcc

from datetime import datetime, timedelta

from common import BASE_CURRENCIES
from common import CRYPTO_CURRENCIES
from common import TODAY_DATE



ma_select_config = (

    html.Section(children=[

        html.Div(children=[
            html.Label(
                'Select type: ',
            ),
            dcc.Checklist(
                id='ma-types',
                options=['SMA', 'EMA'],
                value=['SMA'],
                # inline=True,
                style={
                    'padding': '5px',
                }
            )
        ],
            className='select-data higher-width'
        ),

        html.Div(children=[
            html.Label(
                'Select window: ',
            ),
            dcc.Dropdown(
                id='ma-window',
                options=['9', '20', '50', '100', '200'],
                value='50'
            ),
        ],
            className='select-data higher-width'
        ),

        html.Div(children=[
            html.Label(
                'Select time range: ',
            ),
            dcc.Dropdown(
                id='ma-period',
                options= ['Last Week', 'Last Month', 'Last Six Month', 'Last Year'],
                value = "Last Month",
            ),
        ],
            className='select-data higher-width'
        ),

    ],
        className='main-options'
    )
)


ma_graph = (
    html.Section(
        dcc.Graph(
            id='ma-line-graph',
        ),
        className='graph-container'
    )
)