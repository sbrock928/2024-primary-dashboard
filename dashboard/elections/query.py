from typing import Tuple

import pandas as pd

from dashboard.elections.constants import (
    import_columns,
    candidate_names,
    state_code_mapping,
)


def get_national_avg_polling_data() -> pd.DataFrame:
    """
    This function imports national average polling data from FiveThirtyEight, converts to a Panda's dataframe and clean/scrubs data

    returns:
        national_avg_poll_df | Panda's Dataframe : A Panda's dataframe of national polling averages


    """
    # Import csv as dataframe
    national_avg_poll_df = pd.read_csv(
        "https://projects.fivethirtyeight.com/polls/data/presidential_primary_averages.csv",
        engine="python",
    )

    # Remove prior election cycle data and take only columns we need
    national_avg_poll_df = national_avg_poll_df[national_avg_poll_df["cycle"] == 2024]
    national_avg_poll_df = national_avg_poll_df[import_columns]

    # Rename columns
    national_avg_poll_df.rename(
        columns={
            "candidate": "Candidate",
            "pct_estimate": "Percentage",
            "date": "Date",
        },
        inplace=True,
    )

    # Format candidate names and select only top republican candidates
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

    return national_avg_poll_df


def get_national_favorability_polling_data() -> pd.DataFrame:
    """
    This function imports national favorability polling data from FiveThirtyEight, converts to a Panda's dataframe and clean/scrubs data

    returns:
        national_favorability_df | Panda's Dataframe : A Panda's dataframe of national polling averages


    """

    # Import csv as dataframe
    national_favorability_df = pd.read_csv(
        "https://projects.fivethirtyeight.com/polls-page/data/favorability_polls.csv",
        engine="python",
    )

    # Rename columns
    national_favorability_df.rename(
        columns={
            "politician": "Candidate",
            "favorable": "Favorable",
            "unfavorable": "Unfavorable",
            "very_favorable": "Very Favorable",
            "somewhat_favorable": "Somewhat Favorable",
            "somewhat_unfavorable": "Somewhat Unfavorable",
            "very_unfavorable": "Very Unfavorable",
            "end_date": "Date",
        },
        inplace=True,
    )

    # Replace candidate names and select only top republican candidates
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

    return national_favorability_df


def get_state_polling_data() -> pd.DataFrame:
    """
    This function imports state polling data from FiveThirtyEight, converts to a Panda's dataframe and clean/scrubs data

    returns:
        state_polls_df | Panda's Dataframe : A Panda's dataframe of national polling averages


    """

    # Import csv as dataframe
    state_polls_df = pd.read_csv(
        "https://projects.fivethirtyeight.com/polls-page/data/president_primary_polls.csv",
        engine="python",
    )

    # Rename columns
    state_polls_df.rename(
        columns={
            "end_date": "Date",
            "candidate_name": "Candidate",
            "pct": "Percentage",
        },
        inplace=True,
    )

    # Replace state code and
    state_polls_df["Code"] = state_polls_df["state"].map(state_code_mapping)

    # Get rid of rows where state is null
    state_polls_df = state_polls_df[~state_polls_df.Code.isnull()]

    # Replace candidate names and select only top republican candidates
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

    return state_polls_df
