from typing import Any, List
from langchain.vectorstores import Milvus
from agentforge.adapters import VectorStoreProtocol
from langchain.embeddings import HuggingFaceEmbeddings
from agentforge.utils import logger

class MilvusVectorStore(VectorStoreProtocol):
   def __init__(self, model_name: str, collection: str, reset: bool = False):
      encode_kwargs = {'normalize_embeddings': True}
      self.embdeddings = HuggingFaceEmbeddings(model_name=model_name, encode_kwargs=encode_kwargs)
      self.reset = reset
      self.collection = None
      # self.init_store_connection(collection, force=True)

   def init_store_connection(self, collection: str, force: bool = False):
      connection_args = {
         "host": "milvus",
         "port": "19530",
      }
      milvus_store = Milvus(
         embedding_function = self.embdeddings, 
         collection_name = collection,
         connection_args = connection_args,
         # drop_old = self.reset,
      )
      # Default search params when one is not provided.
      milvus_store.default_search_params = {
         "IVF_FLAT": {"metric_type": "IP", "params": {"nprobe": 10}},
         "IVF_SQ8": {"metric_type": "IP", "params": {"nprobe": 10}},
         "IVF_PQ": {"metric_type": "IP", "params": {"nprobe": 10}},
         "HNSW": {"metric_type": "IP", "params": {"ef": 10}},
         "RHNSW_FLAT": {"metric_type": "IP", "params": {"ef": 10}},
         "RHNSW_SQ": {"metric_type": "IP", "params": {"ef": 10}},
         "RHNSW_PQ": {"metric_type": "IP", "params": {"ef": 10}},
         "IVF_HNSW": {"metric_type": "IP", "params": {"nprobe": 10, "ef": 10}},
         "ANNOY": {"metric_type": "IP", "params": {"search_k": 10}},
         "AUTOINDEX": {"metric_type": "IP", "params": {}},
      }
      milvus_store.index_params = {
         "metric_type": "IP",
         "index_type": "HNSW",
         "params": {"M": 8, "efConstruction": 64},
      }
      return milvus_store

   def search(self, query: str, n: int = 4, **kwargs) -> Any:
      # Perform your search here and return the result
      milvus_store = self.init_store_connection(kwargs["collection"])
      # try:
      docs = milvus_store.similarity_search(query, n)
      # except ValueError as e:
      #    # Vectorstore is empty
      #    logger.info(e)
      #    docs = []
      return docs

   def search_with_score(self, query: str, k: int = 4, **kwargs) -> Any:
      # Perform your search here and return the result
      milvus_store = self.init_store_connection(kwargs["collection"])
      try:
         docs = milvus_store.similarity_search_with_score(query=query, k=k)
      except ValueError as e:
         logger.info(e)
         # Vectorstore is empty
         docs = []
      return docs

   def add_texts(self, texts: List[str], metadata: List[Any], **kwargs) -> None:
      milvus_store = self.init_store_connection(kwargs["collection"])
      return milvus_store.add_texts(texts, metadata)
