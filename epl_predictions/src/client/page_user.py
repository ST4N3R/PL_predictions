import mechanize
from bs4 import BeautifulSoup
from lxml import etree
from epl_predictions.src.utils.setup_logging import setup_logging


class PageUser:
    def __init__(self, url: str, link_text: str):
        self.logger = setup_logging()
        self.url = url
        self.link_text = link_text


    def _make_request(self) -> BeautifulSoup:
        try:
            self.logger.debug(f"Making request to: {self.url}")
            
            br = mechanize.Browser()
            br.set_handle_robots(False)
            br.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')]
            br.open(self.url)
            
            return self.get_response(br)
        except Exception as e:
            self.logger.error(f"Error making request to {self.url}: {e}")
            return BeautifulSoup()
    

    def get_response(self, br: mechanize.Browser) -> BeautifulSoup:
        self.link_class = "sr_preset"
        try:
            print(br.find_link(tag="a", predicate=lambda link: self.link_class in link.attrs[0]))
            
            response = br.response().read()
        
            return BeautifulSoup(response, "html.parser")
        except Exception as e:
            self.logger.error(f"Error getting response: {e}")
            return BeautifulSoup()


    def get_soup(self) -> BeautifulSoup:
        return self._make_request()