from dotenv import load_dotenv
import os

from agentforge.adapters import APIClient
from agentforge.interfaces import MongoDBKVStore, DictKVStore, InMemoryVectorStore, APIService, LocalFileStore
from typing import Any

class InterfaceFactory:
    def __init__(self) -> None:
        self.__interfaces: dict[str, Any] = {}

    def create_kvstore(self, kvstore_type: str) -> None:
        # Instantiate the correct KVStore based on kvstore_type
        if kvstore_type == "mongodb":
            self.__interfaces["kvstore"] = MongoDBKVStore()
        elif kvstore_type == "dict":
            self.__interfaces["kvstore"] = DictKVStore()

    def create_filestore(self, filestore_type: str) -> None:
        # Instantiate the correct FileStore based on filestore_type
        if filestore_type == "local":
            self.__interfaces["filestore"] = LocalFileStore()

    def create_service(self, api_client: APIClient) -> None:
        # Instantiate the APIService with the provided APIClient
        self.__interfaces["service"] = APIService(api_client)

    def create_embeddings(self, embeddings_type: str) -> None:
        # Instantiate the correct VectorStore based on embeddings_type
        if embeddings_type == "in_memory":
            self.__interfaces["embeddings"] = InMemoryVectorStore()

    def get_interface(self, interface_name: str) -> Any:
        if interface_name in self.__interfaces:
            return self.__interfaces[interface_name]
        else:
            raise Exception(f"Interface {interface_name} does not exist")