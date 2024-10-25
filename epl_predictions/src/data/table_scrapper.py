from bs4 import BeautifulSoup
import pandas as pd
from typing import Optional
from src.data.page_scrapper import PageScrapper
from src.setup_logging import setup_logging

class TableScrapper:
    def __init__(self):
        self.logger = setup_logging()


    def _extract_table_data(self, table) -> list:
        rows = []
        for row in table.find_all('tr'):
            cols = row.find_all(['th', 'td'])
            if cols:
                row_data = [col.text.strip() for col in cols]
                rows.append(row_data)
        return rows


    def _get_season_table(self, season: Optional[str]) -> Optional[list]:
        if season == None:
            url = "https://fbref.com/en/comps/9/Premier-League-Stats"
            table_id = "results2024-202591_overall"
        else:
            url = f"https://fbref.com/en/comps/9/{season}/Premier-League-Stats"
            table_id = f"results{season}91_overall"

        try:
            pageScrapper = PageScrapper()
            soup = pageScrapper.get_page_html(url=url)
            table = soup.find('table', {'id': table_id})
            
            if table is None:
                self.logger.error("Couldn't find the standings table")
            
            rows = self._extract_table_data(table)

            return rows
        
        except Exception as e:
            self.logger.error(e)
            return None


    def _get_season_dataframe(self, rows: Optional[list]) -> pd.DataFrame:
        if rows == None:
            df = pd.DataFrame()
        else:
            df = pd.DataFrame(rows[1:], columns=rows[0])
            df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        
        return df


    def get_current_table(self) -> pd.DataFrame:
        rows = self._get_season_table(None)
        current_df = self._get_season_dataframe(rows)

        return current_df


    def get_previous_tables(self, start_season: str="1995-1996", end_season: str="2023-2024") -> pd.DataFrame:
        start_year = int(start_season[:4])
        end_year = int(end_season[:4])
        previous_df = pd.DataFrame()
        
        for year in range(start_year, end_year + 1):
            season = f"{year}-{str(year+1)}"
            self.logger.info(f"Scraping season {season}")
            
            rows = self._get_season_table(season)
            season_df = self._get_season_dataframe(rows)
            season_df['Season'] = season

            previous_df = pd.concat([previous_df, season_df], ignore_index=True)
            self.logger.info(f"Successfuly scraped the table of {season} season")
        
        return previous_df


    def save_table(self, df: pd.DataFrame, name: str) -> None:
        if df is not None:
            df.to_csv(f"epl_predictions/data/raw/{name}.csv", index=False)
            self.logger.info("Current table saved fo data/raw")