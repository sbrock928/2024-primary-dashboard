import dash_bootstrap_components as dbc
from dash import html, dash_table, dcc

simulation_power_table = dash_table.DataTable(
    id="simulation-power-table",
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

banzhaf_power_table = dash_table.DataTable(
    id="banzhaf-power-table",
    columns=[
        {"name": "State", "id": "State"},
        {"name": "Electoral Votes", "id": "Electoral Votes"},
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

political_power_tab = dbc.Tab(
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
            dbc.Col(
                dbc.Card(
                    children=[
                        dbc.CardHeader("General Election Power"),
                        dbc.CardBody(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                dbc.Card(
                                                    dcc.Loading(
                                                        children=[
                                                            html.Div(
                                                                banzhaf_power_table
                                                            )
                                                        ],
                                                        type="circle",
                                                    ),
                                                )
                                            ],
                                            sm=12,
                                            xxl=8,
                                        ),
                                        dbc.Col(
                                            [
                                                dbc.Card(
                                                    dcc.Loading(
                                                        children=[
                                                            dcc.Graph(
                                                                id="banzhaf-power-bar",
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
                                            xxl=4,
                                        ),
                                    ]
                                ),
                            ]
                        ),
                    ],
                )
            )
        ),
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    id="results-card-state-power",
                    children=[
                        dbc.CardHeader("Results"),
                        dbc.CardBody(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                dcc.Dropdown(
                                                    id="trial-count-political-power",
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
                                                    id="run-simulation-political-power",
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
                                                dbc.Card(
                                                    dcc.Loading(
                                                        children=[
                                                            html.Div(
                                                                simulation_power_table
                                                            )
                                                        ],
                                                        type="circle",
                                                    ),
                                                )
                                            ],
                                            sm=12,
                                            xxl=8,
                                        ),
                                        dbc.Col(
                                            [
                                                dbc.Card(
                                                    dcc.Loading(
                                                        children=[
                                                            dcc.Graph(
                                                                id="simulation-power-bar",
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
                                            xxl=4,
                                        ),
                                    ]
                                ),
                            ]
                        ),
                    ],
                )
            )
        ),
    ],
    label="Political Power Simulation",
)
