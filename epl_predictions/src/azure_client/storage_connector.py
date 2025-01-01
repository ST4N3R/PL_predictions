import pandas as pd
from azure.storage.blob.aio import ContainerClient, BlobServiceClient
from azure.storage.blob import BlobServiceClient
from typing import Tuple
from ..utils.setup_logging import setup_logging
from ..config.config import LEAGUEDB_CONNECTION_STR1


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