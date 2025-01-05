import pandas as pd
from azure.storage.blob.aio import ContainerClient
from typing import List, Optional
from .setup_logging import setup_logging
from ..config.config import DATA_PATH


class Saver:
    def __init__(self):
        self.logger = setup_logging()


    def save_table_to_file(self, df: pd.DataFrame, name: str) -> bool:
        if df is None:
            self.logger.error("Df is none")
            return False

        #ToDo: Sprawdzać czy ma się dostęp oraz, czy folder istnieje
        df = df.reset_index()
        df.to_csv(DATA_PATH + f"raw/{name}.csv", index=False)
        self.logger.debug(f"Current table saved to {DATA_PATH}/raw")

        return True
    

    def save_table_to_html(self, df: pd.DataFrame, cols_to_delete: Optional[List[str]] = [], classes: str = 'table table-striped', index: bool = False) -> str:
        if df is None:
            self.logger.error("Df is none")
            return ""
        
        df = df.drop(cols_to_delete, axis=1)
        return df.to_html(classes=classes, index=index)
    

    def save_table_to_container(self, df: pd.DataFrame, blob_name: str, container_client: ContainerClient) -> None:
        try:
            blob_client = container_client.get_blob_client(blob_name)
            blob_client.upload_blob(df, overwrite=True)
            self.logger.debug("File uploaded succesfuly!")
        except Exception as e:
            self.logger.error(e)