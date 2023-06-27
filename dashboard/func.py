import plotly.express as px
from collections import OrderedDict
from random import randint
import pandas as pd
import plotly.graph_objects as go


color_mapping_dict = dict(
    Trump="red",
    DeSantis="blue",
    Pence="green",
    Haley="goldenrod",
    Scott="magenta",
    Hutchinson="purple",
    Ramaswamy="yellow",
    Burgum="orange",
    Christie="teal",
    Undecided="gray",
)


def state_standing_map(df):

    """
    This function calculates the current leader of each state
    :param df: Dataframe consisting of state polling data
    :return: Choropleth graph of current state poll leader
    """

    df["Date"] = pd.to_datetime(df["Date"], utc=False)

    df = df.loc[df.groupby(["Code", "Candidate"]).Date.idxmax()].sort_values(
        ["Percentage"], ascending=False
    )
    df["max"] = df.groupby("Code")["Percentage"].transform("max")
    winner = df.groupby("Code").apply(lambda x: x.loc[x["max"].idxmax(), "Candidate"])
    winner.name = "Winner"
    df = df.merge(winner, how="left", left_on="Code", right_on="Code")

    for col in df.columns:
        df[col] = df[col].astype(str)

    fig = px.choropleth(
        df,
        locationmode="USA-states",
        locations="Code",
        color="Winner",
        hover_data=["Percentage"],
    )

    fig.update_geos(fitbounds="locations")

    return fig


def candidate_voting_trend(df, candidate, start_date):

    """
    This function creates a historical line graph of candidate vote pct.
    :param df: A dataframe consisting of national average poll data
    :param candidate: A list of candidates
    :param start_date: A date
    :return: A line graph
    """
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


def candidate_favorability_trend(df, candidate, start_date):
    """
     This function creates a historical line graph of candidate favorability vs unfavorability.
    :param df: A dataframe of favorability polls
    :param candidate: A string representing a candidate
    :param start_date: A date
    :return: A line graph
    """
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


def party_favorability_stacked_bar(df):
    """

    :param df: A dataframe of favorability polls
    :return: A bar chart of all candidate's favorability
    """
    df["Date"] = pd.to_datetime(df["Date"], utc=False)

    df = df.loc[df.groupby(["Candidate"]).Date.idxmax()]

    fig = px.bar(
        df,
        y="Candidate",
        x=[
            "Very Favorable",
            "Somewhat Favorable",
            "Somewhat Unfavorable",
            "Very Unfavorable",
        ],
        title="Favorability (Entire Party)",
        orientation="h",
        text_auto=True,
        color_discrete_map={
            "Very Unfavorable": "red",
            "Very Favorable": "green",
            "Somewhat Unfavorable": "Orange",
            "Somewhat Favorable": "yellow",
        },
    )

    fig.update_layout(legend_title="")

    return fig


def party_voting_pie(df):
    """
    This function creates a pie chart of the current standing of all republican candidates

    :param df: Pandas dataframe containing historical national average standings for each candidate
    :return: Pie chart of current standings

    """

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


def candidate_favorability_kpi_card(df, candidate, start_date):
    """

    :param df: A dataframe of favorability polls
    :param candidate: A string representing a candidate
    :param start_date: A date
    :return: a KPI card for candidate favorability
    """
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
            title={"text": "Favorable"},
        )
    )
    fig.add_trace(
        go.Indicator(
            mode="number+delta",
            value=current_result["Unfavorable"],
            delta={"position": "right", "reference": past_result["Unfavorable"]},
            domain={"x": [0, 1], "y": [0, 0.5]},
            title={"text": "Unfavorable"},
        )
    )

    return fig


def candidate_voting_kpi_card(df, candidate, start_date):
    """

    :param df: A dataframe of national polling info
    :param candidate: A string representing a candidate
    :param start_date: A date
    :return: A kpi card representing a candidate's projected votes
    """
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
            delta={"position": "right", "reference": past_pct},
            domain={"x": [0, 1], "y": [0, 0.5]},
            title={"text": "Vote"},
        )
    )

    return fig


def power_bar(df):
    fig = px.bar(
        df,
        y="Winning Coalition Count",
        x="State",
    )

    return fig


def monte_carlo(n_trials):
    states = OrderedDict()
    red_states = OrderedDict()

    # Initialize States and Delegate Counts
    states["IA"] = {"Delegates": 30, "Winning Coalition Count": 0}
    states["NH"] = {"Delegates": 23, "Winning Coalition Count": 0}
    states["SC"] = {"Delegates": 50, "Winning Coalition Count": 0}
    states["NV"] = {"Delegates": 30, "Winning Coalition Count": 0}
    states["VA"] = {"Delegates": 49, "Winning Coalition Count": 0}
    states["VT"] = {"Delegates": 16, "Winning Coalition Count": 0}
    states["TX"] = {"Delegates": 155, "Winning Coalition Count": 0}
    states["TN"] = {"Delegates": 58, "Winning Coalition Count": 0}
    states["OK"] = {"Delegates": 43, "Winning Coalition Count": 0}
    states["MN"] = {"Delegates": 38, "Winning Coalition Count": 0}
    states["MA"] = {"Delegates": 43, "Winning Coalition Count": 0}
    states["GA"] = {"Delegates": 76, "Winning Coalition Count": 0}
    states["AR"] = {"Delegates": 40, "Winning Coalition Count": 0}
    states["AK"] = {"Delegates": 28, "Winning Coalition Count": 0}
    states["AL"] = {"Delegates": 50, "Winning Coalition Count": 0}
    states["ME"] = {"Delegates": 23, "Winning Coalition Count": 0}
    states["LA"] = {"Delegates": 46, "Winning Coalition Count": 0}
    states["KY"] = {"Delegates": 46, "Winning Coalition Count": 0}
    states["KS"] = {"Delegates": 40, "Winning Coalition Count": 0}
    states["PR"] = {"Delegates": 23, "Winning Coalition Count": 0}
    states["MS"] = {"Delegates": 40, "Winning Coalition Count": 0}
    states["MI"] = {"Delegates": 59, "Winning Coalition Count": 0}
    states["ID"] = {"Delegates": 32, "Winning Coalition Count": 0}
    states["HI"] = {"Delegates": 19, "Winning Coalition Count": 0}
    states["VI"] = {"Delegates": 9, "Winning Coalition Count": 0}
    states["DC"] = {"Delegates": 19, "Winning Coalition Count": 0}
    states["GU"] = {"Delegates": 9, "Winning Coalition Count": 0}
    states["OH"] = {"Delegates": 66, "Winning Coalition Count": 0}
    states["MP"] = {"Delegates": 9, "Winning Coalition Count": 0}
    states["NC"] = {"Delegates": 72, "Winning Coalition Count": 0}
    states["MO"] = {"Delegates": 52, "Winning Coalition Count": 0}
    states["IL"] = {"Delegates": 69, "Winning Coalition Count": 0}
    states["FL"] = {"Delegates": 99, "Winning Coalition Count": 0}
    states["UT"] = {"Delegates": 40, "Winning Coalition Count": 0}
    states["AZ"] = {"Delegates": 58, "Winning Coalition Count": 0}
    states["AS"] = {"Delegates": 9, "Winning Coalition Count": 0}
    states["ND"] = {"Delegates": 28, "Winning Coalition Count": 0}
    states["WI"] = {"Delegates": 42, "Winning Coalition Count": 0}
    states["CO"] = {"Delegates": 37, "Winning Coalition Count": 0}
    states["WY"] = {"Delegates": 29, "Winning Coalition Count": 0}
    states["NY"] = {"Delegates": 95, "Winning Coalition Count": 0}
    states["RI"] = {"Delegates": 19, "Winning Coalition Count": 0}
    states["PA"] = {"Delegates": 71, "Winning Coalition Count": 0}
    states["MD"] = {"Delegates": 38, "Winning Coalition Count": 0}
    states["DE"] = {"Delegates": 16, "Winning Coalition Count": 0}
    states["CT"] = {"Delegates": 28, "Winning Coalition Count": 0}
    states["IN"] = {"Delegates": 57, "Winning Coalition Count": 0}
    states["WV"] = {"Delegates": 34, "Winning Coalition Count": 0}
    states["NE"] = {"Delegates": 36, "Winning Coalition Count": 0}
    states["OR"] = {"Delegates": 28, "Winning Coalition Count": 0}
    states["WA"] = {"Delegates": 44, "Winning Coalition Count": 0}
    states["CA"] = {"Delegates": 172, "Winning Coalition Count": 0}
    states["MT"] = {"Delegates": 27, "Winning Coalition Count": 0}
    states["NJ"] = {"Delegates": 51, "Winning Coalition Count": 0}
    states["NM"] = {"Delegates": 24, "Winning Coalition Count": 0}
    states["SD"] = {"Delegates": 29, "Winning Coalition Count": 0}

    # Number of Simulations
    trial_count = n_trials
    for trials in range(0, trial_count):
        redSum = 0
        blueSum = 0

        red_states["IA"] = 0
        red_states["NH"] = 0
        red_states["SC"] = 0
        red_states["NV"] = 0
        red_states["VA"] = 0
        red_states["VT"] = 0
        red_states["TX"] = 0
        red_states["TN"] = 0
        red_states["OK"] = 0
        red_states["MN"] = 0
        red_states["MA"] = 0
        red_states["GA"] = 0
        red_states["AR"] = 0
        red_states["AK"] = 0
        red_states["AL"] = 0
        red_states["ME"] = 0
        red_states["LA"] = 0
        red_states["KY"] = 0
        red_states["KS"] = 0
        red_states["PR"] = 0
        red_states["MS"] = 0
        red_states["MI"] = 0
        red_states["ID"] = 0
        red_states["HI"] = 0
        red_states["VI"] = 0
        red_states["DC"] = 0
        red_states["GU"] = 0
        red_states["OH"] = 0
        red_states["MP"] = 0
        red_states["NC"] = 0
        red_states["MO"] = 0
        red_states["IL"] = 0
        red_states["FL"] = 0
        red_states["UT"] = 0
        red_states["AZ"] = 0
        red_states["AS"] = 0
        red_states["ND"] = 0
        red_states["WI"] = 0
        red_states["CO"] = 0
        red_states["WY"] = 0
        red_states["NY"] = 0
        red_states["RI"] = 0
        red_states["PA"] = 0
        red_states["MD"] = 0
        red_states["DE"] = 0
        red_states["CT"] = 0
        red_states["IN"] = 0
        red_states["WV"] = 0
        red_states["NE"] = 0
        red_states["OR"] = 0
        red_states["WA"] = 0
        red_states["CA"] = 0
        red_states["MT"] = 0
        red_states["NJ"] = 0
        red_states["NM"] = 0
        red_states["SD"] = 0

        # Iterate over each state in order by when they vote
        for state in states:
            # 1237 delegates means we have a nominee
            if redSum < 1237 and blueSum < 1237:
                randomNum = randint(0, 1)
                if randomNum == 0:
                    redSum += states[state]["Delegates"]
                    red_states[state] = 1
                else:
                    blueSum += states[state]["Delegates"]
            else:
                break

        if redSum >= 1237:
            for state in states:
                if red_states[state] == 1:
                    states[state]["Winning Coalition Count"] += 1

    df = pd.DataFrame.from_dict(states, orient="index").sort_values(
        ["Winning Coalition Count"], ascending=False
    )
    df["Winning Coalition Pct"] = (df["Winning Coalition Count"] / trial_count) * 100
    df.reset_index(inplace=True)
    df.rename(columns={"index": "State"}, inplace=True)

    return df
