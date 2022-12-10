from dash import html, dash_table, dcc
import dash_daq as daq

from common import COLORS


crypto_amount = (
    html.Div([
    daq.LEDDisplay(
        id='my-crypto-LED-display-1',
        label="Amount of crypto",
        value=10,
        backgroundColor='#111111'
    )
],
    className="LED-display-container"
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
        className="main-options"
    )
 )