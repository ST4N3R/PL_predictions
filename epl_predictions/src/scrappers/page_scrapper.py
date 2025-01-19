import pandas as pd
from typing import Optional, Union
from bs4 import BeautifulSoup, Tag, NavigableString, ResultSet
from lxml import etree
from ..utils.setup_logging import setup_logging


class PageScrapper:

    def __init__(self, soup: BeautifulSoup, table_id: Optional[str] = None, table_xpath: Optional[str] = None) -> None:
        self.soup = soup
        self.table = None

        self.logger = setup_logging()

        if table_id == None and table_xpath != None:
            self._extract_table_with_xpath(table_xpath)
        else:
            self._extract_table_wiht_id(table_id)


    def _preprocess_table_data(self, tag_table: Optional[Union[Tag, NavigableString]]) -> list:
        rows = []

        if tag_table == None or type(tag_table) == NavigableString:
            return rows

        for row in tag_table.find_all("tr"):
            cols = row.find_all(["th", "td"])
            if cols:
                row_data = [col.text.strip() for col in cols]
                rows.append(row_data)

        return rows


    def _extract_table_wiht_id(self, table_id: str) -> None:
        try:        
            tag_table = self.soup.find("table", {'id': table_id})
        except AttributeError as e:
            self.logger.error(e)
            tag_table = None

        if tag_table is None:
            self.logger.error("Couldn't find the standings table")

        self.table = self._preprocess_table_data(tag_table)


    def _extract_table_with_xpath(self, xpath: str) -> None:
        element_soup = self._find_element_by_xpath(xpath)
        rows = []

        for row in element_soup.find_all("tr"):
            cols = row.find_all(["th", "td"])
            if cols:
                row_data = [col.text.strip() for col in cols]
                rows.append(row_data)

        self.table = rows
    

    def _find_element_by_xpath(self, xpath: str) -> BeautifulSoup:
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


    def get_table_as_dataframe(self) -> pd.DataFrame:
        if self.table == []:
            return pd.DataFrame()
        
        df = pd.DataFrame(self.table[1:], columns=self.table[0])
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        
        return df