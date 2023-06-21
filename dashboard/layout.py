import dash
from dash import dcc, html, Input, Output, callback, dash_table, callback_context, no_update
import dash_bootstrap_components as dbc
from dashboard.query import queryData
import plotly.express as px
import plotly.graph_objects as go

from dashboard import query, func


data_df = queryData()
detail_table = dash_table.DataTable(id='detail_table',
                                    columns=[{"name": i, "id": i} for i in data_df],
                                    data=data_df.to_dict('records'),
                                    page_size=10,
                                    style_as_list_view=True,
                                    sort_action='native',
                                    style_table={'overflowX': 'auto',
                                                 'border': '3px solid black'},
                                    style_header={'padding-left':'0px',
                                                  'margin-left' :'0px',
                                                  'textAlign': 'left',
                                                  'fontWeight': 'bold',
                                                  'backgroundColor': '#3B3331',
                                                  'color': 'white'},
                                    style_cell={'padding-left': '0px',
                                                'textAlign': 'left',
                                                'overflow': 'hidden',
                                                'textOverflow': 'ellipsis',
                                                'color': 'black',
                                                'minWidth': '10px',
                                                'width': '10px',
                                                'maxWidth': '250px'},
                                    css = [{'selector': '.column-header-name', 'rule' : 'margin-left:unset;'}])

sim_table = dash_table.DataTable(id='sim-table',
                                 columns=[
                                     {"name": 'State', "id": 'State'},
                                     {"name": 'Delegates', "id": 'Delegates'},
                                     {"name": 'Winning Coalition Count', "id": 'Winning Coalition Count'},
                                     {"name": 'Winning Coalition Pct', "id": 'Winning Coalition Pct'},
                                 ],
                                 # data=data_df.to_dict('records'),
                                 page_size=10,
                                 style_as_list_view=True,
                                 sort_action='native',
                                 style_table={'overflowX': 'auto',
                                              'border': '3px solid black'},
                                 style_header={'padding-left':'0px',
                                               'margin-left' :'0px',
                                               'textAlign': 'left',
                                               'fontWeight': 'bold',
                                               'backgroundColor': '#3B3331',
                                               'color': 'white'},
                                 style_cell={'padding-left': '0px',
                                             'textAlign': 'left',
                                             'overflow': 'hidden',
                                             'textOverflow': 'ellipsis',
                                             'color': 'black',
                                             'minWidth': '10px',
                                             'width': '10px',
                                             'maxWidth': '250px'},
                                 css = [{'selector': '.column-header-name', 'rule' : 'margin-left:unset;'}])


names = data_df['candidate_name'].tolist()
candidate_dropdown = dcc.Dropdown(id='candidate-select', multi=True)
state_dropdown = dcc.Dropdown(id='state-select', value = 'IA', clearable=False)

summary = html.Div([

    html.H2('Stephen Brock | Republican Primary Dataset',
            style={'padding-left': 25,
                   'padding-top': 10,
                   'padding-bottom': 5,
                   'background-color': '#FF0000',
                   'color': 'white',
                   'border-bottom': 'black'}),

    dbc.Container([
        dbc.Tabs(
            [
                dbc.Tab(
                    [
                        dbc.Row([
                            dbc.Col([
                                candidate_dropdown,
                                state_dropdown
                            ], width=3),
                        ], style={'padding-top': '10px'}),
                        dbc.Row([
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardHeader("Gender Breakout"),
                                    dbc.CardBody([dcc.Graph(id='average-pie', config={'displayModeBar': False})]),
                                ])
                            ], width=6),
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardHeader("Gender Breakout"),
                                    dbc.CardBody([dcc.Graph(id='historical-line', config={'displayModeBar': False})])
                                ])
                            ], width=6),
                        ], style={'padding-top': '10px', 'padding-bottom': '10px'}),
                        dbc.Row(detail_table)
                    ],
                    label = 'State Polling'
                ),
                dbc.Tab(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dcc.Dropdown(id='trial-count',
                                                     options=[
                                                              {'label': '10,000', 'value': '10000'},
                                                              {'label': '50,000', 'value': '50000'},
                                                              {'label': '100,000', 'value': '100000'},
                                                              {'label': '1,000,000', 'value': '1000000'}
                                                     ],
                                                     placeholder='Select Number of Trials',
                                                     value=10000,
                                                     clearable=False)
                                    ]
                                ),
                                dbc.Col(
                                    [
                                        html.Button('Run Simulation',id='run-simulation')
                                    ]
                                )
                            ], style={'padding-top': '10px', 'padding-bottom': '10px'}
                        ),
                        dbc.Row(
                            dbc.Col(
                                dcc.Loading(
                                    id="loading2",
                                    children=[dcc.Graph(id='power-bar', config={'displayModeBar': False})],
                                    type="circle",
                                ),

                            )
                        ),
                        dbc.Row([
                            dbc.Col(
                                [
                                    dcc.Loading(
                                        id="loading",
                                        children=[html.Div(sim_table)],
                                        type="circle",
                                    ),
                                ]
                            )
                        ])
                    ],
                    label='Prediction'
                ),
            ]
        )
    ], fluid=True)
])

@callback(
    [
        Output('candidate-select', 'options'),
        Output('state-select', 'options')
    ],
    Input('interval-component', 'n_intervals'),
)
def update(n):

    df = query.queryData()

    candidate_options = [{'label': i, 'value': i} for i in df['candidate_name'].unique()]

    state_list = df['state'].dropna().sort_values(ascending=True).unique()

    state_options = [{'label': i, 'value': i} for i in state_list]
    return candidate_options, state_options


@callback([Output('detail_table', 'data'),
           Output('detail_table', 'page_current'),
           Output('average-pie', 'figure'),
           Output('historical-line', 'figure'),
           ],
          [
              Input('candidate-select', 'value'),
              Input('state-select', 'value'),
          ])
def update_figures(candidate, state):

    temp_df = query.queryData()

    if candidate is not None and len(candidate) >= 1:
        temp_df = temp_df.loc[temp_df['candidate_name'].isin(candidate)]

    if state is not None and len(state) >= 1:
        temp_df = temp_df.loc[temp_df['state'] == state]

    average_pie = func.avg_pie(temp_df)
    historical_line = func.historical(temp_df)


    return temp_df.to_dict('records'), 0, average_pie, historical_line


@callback([Output('sim-table', 'data'),
           Output('sim-table', 'page_current'),
           Output('power-bar', 'figure'),
           ],
          [
              Input('trial-count', 'value'),
              Input('run-simulation', 'n_clicks')
          ])
def update_sim(n_trials, run_sim):
    ctx = callback_context
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]


    if input_id != 'trial-count':
        df = func.monte_carlo(int(n_trials))
        cols = [{"name": i, "id": i} for i in df]
        power_bar = func.power_bar(df)

        return df.to_dict('records'), 0, power_bar
    else:
        return no_update, no_update, no_update