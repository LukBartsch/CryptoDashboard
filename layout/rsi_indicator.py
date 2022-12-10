from dash import html, dcc
import dash_bootstrap_components as dbc


rsi_index_info = (

    html.Div(children=[
            dbc.Button(
                "What is Relative Strength Indicator?",
                id="rsi-collapse-button",
                className="mb-3",
                color="primary",
                n_clicks=0,
            ),
            dbc.Collapse(
                dbc.Card(dbc.CardBody("One of the market indicators of technical analysis of the financial markets that serves as a speed oscillator that measures the speed and change of price movements. It oscillates between 0 and 100. It is assumed that when the RSI is at the level of 70 and above, it is a cryptocurrency sell signal (market overbought signal). If the RSI is at 30 and below, it is a cryptocurrency buy signal (market oversold signal). When the RSI is at 0, it means that the probability of a reversal of the trend to an upward one is highly probable. The RSI works by taking into account recent price movements exponentially, with the most recent changes weighing more heavily than older ones."),
                    className="collaps-button-area"
                ),
                    id="rsi-collapse",
                    is_open=False,
                ),
            ],
            className='main-fng-box'
        )
)


rsi_index_line_graph = (

    html.Section(children=[
        html.Div([
        

            html.Div(children=[
                html.Label(
                    ' ',
                ),
                dcc.Dropdown(
                    id='rsi-checklist',
                    options= ['Last Day', 'Last Week', 'Last Two Weeks', 'Last Month'],
                    value = "Last Two Weeks",
                )
            ],
                className='select-data higher-width'
            ),

            dcc.Graph(id="rsi-line-graph")
            ])
        ],
        className='graph-container'
    )
)