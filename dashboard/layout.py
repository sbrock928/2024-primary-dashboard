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
detail_table = dash_table.DataTable(
    id="detail_table",
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

candidate_dropdown = dcc.Dropdown(id="candidate-select", multi=True)


summary = html.Div(
    [
        dcc.Store(id="average-polls-store"),
        dcc.Store(id="favorability-polls-store"),
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
                                        candidate_dropdown,
                                    ],
                                    width=3,
                                ),
                            ],
                            style={"padding-top": "10px"},
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Card(
                                            [
                                                dbc.CardHeader("Gender Breakout"),
                                                dbc.CardBody(
                                                    [
                                                        dcc.Graph(
                                                            id="average-pie",
                                                            config={
                                                                "displayModeBar": False
                                                            },
                                                        )
                                                    ]
                                                ),
                                            ]
                                        )
                                    ],
                                    width=6,
                                ),
                                dbc.Col(
                                    [
                                        dbc.Card(
                                            [
                                                dbc.CardHeader("Gender Breakout"),
                                                dbc.CardBody(
                                                    [
                                                        dcc.Graph(
                                                            id="historical-line",
                                                            config={
                                                                "displayModeBar": False
                                                            },
                                                        )
                                                    ]
                                                ),
                                            ]
                                        )
                                    ],
                                    width=6,
                                ),
                            ],
                            style={"padding-top": "10px", "padding-bottom": "10px"},
                        ),
                        dbc.Row(detail_table),
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
                                                {"label": "10,000", "value": "10000"},
                                                {"label": "50,000", "value": "50000"},
                                                {"label": "100,000", "value": "100000"},
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
                                    [html.Button("Run Simulation", id="run-simulation")]
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
                dbc.Tab(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    dcc.Dropdown(
                                        id="state-select", value="IA", clearable=False
                                    )
                                )
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dcc.Loading(
                                            children=[html.Div(state_table)],
                                            type="circle",
                                        ),
                                    ]
                                )
                            ]
                        ),
                    ],
                    label="State Polling",
                ),
            ]
        ),
    ]
)


@callback(
    [
        Output("average-polls-store", "data"),
        Output("favorability-polls-store", "data"),
        Output("state-polls-store", "data"),
        Output("candidate-select", "options"),
        Output("state-select", "options"),
    ],
    Input("interval-component", "n_intervals"),
)
def update(n):
    average_polls_df, favorability_polls_df, state_polls_df = query.queryData()

    candidate_options = [
        {"label": i, "value": i} for i in average_polls_df["candidate"].unique()
    ]
    favorability_polls_df = favorability_polls_df.loc[
        favorability_polls_df["politician"].isin(average_polls_df["candidate"].unique())
    ]
    state_list = state_polls_df["state"].dropna().sort_values(ascending=True).unique()

    return (
        average_polls_df.to_dict("records"),
        favorability_polls_df.to_dict("records"),
        state_polls_df.to_dict("records"),
        candidate_options,
        state_list,
    )


@callback(
    [
        Output("detail_table", "data"),
        Output("detail_table", "page_current"),
        Output("average-pie", "figure"),
        Output("historical-line", "figure"),
    ],
    [
        Input("candidate-select", "value"),
        Input("average-polls-store", "data"),
        Input("favorability-polls-store", "data"),
    ],
)
def update_figures(candidate, average_polls, favorability_polls):
    average_polls_df = pd.DataFrame(average_polls)
    favorability_polls_df = pd.DataFrame(favorability_polls)

    if candidate is not None and len(candidate) >= 1:
        average_polls_df = average_polls_df.loc[
            average_polls_df["candidate"].isin(candidate)
        ]
        favorability_polls_df = favorability_polls_df.loc[
            favorability_polls_df["politician"].isin(candidate)
        ]

    average_pie = func.avg_pie(favorability_polls_df)
    historical_line = func.historical(average_polls_df)

    return average_polls_df.to_dict("records"), 0, average_pie, historical_line


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


@callback(
    [
        Output("state-table", "data"),
        Output("state-table", "page_current"),
    ],
    [Input("state-polls-store", "data")],
)
def update_states(state_polls):
    state_polls_df = pd.DataFrame(state_polls)
    state_polls_df = (
        state_polls_df.groupby(["candidate_name"])["pct"]
        .mean()
        .round(2)
        .reset_index()
        .sort_values(["pct"], ascending=False)
    )

    # if candidate is not None and len(candidate) >= 1:
    #     state_polls_df = state_polls_df.loc[state_polls_df['candidate_name'].isin(candidate)]

    return state_polls_df.to_dict("records"), 0
