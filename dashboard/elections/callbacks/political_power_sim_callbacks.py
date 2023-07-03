from dash import Input, Output, callback_context, no_update, Dash


import pandas as pd

import plotly.express as px


from dashboard.elections import func
from dashboard.elections.constants import electoral_votes, electoral_state_order

from typing import Any, Tuple, List, Dict


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
        elif input_id == "trial-count-political-power":
            return no_update, no_update, no_update, no_update, no_update, no_update
        else:
            banzhaf_index = func.banzhaf(electoral_votes, 270)
            general_election_power = {}
            for i in range(len(banzhaf_index)):
                general_election_power[electoral_state_order[i]] = {
                    "Electoral Votes": electoral_votes[i],
                    "Power": banzhaf_index[i],
                }

            ge_power_df = pd.DataFrame.from_dict(general_election_power, orient="index")
            ge_power_df.reset_index(inplace=True)
            ge_power_df.rename(columns={"index": "State", 0: "Power"}, inplace=True)
            ge_power_df.sort_values(by="Power", ascending=False, inplace=True)
            ge_power_bar = func.political_power_bar(ge_power_df)

            results_df = func.primary_election_power_monte_carlo(
                int(n_trials),
            )
            power_bar = func.political_power_bar(results_df)

            return (
                ge_power_bar,
                ge_power_df.to_dict("records"),
                0,
                power_bar,
                results_df.to_dict("records"),
                0,
            )
