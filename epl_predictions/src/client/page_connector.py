import requests
import time
import pandas as pd
from bs4 import BeautifulSoup
from typing import Optional
from ..utils.setup_logging import setup_logging


class PageConnector:
    
    def __init__(self, url: str):
        self.logger = setup_logging()

        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        self.url = url
        self.soup = self._make_request(self.url)


    def _make_request(self, url: str) -> BeautifulSoup:
        try:
            self.logger.debug(f"Making request to: {url}")
            
            time.sleep(5)
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            return BeautifulSoup(response.text, "html.parser")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error making request to {url}: {e}")
            return BeautifulSoup()


    def get_page(self) -> BeautifulSoup:
        return self.soup