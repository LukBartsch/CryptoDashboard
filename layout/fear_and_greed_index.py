from dash import html, dcc, dash_table
import dash_daq as daq
import dash_bootstrap_components as dbc

from callbacks import df_short_fng


fng_index_table = (

    html.Section(children=[
        html.Div(
            daq.Gauge(
                id='fear_greed_index',
                color={"gradient":True,"ranges":{"red":[0,33],"yellow":[33,66],"green":[66,100]}},
                value=int(df_short_fng['Value'].loc[0]),
                showCurrentValue=True,
                label='Fear and Greed Index ',
                max=100,
                min=0,
            ),
            className='fng-part-data'
        ),


        html.Div(
            dash_table.DataTable(
                data = df_short_fng.to_dict('records'), 
                columns = [{"name": i, "id": i} for i in df_short_fng.columns],

                style_header={
                    'backgroundColor': 'rgb(30, 30, 30)',
                    'color': 'white',
                    'text-align': 'center',
                    'display': 'none'
                },
                style_data={
                    'backgroundColor': 'rgb(50, 50, 50)',
                    'color': 'white',
                    'text-align': 'center'
                },
                style_cell_conditional=[
                    {
                        'if': {
                            'column_id': 'Value'
                        },
                        'width': '70px'
                    },
                    {
                        'if': {
                            'column_id': 'Label'
                        },
                        'width': '150px'
                    },
                    {
                        'if': {
                            'column_id': 'Time'
                        },
                        'width': '100px'
                    }
                ],
                style_data_conditional=[
                    {
                        'if': {
                            'filter_query': '{Value} > 0 && {Value} <= 25',
                            'column_id': 'Value'
                        },
                        'backgroundColor': 'tomato',
                        'color': 'white'
                    },
                    {
                        'if': {
                            'filter_query': '{Value} > 25 && {Value} < 50',
                            'column_id': 'Value'
                        },
                        'backgroundColor': 'rgba(206, 140, 104, 1)',
                        'color': 'white'
                    },
                    {
                        'if': {
                            'filter_query': '{Value} = 50',
                            'column_id': 'Value'
                        },
                        'backgroundColor': 'rgb(220, 220, 7)',
                        'color': 'white'
                    },
                    {
                        'if': {
                            'filter_query': '{Value} > 50 && {Value} <= 75',
                            'column_id': 'Value'
                        },
                        'backgroundColor': 'rgb(41, 183, 41)',
                        'color': 'white'
                    },
                    {
                        'if': {
                            'filter_query': '{Value} > 75 && {Value} <= 100',
                            'column_id': 'Value'
                        },
                        'backgroundColor': 'rgb(8, 130, 8)',
                        'color': 'white'
                    },
                    {
                        'if': {
                            'filter_query': '{Value} > 0 && {Value} <= 25',
                            'column_id': 'Label'
                        },
                        'color': 'tomato'
                    },
                    {
                        'if': {
                            'filter_query': '{Value} > 25 && {Value} < 50',
                            'column_id': 'Label'
                        },
                        'color': 'rgba(206, 140, 104, 1)'
                    },
                    {
                        'if': {
                            'filter_query': '{Value} = 50',
                            'column_id': 'Label'
                        },
                        'color': 'rgb(220, 220, 7)'
                    },
                    {
                        'if': {
                            'filter_query': '{Value} > 50 && {Value} <= 75',
                            'column_id': 'Label'
                        },
                        'color': 'rgb(41, 183, 41)'
                    },
                    {
                        'if': {
                            'filter_query': '{Value} > 75 && {Value} <= 100',
                            'column_id': 'Label'
                        },
                        'color': 'rgb(8, 130, 8)'
                    },
                ]
                    
            ),
            className='fng-part-data'
        ),

    ],
        className='main-fng-box'
    )
)

fng_index_line_graph = (

    html.Section(children=[
        html.Div([
        

            html.Div(children=[
                html.Label(
                    'Select time range: ',
                ),
                dcc.Dropdown(
                    id='checklist',
                    options= ['Last Week', 'Last Month', 'Last Six Month', 'Last Year'],
                    value = "Last Month",
                ),
            ],
                className='select-data higher-width'
            ),

            dcc.Graph(id="fng-line-graph")
            ])
        ],
        className='graph-container'
    )
)

fng_index_info = (

    html.Div(children=[
            dbc.Button(
                "What is Fear and Greed Index?",
                id="collapse-button",
                className="mb-3",
                color="primary",
                n_clicks=0,
            ),
            dbc.Collapse(
                dbc.Card(dbc.CardBody("The crypto market behaviour is very emotional. People tend to get greedy when the market is rising which results in FOMO (Fear of missing out). Also, people often sell their coins in irrational reaction of seeing red numbers. With our Fear and Greed Index, we try to save you from your own emotional overreactions. Therefore, we analyze the current sentiment of the Bitcoin market and crunch the numbers into a simple meter from 0 to 100. Zero means 'Extreme Fear', while 100 means 'Extreme Greed'."),
                    className="collaps-button-area"
                ),
                    id="collapse",
                    is_open=False,
                ),
            ],
            className='main-fng-box'
        )
)