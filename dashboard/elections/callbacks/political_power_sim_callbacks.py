from typing import Any, Tuple, List, Dict

import plotly.express as px
from dash import Input, Output, callback_context, no_update, Dash

from dashboard.elections import func
from dashboard.elections.constants import electoral_votes


def register_callbacks(app: Dash) -> None:
    @app.callback(
        [
            Output("banzhaf-power-bar", "figure"),
            Output("banzhaf-power-table", "data"),
            Output("banzhaf-power-table", "page_current"),
            Output("simulation-power-bar", "figure"),
            Output("simulation-power-table", "data"),
            Output("simulation-power-table", "page_current"),
        ],
        [
            Input("trial-count-political-power", "value"),
            Input("run-simulation-political-power", "n_clicks"),
        ],
    )
    def update_political_power_simulation_figures(
        n_trials: int, run_sim: int
    ) -> Tuple[px.bar, List[Dict[Any, Any]], int, px.bar, List[Dict[Any, Any]], int]:
        """
        This callback updates all visualizations on the "Election Simulation" tab.

        inputs:
            trial-count-political-power | n_trials - int : Number of simulation trials to run
            run-simulation-political-power | n_clicks - int: Number of times the button has been pressed


        returns:
            banzhaf-power-bar | figure: A bar graph of each state's political power in the general election
            banzhaf-power-table | data list(dict): Records containing each states banzhaf results
            banzhaf-power-table | page_current int: Return 0 to reset table to first page upon update
            simulation-power-bar | figure: A bar graph of each state's political power
            simulation-power-table | data list(dict): Records containing each states simulation results
            simulation-power-table | page_current int: Return 0 to reset table to first page upon update
        """

        ctx = callback_context
        input_id = ctx.triggered[0]["prop_id"].split(".")[0]

        # Callback triggered by button click - return monte carlo results only
        if input_id == "run-simulation-political-power":
            results_df = func.primary_election_power_monte_carlo(
                int(n_trials),
            )
            power_bar = func.political_power_bar(results_df)
            return (
                no_update,
                no_update,
                no_update,
                power_bar,
                results_df.to_dict("records"),
                0,
            )

        # Callback triggered by selecting trial # in dropdown -- do nothing
        elif input_id == "trial-count-political-power":
            return no_update, no_update, no_update, no_update, no_update, no_update

        # Callback triggered by initial load -- populate everything
        else:
            # Calculate Banzhaf PI for general election and create visualization
            power_df = func.banzhaf(electoral_votes, 270)
            ge_power_bar = func.political_power_bar(power_df)

            # Run Primary election monte carlo and create visualization
            results_df = func.primary_election_power_monte_carlo(
                int(n_trials),
            )
            power_bar = func.political_power_bar(results_df)

            return (
                ge_power_bar,
                power_df.to_dict("records"),
                0,
                power_bar,
                results_df.to_dict("records"),
                0,
            )
