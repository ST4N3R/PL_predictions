from bs4 import BeautifulSoup
from lxml import etree
from epl_predictions.src.utils.setup_logging import setup_logging


class PageUser:
    def __init__(self, soup: BeautifulSoup):
        self.logger = setup_logging()
        self.soup = soup

    
    def get_element_by_xpath(self, xpath: str) -> BeautifulSoup:
        try:
            tree = etree.HTML(str(self.soup))
            element = tree.xpath(xpath)

            if element:
                element_html = etree.tostring(element[0], pretty_print=True).decode()
                return BeautifulSoup(element_html, "html.parser")
            else:
                self.logger.error(f"Element not found for XPATH: {xpath}")
                return BeautifulSoup()
            
        except Exception as e:
            self.logger.error(f"Error finding element by XPATH {xpath}: {e}")
            return BeautifulSoup()