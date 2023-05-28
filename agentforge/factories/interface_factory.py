import os
from agentforge.interfaces import MongoDBKVStore, DictKVStore, InMemoryVectorStore, LocalFileStore, DeepLakeVectorStore
from agentforge.interfaces import LLMService, TTSService, W2LService
from agentforge.config import DbConfig
from typing import Any

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
        else:
            raise Exception(f"KVStore {kvstore_type} does not exist")

    def create_filestore(self) -> None:
        filestore_type = os.getenv("FILESTORE_TYPE")
        # Instantiate the correct FileStore based on filestore_type
        if filestore_type == "local":
            self.__interfaces["filestore"] = LocalFileStore(os.getenv("LOCAL_FILESTORE_PATH"))
        else:
            raise Exception(f"FileStore {filestore_type} does not exist")

    def create_service(self, service_type: str) -> None:
        # Instantiate the APIService with the provided APIClient
        if service_type == "llm":
            self.__interfaces["service"] = LLMService()
        elif service_type == "tts":
            self.__interfaces["service"] = TTSService()
        elif service_type == "w2l":
            self.__interfaces["service"] = W2LService()

    def create_embeddings(self) -> None:
        embeddings_type = os.getenv("EMBEDDINGS_TYPE")
        # Instantiate the correct VectorStore based on embeddings_type
        if embeddings_type == "in_memory":
            self.__interfaces["embeddings"] = InMemoryVectorStore()
        else:
            raise Exception(f"Embeddings {embeddings_type} does not exist")

    def create_vectorstore(self) -> None:
        vectorstore_type = os.getenv("VECTORSTORE_TYPE")
        # Instantiate the correct VectorStore based on embeddings_type
        if vectorstore_type == "deeplake":
            deeplake_path = os.getenv("DEEPLAKE_PATH")
            model_name = os.getenv("DEEPLAKE_MODEL_NAME")    
            self.__interfaces["vectorstore"] = DeepLakeVectorStore(model_name, deeplake_path)
        elif vectorstore_type == "in_memory":
            self.__interfaces["vectorstore"] = InMemoryVectorStore()
        else:
            raise Exception(f"VectorStore {vectorstore_type} does not exist")

    def get_interface(self, interface_name: str) -> Any:
        if interface_name in self.__interfaces:
            return self.__interfaces[interface_name]
        else:
            raise Exception(f"Interface {interface_name} does not exist")
