from epl_predictions.src.client.page_user import PageUser
from bs4 import BeautifulSoup


with open("Ipswich-Town-Liverpool-August-17-2024-Premier-League", "r", encoding="utf-8") as f:
    file = f.read()

soup = BeautifulSoup(file, "html.parser")
page_user = PageUser(soup)
element_soup = page_user.get_element_by_xpath("/html/body/div/div/div/div/div/table")

if element_soup:
    print(element_soup.prettify())
else:
    print("Element not found")


# for row in element_soup.find_all("tr"):
#     cols = row.find_all(["th", "td"])
#     print(row)

