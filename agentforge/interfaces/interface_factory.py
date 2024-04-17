import os, importlib, redis
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
            RedisKVStore = getattr(importlib.import_module('agentforge.interfaces.rediskvstore'), 'RedisKVStore')
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

    def create_image_generator(self, generator_type: str) -> None:
        if generator_type == "pixart":
            pixArtService = getattr(importlib.import_module('agentforge.interfaces.api'), 'PixArtService')
            self.__interfaces["image_gen"] = pixArtService()
        else:
            raise Exception(f"Service {generator_type} does not exist")

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
        elif service_type == "vllm":
            vLLMService = getattr(importlib.import_module('agentforge.interfaces.api'), 'vLLMService')
            self.__interfaces["llm"] = vLLMService()
        elif service_type == "tokenizer":
            TokenizerService = getattr(importlib.import_module('agentforge.interfaces.api'), 'TokenizerService')
            self.__interfaces["tokenizer"] = TokenizerService()
        # elif service_type == "vqa":
        #     W2LService = getattr(importlib.import_module('agentforge.interfaces.api'), 'VQAService')
        #     self.__interfaces["vqa"] = VQAService()
        else:
            raise Exception(f"Service {service_type} does not exist")

    def create_vectorstore(self) -> None:
        vectorstore_type = os.getenv("VECTORSTORE_TYPE")
        ### Delete Vectorstore memory if refresh is set to true -- DESTRUCTIVE DEV CONFIG ONLY
        reset = os.getenv("VECTORSTORE_REFRESH").lower() in ["true", "y", "1", 1]
        dev = os.getenv("AGENTFORGE_ENV").lower() in ["test", "dev"]

        # Instantiate the deeplake VectorStore running locally on the AgentForge
        if vectorstore_type == "deeplake":
            deeplake_path = os.getenv("DEEPLAKE_PATH")
            model_name = os.getenv("VECTOR_EMBEDDINGS_MODEL_NAME")
            DeepLakeVectorStore = getattr(importlib.import_module('agentforge.interfaces.deeplake'), 'DeepLakeVectorStore')
            VectorStoreMemory = getattr(importlib.import_module('agentforge.interfaces.vectorstorememory'), 'VectorStoreMemory')
            self.__interfaces["vectorstore"] = DeepLakeVectorStore(model_name, deeplake_path, reset=(reset and dev))
            self.__interfaces["vectorstore_memory"] = VectorStoreMemory(self.__interfaces["vectorstore"])
        # Requires Remote Milvus Server
        elif vectorstore_type == "milvus":
            milvus_collection = os.getenv("MILVUS_COLLECTION")
            model_name = os.getenv("VECTOR_EMBEDDINGS_MODEL_NAME")
            MilvusVectorStore = getattr(importlib.import_module('agentforge.interfaces.milvusstore'), 'MilvusVectorStore')
            VectorStoreMemory = getattr(importlib.import_module('agentforge.interfaces.vectorstorememory'), 'VectorStoreMemory')
            self.__interfaces["vectorstore"] = MilvusVectorStore(model_name, milvus_collection, reset=(reset and dev))
            self.__interfaces["vectorstore_memory"] = VectorStoreMemory(self.__interfaces["vectorstore"])
        # Simple in-memory vector store -- not persistent
        elif vectorstore_type == "in_memory":
            InMemoryVectorStore = getattr(importlib.import_module('agentforge.interfaces.inmemoryvectorstore'), 'InMemoryVectorStore')
            self.__interfaces["vectorstore"] = InMemoryVectorStore()    
            VectorStoreMemory = getattr(importlib.import_module('agentforge.interfaces.vectorstorememory'), 'VectorStoreMemory')
            self.__interfaces["vectorstore_memory"] = VectorStoreMemory(self.__interfaces["vectorstore"])
        else:
            raise Exception(f"VectorStore {vectorstore_type} does not exist")
    
    # Default redis_store for streaming
    def create_redis_connection(self) -> None:
        # Check if the environment variables are provided
        if self.redis_config.host is None:
            raise ValueError("Environment variable REDIS_HOST is not set")
        if self.redis_config.port is None:
            raise ValueError("Environment variable REDIS_PORT is not set")
        if self.redis_config.db is None:
            raise ValueError("Environment variable REDIS_DB is not set")

        # Try to convert redis_db to integer
        try:
            redis_db = int(self.redis_config.db)
        except ValueError:
            raise ValueError("Environment variable REDIS_DB should be an integer")

        # Create the Redis connection
        redis_store = redis.StrictRedis(host=self.redis_config.host, port=self.redis_config.port, db=self.redis_config.db)
        
        return redis_store

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
