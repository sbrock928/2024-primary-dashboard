import pandas as pd
import pathlib

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
    "Pence": "Mike Pence",
    "Haley": "Nikki Haley",
    "DeSantis": "Ron DeSantis",
    "T. Scott": "Tim Scott",
    "Trump": "Donald Trump",
    "Hutchinson": "Asa Hutchinson",
    "Ramaswamy": "Vivek G. Ramaswamy",
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

    PATH = pathlib.Path(__file__).parent
    DATA_PATH = PATH.joinpath("../datasets").resolve()

    average_polls_df = pd.read_csv(
        DATA_PATH.joinpath("presidential_primary_averages.csv"), engine="python"
    )
    average_polls_df = average_polls_df[average_polls_df["cycle"] == 2024]
    average_polls_df = average_polls_df[import_columns]
    average_polls_df["candidate"] = average_polls_df["candidate"].replace(
        candidate_names
    )

    favorability_polls_df = pd.read_csv(
        DATA_PATH.joinpath("favorability_polls.csv"), engine="python"
    )

    state_polls_df = pd.read_csv(
        DATA_PATH.joinpath("president_primary_polls.csv"), engine="python"
    )
    state_polls_df["Code"] = state_polls_df["state"].map(code)
    state_polls_df["state"] = state_polls_df["state"].map(code)

    return average_polls_df, favorability_polls_df, state_polls_df
