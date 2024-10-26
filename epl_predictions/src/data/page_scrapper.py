import requests
import time
import pandas as pd
from bs4 import BeautifulSoup
from typing import Optional
from src.setup_logging import setup_logging

class PageScrapper:
    def __init__(self, url: str, table_id: str):
        self.logger = setup_logging()

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        self.soup = None
        self.url = url
        self.table_id = table_id


    def _make_request(self, url: str, delay: int) -> Optional[BeautifulSoup]:
        """Make a request to the specified URL and return BeautifulSoup object.

        Args:
            url (str): The URL to request
            delay (int): Delay in seconds between requests

        Returns:
            Optional[BeautifulSoup]: BeautifulSoup object if successful, None otherwise
        """

        try:
            time.sleep(delay)
            self.logger.info(f"Making request to: {url}")
            
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            self.logger.info("Request successful")
            return BeautifulSoup(response.text, 'html.parser')
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error making request to {url}: {e}")
            return None


    def get_page_html(self, delay=3) -> Optional[BeautifulSoup]:
        """Get the HTML content of a page.

        Args:
            url (Optional[str], optional): URL to scrape. If None, uses default EPL URL
            delay (int, optional): Delay in seconds between requests

        Returns:
            Optional[BeautifulSoup]: BeautifulSoup object if successful, None otherwise
        """
        self.soup = self._make_request(self.url, delay)

        return self.soup
    

    def _extract_table_data(self, table) -> list:
        rows = []
        for row in table.find_all('tr'):
            cols = row.find_all(['th', 'td'])
            if cols:
                row_data = [col.text.strip() for col in cols]
                rows.append(row_data)
        return rows


    def _get_season_dataframe(self, rows: Optional[list]) -> pd.DataFrame:
        if rows == None:
            df = pd.DataFrame()
        else:
            df = pd.DataFrame(rows[1:], columns=rows[0])
            df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        
        return df


    def get_page_table(self) -> pd.DataFrame:
        table = self.soup.find('table', {'id': self.table_id})

        if table is None:
            self.logger.error("Couldn't find the standings table")

        rows = self._extract_table_data(table)
        df = self._get_season_dataframe(rows)

        return df
    

    def get_match_report_link(self) -> list:
        links = []
        td_match_report = self.soup.select('td[data-stat="match_report"]')

        for td in td_match_report:
            link = td.a

            if link == None:
                continue

            links.append("https://fbref.com" + link['href'])
        
        return links