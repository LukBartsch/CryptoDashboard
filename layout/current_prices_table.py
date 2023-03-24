from dash import html, dash_table
import dash_daq as daq
import dash_bootstrap_components as dbc

from common import COLORS
from common import BASE_CURRENCIES


warning_message = (

    html.Section(children=[
        dbc.Alert(
            color="warning",
            id="alert",
            dismissable=True,
            is_open=False,
        ),
    ],
        className='main-options'
    )
)



crypto_amount = (

    html.Section(children=[
        html.Div(children=[
            daq.LEDDisplay(
                id='LED-display-usd',
                label=f"USD [{BASE_CURRENCIES['USD']}]",
                backgroundColor='#111111'
            ),
        ],
            className='select-data higher-width'
        ),
        html.Div(children=[
            daq.LEDDisplay(
                id='LED-display-pln',
                label=f"PLN [{BASE_CURRENCIES['PLN']}]",
                backgroundColor='#111111'
            ),
        ],
            className='select-data higher-width'
        ),
        html.Div(children=[
            daq.LEDDisplay(
                id='LED-display-eur',
                label=f"EUR [{BASE_CURRENCIES['EUR']}]",
                backgroundColor='#111111'
            ),
        ],
            className='select-data higher-width'
        ),
        html.Div(children=[
            daq.LEDDisplay(
                id='LED-display-gpb',
                label=f"GBP [{BASE_CURRENCIES['GBP']}]",
                backgroundColor='#111111'
            ),
        ],
            className='select-data higher-width'
        ),
        html.Div(children=[
            daq.LEDDisplay(
                id='LED-display-chf',
                label=f"CHF [{BASE_CURRENCIES['CHF']}]",
                backgroundColor='#111111'
            ),
        ],
            className='select-data higher-width'
        )
    ],
        className='main-options'
    )
)



current_prices_table = (
    
     html.Section(children=[
        html.H2(
            id="table-header",
        ),
        dash_table.DataTable(
            id='crypto-table',
            merge_duplicate_headers=True,
            style_header={
                'backgroundColor': 'rgb(30, 30, 30)',
                'color': '#007eff',
                'textAlign': 'center',
                'fontWeight': 'bold',
                'fontSize': '15px'
            },
            style_cell={
                'padding': '10px',
                'backgroundColor': COLORS['background'],
                'color': COLORS['text'],
                'textAlign': 'center'
            },
            style_data_conditional=[
                {
                        'if': {
                            'filter_query': '{Change24h[%]} < 0',
                            'column_id': 'Change24h[%]'
                        },
                        'color': 'tomato'
                },
                {
                        'if': {
                            'filter_query': '{Change24h[%]} > 0',
                            'column_id': 'Change24h[%]'
                        },
                        'color': 'rgb(8, 130, 8)'
                },
                {
                        'if': {
                            'column_id': 'Logo'
                        },
                        'padding-top': '25px'
                },
            ]
        ),
    ],
        className="main-table-options"
    )
 )