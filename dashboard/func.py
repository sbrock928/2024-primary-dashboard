import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from copy import copy
from random import randint
from dashboard.constants import color_mapping_dict, states, state_order_list
from datetime import datetime, date
from typing import Any, Tuple, List


def state_standing_map(state_poll_df: pd.DataFrame) -> px.bar:
    """
    This function creates a choropleth map displaying the current poll leader in each state

    inputs:
        state_poll_df - dataframe : A dataframe of state poll data

    returns:
        fig | figure: A choropleth map displaying the current poll leader in each state

    """
    df = copy(state_poll_df)

    df["Date"] = pd.to_datetime(df["Date"], utc=False)
    df = df[df["notes"] != "head-to-head poll"]

    df = df.loc[df.groupby(["Code", "Candidate"]).Date.idxmax()].sort_values(
        ["Percentage"], ascending=False
    )

    df.sort_values(["Code", "Percentage"], ascending=[True, True], inplace=True)
    df["shift"] = df.groupby("Code")["Percentage"].shift()
    df["Diff"] = df.groupby(["Code"])["Percentage"].transform(lambda x: x.diff())

    df.sort_values(
        ["Code", "Percentage", "Diff"], ascending=[True, False, True], inplace=True
    )
    df = df[["Code", "Candidate", "Percentage", "Diff"]]
    df = df.groupby("Code").first()
    df.reset_index(inplace=True)

    fig = px.choropleth(
        df,
        locationmode="USA-states",
        locations="Code",
        color="Candidate",
        hover_data=["Percentage"],
    )

    fig.update_geos(fitbounds="locations")

    return fig


def candidate_voting_trend(
    national_avg_poll_df: pd.DataFrame, candidate: str, start_date: date
) -> go.Figure:
    """
    This function creates a historical line graph of candidate vote pct and a 5 day rolling average.

    inputs:
        national_avg_poll_df - dataframe: A dataframe of the national average poll data
        candidate - str: Candidate to filter by
        start_date - datetime: Beginning date of data to plot

    returns:
        fig | figure: A historical line graph of candidate vote pct and a 5 day rolling average.

    """

    df = copy(national_avg_poll_df)

    df["Date"] = pd.to_datetime(df["Date"], utc=False)

    if type(candidate) == str:
        df = df[df["Candidate"] == candidate].sort_values("Date", ascending=True)
    else:
        df = df[df["Candidate"].isin(candidate)].sort_values("Date", ascending=True)

    df["Rolling"] = df.groupby(["Candidate"])["Percentage"].transform(
        lambda x: x.rolling(5).mean()
    )

    df = df[df["Date"] >= (pd.to_datetime(start_date))]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["Percentage"],
            mode="markers",
            name="Historical",
            marker=dict(color=color_mapping_dict[candidate]),
        )
    )
    fig.add_trace(
        go.Line(
            x=df["Date"],
            y=df["Rolling"],
            name="Rolling Avg.",
            line=dict(color=color_mapping_dict[candidate], width=2),
        )
    )
    fig["layout"]["yaxis"].update(autorange=True)

    fig.update_layout(title="Projected Votes (Actual vs Rolling)")
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)

    return fig


def candidate_favorability_trend(
    national_favorability_df: pd.DataFrame, candidate: str, start_date: date
) -> go.Figure:
    """
     This function creates a historical line graph of candidate favorability vs unfavorability.

    inputs:
        national_favorability_df - dataframe: A dataframe of the national favorability poll data
        candidate - str: Candidate to filter by
        start_date - datetime: Beginning date of data to plot

    returns:
        fig | figure: A historical line graph of candidate favorability vs unfavorability.

    """
    df = copy(national_favorability_df)

    df["Date"] = pd.to_datetime(df["Date"], utc=False)
    favorable_df = df.copy()
    unfavorable_df = df.copy()

    favorable_df = (
        favorable_df.groupby(["Candidate", "Date"])["Favorable"]
        .mean()
        .round(2)
        .reset_index()
    )
    unfavorable_df = (
        unfavorable_df.groupby(["Candidate", "Date"])["Unfavorable"]
        .mean()
        .round(2)
        .reset_index()
    )

    favorable_df = favorable_df[favorable_df["Candidate"] == candidate].sort_values(
        "Date", ascending=True
    )
    unfavorable_df = unfavorable_df[
        unfavorable_df["Candidate"] == candidate
    ].sort_values("Date", ascending=True)

    favorable_df["Rolling Favorable"] = favorable_df.groupby(["Candidate"])[
        "Favorable"
    ].transform(lambda x: x.rolling(5).mean())
    unfavorable_df["Rolling Unfavorable"] = unfavorable_df.groupby(["Candidate"])[
        "Unfavorable"
    ].transform(lambda x: x.rolling(5).mean())

    favorable_df = favorable_df[favorable_df["Date"] >= (pd.to_datetime(start_date))]
    unfavorable_df = unfavorable_df[
        unfavorable_df["Date"] >= (pd.to_datetime(start_date))
    ]

    fig = go.Figure()
    fig.add_trace(
        go.Line(
            x=unfavorable_df["Date"],
            y=unfavorable_df["Rolling Unfavorable"],
            name="Unfavorable",
            line=dict(color="red"),
        )
    )
    fig.add_trace(
        go.Line(
            x=favorable_df["Date"],
            y=favorable_df["Rolling Favorable"],
            name="Favorable",
            line=dict(color="blue"),
        )
    )

    fig.update_layout(legend_title="")
    fig.update_layout(title="Favorability vs Unfavorability (Rolling)")
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)

    return fig


def party_favorability_stacked_bar(national_favorability_df: pd.DataFrame) -> px.bar:
    """
    This function creates a stacked bar of favorable vs unfavorable for the entire candidate field

    inputs:
        national_favorability_df - dataframe: A dataframe of the national favorability poll data


    returns:
        fig | figure: A stacked bar of favorable vs unfavorable for the entire candidate field

    """

    df = copy(national_favorability_df)

    df["Date"] = pd.to_datetime(df["Date"], utc=False)
    df.sort_values("Date", inplace=True, ascending=True)

    df = df.loc[df.groupby(["Candidate"]).Date.idxmax()]

    fig = px.bar(
        df,
        y="Candidate",
        x=[
            "Favorable",
            "Unfavorable",
        ],
        title="Favorability (Entire Party)",
        orientation="h",
        text_auto=True,
        color_discrete_map={
            "Unfavorable": "red",
            "Favorable": "blue",
        },
    )

    fig.update_layout(legend_title="")

    return fig


def party_voting_pie(national_avg_poll_df: pd.DataFrame) -> go.Figure:
    """
    This function creates a pie chart of the current standing of all republican candidates

    inputs:
        national_avg_poll_df - dataframe: A dataframe of the national average poll data

    returns:
        fig - figure: A pie chart of current vote % for the entire field

    """

    df = copy(national_avg_poll_df)

    df["Date"] = pd.to_datetime(df["Date"], utc=False)
    df = df.loc[df.groupby(["Candidate"]).Date.idxmax()]

    # Append a row for undecided voters
    df.loc[-1] = ["Undecided", None, (100 - df["Percentage"].sum()), None, None, 2024]

    # go.Pie doesn't accept a dictionary -- colors must be in order of slices
    df.sort_values("Percentage", ascending=False, inplace=True)
    colors_list = []
    for index, row in df.iterrows():
        candidate = row["Candidate"]
        color = color_mapping_dict[candidate]
        colors_list.append(color)

    fig = go.Figure(
        go.Pie(
            name="",
            values=df["Percentage"],
            labels=df["Candidate"],
        )
    )

    fig.update_traces(
        textinfo="percent+label",
        hovertemplate="Candidate:%{label}: <br>Percentage: %{value:.1f}% </br>",
        marker=dict(colors=colors_list),
    )
    fig.update_layout(showlegend=False)
    fig.update_layout(title="Projected Votes (Entire Party)")

    return fig


def candidate_favorability_kpi_card(
    national_favorability_df: pd.DataFrame, candidate: str, start_date: date
) -> go.Figure:
    """
    This function creates the KPI card of candidate favorability data

    inputs:
        national_favorability_df - dataframe: A dataframe of the national favorability poll data
        candidate - str: Candidate to filter by
        start_date - datetime: Beginning date of data to plot

    returns:
        fig - figure: A figure containing a KPI card of acandidate's favorability data
    """

    df = copy(national_favorability_df)
    df["Date"] = pd.to_datetime(df["Date"], utc=False)

    df = df[df["Candidate"] == candidate]

    current_result = df.loc[df.Date.idxmax()]

    past_result = (
        df[df["Date"] >= (pd.to_datetime(start_date))]
        .sort_values("Date", ascending=False)
        .iloc[-1]
    )

    fig = go.Figure()
    fig.add_trace(
        go.Indicator(
            mode="number+delta",
            value=current_result["Favorable"],
            delta={"position": "right", "reference": past_result["Favorable"]},
            domain={"x": [0, 1], "y": [0.5, 1]},
            title={"text": "Favorable %"},
        )
    )
    fig.add_trace(
        go.Indicator(
            mode="number+delta",
            value=current_result["Unfavorable"],
            delta={"position": "right", "reference": past_result["Unfavorable"]},
            domain={"x": [0, 1], "y": [0, 0.5]},
            title={"text": "Unfavorable %"},
        )
    )

    return fig


def candidate_voting_kpi_card(
    national_avg_poll_df: pd.DataFrame, candidate: str, start_date: date
) -> go.Figure:
    """
    This function creates the KPI card of a candidate's vote percent and position in the race

    inputs:
        national_avg_poll_df - dataframe: A dataframe of the national average poll data
        candidate - str: Candidate to filter by
        start_date - datetime: Beginning date of data to plot

    returns:
        fig - figure: A figure containing a KPI card of acandidate's vote and position data
    """

    df = copy(national_avg_poll_df)

    df["Date"] = pd.to_datetime(df["Date"], utc=False)

    current_result = df.copy()
    current_result = current_result[current_result["Date"] == current_result.Date.max()]
    current_result["Rank"] = (
        current_result.sort_values(["Percentage"], ascending=False)
        .groupby(["Candidate"], sort=False)
        .ngroup()
        + 1
    )
    current_result = current_result[current_result["Candidate"] == candidate]
    current_result = current_result.loc[current_result.Date.idxmax()]

    past_result = df.copy()
    past_result = past_result[
        past_result["Date"] >= (pd.to_datetime(start_date))
    ].sort_values("Date", ascending=False)

    past_result = past_result[past_result["Date"] == past_result.Date.min()]
    past_result["Rank"] = (
        past_result.sort_values(["Percentage"], ascending=False)
        .groupby(["Candidate"], sort=False)
        .ngroup()
        + 1
    )
    past_result = past_result[past_result["Candidate"] == candidate]

    past_rank = 0
    past_pct = 0
    if not past_result.empty:
        past_rank = past_result["Rank"].values[0]
        past_pct = past_result["Percentage"].values[0]

    fig = go.Figure()
    fig.add_trace(
        go.Indicator(
            mode="number+delta",
            value=int(current_result["Rank"]),
            domain={"x": [0, 1], "y": [0.5, 1]},
            delta={"reference": past_rank, "position": "right"},
            title={"text": "Position"},
        )
    )

    fig.add_trace(
        go.Indicator(
            mode="number+delta",
            value=current_result["Percentage"],
            delta={"position": "right", "reference": past_pct, "valueformat": ".2f"},
            domain={"x": [0, 1], "y": [0, 0.5]},
            title={"text": "Vote %"},
            number={"valueformat": ".2f"},
        )
    )

    return fig


def state_ranking_df(state_poll_df: pd.DataFrame, state: str) -> pd.DataFrame:
    """
    This function creates a dataframe containing a state's current poll data

    inputs:
        state_poll_df - dataframe: A dataframe of state polling data
        state - str: A state to filter by

    returns:
        df - dataframe: A dataframe containing a state's current poll data
    """

    df = copy(state_poll_df)

    df["Date"] = pd.to_datetime(df["Date"], utc=False)
    df = df[df["notes"] != "head-to-head poll"]
    df = df.loc[df.groupby(["Code", "Candidate"]).Date.idxmax()].sort_values(
        ["Percentage"], ascending=False
    )

    df.sort_values(["Code", "Percentage"], ascending=[True, True], inplace=True)
    df["shift"] = df.groupby("Code")["Percentage"].shift()
    df["Diff"] = df.groupby(["Code"])["Percentage"].transform(lambda x: x.diff())

    df.sort_values(
        ["Code", "Percentage", "Diff"], ascending=[True, False, True], inplace=True
    )
    df = df[["Code", "Candidate", "Percentage", "Diff"]]

    df = df[df["Code"] == state]

    return df


def states_ranking_df(state_poll_df: pd.DataFrame) -> pd.DataFrame:
    """
    This function calculates the current leader of each state

    inputs:
        state_poll_df - dataframe: A dataframe of state polling data

    returns:
        df - dataframe: A dataframe containing the current leader of each state
    """

    df = copy(state_poll_df)

    df["Date"] = pd.to_datetime(df["Date"], utc=False)
    df = df[df["notes"] != "head-to-head poll"]
    df = df.loc[df.groupby(["Code", "Candidate"]).Date.idxmax()].sort_values(
        ["Percentage"], ascending=False
    )

    df.sort_values(["Code", "Percentage"], ascending=[True, True], inplace=True)
    df["shift"] = df.groupby("Code")["Percentage"].shift()
    df["Diff"] = df.groupby(["Code"])["Percentage"].transform(lambda x: x.diff())

    df.sort_values(
        ["Code", "Percentage", "Diff"], ascending=[True, False, True], inplace=True
    )
    df = df[["Code", "Candidate", "Percentage", "Diff"]]
    df["Scenario"] = None

    df = df.groupby("Code").first()

    df2 = pd.DataFrame({"Code": state_order_list}, columns=["Code"])
    new_df = df2.merge(df, how="left", left_on="Code", right_on="Code")

    return new_df


def political_power_bar(results_df: pd.DataFrame) -> px.bar:
    """
    This function creates a bar chart of each state's political power

    inputs:
        results_df - dataframe: A dataframe of simulation results

    returns:
        fig - figure: A bar chart of each state's political power
    """

    df = copy(results_df)
    df.sort_values(by="Power", ascending=True, inplace=True)

    fig = px.bar(df, x="Power", y="State", orientation="h")

    return fig


def ge_political_power_bar(results_df: pd.DataFrame) -> px.bar:
    """
    This function creates a bar chart of each state's political power in the general election

    inputs:
        results_df - dataframe: A dataframe of simulation results

    returns:
        fig - figure: A bar chart of each state's political power
    """

    df = copy(results_df)
    df.sort_values(by="Power", ascending=True, inplace=True)

    fig = px.bar(df, x="Power", y="State", orientation="h")

    return fig


def banzhaf(weight: List[Any], quota: int) -> List[Any]:
    """
    From https://gist.github.com/HeinrichHartmann/8ec2e2245f2a70441257
    """
    max_order = sum(weight)

    polynomial = [1] + max_order * [
        0
    ]  # create a list to hold the polynomial coefficients

    current_order = 0  # compute the polynomial coefficients
    aux_polynomial = polynomial[:]
    for i in range(len(weight)):
        current_order = current_order + weight[i]
        offset_polynomial = weight[i] * [0] + polynomial
        for j in range(current_order + 1):
            aux_polynomial[j] = polynomial[j] + offset_polynomial[j]
        polynomial = aux_polynomial[:]

    banzhaf_power = len(weight) * [
        0
    ]  # create a list to hold the Banzhaf Power for each voter
    swings = quota * [0]  # create a list to compute the swings for each voter

    for i in range(len(weight)):  # compute the Banzhaf Power
        for j in range(quota):  # fill the swings list
            if j < weight[i]:
                swings[j] = polynomial[j]
            else:
                swings[j] = polynomial[j] - swings[j - weight[i]]
        for k in range(weight[i]):  # fill the Banzhaf Power vector
            banzhaf_power[i] = banzhaf_power[i] + swings[quota - 1 - k]

    # Normalize Index
    total_power = float(sum(banzhaf_power))
    banzhaf_index = map(lambda x: x / total_power, banzhaf_power)

    return list(banzhaf_index)


def primary_election_power_monte_carlo(n_trials: int) -> pd.DataFrame:
    """
    This function performs a monte carlo simulation of political power of the republican primary election

    inputs:
        n_trials - int: Numbermn of trials to run in the simulation

    returns:
        results_df - dataframe: A dataframe of simulation results

    """

    states_ordered_dict = copy(states)

    for state in states_ordered_dict:
        states_ordered_dict[state]["Winning Coalition Count"] = 0

    red_team_wins = 0
    blue_team_wins = 0

    # Number of Simulations
    trial_count = n_trials
    for trials in range(0, trial_count):
        red_sum = 0
        blue_sum = 0

        for state in states_ordered_dict:
            states_ordered_dict[state]["Win Tally"] = 0

        # Iterate over each state in order by when they vote
        for state in states_ordered_dict:
            # 1237 delegates means we have a nominee
            if red_sum < 1234 and blue_sum < 1234:
                rand_int = randint(0, 1)

                if rand_int == 0:
                    red_sum += states_ordered_dict[state]["Delegates"]
                    states_ordered_dict[state]["Win Tally"] = 1
                else:
                    blue_sum += states_ordered_dict[state]["Delegates"]
            else:
                break

        if red_sum >= 1234:
            for state in states_ordered_dict:
                if states_ordered_dict[state]["Win Tally"] == 1:
                    states_ordered_dict[state]["Winning Coalition Count"] += 1
            red_team_wins += 1
        else:
            blue_team_wins += 1

    results_df = pd.DataFrame.from_dict(states, orient="index").sort_values(
        ["Winning Coalition Count"], ascending=False
    )
    results_df["Winning Coalition Pct"] = (
        results_df["Winning Coalition Count"] / trial_count
    )
    results_df["Power"] = (
        results_df["Winning Coalition Count"]
        / results_df["Winning Coalition Count"].sum()
    )
    results_df.reset_index(inplace=True)
    results_df.rename(columns={"index": "State"}, inplace=True)

    return results_df


def election_simulation_monte_carlo(
    n_trials: int, hypo_dict: dict[str, Any]
) -> Tuple[pd.DataFrame, float]:
    """
    This function performs a monte carlo simulation of the republican primary election

    inputs:
        n_trials - int: Numbermn of trials to run in the simulation
        hypo_dict - dic: A dictionary containing state hypo data.

    returns:
        df - dataframe: A dataframe of simulation results
        trump_win_pct - float: A percentage of trials won
    """

    states_ordered_dict = copy(states)

    for state in states_ordered_dict:
        states_ordered_dict[state]["Winning Coalition Count"] = 0

    trumpWins = 0
    oppositionWins = 0

    # Number of Simulations
    trial_count = n_trials
    for trials in range(0, trial_count):
        trumpSum = 0
        blueSum = 0

        for state in states_ordered_dict:
            states_ordered_dict[state]["Win Tally"] = 0

        # Iterate over each state in order by when they vote
        for state in states_ordered_dict:
            # 1237 delegates means we have a nominee
            if trumpSum < 1234 and blueSum < 1234:
                randomNum = randint(0, 1)
                scenario = hypo_dict[state]

                if scenario == "Trump":
                    trumpSum += states_ordered_dict[state]["Delegates"]
                    states_ordered_dict[state]["Win Tally"] = 1
                elif scenario == "Opposition":
                    blueSum += states_ordered_dict[state]["Delegates"]
                elif randomNum == 0:
                    trumpSum += states_ordered_dict[state]["Delegates"]
                    states_ordered_dict[state]["Win Tally"] = 1
                else:
                    blueSum += states_ordered_dict[state]["Delegates"]
            else:
                break

        if trumpSum >= 1234:
            for state in states_ordered_dict:
                if states_ordered_dict[state]["Win Tally"] == 1:
                    states_ordered_dict[state]["Winning Coalition Count"] += 1
            trumpWins += 1
        elif blueSum >= 1234:
            oppositionWins += 1

    trump_win_pct = (trumpWins / trial_count) * 100

    df = pd.DataFrame.from_dict(states, orient="index").sort_values(
        ["Winning Coalition Count"], ascending=False
    )
    df["Winning Coalition Pct"] = df["Winning Coalition Count"] / trial_count
    df["Power"] = df["Winning Coalition Count"] / df["Winning Coalition Count"].sum()
    df.reset_index(inplace=True)
    df.rename(columns={"index": "State"}, inplace=True)

    return df, trump_win_pct
