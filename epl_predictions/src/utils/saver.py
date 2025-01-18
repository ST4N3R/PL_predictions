import pandas as pd
from azure.storage.blob.aio import ContainerClient
from typing import List, Optional
from .setup_logging import setup_logging
from ..config.config import DATA_PATH
from .loader import Loader


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
    

    def _check_blob_instance(self, container_client: ContainerClient, name: str) -> bool:
        names = container_client.list_blob_names()

        if name in names:
            return True
        
        return False


    def _combine_new_and_old_blob(self, df: pd.DataFrame, container_client: ContainerClient, blob_name: str) -> pd.DataFrame:
        loader = Loader()
        old_df = loader.load_table_from_container(blob_name, container_client)

        combined_df = pd.concat([old_df, df]).reset_index(drop=True)

        self.logger.debug(f"Table now have {combined_df.shape[0]} rows")

        return combined_df


    def save_table_to_container(self, df: pd.DataFrame, blob_name: str, container_client: ContainerClient) -> None:
        if self._check_blob_instance(container_client, blob_name):
            df = self._combine_new_and_old_blob(df, container_client, blob_name)

        try:
            blob_client = container_client.get_blob_client(blob_name)
            blob_client.upload_blob(df.to_csv(index_label="index"), overwrite=True)
            self.logger.debug("File uploaded succesfuly!")
        except Exception as e:
            self.logger.error(e)

        return None