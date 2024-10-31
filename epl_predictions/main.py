from src.client.page_connector import PageConnector
from src.scrappers.page_scrapper import PageScrapper
from src.scrappers.league_table_scrapper import LeagueTableScrapper
from src.scrappers.results_scrapper import ResultsScrapper
import pandas as pd
from src.config.config import URL_BEGGINING


#ToDo: Fix connection problems with fbref
#ToDo: ?Add form column
#ToDo: ?Add form between clubs column
#ToDo: Add update option, to ResultsScrapper
#ToDo: Uzupełnić NULL w xG -> na liczbę goli


"""
Oddzielny folder na część wizualną -> dwa foldery, jeden na frontend (flask lub inny framework), a drugi na na backend (skrypty na dane, obrókę oraz uczenie modelu)
"""


url = URL_BEGGINING + "/en/comps/9/Premier-League-Stats"
table_id = "results2024-202591_overall"

# pc = PageConnector(url)
# page = pc.get_page()

# ps = PageScrapper(url, table_id)
# df = ps.get_table_as_dataframe()

# lts = LeagueTableScrapper()
# df = lts.get_current_league_table()
# lts.save_table(df, "current_table")

# url = URL_BEGGINING + "/en/comps/9/schedule/Premier-League-Scores-and-Fixtures"
# table_id = "sched_2024-2025_9_1"

rs = ResultsScrapper()
df = rs.get_previous_fixtures()
rs.save_table(df, "results")

# print(df)