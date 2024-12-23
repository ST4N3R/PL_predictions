from dotenv import load_dotenv
import os


load_dotenv()


URL_BEGGINING = os.getenv("URL_BEGGINING")
DATA_PATH = os.getenv("DATA_PATH")
CURRENT_SEASON = os.getenv("CURRENT_SEASON")
LEAGUEDB_CONNECTION_STR1 = os.getenv("LEAGUEDB_CONNECTION_STR1")
LEAGUEDB_CONTAINER_NAME = os.getenv("LEAGUEDB_CONTAINER_NAME")
LAST_SCRAPPED_MATCH_DATE = os.getenv("LAST_SCRAPPED_MATCH_DATE")
LAST_SCRAPPED_MATCH_HOUR = os.getenv("LAST_SCRAPPED_MATCH_HOUR")