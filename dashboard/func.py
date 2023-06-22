import plotly.express as px
from collections import OrderedDict
from random import randint
import pandas as pd
import plotly.graph_objects as go
import datetime


def state_standing_map(df):
    df["start_date"] = pd.to_datetime(df["start_date"])
    # df = df.loc[df.groupby('Code')['candidate_name'].start_date.idxmax()]
    df = df.loc[df.groupby(["Code", "candidate_name"]).start_date.idxmax()].sort_values(
        ["pct"], ascending=True
    )
    df["max"] = df.groupby("Code")["pct"].transform("max")
    # df_new = df.loc[df.groupby(['Code','candidate_name'])

    print(df[df["Code"] == "TX"].to_string())

    # df.groupby(['Sex', 'Age_Group'])[metric].count().reset_index()

    # df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_us_ag_exports.csv')

    for col in df.columns:
        df[col] = df[col].astype(str)

    # fig = go.Figure(data=go.Choropleth(
    #     locations=df['Code'],
    #     z=df['pct'].astype(float),
    #     locationmode='USA-states',
    #     colorscale='Reds',
    #     autocolorscale=False,
    #     text=df['candidate_name'],
    #     marker_line_color='white',  # line markers between states
    #     colorbar_title="State Polls"
    # ))
    # fig.update_layout(
    #     title_text='2011 US Agriculture Exports by State<br>(Hover for breakdown)',
    #     geo=dict(
    #         scope='usa',
    #         projection=go.layout.geo.Projection(type='albers usa'),
    #         showlakes=True,  # lakes
    #         lakecolor='rgb(255, 255, 255)'),
    # )

    fig = px.choropleth(
        df,
        locationmode="USA-states",
        locations="Code",
        color="candidate_name",
        hover_data=["pct"],
    )
    fig.update_geos(fitbounds="locations")

    return fig


def national_average_trend(df):
    df["date"] = pd.to_datetime(df["date"])
    # fig = px.line(df, x="date", y="pct_estimate", color= 'candidate', title='Life expectancy in Canada', markers = True)
    fig = px.scatter(
        df,
        x="date",
        y="pct_estimate",
        color="candidate",
        trendline="rolling",
        trendline_options=dict(window=5),
    )

    return fig


def national_favorability_trend(df):
    df["start_date"] = pd.to_datetime(df["start_date"])
    # fig = px.line(df, x="date", y="pct_estimate", color= 'candidate', title='Life expectancy in Canada', markers = True)
    fig = px.line(
        df, x="start_date", y="favorable", color="politician", title="Historical"
    )

    return fig


def national_favorability_stacked_bar(df):
    df["start_date"] = pd.to_datetime(df["start_date"])
    df = df.loc[df.groupby(["politician"]).start_date.idxmax()]

    print(df.to_string())

    fig = px.bar(
        df,
        y="politician",
        x=[
            "very_favorable",
            "somewhat_favorable",
            "somewhat_unfavorable",
            "very_unfavorable",
        ],
        # x="politician",
        # y=["very_favorable", "somewhat_favorable", "somewhat_unfavorable", "very_unfavorable"],
        title="Current",
        orientation="h",
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
