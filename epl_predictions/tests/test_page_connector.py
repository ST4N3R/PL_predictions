from unittest.mock import patch, Mock
import pytest
import requests
from bs4 import BeautifulSoup
from src.client.page_connector import PageConnector


class TestPageConnector:
    
    def test_initialization(self):
        url = "http://example.com"
        connector = PageConnector(url)
        assert connector.url == url
        assert isinstance(connector.soup, (BeautifulSoup, type(None)))

    
    @patch("src.client.page_connector.requests.get", 
           return_value=Mock(status_code=200, text="<html><head><title>Test Page</title></head><body></body></html>"))
    def test_make_request_success(self, mock_get):
        connector = PageConnector("http://example.com")
        assert connector.soup is not None
        assert isinstance(connector.soup, BeautifulSoup)
        assert connector.soup.title.string == "Test Page"


    @patch("src.client.page_connector.requests.get", side_effect=requests.exceptions.RequestException("Failed request"))
    def test_make_request_failure(self, mock_get):
        connector = PageConnector("http://invalid-url.com")
        assert connector.soup is None
