from typing import Any, Dict, List, Tuple

import pandas as pd
import plotly.express as px
from dash import Input, Output, callback_context, no_update, Dash

from dashboard.elections import func


def register_callbacks(app: Dash) -> None:
    @app.callback(
        [
            Output("state-input-table", "data"),
            Output("state-input-table", "page_current"),
        ],
        Input("state-polls-store", "data"),
    )
    def update_state_input_table(
        state_poll_data: List[Dict[Any, Any]]
    ) -> Tuple[List[Dict[Any, Any]], int]:
        """
        This callback populates the state input table on the 'Election Simulation' tab

        inputs:
            state-polls-store | state_poll_data - list(dict) : A dictionary of state polling data

        returns:
            state-input-table | data list(dict): Records containing each state, it's leading candidate and their current vote %
            state-input-table | page_current int: Return 0 to reset table to first page upon update
        """

        # Create dataframe(s) from store data
        state_poll_df = pd.DataFrame(state_poll_data)

        # Convert date column(s) to datetime
        state_poll_df["Date"] = pd.to_datetime(state_poll_df["Date"], utc=False)

        # Create visualization(s)
        state_leaders_df = func.states_ranking_df(state_poll_df)

        return state_leaders_df.to_dict("records"), 0

    @app.callback(
        [
            Output("simulation-election-table", "data"),
            Output("simulation-election-table", "page_current"),
            Output("simulation-election-bar", "figure"),
            Output("results-card", "style"),
            Output("trump-win-pct", "children"),
        ],
        [
            Input("trial-count-election", "value"),
            Input("run-simulation-election", "n_clicks"),
            Input("state-input-table", "data"),
        ],
    )
    def update_election_simulation_figures(
        n_trials: int, run_sim: int, state_input_df: pd.DataFrame
    ) -> Tuple[List[Dict[Any, Any]], int, px.bar, Dict[Any, Any], str]:
        """
        This callback updates all visualizations on the "Election Simulation" tab.

        inputs:
            trial-count-election | n_trials - int : Number of simulation trials to run
            run-simulation-election | n_clicks - int: Number of times the button has been pressed
            state-input-table | df: A dataframe containing the state hypo data.


        returns:
            simulation-election-table | data list(dict): Records containing each states simulation results
            simulation-election-table | page_current int: Return 0 to reset table to first page upon update
            simulation-election-bar | figure: A bar graph of each state's political power
            results-card | style: Show/hide the bottom card
            trump-win-pct | children: A card showing Trump's calculated win percentage
        """

        ctx = callback_context
        input_id = ctx.triggered[0]["prop_id"].split(".")[0]

        hypo_df = pd.DataFrame(state_input_df)
        hypo_df = hypo_df[["Code", "Scenario"]]
        hypo_df.set_index("Code", inplace=True)
        hypo_dict = hypo_df.to_dict()

        if input_id == "run-simulation-election":
            results_df, trump_win_pct = func.election_simulation_monte_carlo(
                int(n_trials), hypo_dict["Scenario"]
            )
            power_bar = func.political_power_bar(results_df)

            return (
                results_df.to_dict("records"),
                0,
                power_bar,
                {"display": "block"},
                format(trump_win_pct / 100, ".2%"),
            )
        else:
            return no_update, no_update, no_update, no_update, no_update
