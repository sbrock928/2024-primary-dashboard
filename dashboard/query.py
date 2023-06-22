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

    url = 'https://projects.fivethirtyeight.com/polls/data/presidential_primary_averages.csv'
    s = requests.get(url).content.decode('utf8')
    national_avg_poll_df = pd.read_csv(io.StringIO(s), engine='python')



    national_avg_poll_df = national_avg_poll_df[national_avg_poll_df["cycle"] == 2024]
    national_avg_poll_df = national_avg_poll_df[import_columns]
    national_avg_poll_df["candidate"] = national_avg_poll_df["candidate"].replace(
        candidate_names
    )

    url = "https://projects.fivethirtyeight.com/polls-page/data/favorability_polls.csv"
    s = requests.get(url).content.decode('utf8')
    national_favorability_df = pd.read_csv(io.StringIO(s), engine='python')


    url = "https://projects.fivethirtyeight.com/polls-page/data/president_primary_polls.csv"
    s = requests.get(url).content.decode('utf8')
    state_polls_df = pd.read_csv(io.StringIO(s), engine='python')



    state_polls_df["Code"] = state_polls_df["state"].map(code)
    state_polls_df["state"] = state_polls_df["state"].map(code)
    state_polls_df = state_polls_df[~state_polls_df.Code.isnull()]
    state_polls_df = state_polls_df[
        state_polls_df["candidate_name"].isin(
            [
                "Mike Pence",
                "Nikki Haley",
                "Ron DeSantis",
                "Tim Scott",
                "Donald Trump",
                "Asa Hutchinson",
                "Vivek G. Ramaswamy",
            ]
        )
    ]

    return national_avg_poll_df, national_favorability_df, state_polls_df
