import requests
from bs4 import BeautifulSoup
import time
import logging
from typing import Optional

class PageScrapper:
    def __init__(self):
        self._setup_logging()

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        self.soup = None


    def _setup_logging(self) -> None:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(self.__class__.__name__)


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


    def get_page_html(self, url: Optional[str] = None, delay=3) -> Optional[BeautifulSoup]:
        """Get the HTML content of a page.

        Args:
            url (Optional[str], optional): URL to scrape. If None, uses default EPL URL
            delay (int, optional): Delay in seconds between requests

        Returns:
            Optional[BeautifulSoup]: BeautifulSoup object if successful, None otherwise
        """

        url = url or "https://fbref.com/en/comps/9/Premier-League-Stats"

        self.soup = self._make_request(url, delay)

        return self.soup