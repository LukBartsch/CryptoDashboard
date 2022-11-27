from dash import html, dcc


rsi_index_line_graph = (

    html.Section(children=[
        html.Div([
        

            html.Div(children=[
                html.Label(
                    'Select time range: ',
                ),
                dcc.Dropdown(
                    id='rsi-checklist',
                    options= ['Last Week', 'Last Month', 'Last Six Month', 'Last Year'],
                    value = "Last Month",
                ),
            ],
                className='select-data higher-width'
            ),

            dcc.Graph(id="rsi-line-graph")
            ])
        ],
        className='graph-container'
    )
)