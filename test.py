from epl_predictions.src.azure_client.storage_connector import StorageConnector
from epl_predictions.src.utils.loader import Loader
from bs4 import BeautifulSoup
import pandas as pd





sc = StorageConnector()
container = sc.conntect_to_container("final")

loader = Loader()
df = loader.load_table_from_container("results.csv", container)

print(df.head())