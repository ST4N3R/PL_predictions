from dotenv import load_dotenv
import os


load_dotenv()


URL_BEGGINING = os.getenv("URL_BEGGINING")
DATA_PATH = os.getenv("DATA_PATH")
CURRENT_SEASON = os.getenv("CURRENT_SEASON")