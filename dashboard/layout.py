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

import pandas as pd
import datetime

from dashboard import query, func
from dashboard.constants import states

date_picker = (
    dcc.DatePickerSingle(
        id="date-range",
        min_date_allowed=datetime.date(2023, 3, 1),
    ),
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

states_table = dash_table.DataTable(
    id="states-table",
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
    style_data_conditional=[
        {
            "if": {"filter_query": "{Diff} > 5 && {Diff} < 19", "column_id": "Diff"},
            "backgroundColor": "#7CFC00",
            "color": "black",
        },
        {
            "if": {"filter_query": "{Diff} >= 19", "column_id": "Diff"},
            "backgroundColor": "#006400",
            "color": "white",
        },
    ],
    css=[{"selector": ".column-header-name", "rule": "margin-left:unset;"}],
    editable=True,
    columns=[
        {"name": "Code", "id": "Code"},
        {"name": "Candidate", "id": "Candidate"},
        {"name": "Percentage", "id": "Percentage"},
        {"name": "Diff", "id": "Diff"},
        {"name": "Scenario", "id": "Scenario", "presentation": "dropdown"},
    ],
    dropdown={
        "Scenario": {
            "options": [
                {"label": "Trump", "value": "Trump"},
                {"label": "Opposition", "value": "Opposition"},
            ]
        }
    },
)

candidate_dropdown = dcc.Dropdown(
    id="candidate-select",
    options=[
        {"label": "Trump", "value": "Trump"},
        {
            "label": "DeSantis",
            "value": "DeSantis",
        },
        {
            "label": "Pence",
            "value": "Pence",
        },
        {
            "label": "Haley",
            "value": "Haley",
        },
        {
            "label": "Scott",
            "value": "Scott",
        },
        {
            "label": "Ramaswamy",
            "value": "Ramaswamy",
        },
        {
            "label": "Hutchinson",
            "value": "Hutchinson",
        },
        {
            "label": "Burgum",
            "value": "Burgum",
        },
        {
            "label": "Christie",
            "value": "Christie",
        },
    ],
    value="Trump",
    clearable=False,
    multi=False,
)


state_dropdown = dcc.Dropdown(
    id="state-select",
    value="IA",
    options=[{"label": i, "value": i} for i in states],
    clearable=False,
)

rep_primary_layout = dcc.Loading(
    html.Div(
        [
            dcc.Store(id="national-average-store"),
            dcc.Store(id="national-favorability-store"),
            dcc.Store(id="state-polls-store", storage_type="memory"),
            html.H2(
                "Republican Primary Dataset",
            ),
            dbc.Tabs(
                [
                    dbc.Tab(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(html.P("Candidate:"), sm=1, xxl=1),
                                    dbc.Col(candidate_dropdown, sm=11, xxl=3),
                                ],
                                style={"padding-top": "10px"},
                            ),
                            dbc.Row(
                                [
                                    dbc.Col(html.P("Start Date:"), sm=1, xxl=1),
                                    dbc.Col(date_picker, sm=11, xxl=3),
                                ],
                                style={"padding-top": "10px"},
                            ),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            dbc.Card(
                                                [
                                                    dbc.CardHeader("Projected Votes"),
                                                    dbc.CardBody(
                                                        [
                                                            dbc.Row(
                                                                [
                                                                    dbc.Col(
                                                                        dbc.Card(
                                                                            dcc.Loading(
                                                                                dcc.Graph(
                                                                                    id="candidate-voting-kpi-card",
                                                                                    config={
                                                                                        "displayModeBar": False
                                                                                    },
                                                                                ),
                                                                            )
                                                                        ),
                                                                        sm=12,
                                                                        xl=3,
                                                                    ),
                                                                    dbc.Col(
                                                                        dbc.Card(
                                                                            dcc.Loading(
                                                                                dcc.Graph(
                                                                                    id="party-voting-pie",
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
                                                                                    id="candidate-voting-trend",
                                                                                    config={
                                                                                        "displayModeBar": False
                                                                                    },
                                                                                ),
                                                                            ),
                                                                        ),
                                                                        sm=12,
                                                                        xxl=5,
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
                                                    dbc.CardHeader("Favorability"),
                                                    dbc.CardBody(
                                                        [
                                                            dbc.Row(
                                                                [
                                                                    dbc.Col(
                                                                        dbc.Card(
                                                                            dcc.Loading(
                                                                                dcc.Graph(
                                                                                    id="candidate-favorability-kpi-card",
                                                                                    config={
                                                                                        "displayModeBar": False
                                                                                    },
                                                                                )
                                                                            ),
                                                                        ),
                                                                        sm=12,
                                                                        xxl=3,
                                                                    ),
                                                                    dbc.Col(
                                                                        dbc.Card(
                                                                            dcc.Loading(
                                                                                dcc.Graph(
                                                                                    id="party-favorability-bar",
                                                                                    config={
                                                                                        "displayModeBar": False
                                                                                    },
                                                                                ),
                                                                            )
                                                                        ),
                                                                        sm=12,
                                                                        xl=4,
                                                                    ),
                                                                    dbc.Col(
                                                                        dbc.Card(
                                                                            dcc.Loading(
                                                                                dcc.Graph(
                                                                                    id="candidate-favorability-trend",
                                                                                    config={
                                                                                        "displayModeBar": False
                                                                                    },
                                                                                ),
                                                                            )
                                                                        ),
                                                                        sm=12,
                                                                        xl=5,
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
                                                                "State Polls"
                                                            ),
                                                            dbc.CardBody(
                                                                [
                                                                    dbc.Row(
                                                                        [
                                                                            dbc.Col(
                                                                                html.P(
                                                                                    "State:"
                                                                                ),
                                                                                sm=1,
                                                                                xxl=1,
                                                                            ),
                                                                            dbc.Col(
                                                                                state_dropdown,
                                                                                sm=11,
                                                                                xxl=3,
                                                                            ),
                                                                        ],
                                                                        style={
                                                                            "padding-top": "10px"
                                                                        },
                                                                    ),
                                                                    dbc.Row(
                                                                        [
                                                                            dbc.Col(
                                                                                [
                                                                                    dbc.Card(
                                                                                        dcc.Loading(
                                                                                            state_table
                                                                                        )
                                                                                    )
                                                                                ],
                                                                                sm=12,
                                                                                xxl=4,
                                                                            ),
                                                                            dbc.Col(
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
                                                                                    )
                                                                                ],
                                                                                sm=12,
                                                                                xxl=8,
                                                                            ),
                                                                        ],
                                                                        style={
                                                                            "padding-top": "10px"
                                                                        },
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
                        label="Current Polling",
                    ),
                    dbc.Tab(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            dbc.Card(
                                                [
                                                    dbc.CardHeader("Instructions"),
                                                    dbc.CardBody(
                                                        [
                                                            dbc.Row(
                                                                [
                                                                    dbc.Col(
                                                                        [
                                                                            dcc.Markdown(
                                                                                """
                                                                                This simulation allows simulation of Trump's winning chances based on different hypothetical scenarios of states won.\
                                                                                Users can select different states to assign to Trump, the Opposition candidate, or random chance between the two.
                                                                                
                                                                                1. Select number of trials to be run (Dropdown Below)
                                                                                2. In the 'Scenario' column of the below table, select the dropdown on a state if you wish to guarantee a win
                                                                                3. Click 'Run Simulation'
                                                                            """
                                                                            )
                                                                        ]
                                                                    ),
                                                                ],
                                                                style={
                                                                    "padding-top": "10px",
                                                                    "padding-bottom": "10px",
                                                                },
                                                            )
                                                        ]
                                                    ),
                                                ]
                                            )
                                        ],
                                        sm=12,
                                        xxl=12,
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
                                                    dbc.CardHeader("Inputs"),
                                                    dbc.CardBody(
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
                                                                                "Run Simulation",
                                                                                id="run-simulation",
                                                                            )
                                                                        ]
                                                                    ),
                                                                ],
                                                                style={
                                                                    "padding-top": "10px",
                                                                    "padding-bottom": "10px",
                                                                },
                                                            ),
                                                            dbc.Row(
                                                                [
                                                                    dbc.Col(
                                                                        [
                                                                            html.Div(
                                                                                states_table
                                                                            ),
                                                                        ],
                                                                        sm=12,
                                                                        xxl=6,
                                                                    )
                                                                ]
                                                            ),
                                                        ]
                                                    ),
                                                ]
                                            )
                                        ],
                                        sm=12,
                                        xxl=12,
                                    )
                                ],
                                style={"padding-top": "10px", "padding-bottom": "10px"},
                            ),
                            dbc.Row(
                                dbc.Col(
                                    dbc.Card(
                                        id="results-card",
                                        children=[
                                            dbc.CardHeader("Results"),
                                            dbc.CardBody(
                                                [
                                                    dbc.Row(
                                                        [
                                                            dbc.Col(
                                                                dbc.Card(
                                                                    html.Div(
                                                                        id="trump-win-pct"
                                                                    )
                                                                )
                                                            ),
                                                            dbc.Col(
                                                                dbc.Card(
                                                                    dcc.Loading(
                                                                        id="loading2",
                                                                        children=[
                                                                            dcc.Graph(
                                                                                id="power-bar",
                                                                                config={
                                                                                    "displayModeBar": False
                                                                                },
                                                                            )
                                                                        ],
                                                                        type="circle",
                                                                    ),
                                                                )
                                                            ),
                                                        ]
                                                    ),
                                                    dbc.Row(
                                                        [
                                                            dbc.Col(
                                                                [
                                                                    dcc.Loading(
                                                                        id="loading3",
                                                                        children=[
                                                                            html.Div(
                                                                                sim_table
                                                                            )
                                                                        ],
                                                                        type="circle",
                                                                    ),
                                                                ]
                                                            )
                                                        ]
                                                    ),
                                                ]
                                            ),
                                        ],
                                        style={"display": "none"},
                                    )
                                )
                            ),
                        ],
                        label="Election Simulation",
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
        Output("date-range", "date"),
        Output("date-range", "max_date_allowed"),
    ],
    Input("interval-component", "n_intervals"),
)
def update(n):
    """
    This function populates data stores and components
    """
    national_avg_poll_df, national_favorability_df, state_polls_df = query.queryData()

    date = datetime.date.today() - datetime.timedelta(days=30)
    max_date_allowed = datetime.date.today()

    return (
        national_avg_poll_df.to_dict("records"),
        national_favorability_df.to_dict("records"),
        state_polls_df.to_dict("records"),
        date,
        max_date_allowed,
    )


@callback(
    [
        Output("candidate-voting-kpi-card", "figure"),
        Output("party-voting-pie", "figure"),
        Output("candidate-voting-trend", "figure"),
        Output("candidate-favorability-kpi-card", "figure"),
        Output("candidate-favorability-trend", "figure"),
        Output("party-favorability-bar", "figure"),
        Output("state-choropleth", "figure"),
        Output("state-table", "data"),
        Output("state-table", "page_current"),
        Output("states-table", "data"),
        Output("states-table", "page_current"),
    ],
    [
        Input("national-average-store", "data"),
        Input("national-favorability-store", "data"),
        Input("state-polls-store", "data"),
        Input("candidate-select", "value"),
        Input("date-range", "date"),
        Input("state-select", "value"),
    ],
)
def update_current_standing_figures(
    national_avg_data,
    national_favorability_data,
    state_poll_data,
    candidate,
    start_date,
    state,
):
    """
    This function generates all visualizations
    :param national_avg_data:
    :param national_favorability_data:
    :param state_poll_data:
    :param candidate:
    :param start_date:
    :return:
    """
    national_avg_poll_df = pd.DataFrame(national_avg_data)
    national_favorability_df = pd.DataFrame(national_favorability_data)
    state_poll_df = pd.DataFrame(state_poll_data)

    candidate_voting_kpi_card = func.candidate_voting_kpi_card(
        national_avg_poll_df, candidate, start_date
    )
    party_voting_pie = func.party_voting_pie(national_avg_poll_df)

    candidate_voting_trend = func.candidate_voting_trend(
        national_avg_poll_df, candidate, start_date
    )

    candidate_favorability_kpi_card = func.candidate_favorability_kpi_card(
        national_favorability_df, candidate, start_date
    )

    candidate_favorability_trend = func.candidate_favorability_trend(
        national_favorability_df, candidate, start_date
    )
    party_favorability_bar = func.party_favorability_stacked_bar(
        national_favorability_df
    )

    state_standing_df = func.state_ranking_df(state_poll_df, state)
    state_leaders_df = func.states_ranking_df(state_poll_df)

    state_standing_map = func.state_standing_map(state_poll_df)

    return (
        candidate_voting_kpi_card,
        party_voting_pie,
        candidate_voting_trend,
        candidate_favorability_kpi_card,
        candidate_favorability_trend,
        party_favorability_bar,
        state_standing_map,
        state_standing_df.to_dict("records"),
        0,
        state_leaders_df.to_dict("records"),
        0,
    )


@callback(
    [
        Output("sim-table", "data"),
        Output("sim-table", "page_current"),
        Output("power-bar", "figure"),
        Output("results-card", "style"),
        Output("trump-win-pct", "children"),
    ],
    [
        Input("trial-count", "value"),
        Input("run-simulation", "n_clicks"),
        Input("states-table", "data"),
    ],
)
def update_sim(n_trials, run_sim, df):
    ctx = callback_context
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]

    hypo_df = pd.DataFrame(df)
    hypo_df = hypo_df[["Code", "Scenario"]]
    hypo_df.set_index("Code", inplace=True)
    hypo_dict = hypo_df.to_dict()

    if input_id == "run-simulation":
        df, trump_win_pct = func.monte_carlo(int(n_trials), hypo_dict["Scenario"])
        power_bar = func.power_bar(df)

        return df.to_dict("records"), 0, power_bar, {"display": "block"}, trump_win_pct
    else:
        return no_update, no_update, no_update, no_update, no_update
