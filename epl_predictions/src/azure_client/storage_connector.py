from azure.storage.blob.aio import ContainerClient, BlobServiceClient
from azure.storage.blob import BlobServiceClient
from typing import Tuple
from ..setup_logging import setup_logging
from ..config.config import DATA_PATH, LEAGUEDB_CONNECTION_STR1


class StorageConnector():
    def __init__(self) -> None:
        self.logger = setup_logging()
        self.blob_service_client = None

        try:
            self.blob_service_client = self._conntect_to_blob_service()
            self.logger.debug("Connection went good!")
        except Exception as e:
            self.logger.error(e)


    def _conntect_to_blob_service(self) -> BlobServiceClient:
        blob_client = BlobServiceClient.from_connection_string(LEAGUEDB_CONNECTION_STR1)
        return blob_client


    def conntect_to_container(self, container_name: str) -> ContainerClient:
        container_client = self.blob_service_client.get_container_client(container_name)
        return container_client
    

    def save_to_cantainer(self, path: str, blob_name: str, container_client: ContainerClient) -> None:
        file_path = DATA_PATH + path

        try:
            blob_client = container_client.get_blob_client(blob_name)
            with open(file_path, "rb") as data:
                blob_client.upload_blob(data, overwrite=True)
            self.logger.debug("File uploaded succesfuly!")
        except Exception as e:
            self.logger.error(e)