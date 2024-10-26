from bs4 import BeautifulSoup
import pandas as pd
from typing import Optional
from src.data.page_scrapper import PageScrapper
from src.setup_logging import setup_logging


class TableScrapper:
    def __init__(self):
        self.logger = setup_logging()


    def get_current_table(self) -> pd.DataFrame:
        url = "https://fbref.com/en/comps/9/Premier-League-Stats"
        table_id = "results2024-202591_overall"

        try:
            pageScrapper = PageScrapper(url, table_id)
            pageScrapper.get_page_html()
            current_df = pageScrapper.get_page_table()

            return current_df
        except Exception as e:
            self.logger.error(e)
            return None


    def get_previous_tables(self, start_season: str="1995-1996", end_season: str="2023-2024") -> pd.DataFrame:
        start_year = int(start_season[:4])
        end_year = int(end_season[:4])
        previous_df = pd.DataFrame()
        
        for year in range(start_year, end_year + 1):
            season = f"{year}-{str(year+1)}"
            url = f"https://fbref.com/en/comps/9/{season}/Premier-League-Stats"
            table_id = f"results{season}91_overall"

            self.logger.info(f"Scraping table {season} season")
            
            pageScrapper = PageScrapper(url, table_id)
            pageScrapper.get_page_html()
            season_df = pageScrapper.get_page_table()
            season_df['Season'] = season

            previous_df = pd.concat([previous_df, season_df], ignore_index=True)
            self.logger.info(f"Successfuly scraped the table of {season} season")
        
        return previous_df


    def save_table(self, df: pd.DataFrame, name: str) -> None:
        if df is not None:
            df.to_csv(f"epl_predictions/data/raw/{name}.csv", index=False)
            self.logger.info("Current table saved fo data/raw")