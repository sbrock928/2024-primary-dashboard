import datetime
from typing import Any, Dict, List, Tuple

from dash import Input, Output, Dash

from dashboard.elections import query


def register_callbacks(app: Dash) -> None:
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

        national_avg_poll_df = query.get_national_avg_polling_data()
        national_favorability_df = query.get_national_favorability_polling_data()
        state_polls_df = query.get_state_polling_data()

        date = datetime.date.today() - datetime.timedelta(days=30)
        max_date_allowed = datetime.date.today()

        return (
            national_avg_poll_df.to_dict("records"),
            national_favorability_df.to_dict("records"),
            state_polls_df.to_dict("records"),
            date,
            max_date_allowed,
        )
