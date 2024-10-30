from unittest.mock import patch, MagicMock
import pytest
import requests
import pandas as pd
from bs4 import BeautifulSoup
from src.scrappers.page_scrapper import PageScrapper
from src.scrappers.results_scrapper import ResultsScrapper


class TestPageScrapper:

    def setup_method(self):
        self.results_scrapper = ResultsScrapper()

    
    def test__remove_all_null_rows(self):
        test_df = pd.DataFrame({'Column1': ['Data1', '', ''], 'Column2': ['Data2', '', 'Data3']})

        result_df = self.results_scrapper._remove_all_null_rows(test_df)

        assert len(result_df) == 2
        assert result_df.iloc[0]['Column1'] == 'Data1'
        assert result_df.iloc[1]['Column2'] == 'Data3'


    def test__change_xG_columns_names_dont_have_xG(self):
        df = pd.DataFrame(columns=['Wk', 'Day', 'Date', 'Time', 'Home', 'Score', 'Away', 'Attendance', 'Venue', 'Referee', 'Match Report', 'Notes'])
        result = self.results_scrapper._change_xG_columns_names(df)
        
        assert 'xG_Home' in result.columns
        assert 'xG_Away' in result.columns


    def test__change_xG_columns_names_have_xG(self):
        df = pd.DataFrame(columns=['Wk', 'Day', 'Date', 'Time', 'Home', 'xG', 'Score', 'xG', 'Away', 'Attendance', 'Venue', 'Referee', 'Match Report', 'Notes'])
        result = self.results_scrapper._change_xG_columns_names(df)
        
        assert 'xG_Home' in result.columns
        assert 'xG_Away' in result.columns
    

    def test__scrapp_match_report_link(self):
        pass


    def test__preprocess_fixtures_df(self):
        pass


    def test__extract_fixtures(self):
        pass


    def test__split_reusults_and_fixtures(self):
        pass


    def test_get_next_fixtures(self):
        pass


    def test__change_season_str_to_int(self):
        start, end = self.results_scrapper._change_seasons_str_to_int("2020-2021", "2021-2022")
        assert start == 2020
        assert end == 2021

    
    def test__validate_season_str(self):
        assert self.results_scrapper._validate_season_str("") == False
        assert self.results_scrapper._validate_season_str("123456789") == False
        assert self.results_scrapper._validate_season_str("12345678-") == False
        assert self.results_scrapper._validate_season_str("1234567-8") == False
        assert self.results_scrapper._validate_season_str("four-four") == False
        assert self.results_scrapper._validate_season_str("2020-2022") == False


    def test_get_previous_fixtures(self):
        pass


    def test_save_table_none_df(self):
        result = self.results_scrapper.save_table(None, "test")

        assert result == False


    @patch.object(pd.DataFrame, 'to_csv')
    def test_save_table_success(self, mock_to_csv):
        df = pd.DataFrame({'Column1': ['Data1'], 'Column2': ['Data2']})

        result = self.results_scrapper.save_table(df, "test")

        assert result == True
        assert mock_to_csv.called