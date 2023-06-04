from .deeplake import DeepLakeVectorStore
from .dictkvstore import DictKVStore
from .inmemoryvectorstore import InMemoryVectorStore
from .mongodb import MongoDBKVStore
from .localfilestore import LocalFileStore
from .barktts.resource import BarkTextToSpeech
from .localllm.resource import LocalLLM
from .wav2lip.resource import Wav2LipModel
from .tts.resource import TextToSpeech
from .api import LLMService, TTSService, W2LService
from agentforge.interfaces.interface_factory import InterfaceFactory
from .rediskvstore import RedisKVStore
# from .dbkeygenerator import DBKeyGenerator

interface_interactor = InterfaceFactory()

interface_interactor.create_db()
interface_interactor.create_kvstore()
interface_interactor.create_filestore()
interface_interactor.create_vectorstore()
interface_interactor.create_session_memory()
interface_interactor.create_keygenerator() # requires kvstore

interface_interactor.create_service("llm")
interface_interactor.create_service("tts")
interface_interactor.create_service("w2l")

__all__ = ["DeepLakeVectorStore", "DictKVStore", "InMemoryVectorStore", "MongoDBKVStore", "LocalFileStore", "BarkTextToSpeech",
            "LocalLLM", "Wav2LipModel", "TextToSpeech", "LLMService", "TTSService", "W2LService", "interface_interactor", "RedisKVStore"]