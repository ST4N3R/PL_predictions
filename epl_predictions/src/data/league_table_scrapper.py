import pandas as pd
from src.data.page_scrapper import PageScrapper
from src.client.page_connector import PageConnector
from src.setup_logging import setup_logging
from src.config.config import URL_BEGGINING, DATA_PATH


class LeagueTableScrapper:
    def __init__(self):
        self.logger = setup_logging()


    #ToDo: testy na zwrócenie odpowiednich rzeczy w PageConnector
    #ToDp: testy na zwrócenie odpowiednich rzeczy w PageScrapper
    #ToDo: testy na
    def _extract_league_table(self, url: str, table_id: str) -> pd.DataFrame:
        page_connector = PageConnector(url)
        page = page_connector.get_page()

        page_scrapper = PageScrapper(page, table_id)

        return page_scrapper.get_table_as_dataframe()


    def get_current_league_table(self) -> pd.DataFrame:
        url = URL_BEGGINING + "/en/comps/9/Premier-League-Stats"
        table_id = "results2024-202591_overall"

        try:
            current_df = self._extract_league_table(url, table_id)

            return current_df
        except Exception as e:
            self.logger.error(e)
            return pd.Dataframe()


    def _change_seasons_to_int(self, start_season: str, end_season: str) -> list:
        return [int(start_season[:4]), int(end_season[:4])]


    #ToDo: Dodać walidację str
    def _validate_season_str(self, season: str) -> bool:
        return True


    def get_previous_league_tables(self, start_season: str="1995-1996", end_season: str="2023-2024") -> pd.DataFrame: 
        if not self._validate_season_str(start_season):
            return pd.DataFrame()
        if not self._validate_season_str(end_season):
            return pd.DataFrame()

        start_year, end_year = self._change_seasons_to_int(start_season, end_season)
        previous_df = pd.DataFrame()
        
        for year in range(start_year, end_year + 1):
            season = f"{year}-{str(year + 1)}"

            url = URL_BEGGINING + f"/en/comps/9/{season}/Premier-League-Stats"
            table_id = f"results{season}91_overall"

            self.logger.debug(f"Scraping table {season} season")
            
            season_df = self._extract_league_table(url, table_id)
            season_df['Season'] = season

            previous_df = pd.concat([previous_df, season_df], ignore_index=True)
            self.logger.debug(f"Successfuly scraped the table of {season} season")
        
        return previous_df


    def save_table(self, df: pd.DataFrame, name: str) -> None:
        if df is None:
            self.logger.error("Df is none")
            return None

        #ToDo: Sprawdzać czy ma się dostęp oraz, czy folder istnieje
        df = df.reset_index()
        df.to_csv(DATA_PATH + f"raw/{name}.csv", index=False)
        self.logger.debug(f"Current table saved to {DATA_PATH}/raw")