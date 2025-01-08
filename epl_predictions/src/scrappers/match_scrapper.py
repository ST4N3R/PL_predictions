import pandas as pd
from bs4 import BeautifulSoup
from typing import Tuple
from ..utils.setup_logging import setup_logging
from ..utils.loader import Loader
from ..azure_client.storage_connector import StorageConnector
from ..client.page_connector import PageConnector
from ..scrappers.page_scrapper import PageScrapper


class MatchScrapper:
    def __init__(self):
        self.logger = setup_logging()


    def get_data_from_match_report_df(self, df: pd.DataFrame) -> pd.Series:
        try:
            match_report_links = df["Match Report"]
        except:
            self.logger.error("Match Report column not found")
            return pd.DataFrame()
        
        match_report_links = match_report_links.dropna()

        return match_report_links


    def extract_table(self, page: BeautifulSoup,table_id: str) -> pd.DataFrame:
        page_scrapper = PageScrapper(page, table_id)

        return page_scrapper.get_table_as_dataframe()


    def extract_match_report(self, url: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
        try:
            page_connector = PageConnector(url)
            page = page_connector.get_page()

            df_home_team = self.extract_table(page, "...")
            df_away_team = self.extract_table(page, "...")

            self.logger.info(f"Successfuly extracted match report from {url}")
            return (df_home_team, df_away_team)
        except Exception as e:
            self.logger.error(e)
            return (pd.DataFrame(), pd.DataFrame())


    def get_match_data(self, df: pd.DataFrame = None):
        resutlt_df = pd.DataFrame()
        if df is None:
            container_client = StorageConnector()
            container_client.conntect_to_container("raw")

            loader = Loader()
            df = loader.load_table_from_container("matches.csv", container_client)
        
        data = self.get_data_from_match_report_df(df)
        for n in data:
            self.extract_match_report(n)

