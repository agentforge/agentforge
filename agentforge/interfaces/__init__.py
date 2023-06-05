import os
from .deeplake import DeepLakeVectorStore
from .dictkvstore import DictKVStore
from .inmemoryvectorstore import InMemoryVectorStore
from .mongodb import MongoDBKVStore
from .localfilestore import LocalFileStore
from .api import LLMService, TTSService, W2LService
from agentforge.interfaces.interface_factory import InterfaceFactory
from .rediskvstore import RedisKVStore

RESOURCE = os.environ.get('RESOURCE')

if RESOURCE == "AGENT":
    interface_interactor = InterfaceFactory()
    interface_interactor.create_db()
    interface_interactor.create_kvstore()
    interface_interactor.create_filestore()
    interface_interactor.create_vectorstore()
    interface_interactor.create_working_memory()
    interface_interactor.create_keygenerator() # requires kvstore
    interface_interactor.create_service("llm")
    interface_interactor.create_service("tts")
    interface_interactor.create_service("w2l")

__all__ = ["DeepLakeVectorStore", "DictKVStore", "InMemoryVectorStore", "MongoDBKVStore", "LocalFileStore",
            "LLMService", "TTSService", "W2LService", "interface_interactor", "RedisKVStore"]