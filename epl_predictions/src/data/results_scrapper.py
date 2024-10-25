from typing import Optional
from src.data.page_scrapper import PageScrapper
from src.setup_logging import setup_logging


class ResultsScrapper:
    def __init__(self) -> None:
        self.logger = setup_logging()


    def _extract_table_data(self, table) -> list:
        rows = []
        for row in table.find_all('tr'):
            cols = row.find_all(['th', 'td'])
            if cols:
                row_data = [col.text.strip() for col in cols]
                rows.append(row_data)
        return rows


    def _get_season_fixtures(self, season: Optional[str]):
        if season == None:
            url = "https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures"
            table_id = "sched_2024-2025_9_1"
        else:
            url = f"https://fbref.com/en/comps/9/{season}/schedule/{season}-Premier-League-Scores-and-Fixtures"
            table_id = f"sched_{season}_9_1"


        pageScrapper = PageScrapper()
        soup = pageScrapper.get_page_html(url=url)
        table = soup.find('table', {'id': table_id})

        if table is None:
            self.logger.error("Couldn't find the fixtures table")

        rows = self._extract_table_data(table)