from unittest.mock import patch, MagicMock
import pytest
import requests
import pandas as pd
from bs4 import BeautifulSoup
from src.scrappers.page_scrapper import PageScrapper
from src.scrappers.league_table_scrapper import LeagueTableScrapper


class TestPageScrapper:

    def setup_method(self):
        self.lts = LeagueTableScrapper()


    @patch('src.scrappers.league_table_scrapper.PageConnector')
    @patch('src.scrappers.league_table_scrapper.PageScrapper')
    def test_extract_league_table(self, MockPageScrapper, MockPageConnector):
        html_content = """
                <html>
                    <body>
                        <table id="test-table">
                            <tr><th>Column1</th><th>Column2</th></tr>
                            <tr><td>Data1</td><td>Data2</td></tr>
                        </table>
                    </body>
                </html>
                """
        soup = BeautifulSoup(html_content, 'html.parser')

        mock_page_instance = MockPageConnector.return_value
        mock_page_instance.get_page.return_value = soup
        
        mock_scraper_instance = MockPageScrapper.return_value
        mock_scraper_instance.get_table_as_dataframe.return_value = pd.DataFrame({'Column1': ['Data1'], 'Column2': ['Data2']})
        
        result_df = self.lts._extract_league_table("http://mockurl.com", "test-table")
        
        assert MockPageConnector.called
        assert MockPageScrapper.called
        assert isinstance(result_df, pd.DataFrame)
        assert list(result_df.columns) == ['Column1', 'Column2']
        assert result_df.iloc[0]['Column1'] == 'Data1' and result_df.iloc[0]['Column2'] == 'Data2'


    @patch('src.scrappers.league_table_scrapper.LeagueTableScrapper._extract_league_table', return_value = pd.DataFrame({'Column1': ['Data1'], 'Column2': ['Data2']}))
    def test_get_current_league_table(self, mock_extract):
        result_df = self.lts.get_current_league_table()

        assert type(result_df) == pd.DataFrame
        assert len(result_df) == 1
        assert mock_extract.called

    
    def test__change_season_str_to_int(self):
        start, end = self.lts._change_seasons_str_to_int("2020-2021", "2021-2022")
        assert start == 2020
        assert end == 2021

    
    def test__validate_season_str(self):
        assert self.lts._validate_season_str("") == False
        assert self.lts._validate_season_str("123456789") == False
        assert self.lts._validate_season_str("12345678-") == False
        assert self.lts._validate_season_str("1234567-8") == False
        assert self.lts._validate_season_str("four-four") == False
        assert self.lts._validate_season_str("2020-2022") == False


    @patch('src.scrappers.league_table_scrapper.LeagueTableScrapper._validate_season_str', return_value=True)
    @patch('src.scrappers.league_table_scrapper.LeagueTableScrapper._extract_league_table', return_value = pd.DataFrame({'Column1': ['Data1'], 'Column2': ['Data2']}))
    def test_get_previous_league_tables(self, mock_extract, mock_validate):
        result_df = self.lts.get_previous_league_tables("2022-2023", "2023-2024")
        
        assert type(result_df) == pd.DataFrame
        assert len(result_df) == 2
        assert mock_extract.called


    def test_save_table_none_df(self):
        result = self.lts.save_table(None, "test")

        assert result == False


    @patch.object(pd.DataFrame, 'to_csv')
    def test_save_table_success(self, mock_to_csv):
        df = pd.DataFrame({'Column1': ['Data1'], 'Column2': ['Data2']})

        result = self.lts.save_table(df, "test")

        assert result == True
        assert mock_to_csv.called