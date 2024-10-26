import pandas as pd
from typing import Optional
from src.data.page_scrapper import PageScrapper
from src.setup_logging import setup_logging


class ResultsScrapper:
    def __init__(self) -> None:
        self.logger = setup_logging()

        self.next_fixtures_df = None
        self.result_prev_seasons_df = None
        self.result_curr_season_df = None


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


    def _split_reusults_fixtures(self, df: pd.DataFrame) -> None:
        try:
            self.next_fixtures_df = df[df['Score'].isna()]

            self.result_curr_season_df = df[~df['Score'].isna()]
            self.result_curr_season_df['Season'] = "2024-2025"

            self.logger.info("Current season data split into results and fixture still to be played")
        except Exception as e:
            self.logger.error(e)


    def _format_fixtures_df(self, df: pd.DataFrame, ps: PageScrapper) -> pd.DataFrame:
        df = self._remove_all_null_rows(df)
        df = self._change_xG_columns_names(df)

        links = ps.get_match_report_link()
        df['Match Report'] = links

        return df


    def get_next_fixtures(self) -> Optional[pd.DataFrame]:
        url = "https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures"
        table_id = "sched_2024-2025_9_1"

        try:
            pageScrapper = PageScrapper(url, table_id)
            pageScrapper.get_page_html()

            temp_df = pageScrapper.get_page_table()
            temp_df = self._format_fixtures_df(temp_df, pageScrapper)

            self._split_reusults_fixtures(temp_df)

            return self.next_fixtures_df
        except Exception as e:
            self.logger.error(e)
            return None


    def get_previous_fixtures(self, start_season: str="1995-1996", end_season: str="2023-2024") -> pd.DataFrame:
        if self.result_curr_season_df == None:
            self.get_next_fixtures()

        start_year = int(start_season[:4])
        end_year = int(end_season[:4])
        previous_df = pd.DataFrame()

        for year in range(start_year, end_year + 1):
            season = f"{year}-{str(year+1)}"
            url = f"https://fbref.com/en/comps/9/{season}/schedule/{season}-Premier-League-Scores-and-Fixtures"
            table_id = f"sched_{season}_9_1"

            self.logger.info(f"Scraping results from {season} season")
            
            pageScrapper = PageScrapper(url, table_id)
            pageScrapper.get_page_html()

            season_df = pageScrapper.get_page_table()
            season_df = self._format_fixtures_df(season_df, pageScrapper)
            season_df['Season'] = season

            try:
                previous_df = pd.concat([previous_df, season_df])
                self.logger.info(f"Successfuly scraped the table of {season} season")
            except pd.errors.InvalidIndexError:
                self.logger.error("Problem with indexes in your df")
                previous_df.to_csv(f"epl_predictions/data/raw/results.csv", index=False)
        
        self.result_prev_seasons_df = pd.concat([previous_df, self.result_curr_season_df])
        return self.result_prev_seasons_df


    def save_table(self, df: pd.DataFrame, name: str) -> None:
        if df is not None:
            df.to_csv(f"epl_predictions/data/raw/{name}.csv", index=False)
            self.logger.info("Current table saved fo data/raw")