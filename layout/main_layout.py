
from dash import html, dcc

from layout.crypto_graph_section import main_crypto_title, crypto_and_date_section, crypto_graph
from layout.fear_and_greed_index import fng_index_table, fng_index_line_graph, fng_index_info
from layout.rsi_indicator import rsi_index_line_graph, rsi_index_info
from layout.current_prices_table import current_prices_table
from layout.moving_averages import ma_select_config, ma_graph






layout = html.Div(className="main", children=[

    main_crypto_title,
    crypto_and_date_section,
    crypto_graph,


    html.Div([
    dcc.Tabs([
        dcc.Tab(label='Ranking', children=[
            
            current_prices_table
        ],
        style={
                'backgroundColor': 'rgb(50, 50, 50)',
                'borderBottom': '1px solid #d6d6d6',
        },
        selected_style={
                'backgroundColor': '#111111',
                'borderTop': '2px solid #007eff',
                'borderBottom': '1px solid #d6d6d6',
                'color': '#007eff',
        },
        className="tab-box"
        ),

        dcc.Tab(label='Fear and Greed Index', children=[
            fng_index_table,
            fng_index_line_graph,
            fng_index_info
        ],
        style={
                'backgroundColor': 'rgb(50, 50, 50)',
                'borderBottom': '1px solid #d6d6d6',
        },
        selected_style={
                'backgroundColor': '#111111',
                'borderTop': '2px solid #007eff',
                'borderBottom': '1px solid #d6d6d6',
                'color': '#007eff',
        },
        className="tab-box"
        ),

        dcc.Tab(label='Relative Strength Index', children=[
            rsi_index_line_graph,
            rsi_index_info
        ],
        style={
                'backgroundColor': 'rgb(50, 50, 50)',
                'borderBottom': '1px solid #d6d6d6',
        },
        selected_style={
                'backgroundColor': '#111111',
                'borderTop': '2px solid #007eff',
                'borderBottom': '1px solid #d6d6d6',
                'color': '#007eff',
        },
        className="tab-box"
        ),

        dcc.Tab(label='Moving Averages', children=[
            ma_select_config,
            ma_graph
        ],
        style={
                'backgroundColor': 'rgb(50, 50, 50)',
                'borderBottom': '1px solid #d6d6d6',
        },
        selected_style={
                'backgroundColor': '#111111',
                'borderTop': '2px solid #007eff',
                'borderBottom': '1px solid #d6d6d6',
                'color': '#007eff',
        },
        className="tab-box"
        ),
    ])
    ],
        className='tabs-menu'
    )
])


