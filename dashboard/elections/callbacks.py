from dash import Input, Output, callback_context, no_update, Dash


import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import datetime

from dashboard.elections import func, query
from dashboard.elections.constants import electoral_votes, electoral_state_order

from typing import Any, Dict, List, Tuple


def get_callbacks(app: Dash) -> None:
    @app.callback(
        [
            Output("national-average-store", "data"),
            Output("national-favorability-store", "data"),
            Output("state-polls-store", "data"),
            Output("date-range", "date"),
            Output("date-range", "max_date_allowed"),
        ],
        Input("interval-component", "n_intervals"),
    )
    def update_data_stores(
        n: int,
    ) -> Tuple[
        List[Dict[Any, Any]],
        List[Dict[Any, Any]],
        List[Dict[Any, Any]],
        datetime.date,
        datetime.date,
    ]:
        """
        This callback populates the 3 data stores with polling data

        inputs:
            n (int): Number of intervals from the interval component

        returns:
            national-average-store | data - list(dict) : A list of dictionaries of national polling averages
            national-favorability-store | data - list(dict) : A list of dictionaries of national candidate favorability polls
            state-polls-store | data - list(dict) : A list of dictionaries of state polling data
            date-range  | date - datetime: 30 days prior to today
            date-range | max_date_allowed - datetime: Today's date

        """
        (
            national_avg_poll_df,
            national_favorability_df,
            state_polls_df,
        ) = query.query_data()

        date = datetime.date.today() - datetime.timedelta(days=30)
        max_date_allowed = datetime.date.today()

        return (
            national_avg_poll_df.to_dict("records"),
            national_favorability_df.to_dict("records"),
            state_polls_df.to_dict("records"),
            date,
            max_date_allowed,
        )

    @app.callback(
        [
            Output("candidate-voting-kpi-card", "figure"),
            Output("party-voting-pie", "figure"),
            Output("candidate-voting-trend", "figure"),
            Output("candidate-favorability-kpi-card", "figure"),
            Output("candidate-favorability-trend", "figure"),
            Output("party-favorability-bar", "figure"),
            Output("state-choropleth", "figure"),
            Output("state-poll-table", "data"),
            Output("state-poll-table", "page_current"),
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
    def update_current_polling_figures(
        national_avg_data: List[Dict[Any, Any]],
        national_favorability_data: List[Dict[Any, Any]],
        state_poll_data: List[Dict[Any, Any]],
        candidate: str,
        start_date: datetime.date,
        state: str,
    ) -> Tuple[
        go.Figure,
        go.Figure,
        go.Figure,
        go.Figure,
        go.Figure,
        px.bar,
        px.choropleth,
        List[Dict[Any, Any]],
        int,
        List[Dict[Any, Any]],
        int,
    ]:
        """
        This callback updates all visualizations on the 'Current Polling' tab

        inputs:
            national-average-store | national_avg_data - list(dict) : A dictionary of national polling averages
            national-favorability-store | national_favorability_data - list(dict) : A dictionary of national candidate favorability polls
            state-polls-store | state_poll_data - list(dict) : A dictionary of state polling data
            candidate | value -  str: Candidate selected in dropdown component
            date-range  | start_date - datetime: Start date selected by user in dropdown component
            state-select | state - datetime: State selected by user in dropdown

        returns:
            candidate-voting-kpi-card | figure: A KPI card containing the candidate's current position and vote %
            party-voting-pie | figure: A pie chart of the entire field's vote %
            candidate-voting-trend | figure: A historical line graph containing the actual poll data and a rolling average
            candidate-favorability-kpi-card | figure: A KPI card containing the canddiate's current favorability and unfavorability data
            candidate-favorability-trend | figure: A line graph containing the average favorable v unfavorable for the candidate
            party-favorability-bar | figure: A stacked bar chart of the entire field's favorability and unfavorability
            state-choropleth | figure: A map showing each state's current poll leader
            state-table | data list(dict): Records containing the selected states current polling
            state-table | page_current int: Return 0 to reset table to first page upon state change
            states-table | data list(dict): Records containing each state, it's leading candidate and their current vote %
            states-table | page_current int: Return 0 to reset table to first page upon update
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

    @app.callback(
        [
            Output("power-bar-ge-banzhaf", "figure"),
            Output("ge-banzhaf-power-sim-table", "data"),
            Output("ge-banzhaf-power-sim-table", "page_current"),
            Output("power-bar-state-power", "figure"),
            Output("political-power-sim-table", "data"),
            Output("political-power-sim-table", "page_current"),
        ],
        [
            Input("trial-count-state-power", "value"),
            Input("run-simulation-state-power", "n_clicks"),
        ],
    )
    def update_political_power_simulation_figures(
        n_trials: int, run_sim: int
    ) -> Tuple[px.bar, Any, int, px.bar, Any, int]:
        """
        This callback updates all visualizations on the "Election Simulation" tab.

        inputs:
            trial-count-state-power | n_trials - int : Number of simulation trials to run
            run-simulation-state-power | n_clicks - int: Number of times the button has been pressed


        returns:
            power-bar-ge-banzhaf | figure: A bar graph of each state's political power in the general election
            ge-political-power-sim-table | data list(dict): Records containing each states banzhaf results
            ge-political-power-sim-table | page_current int: Return 0 to reset table to first page upon update
            power-bar-state-power | figure: A bar graph of each state's political power
            political-power-sim-table | data list(dict): Records containing each states simulation results
            political-power-sim-table | page_current int: Return 0 to reset table to first page upon update
        """

        ctx = callback_context
        input_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if input_id == "run-simulation-state-power":
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
        elif input_id == "trial-count-state-power":
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

    @app.callback(
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
    def update_election_simulation_figures(
        n_trials: int, run_sim: int, df: pd.DataFrame
    ) -> Tuple[Any, int, px.bar, Dict[Any, Any], str]:
        """
        This callback updates all visualizations on the "Election Simulation" tab.

        inputs:
            trial-count | n_trials - int : Number of simulation trials to run
            run-simulation | n_clicks - int: Number of times the button has been pressed
            states-table | df: A dataframe containing the state hypo data.


        returns:
            sim-table | data list(dict): Records containing each states simulation results
            sim-table | page_current int: Return 0 to reset table to first page upon update
            power-bar | figure: A bar graph of each state's political power
            results-card | style: Show/hide the bottom card
            trump-win-pct | children: A card showing Trump's calculated win percentage
        """

        ctx = callback_context
        input_id = ctx.triggered[0]["prop_id"].split(".")[0]

        hypo_df = pd.DataFrame(df)
        hypo_df = hypo_df[["Code", "Scenario"]]
        hypo_df.set_index("Code", inplace=True)
        hypo_dict = hypo_df.to_dict()

        if input_id == "run-simulation":
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
