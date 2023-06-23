import dash
from dash import (
    dcc,
    html,
    Input,
    Output,
    callback,
    dash_table,
    callback_context,
    no_update,
    State,
)
import dash_bootstrap_components as dbc
from dashboard.query import queryData
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from dashboard import query, func


data_df = queryData()

sim_table = dash_table.DataTable(
    id="sim-table",
    columns=[
        {"name": "State", "id": "State"},
        {"name": "Delegates", "id": "Delegates"},
        {"name": "Winning Coalition Count", "id": "Winning Coalition Count"},
        {"name": "Winning Coalition Pct", "id": "Winning Coalition Pct"},
    ],
    page_size=10,
    style_as_list_view=True,
    sort_action="native",
    style_table={"overflowX": "auto", "border": "3px solid black"},
    style_header={
        "padding-left": "0px",
        "margin-left": "0px",
        "textAlign": "left",
        "fontWeight": "bold",
        "backgroundColor": "#3B3331",
        "color": "white",
    },
    style_cell={
        "padding-left": "0px",
        "textAlign": "left",
        "overflow": "hidden",
        "textOverflow": "ellipsis",
        "color": "black",
        "minWidth": "10px",
        "width": "10px",
        "maxWidth": "250px",
    },
    css=[{"selector": ".column-header-name", "rule": "margin-left:unset;"}],
)

state_table = dash_table.DataTable(
    id="state-table",
    page_size=10,
    style_as_list_view=True,
    sort_action="native",
    style_table={"overflowX": "auto", "border": "3px solid black"},
    style_header={
        "padding-left": "0px",
        "margin-left": "0px",
        "textAlign": "left",
        "fontWeight": "bold",
        "backgroundColor": "#3B3331",
        "color": "white",
    },
    style_cell={
        "padding-left": "0px",
        "textAlign": "left",
        "overflow": "hidden",
        "textOverflow": "ellipsis",
        "color": "black",
        "minWidth": "10px",
        "width": "10px",
        "maxWidth": "250px",
    },
    css=[{"selector": ".column-header-name", "rule": "margin-left:unset;"}],
)


rep_primary_layout = dcc.Loading(
    html.Div(
        [
            dcc.Store(id="national-average-store"),
            dcc.Store(id="national-favorability-store"),
            dcc.Store(id="state-polls-store"),
            html.H2(
                "Republican Primary Dataset",
                style={
                    "padding-left": 25,
                    "padding-top": 10,
                    "padding-bottom": 5,
                    "background-color": "#FF0000",
                    "color": "white",
                    "border-bottom": "black",
                },
            ),
            dbc.Tabs(
                [
                    dbc.Tab(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            dbc.Card(
                                                [
                                                    dbc.CardHeader("Current Polls"),
                                                    dbc.CardBody(
                                                        [
                                                            dbc.Row(
                                                                [
                                                                    dbc.Col(
                                                                        dbc.Card(
                                                                            dcc.Loading(
                                                                                dcc.Graph(
                                                                                    id="current-standing-pie",
                                                                                    config={
                                                                                        "displayModeBar": False
                                                                                    },
                                                                                )
                                                                            ),
                                                                        ),
                                                                        sm=12,
                                                                        xxl=4,
                                                                    ),
                                                                    dbc.Col(
                                                                        dbc.Card(
                                                                            dcc.Loading(
                                                                                dcc.Graph(
                                                                                    id="favorability-stacked-bar",
                                                                                    config={
                                                                                        "displayModeBar": False
                                                                                    },
                                                                                ),
                                                                            )
                                                                        ),
                                                                        sm=12,
                                                                        xxl=8,
                                                                    ),
                                                                ]
                                                            )
                                                        ]
                                                    ),
                                                ]
                                            )
                                        ],
                                        width=12,
                                    )
                                ],
                                style={"padding-top": "10px", "padding-bottom": "10px"},
                            ),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            dbc.Card(
                                                [
                                                    dbc.CardHeader("Historical Polls"),
                                                    dbc.CardBody(
                                                        [
                                                            dbc.Row(
                                                                [
                                                                    dbc.Col(
                                                                        dbc.Card(
                                                                            dcc.Loading(
                                                                                dcc.Graph(
                                                                                    id="historical-line",
                                                                                    config={
                                                                                        "displayModeBar": False
                                                                                    },
                                                                                ),
                                                                            )
                                                                        ),
                                                                        sm=12,
                                                                        xl=6,
                                                                    ),
                                                                    dbc.Col(
                                                                        dbc.Card(
                                                                            dcc.Loading(
                                                                                dcc.Graph(
                                                                                    id="favorability-trend",
                                                                                    config={
                                                                                        "displayModeBar": False
                                                                                    },
                                                                                ),
                                                                            )
                                                                        ),
                                                                        sm=12,
                                                                        xl=6,
                                                                    ),
                                                                ]
                                                            )
                                                        ]
                                                    ),
                                                ]
                                            )
                                        ],
                                        width=12,
                                    ),
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                [
                                                    dbc.Card(
                                                        [
                                                            dbc.CardHeader(
                                                                "Current Standings"
                                                            ),
                                                            dbc.CardBody(
                                                                [
                                                                    dbc.Card(
                                                                        dcc.Loading(
                                                                            dcc.Graph(
                                                                                id="state-choropleth",
                                                                                config={
                                                                                    "displayModeBar": False
                                                                                },
                                                                            ),
                                                                        )
                                                                    ),
                                                                ]
                                                            ),
                                                        ]
                                                    )
                                                ],
                                                width=12,
                                            )
                                        ],
                                        style={
                                            "padding-top": "10px",
                                            "padding-bottom": "10px",
                                        },
                                    ),
                                ],
                                style={"padding-top": "10px", "padding-bottom": "10px"},
                            ),
                        ],
                        label="National Polls",
                    ),
                    dbc.Tab(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            dcc.Dropdown(
                                                id="trial-count",
                                                options=[
                                                    {
                                                        "label": "10,000",
                                                        "value": "10000",
                                                    },
                                                    {
                                                        "label": "50,000",
                                                        "value": "50000",
                                                    },
                                                    {
                                                        "label": "100,000",
                                                        "value": "100000",
                                                    },
                                                    {
                                                        "label": "1,000,000",
                                                        "value": "1000000",
                                                    },
                                                ],
                                                placeholder="Select Number of Trials",
                                                value=10000,
                                                clearable=False,
                                            )
                                        ]
                                    ),
                                    dbc.Col(
                                        [
                                            html.Button(
                                                "Run Simulation", id="run-simulation"
                                            )
                                        ]
                                    ),
                                ],
                                style={"padding-top": "10px", "padding-bottom": "10px"},
                            ),
                            dbc.Row(
                                dbc.Col(
                                    dcc.Loading(
                                        id="loading2",
                                        children=[
                                            dcc.Graph(
                                                id="power-bar",
                                                config={"displayModeBar": False},
                                            )
                                        ],
                                        type="circle",
                                    ),
                                )
                            ),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            dcc.Loading(
                                                id="loading",
                                                children=[html.Div(sim_table)],
                                                type="circle",
                                            ),
                                        ]
                                    )
                                ]
                            ),
                        ],
                        label="State Political Power",
                    ),
                ]
            ),
        ]
    )
)


@callback(
    [
        Output("national-average-store", "data"),
        Output("national-favorability-store", "data"),
        Output("state-polls-store", "data"),
    ],
    Input("interval-component", "n_intervals"),
)
def update(n):
    national_avg_poll_df, national_favorability_df, state_polls_df = query.queryData()

    national_favorability_df = national_favorability_df.loc[
        national_favorability_df["politician"].isin(
            national_avg_poll_df["candidate"].unique()
        )
    ]

    return (
        national_avg_poll_df.to_dict("records"),
        national_favorability_df.to_dict("records"),
        state_polls_df.to_dict("records"),
    )


@callback(
    [
        Output("current-standing-pie", "figure"),
        Output("historical-line", "figure"),
        Output("favorability-trend", "figure"),
        Output("favorability-stacked-bar", "figure"),
        Output("state-choropleth", "figure"),
    ],
    [
        Input("national-average-store", "data"),
        Input("national-favorability-store", "data"),
        Input("state-polls-store", "data"),
    ],
)
def update_current_standing_figures(
    national_avg_data, national_favorability_data, state_poll_data
):
    national_avg_poll_df = pd.DataFrame(national_avg_data)
    national_favorability_df = pd.DataFrame(national_favorability_data)
    state_poll_df = pd.DataFrame(state_poll_data)

    state_standing_map = func.state_standing_map(state_poll_df)
    historical_line = func.national_average_trend(national_avg_poll_df)
    current_standing_pie = func.national_standing_pie(national_avg_poll_df)

    favorability_trend_graph = func.national_favorability_trend(
        national_favorability_df
    )
    favorability_trend_bar = func.national_favorability_stacked_bar(
        national_favorability_df
    )

    return (
        current_standing_pie,
        historical_line,
        favorability_trend_graph,
        favorability_trend_bar,
        state_standing_map,
    )


@callback(
    [
        Output("sim-table", "data"),
        Output("sim-table", "page_current"),
        Output("power-bar", "figure"),
    ],
    [
        Input("trial-count", "value"),
        Input("run-simulation", "n_clicks"),
    ],
)
def update_sim(n_trials, run_sim):
    ctx = callback_context
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if input_id != "trial-count":
        df = func.monte_carlo(int(n_trials))
        cols = [{"name": i, "id": i} for i in df]
        power_bar = func.power_bar(df)

        return df.to_dict("records"), 0, power_bar
    else:
        return no_update, no_update, no_update
