import os

from agentforge.adapters import APIClient
from agentforge.interfaces import MongoDBKVStore, DictKVStore, InMemoryVectorStore, APIService, LocalFileStore, DeepLake
from agentforge.config import DbConfig
from typing import Any

### ResourceFactory brings together the resources and adapters
### to provide access to either local GPU containers or remote
class InterfaceFactory:
    def __init__(self) -> None:
        self.__interfaces: dict[str, Any] = {}
        self.config = DbConfig.from_env()

    def create_kvstore(self) -> None:
        kvstore_type = os.getenv("KVSTORE_TYPE")
        # Instantiate the correct KVStore based on kvstore_type
        if kvstore_type == "mongodb":
            self.__interfaces["kvstore"] = MongoDBKVStore(self.config)
        elif kvstore_type == "dict":
            self.__interfaces["kvstore"] = DictKVStore()

    def create_filestore(self) -> None:
        filestore_type = os.getenv("FILESTORE_TYPE")
        # Instantiate the correct FileStore based on filestore_type
        if filestore_type == "local":
            self.__interfaces["filestore"] = LocalFileStore(os.getenv("LOCAL_FILESTORE_PATH"))

    def create_service(self) -> None:
        api_client = APIClient()
        # Instantiate the APIService with the provided APIClient
        self.__interfaces["service"] = APIService(api_client)

    def create_embeddings(self) -> None:
        embeddings_type = os.getenv("EMBEDDINGS_TYPE")
        # Instantiate the correct VectorStore based on embeddings_type
        if embeddings_type == "in_memory":
            self.__interfaces["embeddings"] = InMemoryVectorStore()

    def create_vectorstore(self) -> None:
        vectorstore_type = os.getenv("VECTORSTORE_TYPE")
        # Instantiate the correct VectorStore based on embeddings_type
        if vectorstore_type == "deeplake":
            self.__interfaces["vectorstore"] = DeepLake()
        elif vectorstore_type == "in_memory":
            self.__interfaces["vectorstore"] = InMemoryVectorStore()

    def get_interface(self, interface_name: str) -> Any:
        if interface_name in self.__interfaces:
            return self.__interfaces[interface_name]
        else:
            raise Exception(f"Interface {interface_name} does not exist")
