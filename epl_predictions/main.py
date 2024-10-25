from src.data.table_scrapper import TableScrapper
from src.data.page_scrapper import PageScrapper


ps = PageScrapper()
res = ps.get_page_html("https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures")