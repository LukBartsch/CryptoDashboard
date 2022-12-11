from dash import html, dcc
import dash_bootstrap_components as dbc

ma_select_config = (

    html.Section(children=[

        html.Div(children=[
            html.Label(
                'Select MA type: ',
            ),
            dcc.Checklist(
                id='ma-types',
                options=['  Simple Moving Average (SMA)', '  Exponential Moving Average (EMA)'],
                value=['  Simple Moving Average (SMA)', '  Exponential Moving Average (EMA)'],
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
                'Select window size used to calculate: ',
            ),
            dcc.Dropdown(
                id='ma-window',
                options=['50 days', '200 days'],
                value='50 days'
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
                options= ['Last Day', 'Last Week', 'Last Two Weeks', 'Last Month'],
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

ma_indicator_info = (

    html.Div(children=[
            dbc.Button(
                "What is Moving Average?",
                id="ma-collapse-button",
                className="mb-3",
                color="primary",
                n_clicks=0,
            ),
            dbc.Collapse(
                dbc.Card(dbc.CardBody("The Moving Average (MA) is an indicator that smoothes the data from a given market to create an easy-to-read trend indicator. However, taking into account the fact that MA is based on data from the past, this indicator has been categorized into the group of lagging indicators. It is also often called a trend-following indicator. MA is most commonly divided into two main categories: Simple Moving Averages (SMA) and Exponential Moving Averages (EMA)."),
                    className="collaps-button-area"
                ),
                    id="ma-collapse",
                    is_open=False,
                ),
            ],
            className='main-fng-box'
        )
)