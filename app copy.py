import pandas as pd
import numpy as np
from flask import Flask, render_template
from epl_predictions.src.scrappers.results_scrapper import ResultsScrapper
from epl_predictions.src.scrappers.league_table_scrapper import LeagueTableScrapper
from epl_predictions.src.utils.saver import Saver
from epl_predictions.src.config.config import LAST_SCRAPPED_MATCH_DATE, LAST_SCRAPPED_MATCH_HOUR

#ToDo: Add update option, to ResultsScrapper

"""
Oddzielny folder na część wizualną -> dwa foldery, jeden na frontend (flask lub inny framework), a drugi na na backend (skrypty na dane, obrókę oraz uczenie modelu)
"""

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

app = Flask(__name__)

@app.route('/')
def index():
    lts = LeagueTableScrapper()
    rs = ResultsScrapper()
    saver = Saver()

    last_update = 0
    # last_update = LAST_SCRAPPED_MATCH_HOUR + " " + LAST_SCRAPPED_MATCH_DATE
    current_league_table = lts.get_current_league_table()
    matchday_league_table = pd.DataFrame()
    final_league_table = pd.DataFrame()
    next_fixtures = pd.DataFrame(data=np.arange(38), columns=['Round'])
    
    return render_template('index.html', 
                           last_update=last_update, 
                           current_league_table=saver.save_table_to_html(current_league_table, ['index', 'Notes', 'Pts/MP', 'xG', 'xGA', 'xGD', 'xGD/90', 'Last 5', 'Attendance', 'Top Team Scorer', 'Goalkeeper']),
                           matchday_league_table=saver.save_table_to_html(matchday_league_table),
                           final_league_table=saver.save_table_to_html(final_league_table),
                           fixtures=saver.save_table_to_html(next_fixtures))

if __name__ == '__main__':
    app.run(debug=True)