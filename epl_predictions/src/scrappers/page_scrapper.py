from typing import Optional, Union
from bs4 import BeautifulSoup, Tag, NavigableString, ResultSet
import pandas as pd
from ..setup_logging import setup_logging


class PageScrapper:

    def __init__(self, soup: BeautifulSoup, table_id: str) -> None:
        self.table_id = table_id
        self.soup = soup
        self.table = None

        self.logger = setup_logging()

        self._extract_table_from_page()


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


    def _extract_table_from_page(self) -> None:
        try:        
            tag_table = self.soup.find("table", {'id': self.table_id})
        except AttributeError as e:
            self.logger.error(e)
            tag_table = None

        if tag_table is None:
            self.logger.error("Couldn't find the standings table")

        self.table = self._preprocess_table_data(tag_table)
    

    def get_table_as_dataframe(self) -> pd.DataFrame:
        if self.table == []:
            return pd.DataFrame()
        
        df = pd.DataFrame(self.table[1:], columns=self.table[0])
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        
        return df