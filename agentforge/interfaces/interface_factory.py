import os, importlib
from agentforge.config import DbConfig, RedisConfig
from typing import Any

class InterfaceFactory:
    def __init__(self) -> None:
        self.__interfaces: dict[str, Any] = {}
        self.config = DbConfig.from_env()
        self.redis_config = RedisConfig.from_env()

    def create_db(self) -> None:
        db_type = os.getenv("DB_TYPE")
        # Instantiate the correct Database based on db_type
        if db_type == "mongodb":
            MongoDBKVStore = getattr(importlib.import_module('agentforge.interfaces.mongodb'), 'MongoDBKVStore')
            self.__interfaces["db"] = MongoDBKVStore(self.config)
        else:
            raise Exception(f"DB {db_type} does not exist")

    def create_kvstore(self) -> None:
        kvstore_type = os.getenv("KVSTORE_TYPE")
        # Instantiate the correct KVStore based on kvstore_type
        if kvstore_type == "redis":
            RedisKVStore = getattr(importlib.import_module('agentforge.interfaces.rediskvstores'), 'RedisKVStore')
            self.__interfaces["kvstore"] = RedisKVStore(self.redis_config)
        elif kvstore_type == "dict":
            DictKVStore = getattr(importlib.import_module('agentforge.interfaces.dictkvstore'), 'DictKVStore')
            self.__interfaces["kvstore"] = DictKVStore()
        else:
            raise Exception(f"KVStore {kvstore_type} does not exist")

    def create_working_memory(self) -> None:
        working_type = os.getenv("WORKING_MEMORY_TYPE")
        # Instantiate the correct KVStore based on kvstore_type
        if working_type == "mongodb":
            MongoMemory = getattr(importlib.import_module('agentforge.interfaces.mongomemory'), 'MongoMemory')
            self.__interfaces["working_memory"] = MongoMemory(self.config)
        else:
            raise Exception(f"Working memory type {working_type} does not exist")

    def create_filestore(self) -> None:
        filestore_type = os.getenv("FILESTORE_TYPE")
        # Instantiate the correct FileStore based on filestore_type
        if filestore_type == "local":
            LocalFileStore = getattr(importlib.import_module('agentforge.interfaces.localfilestore'), 'LocalFileStore')
            self.__interfaces["filestore"] = LocalFileStore(os.getenv("LOCAL_FILESTORE_PATH"))
        else:
            raise Exception(f"FileStore {filestore_type} does not exist")

    def create_service(self, service_type: str) -> None:
        # Instantiate the APIService with the provided APIClient
        if service_type == "llm":
            LLMService = getattr(importlib.import_module('agentforge.interfaces.api'), 'LLMService')
            self.__interfaces["llm"] = LLMService()
        elif service_type == "tts":
            TTSService = getattr(importlib.import_module('agentforge.interfaces.api'), 'TTSService')
            self.__interfaces["tts"] = TTSService()
        elif service_type == "w2l":
            W2LService = getattr(importlib.import_module('agentforge.interfaces.api'), 'W2LService')
            self.__interfaces["w2l"] = W2LService()
        else:
            raise Exception(f"Service {service_type} does not exist")

    def create_vectorstore(self) -> None:
        vectorstore_type = os.getenv("VECTORSTORE_TYPE")
        # Instantiate the correct VectorStore based on VECTORSTORE_TYPE
        if vectorstore_type == "deeplake":
            deeplake_path = os.getenv("DEEPLAKE_PATH")
            model_name = os.getenv("DEEPLAKE_MODEL_NAME")
            DeepLakeVectorStore = getattr(importlib.import_module('agentforge.interfaces.deeplake'), 'DeepLakeVectorStore')
            VectorStoreMemory = getattr(importlib.import_module('agentforge.interfaces.vectorstorememory'), 'VectorStoreMemory')
            self.__interfaces["vectorstore"] = DeepLakeVectorStore(model_name, deeplake_path)
            self.__interfaces["vectorstore_memory"] = VectorStoreMemory(self.__interfaces["vectorstore"])
        elif vectorstore_type == "in_memory":
            self.__interfaces["vectorstore"] = InMemoryVectorStore()
        else:
            raise Exception(f"VectorStore {vectorstore_type} does not exist")

    def create_keygenerator(self) -> None:
        keygenerator_type = os.getenv("KEYGENERATOR_TYPE")
        # Instantiate the correct KeyGenerator based on keygenerator_type
        if keygenerator_type == "redis":
            DBKeyGenerator = getattr(importlib.import_module('agentforge.interfaces.dbkeygenerator'), 'DBKeyGenerator')
            self.__interfaces["keygen"] = DBKeyGenerator(self.__interfaces["kvstore"])
        else:
            raise Exception(f"KeyGenerator {keygenerator_type} does not exist")    

    def get_interface(self, interface_name: str) -> Any:
        if interface_name in self.__interfaces:
            return self.__interfaces[interface_name]
        else:
            raise Exception(f"Interface {interface_name} does not exist")
