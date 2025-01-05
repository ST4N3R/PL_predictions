import pandas as pd
from azure.storage.blob.aio import ContainerClient
from .setup_logging import setup_logging
from ..config.config import DATA_PATH


class Loader():
    def __init__(self):
        self.logger = setup_logging()


    def load_table_from_file(self, name: str) -> pd.DataFrame:
        try:
            df = pd.read_csv(DATA_PATH + f"raw/{name}.csv")
            self.logger.debug(f"File {name} loaded successfully")
            return df
        except Exception as e:
            self.logger.error(e)
            return pd.DataFrame()
        
    
    def load_table_from_container(self, blob_name: str, container_client: ContainerClient) -> pd.DataFrame:
        try:
            blob_client = container_client.get_blob_client(blob_name)
            df = blob_client.download_blob()
            self.logger.debug("File downloaded succesfuly!")
            return df
        except Exception as e:
            self.logger.error(e)
            return pd.DataFrame()