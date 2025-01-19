import pandas as pd
from epl_predictions.src.scrappers.league_table_scrapper import LeagueTableScrapper
from epl_predictions.src.azure_client.storage_connector import StorageConnector
from epl_predictions.src.preprocessors.process_league_table import ProcessLeagueTable
from epl_predictions.src.utils.saver import Saver


def upload_df_to_blob(df: pd.DataFrame, container_name: str, blob_name: str, override: bool) -> None:
    container_client = StorageConnector()
    container = container_client.conntect_to_container(container_name)

    saver = Saver()
    saver.save_table_to_container(df, blob_name, container, override)


def get_current_league_table() -> pd.DataFrame:
    lts = LeagueTableScrapper()
    df = lts.get_current_league_table()

    upload_df_to_blob(df, "raw", "current_table.csv", True)

    # plt = ProcessLeagueTable()
    # spark_df = plt.preprocess_data(df)

    # upload_df_to_blob(spark_df, "final", "current_table.csv", True)

    return df


# def get_fixtures() -> Tuple[pd.DataFrame, pd.DataFrame]:
#     rs = ResultsScrapper()
#     df_next_fixtures = rs.get_next_fixtures()
#     df_previous_fixtures = rs.get_previous_fixtures()

#     upload_df_to_blob(df_next_fixtures, "raw", "next_fixtures.csv")
#     upload_df_to_blob(df_previous_fixtures, "raw", "{CURRENT_SEASON}" + "_results.csv")
#     return df_next_fixtures, df_previous_fixtures

get_current_league_table()