from unittest.mock import patch, MagicMock
import pytest
import requests
import pandas as pd
from bs4 import BeautifulSoup
from epl_predictions.src.scrappers.page_scrapper import PageScrapper


class TestPageScrapper:

    def setup_method(self):
        html_content = """
                <html>
                    <body>
                        <table id="test-table">
                            <tr><th>Column1</th><th>Column2</th></tr>
                            <tr><td>Data1</td><td>Data2</td></tr>
                            <tr><td>Data3</td><td>Data4</td></tr>
                        </table>
                    </body>
                </html>
                """
        self.soup = BeautifulSoup(html_content, 'html.parser')
        self.scraper = PageScrapper(self.soup, 'test-table')


    def test_initialization(self):
        assert self.scraper.table_id == 'test-table'
        assert self.scraper.soup == self.soup


    def test__preprocess_table_data(self):
        rows = [['Column1', 'Column2'],
                ['Data1', 'Data2'],
                ['Data3', 'Data4']]
        tag_table = self.soup.find('table', {'id': 'test-table'})
        table = self.scraper._preprocess_table_data(tag_table)

        assert table == rows

    
    def test__preprocess_table_data_none_rows(self):
        rows = []
        table = self.scraper._preprocess_table_data(None)

        assert table == rows


    def test__extract_table_from_page_missing_table(self):
        soup = BeautifulSoup("<html></html>", "html.parser")
        page_scrapper = PageScrapper(soup, 'missing-table')

        assert page_scrapper.table == []

    
    def test_get_table_as_dataframe(self):
        rows = [['Column1', 'Column2'],
            ['Data1', 'Data2'],
            ['Data3', 'Data4']]
        test_df = pd.DataFrame(rows[1:], columns=rows[0])
        result_df = self.scraper.get_table_as_dataframe()

        assert type(result_df) == type(test_df)
        assert result_df.shape == test_df.shape
        assert list(result_df.columns) == list(test_df.columns)

    
    def test_get_table_as_dataframe_none_table(self):
        test_df = pd.DataFrame()

        self.scraper.table = None
        result_df = self.scraper.get_table_as_dataframe()

        assert type(result_df) == type(test_df)
        assert result_df.shape == test_df.shape
        assert list(result_df.columns) == list(test_df.columns)