import dash_bootstrap_components as dbc
from dash import html, dash_table, dcc


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

sim_table = dash_table.DataTable(
    id="sim-table",
    columns=[
        {"name": "State", "id": "State"},
        {"name": "Delegates", "id": "Delegates"},
        {"name": "Winning Coalition Count", "id": "Winning Coalition Count"},
        {
            "name": "Winning Coalition Pct",
            "id": "Winning Coalition Pct",
            "type": "numeric",
            "format": dash_table.FormatTemplate.percentage(2),
        },
        {
            "name": "Power",
            "id": "Power",
            "type": "numeric",
            "format": dash_table.FormatTemplate.percentage(2),
        },
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

election_sim_tab = dbc.Tab(
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
                                                                                This is a simulation of Trump's winning chances based on different hypothetical scenarios of states won.\
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
                                                        html.Div(states_table),
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
                                            [
                                                dbc.Card(
                                                    [
                                                        html.Div(
                                                            [
                                                                html.H4(
                                                                    "Trump Est. Winning Pct.",
                                                                    style={
                                                                        "text-align": "center",
                                                                        "vertical-align": "middle",
                                                                    },
                                                                ),
                                                                html.H5(
                                                                    id="trump-win-pct",
                                                                    style={
                                                                        "text-align": "center",
                                                                        "vertical-align": "middle",
                                                                    },
                                                                ),
                                                            ],
                                                            style={
                                                                "text-align": "center",
                                                                "position": "absolute",
                                                                "top": "50%",
                                                                "left": 0,
                                                                "right": 0,
                                                            },
                                                        ),
                                                    ],
                                                    style={"height": "100%"},
                                                )
                                            ],
                                            sm=12,
                                            xxl=3,
                                        ),
                                        dbc.Col(
                                            [
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
                                            ],
                                            sm=12,
                                            xxl=9,
                                        ),
                                    ]
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                dcc.Loading(
                                                    id="loading3",
                                                    children=[html.Div(sim_table)],
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
)
