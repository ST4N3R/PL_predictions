import pandas as pd
from typing import Tuple
from ..scrappers.page_scrapper import PageScrapper
from ..client.page_connector import PageConnector
from ..utils.setup_logging import setup_logging
from ..config.config import URL_BEGGINING, DATA_PATH


class LeagueTableScrapper:
    def __init__(self):
        self.logger = setup_logging()


    def _extract_league_table(self, url: str, table_id: str) -> pd.DataFrame:
        page_connector = PageConnector(url)
        page = page_connector.get_page()

        page_scrapper = PageScrapper(page, table_id)

        return page_scrapper.get_table_as_dataframe()


    #ToDo: Add removing unnecessary columns
    #ToDo: Add season column
    def get_current_league_table(self) -> pd.DataFrame:
        url = URL_BEGGINING + "/en/comps/9/Premier-League-Stats"
        table_id = "results2024-202591_overall"

        try:
            current_df = self._extract_league_table(url, table_id=table_id)
            current_df = current_df.reset_index(drop=True)

            self.logger.info(f"Successfuly scraped the current league table")
            return current_df
        except Exception as e:
            self.logger.error(e)
            return pd.DataFrame()


    def _change_seasons_str_to_int(self, start_season: str, end_season: str) -> Tuple[int, int]:
        return int(start_season[:4]), int(end_season[:4])


    def _validate_season_str(self, season: str) -> bool:
        if len(season) != 9:
            self.logger.error("Season string have too little signs")
            return False
        if '-' not in season:
            self.logger.error("There is no - in string")
            return False
        
        split_str = season.split('-')
        if len(split_str) != 2:
            self.logger.error("- is in wrong place")
            return False
        if len(split_str[1]) != 4:
            self.logger.error("Second year is in wrong format")
            return False
        if len(split_str[0]) != 4:
            self.logger.error("First year is in wrong format")
            return False
        try:
            first_year = int(split_str[0])
            second_year = int(split_str[1])
            
            if first_year + 1 != second_year:
                self.logger.error("Difference between first and second year in season string should be 1")
                return False
        except:
            self.logger.error("Season string is in wrong format")
            return False
        return True


    def get_previous_league_tables(self, start_season: str="1995-1996", end_season: str="2023-2024") -> pd.DataFrame: 
        if not self._validate_season_str(start_season):
            return pd.DataFrame()
        if not self._validate_season_str(end_season):
            return pd.DataFrame()

        start_year, end_year = self._change_seasons_str_to_int(start_season, end_season)
        previous_df = pd.DataFrame()
        
        for year in range(start_year, end_year + 1):
            season = f"{year}-{str(year + 1)}"
            url = URL_BEGGINING + f"/en/comps/9/{season}/Premier-League-Stats"
            table_id = f"results{season}91_overall"
            
            season_df = self._extract_league_table(url, table_id)
            season_df['Season'] = season

            previous_df = pd.concat([previous_df, season_df], ignore_index=True)
            self.logger.info(f"Successfuly scraped the table of {season} season")
        
        return previous_df


    def save_table(self, df: pd.DataFrame, name: str) -> bool:
        if df is None:
            self.logger.error("Df is none")
            return False

        #ToDo: Sprawdzać czy ma się dostęp oraz, czy folder istnieje
        df = df.reset_index()
        df.to_csv(DATA_PATH + f"raw/{name}.csv", index=False)
        self.logger.debug(f"Current table saved to {DATA_PATH}/raw")

        return True