import pandas as pd
from typing import Tuple
from epl_predictions.src.scrappers.league_table_scrapper import LeagueTableScrapper
from epl_predictions.src.scrappers.results_scrapper import ResultsScrapper
from epl_predictions.src.azure_client.storage_connector import StorageConnector
from epl_predictions.src.utils.saver import Saver
from epl_predictions.src.config.config import CURRENT_SEASON


def upload_df_to_blob(df: pd.DataFrame, container_name: str, blob_name: str) -> None:
    container_client = StorageConnector()
    container_client.conntect_to_container(container_name)

    saver = Saver()
    saver.save_table_to_container(df, blob_name, container_client)


def get_current_league_table() -> pd.DataFrame:
    lts = LeagueTableScrapper()
    df = lts.get_current_league_table()

    upload_df_to_blob(df, "raw", "current_table.csv")
    return df


# def get_fixtures() -> Tuple[pd.DataFrame, pd.DataFrame]:
#     rs = ResultsScrapper()
#     df_next_fixtures = rs.get_next_fixtures()
#     df_previous_fixtures = rs.get_previous_fixtures()

#     upload_df_to_blob(df_next_fixtures, "raw", "next_fixtures.csv")
#     upload_df_to_blob(df_previous_fixtures, "raw", "{CURRENT_SEASON}" + "_results.csv")
#     return df_next_fixtures, df_previous_fixtures

