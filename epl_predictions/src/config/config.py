try:
    from dotenv import load_dotenv
    import os
except:
    pass

try:
    load_dotenv()
except:
    pass

try:
    URL_BEGGINING = os.getenv("URL_BEGGINING")
except:
    URL_BEGGINING = ""

try:
    DATA_PATH = os.getenv("DATA_PATH")
except:
    DATA_PATH = ""

try:
    CURRENT_SEASON = os.getenv("CURRENT_SEASON")
except:
    CURRENT_SEASON = ""

try:
    LEAGUEDB_CONNECTION_STR1 = os.getenv("LEAGUEDB_CONNECTION_STR1")
except:
    LEAGUEDB_CONNECTION_STR1 = ""

try:
    LEAGUEDB_CONTAINER_NAME = os.getenv("LEAGUEDB_CONTAINER_NAME")
except:
    LEAGUEDB_CONTAINER_NAME = ""

try:
    LAST_SCRAPPED_MATCH_DATE = os.getenv("LAST_SCRAPPED_MATCH_DATE")
except:
    LAST_SCRAPPED_MATCH_DATE = ""

try:
    LAST_SCRAPPED_MATCH_HOUR = os.getenv("LAST_SCRAPPED_MATCH_HOUR")
except:
    LAST_SCRAPPED_MATCH_HOUR = ""