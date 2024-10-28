import pandas as pd
from bs4 import BeautifulSoup
from src.data.page_scrapper import PageScrapper
from src.client.page_connector import PageConnector
from src.setup_logging import setup_logging
from src.config.config import URL_BEGGINING, DATA_PATH


class ResultsScrapper:
    def __init__(self) -> None:
        self.logger = setup_logging()

        self.next_fixtures_df = None
        self.results_previous_seasons_df = None
        self.results_current_season_df = None


    def _remove_all_null_rows(self, df: pd.DataFrame) -> pd.DataFrame:
        pd.set_option('future.no_silent_downcasting', True)
        
        df = df.replace("", float('nan'))
        df = df.dropna(how='all', ignore_index=True)
        return df


    def _change_xG_columns_names(self, df: pd.DataFrame) -> pd.DataFrame:
        columns = ['Wk', 'Day', 'Date', 'Time', 'Home', 'xG_Home', 'Score', 'xG_Away', 'Away', 'Attendance', 'Venue', 'Referee', 'Match Report', 'Notes']

        if len(df.columns) == len(columns):
            df.columns = columns
        else:
            df['xG_Home'] = float('nan')
            df['xG_Away'] = float('nan')

        return df


    def _scrapp_match_report_link(self, df: pd.DataFrame, soup: BeautifulSoup) -> list:
        links = []
        td_match_report = soup.select('td[data-stat="match_report"]')

        for td in td_match_report:
            link = td.a

            if link == None:
                continue

            links.append(URL_BEGGINING + link['href'])
        
        df['March Report'] = links
        return df


    def _preprocess_fixtures_df(self, df: pd.DataFrame, soup: BeautifulSoup) -> pd.DataFrame:
        df = self._remove_all_null_rows(df)
        df = self._change_xG_columns_names(df)
        df = self._scrapp_match_report_link(df, soup)

        return df


    def _extract_fixtures(self, url: str, table_id: str) -> pd.DataFrame:
        page_connector = PageConnector(url)
        page = page_connector.get_page()

        page_scrapper = PageScrapper(page, table_id)
        df = page_scrapper.get_table_as_dataframe()

        df = self._preprocess_fixtures_df(df, page)

        return df


    def _split_reusults_and_fixtures(self, df: pd.DataFrame) -> None:
        try:
            self.next_fixtures_df = df[df['Score'].isna()]
            self.next_fixtures_df = self.next_fixtures_df.reset_index(drop=True)

            self.results_current_season_df = df[~df['Score'].isna()]
            self.results_current_season_df['Season'] = "2024-2025"

            self.logger.debug("Current season data split into results and fixture still to be played")
        except Exception as e:
            self.logger.error(e)


    def get_next_fixtures(self) -> pd.DataFrame:
        url = URL_BEGGINING + "/en/comps/9/schedule/Premier-League-Scores-and-Fixtures"
        table_id = "sched_2024-2025_9_1"

        try:
            temp_df = self._extract_fixtures(url, table_id)
            self._split_reusults_and_fixtures(temp_df)
        except TypeError:
            self.logger.error(temp_df)
            return pd.DataFrame()
        except Exception as e:
            self.logger.error(e)
            return pd.DataFrame()   
        
        return self.next_fixtures_df


    def _change_seasons_to_int(self, start_season: str, end_season: str) -> list:
        return [int(start_season[:4]), int(end_season[:4])]


    #ToDo: Dodać walidację str
    def _validate_season_str(self, season: str) -> bool:
        return True


    def get_previous_fixtures(self, start_season: str="1995-1996", end_season: str="2023-2024") -> pd.DataFrame:
        if not self._validate_season_str(start_season):
            return pd.DataFrame()
        if not self._validate_season_str(end_season):
            return pd.DataFrame()

        if self.results_current_season_df == None:
            self.get_next_fixtures()

        start_year, end_year = self._change_seasons_to_int(start_season, end_season)
        previous_df = pd.DataFrame()

        for year in range(start_year, end_year + 1):
            season = f"{year}-{str(year+1)}"

            url = URL_BEGGINING + f"/en/comps/9/{season}/schedule/{season}-Premier-League-Scores-and-Fixtures"
            table_id = f"sched_{season}_9_1"

            self.logger.debug(f"Scraping results from {season} season")
            
            season_df = self._extract_fixtures(url, table_id)
            season_df['Season'] = season

            try:
                previous_df = pd.concat([previous_df, season_df])
                self.logger.info(f"Successfuly scraped the table of {season} season")
            except pd.errors.InvalidIndexError:
                self.logger.error("Problem with indexes in your df")
        
        self.results_previous_seasons_df = pd.concat([previous_df, self.results_current_season_df])
        self.results_previous_seasons_df = self.results_previous_seasons_df.reset_index(drop=True)

        return self.results_previous_seasons_df


    def save_table(self, df: pd.DataFrame, name: str) -> None:
        if df is None:
            self.logger.error("Df is none")
            return None
        
        #ToDo: Sprawdzać czy ma się dostęp oraz, czy folder istnieje
        df = df.reset_index()
        df.to_csv(DATA_PATH + f"raw/{name}.csv", index=False)
        self.logger.info(f"Current table saved to {DATA_PATH}/raw")