import pandas as pd
import streamlit as st
from epl_predictions.src.utils.loader import Loader
from epl_predictions.src.azure_client.storage_connector import StorageConnector


st.title("Data")


sc = StorageConnector()
container = sc.conntect_to_container("final")

loader = Loader()
df = loader.load_table_from_file("final/results_league_table.csv")

df.set_index("index", inplace=True)

st.dataframe(df)