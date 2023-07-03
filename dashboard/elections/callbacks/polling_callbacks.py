import datetime
from typing import Any, Dict, List, Tuple

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, Dash

from dashboard.elections import func


def register_callbacks(app: Dash) -> None:
    @app.callback(
        [
            Output("candidate-voting-kpi-card", "figure"),
            Output("party-voting-pie", "figure"),
            Output("candidate-voting-trend", "figure"),
            Output("candidate-favorability-kpi-card", "figure"),
            Output("candidate-favorability-trend", "figure"),
            Output("party-favorability-bar", "figure"),
        ],
        [
            Input("national-average-store", "data"),
            Input("national-favorability-store", "data"),
            Input("candidate-select", "value"),
            Input("date-range", "date"),
        ],
    )
    def update_national_polling_figures(
        national_avg_data: List[Dict[Any, Any]],
        national_favorability_data: List[Dict[Any, Any]],
        candidate: str,
        start_date: datetime.date,
    ) -> Tuple[go.Figure, go.Figure, go.Figure, go.Figure, go.Figure, px.bar,]:
        """
        This callback updates all visualizations on the 'Current Polling' tab

        inputs:
            national-average-store | national_avg_data - list(dict) : A dictionary of national polling averages
            national-favorability-store | national_favorability_data - list(dict) : A dictionary of national candidate favorability polls
            candidate-select | value -  str: Candidate selected in dropdown component
            date-range  | start_date - datetime: Start date selected by user in dropdown component
            state-select | state - datetime: State selected by user in dropdown

        returns:
            candidate-voting-kpi-card | figure: A KPI card containing the candidate's current position and vote %
            party-voting-pie | figure: A pie chart of the entire field's vote %
            candidate-voting-trend | figure: A historical line graph containing the actual poll data and a rolling average
            candidate-favorability-kpi-card | figure: A KPI card containing the canddiate's current favorability and unfavorability data
            candidate-favorability-trend | figure: A line graph containing the average favorable v unfavorable for the candidate
            party-favorability-bar | figure: A stacked bar chart of the entire field's favorability and unfavorability

        """

        # Create dataframe(s) from store data
        national_avg_poll_df = pd.DataFrame(national_avg_data)
        national_favorability_df = pd.DataFrame(national_favorability_data)

        # Convert date column(s) to datetime
        national_avg_poll_df["Date"] = pd.to_datetime(
            national_avg_poll_df["Date"], utc=False
        )
        national_favorability_df["Date"] = pd.to_datetime(
            national_favorability_df["Date"], utc=False
        )

        # Create visualizations
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
        return (
            candidate_voting_kpi_card,
            party_voting_pie,
            candidate_voting_trend,
            candidate_favorability_kpi_card,
            candidate_favorability_trend,
            party_favorability_bar,
        )

    @app.callback(
        [
            Output("state-choropleth", "figure"),
            Output("state-poll-table", "data"),
            Output("state-poll-table", "page_current"),
        ],
        [
            Input("state-polls-store", "data"),
            Input("state-select", "value"),
        ],
    )
    def update_state_polling_figures(
        state_poll_data: List[Dict[Any, Any]],
        state: str,
    ) -> Tuple[px.choropleth, List[Dict[Any, Any]], int,]:
        """
        This callback updates all state polling visualizations on the 'Current Polling' tab

        inputs:
            state-polls-store | state_poll_data - list(dict) : A dictionary of state polling data
            state-select | state - datetime: State selected by user in dropdown

        returns:
            state-choropleth | figure: A map showing each state's current poll leader
            state-table | data list(dict): Records containing the selected states current polling
            state-table | page_current int: Return 0 to reset table to first page upon state change

        """
        # Create dataframe(s) from store data
        state_poll_df = pd.DataFrame(state_poll_data)

        # Convert date column(s) to datetime
        state_poll_df["Date"] = pd.to_datetime(state_poll_df["Date"], utc=False)

        # Create visualizations
        state_standing_df = func.state_ranking_df(state_poll_df, state)
        state_standing_map = func.state_standing_map(state_poll_df)

        return (
            state_standing_map,
            state_standing_df.to_dict("records"),
            0,
        )
