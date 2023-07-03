import datetime

import dash_bootstrap_components as dbc
from dash import html, dash_table, dcc

from dashboard.elections.constants import states

date_picker = (
    dcc.DatePickerSingle(id="date-range", min_date_allowed=datetime.date(2023, 3, 1)),
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

state_poll_table = dash_table.DataTable(
    id="state-poll-table",
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

polling_tab = dbc.Tab(
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
                                        dbc.CardHeader("State Polls"),
                                        dbc.CardBody(
                                            [
                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            html.P("State:"),
                                                            sm=1,
                                                            xxl=1,
                                                        ),
                                                        dbc.Col(
                                                            state_dropdown,
                                                            sm=11,
                                                            xxl=3,
                                                        ),
                                                    ],
                                                    style={"padding-top": "10px"},
                                                ),
                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            [
                                                                dbc.Card(
                                                                    dcc.Loading(
                                                                        state_poll_table
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
                                                    style={"padding-top": "10px"},
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
)
