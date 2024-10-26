from src.data.table_scrapper import TableScrapper
from src.data.page_scrapper import PageScrapper
from src.data.results_scrapper import ResultsScrapper


# ps = PageScrapper()
# res = ps.get_page_html("https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures")

# print(res.prettify())

# ts = TableScrapper()

# df = ts.get_current_table()
# ts.save_table(df, "current_table")

# df = ts.get_previous_tables()
# ts.save_table(df, "previous_tables")

rs = ResultsScrapper()

df = rs.get_previous_fixtures()

rs.save_table(df, "results")