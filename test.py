from epl_predictions.src.azure_client.storage_connector import StorageConnector
from epl_predictions.src.utils.saver import Saver
from bs4 import BeautifulSoup
import pandas as pd

# Dane w formacie list
data = {
    "index": [0, 1, 2, 3, 4],
    "Wk": [1, 1, 1, 1, 1],
    "Day": ["Sat", "Sat", "Sat", "Sat", "Sat"],
    "Date": ["1995-08-19", "1995-08-19", "1995-08-19", "1995-08-19", "1995-08-19"],
    "Time": ["", "", "", "", ""],
    "Home": ["Southampton", "Newcastle Utd", "Wimbledon", "Liverpool", "West Ham"],
    "Score": ["3–4", "3–0", "3–2", "1–0", "1–2"],
    "Away": ["Nott'ham Forest", "Coventry City", "Bolton", "Sheffield Weds", "Leeds United"],
    "Attendance": ["15,164", "36,485", "9,317", "40,535", "22,901"],
    "Venue": ["The Dell", "St. James' Park", "Selhurst Park", "Anfield", "Boleyn Ground"],
    "Referee": ["Gary Willard", "Roger Dilkes", "Keith Cooper", "Paul Durkin", "Keith Burge"],
    "Match Report": [
        "",
        "",
        "",
        "",
        ""
    ],
    "Notes": ["", "", "", "", ""],
    "xG_Home": ["", "", "", "", ""],
    "xG_Away": ["", "", "", "", ""],
    "Season": ["1995-1996", "1995-1996", "1995-1996", "1995-1996", "1995-1996"]
}

# Tworzenie DataFrame z danych w formacie list
df = pd.DataFrame(data)
df = df.set_index('index', drop=True)

# Wyświetlanie DataFrame
print(df)

sc = StorageConnector()
container = sc.conntect_to_container("raw")

saver = Saver()
saver.save_table_to_container(df, "results.csv", container)