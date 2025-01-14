from epl_predictions.src.client.page_user import PageUser
from epl_predictions.src.scrappers.page_scrapper import PageScrapper
from bs4 import BeautifulSoup



page_user = PageUser("https://fbref.com/en/matches/a1d0d529/Ipswich-Town-Liverpool-August-17-2024-Premier-League", "Passing")
soup = page_user.get_soup()

ps = PageScrapper(soup, table_xpath="/html/body/div/div/div/div/div/table")
table = ps.get_table_as_dataframe()

# print(table)

# for row in element_soup.find_all("tr"):
#     cols = row.find_all(["th", "td"])
#     print(row)

