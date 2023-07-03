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
        dbc.Accordion(
            [
                dbc.AccordionItem(
                    [
                        dbc.Row(
                            dbc.Col(
                                dbc.Card(
                                    children=[
                                        dbc.CardHeader(
                                            "Calculating the Banzhaf Power Index"
                                        ),
                                        dbc.CardBody(
                                            [
                                                dbc.Row(
                                                    dbc.Col(
                                                        [
                                                            dcc.Markdown(
                                                                """
                                                                         1. List all winning coalitions.
                                                                         2. In each coalition, identify the players who are critical.
                                                                         3. Count up how many times each player is critical. This number is called the player's Banzhaf score (also called the critical count).
                                                                         4. Add the Banzhaf scores of all players together, to find the total number of times any player is critical. This number is called the total power score.
                                                                         5. Convert the Banzhaf score of each player to a fraction or decimal by dividing it by the total power score. This number is the player's Banzhaf power index. It can be expressed as a fraction, decimal, or percent.
                                                                         
                                                                         
                                                                         
                                                                         For the US General Election, the quota will be 270 electoral votes and the weight will be each state's number of electoral votes 
                                                                         
                                                                         https://mathbooks.unl.edu/Contemporary/sec-6-1-banzhaf.html
                                                                         """
                                                            )
                                                        ],
                                                        sm=12,
                                                        xxl=8,
                                                    )
                                                ),
                                            ]
                                        ),
                                    ],
                                )
                            )
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Card(
                                        children=[
                                            dbc.CardHeader(
                                                "US General Election Banzhaf Power Index"
                                            ),
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
                            ],
                            style={"padding-top": "10px"},
                        ),
                    ],
                    title="General Election - Banzhaf Power Index",
                    item_id="general-election",
                ),
                dbc.AccordionItem(
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
                    title="Republican Primary Election - Monte Carlo",
                    id="primary-election",
                ),
            ],
            active_item="general-election",
            style={"padding-top": "10px"},
            flush=True,
        )
    ],
    label="Political Power Simulation",
)
