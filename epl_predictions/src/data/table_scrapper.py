from bs4 import BeautifulSoup
import pandas as pd
from typing import Optional
from epl_predictions.src.client.page_scrapper import PageScrapper
from src.setup_logging import setup_logging


#ToDo: Podmienić nazwy
class TableScrapper:
    def __init__(self):
        self.logger = setup_logging()


    #ToDo: Zmienić nazwę funkcji
    def get_current_table(self) -> pd.DataFrame:
        url = "https://fbref.com/en/comps/9/Premier-League-Stats"
        table_id = "results2024-202591_overall"

        try:
            page_scrapper = PageScrapper(url, table_id)
            page_scrapper.get_page_html()
            current_df = page_scrapper.get_page_table()

            return current_df
        except Exception as e:
            self.logger.error(e)
            return None


    #ToDo: Zmienić nazwę funkcji
    def get_previous_tables(self, start_season: str="1995-1996", end_season: str="2023-2024") -> pd.DataFrame:
        #ToDo: Przenieść funkcjonalność
        #ToDo: Dodać walidację str
        start_year = int(start_season[:4])
        end_year = int(end_season[:4])
        previous_df = pd.DataFrame()
        
        for year in range(start_year, end_year + 1):
            season = f"{year}-{str(year + 1)}"
            #ToDo: Zmienieć początek url na zmienną globalną
            url = f"https://fbref.com/en/comps/9/{season}/Premier-League-Stats"
            table_id = f"results{season}91_overall"

            self.logger.debug(f"Scraping table {season} season")
            
            pageScrapper = PageScrapper(url, table_id)
            season_df = pageScrapper.get_page_table()
            season_df['Season'] = season

            previous_df = pd.concat([previous_df, season_df], ignore_index=True)
            self.logger.debug(f"Successfuly scraped the table of {season} season")
        
        return previous_df


    def save_table(self, df: pd.DataFrame, name: str) -> None:
        if df is None:
            self.logger.info("You passed ")
            return None

        #ToDo: Zrobić zmienną globalną ze ścieżką
        #ToDo: Sprawdzać czy ma się dostęp oraz, czy folder istnieje
        df.to_csv(f"epl_predictions/data/raw/{name}.csv", index=False)
        self.logger.debug("Current table saved fo data/raw")