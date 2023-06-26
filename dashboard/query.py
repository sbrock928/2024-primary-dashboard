import pandas as pd
import requests
import io


code = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "District of Columbia": "DC",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
}

candidate_names = {
    "Mike Pence": "Pence",
    "Nikki Haley": "Haley",
    "Ron DeSantis": "DeSantis",
    "Tim Scott": "Scott",
    "T. Scott": "Scott",
    "Donald Trump": "Trump",
    "Asa Hutchinson": "Hutchinson",
    "Vivek G. Ramaswamy": "Ramaswamy",
    "Doug Burgum": "Burgum",
    "Chris Christie": "Christie",
}
import_columns = [
    "candidate",
    "date",
    "pct_estimate",
    "state",
    "pct_trend_adjusted",
    "cycle",
]


def queryData():
    # database query step goes here, importing for CSV for demo purposes

    national_avg_poll_df = pd.read_csv(
        "https://projects.fivethirtyeight.com/polls/data/presidential_primary_averages.csv",
        engine="python",
    )

    national_avg_poll_df = national_avg_poll_df[national_avg_poll_df["cycle"] == 2024]
    national_avg_poll_df = national_avg_poll_df[import_columns]

    national_avg_poll_df.rename(
        columns={
            "candidate": "Candidate",
            "pct_estimate": "Percentage",
            "date": "Date",
        },
        inplace=True,
    )


    national_avg_poll_df["Candidate"] = national_avg_poll_df["Candidate"].replace(
        candidate_names
    )
    national_avg_poll_df = national_avg_poll_df[
        national_avg_poll_df["Candidate"].isin(
            [
                "Pence",
                "Haley",
                "DeSantis",
                "Scott",
                "Trump",
                "Ramaswamy",
                "Hutchinson",
                "Burgum",
                "Christie",
            ]
        )
    ]

    national_favorability_df = pd.read_csv(
        "https://projects.fivethirtyeight.com/polls-page/data/favorability_polls.csv",
        engine="python",
    )
    national_favorability_df.rename(
        columns={
            "politician": "Candidate",
            "favorable": "Favorable",
            "very_favorable": "Very Favorable",
            "somewhat_favorable": "Somewhat Favorable",
            "somewhat_unfavorable": "Somewhat Unfavorable",
            "very_unfavorable": "Very Unfavorable",
            "end_date": "Date",
        },
        inplace=True,
    )

    national_favorability_df["Candidate"] = national_favorability_df[
        "Candidate"
    ].replace(candidate_names)
    national_favorability_df = national_favorability_df[
        national_favorability_df["Candidate"].isin(
            [
                "Pence",
                "Haley",
                "DeSantis",
                "Scott",
                "Trump",
                "Ramaswamy",
                "Hutchinson",
                "Burgum",
                "Christie",
            ]
        )
    ]

    state_polls_df = pd.read_csv(
        "https://projects.fivethirtyeight.com/polls-page/data/president_primary_polls.csv",
        engine="python",
    )

    state_polls_df.rename(
        columns={
            "end_date": "Date",
            "candidate_name": "Candidate",
            "pct": "Percentage",
        },
        inplace=True,
    )


    state_polls_df["Code"] = state_polls_df["state"].map(code)
    state_polls_df["state"] = state_polls_df["state"].map(code)
    state_polls_df = state_polls_df[~state_polls_df.Code.isnull()]
    state_polls_df["Candidate"] = state_polls_df["Candidate"].replace(candidate_names)
    state_polls_df = state_polls_df[
        state_polls_df["Candidate"].isin(
            [
                "Pence",
                "Haley",
                "DeSantis",
                "Scott",
                "Trump",
                "Ramaswamy",
                "Hutchinson",
                "Burgum",
                "Christie",
            ]
        )
    ]

    return national_avg_poll_df, national_favorability_df, state_polls_df
