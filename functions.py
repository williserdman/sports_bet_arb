import pandas as pd
import requests


def json_to_df(json_of_response):
    odds_df = pd.json_normalize(
        json_of_response,
        record_path=["bookmakers", "markets", "outcomes"],
        meta=[
            "id",
            "commence_time",
            "home_team",
            "away_team",
            ["bookmakers", "key"],
            ["bookmakers", "title"],
            ["bookmakers", "last_update"],
            ["bookmakers", "markets", "key"],
        ],
    )
    return odds_df
