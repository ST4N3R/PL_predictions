import pandas as pd
from dotenv import load_dotenv, set_key
from ..setup_logging import setup_logging
import os


class LastScrappedResult:
    def __init__(self, dataset: pd.DataFrame, date_col: int = 3, hour_col: int = 4) -> None:
        self.date = dataset.iloc[-1, date_col]
        self.hour = dataset.iloc[-1, hour_col]

        self.logger = setup_logging()


    def change_env_values(self) -> bool:
        try:
            load_dotenv()

            os.environ["LAST_SCRAPPED_MATCH_DATE"] = self.date
            os.environ["LAST_SCRAPPED_MATCH_HOUR"] = self.hour

            set_key(key_to_set="LAST_SCRAPPED_MATCH_DATE", value_to_set=os.environ["LAST_SCRAPPED_MATCH_DATE"])
            set_key(key_to_set="LAST_SCRAPPED_MATCH_HOUR", value_to_set=os.environ["LAST_SCRAPPED_MATCH_HOUR"])

            return True
        except Exception as e:
            self.logger(e)
            return False