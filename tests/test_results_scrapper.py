from unittest.mock import patch, MagicMock
import pytest
import pandas as pd
from bs4 import BeautifulSoup
from epl_predictions.src.scrappers.page_scrapper import PageScrapper
from epl_predictions.src.scrappers.results_scrapper import ResultsScrapper
from epl_predictions.src.config.config import CURRENT_SEASON


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
    

    def test__scrapp_match_report_link_missing_link(self):
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
        
        result_df = self.results_scrapper._scrapp_match_report_link(pd.DataFrame(), BeautifulSoup(html_content, 'html.parser'))
        test_df = pd.DataFrame(columns=['Match Report'])
        assert len(result_df['Match Report']) == len(test_df['Match Report'])


    def test__scrapp_match_report_link(self):
        html_content = """
                    <html>
                        <body>
                            <table id="test-table">
                                <tr><th>Column1</th><th>Column2</th></tr>
                                <tr><td>Data1</td><td data-stat="match_report"><a href="Data2">Data2</a></td></tr>
                                <tr><td>Data3</td><td data-stat="match_report"><a href="Data4">Data4</a></td></tr>
                            </table>
                        </body>
                    </html>
                    """
        result_df = self.results_scrapper._scrapp_match_report_link(pd.DataFrame(), BeautifulSoup(html_content, 'html.parser'))
        test_df = pd.DataFrame(columns=['Match Report'], data=['Data2', 'Data4'])
        print(result_df)
        print(test_df)
        assert len(result_df['Match Report']) == len(test_df['Match Report'])


    @patch('src.scrappers.results_scrapper.PageConnector')
    @patch('src.scrappers.results_scrapper.PageScrapper')
    @patch('src.scrappers.results_scrapper.ResultsScrapper._preprocess_fixtures_df', return_value = pd.DataFrame({'Column1': ['Data1'], 'Column2': ['Data2']}))
    def test__extract_fixtures(self, MockPreprocess, MockPageScrapper, MockPageConnector):
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
        
        result_df = self.results_scrapper._extract_fixtures("http://mockurl.com", "test-table")
        
        assert MockPageConnector.called
        assert MockPageScrapper.called
        assert MockPreprocess.called
        assert isinstance(result_df, pd.DataFrame)
        assert list(result_df.columns) == ['Column1', 'Column2']
        assert result_df.iloc[0]['Column1'] == 'Data1' and result_df.iloc[0]['Column2'] == 'Data2'


    def test__split_results_and_fixtures(self):
        df = pd.DataFrame({'Score': [None, '2-1', None, '1-1', None]})

        self.results_scrapper._split_results_and_fixtures(df)
        
        print(self.results_scrapper.results_current_season_df)

        assert len(self.results_scrapper.next_fixtures_df) == 3
        assert len(self.results_scrapper.results_current_season_df) == 2
        assert self.results_scrapper.results_current_season_df['Season'].iloc[0] == CURRENT_SEASON


    @patch('src.scrappers.results_scrapper.ResultsScrapper._extract_fixtures', return_value = pd.DataFrame({'Column1': ['Data1', 'Data3', 'Data4'], 'Score': ['Data2', None, None]}))
    def test_get_next_fixtures(self, mock_extract):
        result_df = self.results_scrapper.get_next_fixtures()

        next_fixtures_df = self.results_scrapper.next_fixtures_df
        curr_season_results = self.results_scrapper.results_current_season_df

        assert type(result_df) == pd.DataFrame
        assert len(next_fixtures_df) == 2
        assert len(curr_season_results) == 1
        assert mock_extract.called


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


    @patch('src.scrappers.results_scrapper.ResultsScrapper._extract_fixtures', return_value=pd.DataFrame({'Column1': ['Data_1'], 'Score': ['Data_2']}))
    @patch('src.scrappers.results_scrapper.ResultsScrapper._validate_season_str', return_value=True)
    def test_get_previous_fixtures(self, mock_validate, mock_extract):
        self.results_scrapper.next_fixtures_df = pd.DataFrame({'Column1': ['Data1'], 'Score': ['Data2']})
        self.results_scrapper.results_current_season_df = pd.DataFrame({'Column1': ['Data_3'], 'Score': ['Data_4']})
        result_df = self.results_scrapper.get_previous_fixtures("2022-2023", "2023-2024")

        assert type(result_df) == pd.DataFrame
        assert len(result_df) == 3
        assert mock_extract.called


    def test_save_table_none_df(self):
        result = self.results_scrapper.save_table(None, "test")

        assert result == False


    @patch.object(pd.DataFrame, 'to_csv')
    def test_save_table_success(self, mock_to_csv):
        df = pd.DataFrame({'Column1': ['Data1'], 'Column2': ['Data2']})

        result = self.results_scrapper.save_table(df, "test")

        assert result == True
        assert mock_to_csv.called