import pandas as pd
import requests
from environment import API_KEY


class ArbProcessor:
    def __init__(self, key: str):
        self.sport = key
        self.df = self._get_data(key)

        if self.df is None:
            self.potential = False
            return

        self.min_imp_by_outcome, self.min_imp_by_id = self._calculate_implied_prob(
            self.df
        )
        self.surebet_ids = self._identify_surebets(self.min_imp_by_id)
        self.bets_to_take = self._bets_to_take(
            self.surebet_ids, self.min_imp_by_outcome
        )
        self.potential = True if len(self.surebet_ids) > 0 else False

    def get_potential(self):
        return self.potential

    def get_bets_to_take(self):
        return self.bets_to_take

    def _bets_to_take(self, sids, min_imps):
        return min_imps[min_imps["id"].isin(sids)]

    def _identify_surebets(self, imp_prob_df):
        surebet_ids = imp_prob_df.loc[imp_prob_df["imp_prob_sum"] < 1, "id"].tolist()
        return surebet_ids

    def _get_data(self, key: str) -> pd.DataFrame | None:
        url = f"https://api.the-odds-api.com/v4/sports/{key}/odds?regions=us&oddsFormat=decimal&apiKey={API_KEY}"
        r = requests.get(url)
        j = r.json()

        d = self._json_to_df(j)

        return None if d.empty else d

    def _calculate_implied_prob(self, df):
        df["imp_prob"] = 1 / df["price"]
        min_imp_prob_per_outcome = df.loc[
            df.groupby(["id", "name"])["imp_prob"].idxmin()
        ].reset_index(drop=True)
        imp_prob_by_id = (
            min_imp_prob_per_outcome.groupby("id")["imp_prob"]
            .sum()
            .reset_index(name="imp_prob_sum")
        )
        return min_imp_prob_per_outcome, imp_prob_by_id

    def _json_to_df(self, json_of_response) -> pd.DataFrame | None:
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

    @classmethod
    def sports_in_season(cls) -> list[str]:
        return cls.get_sports_df()["key"].to_list()

    @classmethod
    def get_sports_df(cls) -> pd.DataFrame:
        url = f"https://api.the-odds-api.com/v4/sports?apiKey={API_KEY}"
        response = requests.get(url)
        return pd.DataFrame(response.json())


if __name__ == "__main__":
    sports = ArbProcessor.sports_in_season()

    print("Checking these sports:")
    print(sports)

    options = []

    for i in sports:
        a = ArbProcessor(i)
        # print(i)
        if a.get_potential():
            options.append(a)

    print()
    print(f"{len(options)} potential winners found.")

    for o in options:
        print(o.get_bets_to_take())
