import pandas as pd
import numpy as np
import streamlit as st

#ToDo: Add update option, to ResultsScrapper

# Oddzielny folder na część wizualną -> dwa foldery, jeden na frontend (flask lub inny framework), a drugi na na backend (skrypty na dane, obrókę oraz uczenie modelu)

def test_files():
    pass
    # url = URL_BEGGINING + "/en/comps/9/Premier-League-Stats"
    # table_id = "results2024-202591_overall"

    # pc = PageConnector(url)
    # page = pc.get_page()

    # ps = PageScrapper(url, table_id)
    # df = ps.get_table_as_dataframe()

    # lts = LeagueTableScrapper()
    # df = lts.get_current_league_table()
    # lts.save_table(df, "current_table")

    # url = URL_BEGGINING + "/en/comps/9/schedule/Premier-League-Scores-and-Fixtures"
    # table_id = "sched_2024-2025_9_1"

    # rs = ResultsScrapper()
    # df = rs.get_previous_fixtures()
    # rs.save_table(df, "results")

    # print(df)

    # sc = StorageConnector()

    # container = sc.conntect_to_container("raw")
    # sc.save_to_cantainer("/raw/results.csv", "results.csv", container)

dashboard_page = st.Page("epl_predictions/pages/dashboard.py", title="Dashboard")
data_page = st.Page("epl_predictions/pages/data.py", title="Data")

pg = st.navigation([dashboard_page, data_page])
pg.run()