from dash import dcc, html

import dash_bootstrap_components as dbc

from dashboard.elections.layouts.polling_tab_layout import polling_tab
from dashboard.elections.layouts.political_power_layout import political_power_tab
from dashboard.elections.layouts.election_sim_layout import election_sim_tab


election_dashboard_layout = dcc.Loading(
    html.Div(
        [
            dcc.Store(id="national-average-store"),
            dcc.Store(id="national-favorability-store"),
            dcc.Store(id="state-polls-store"),
            html.H2(
                "2024 Presidential Election",
            ),
            dbc.Tabs([polling_tab, political_power_tab, election_sim_tab]),
        ]
    )
)
