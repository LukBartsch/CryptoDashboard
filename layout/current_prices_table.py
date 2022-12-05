from dash import html, dash_table

from common import COLORS

current_prices_table = (
    
     html.Section(children=[
        html.H2(
            id="table-header",
        ),
        dash_table.DataTable(
            id='currency-table',
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
                        'column_id': 'currency'
                    },
                    'fontSize': '15px',
                    'color': '#CCF1FF',
                    'textAlign': 'center'
                },

                {
                        'if': {
                            'column_id': 'Change24h[%]'
                        },
                        'color': 'tomato'
                },
            ]
        ),
    ],
        className="container"
    )
 )