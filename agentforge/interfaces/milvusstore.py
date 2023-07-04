from typing import Any, List
from pymilvus import Collection
from pymilvus import connections
from agentforge.adapters import MilvusStoreProtocol

class MilvusVectorStore(MilvusStoreProtocol):
   def __init__(self) -> connections:
      connections.connect(
         alias="default", 
         host='localhost', 
         port='19530'
         )
      return connections
   
   def collection(self, collection_name: str) -> None:
      #new_key = str(uuid.uuid64())
      collection_param = {
              "collection_name": collection_name,
              "dimension": 8,
              "index_file_size": 2048,
              "metric_type": MetricType.L2
              }
      connections.create_collection(collection_param)
   
   def search(self, n: int, query: str, collection_name: str) -> Any:
      status, results = connections.search(collection_name, n, [query])
      return results 
   

   def add_texts(self, texts: List[str], metadata: List[Any], collection_name: str) -> None:
      collection = Collection(collection_name)
      collection.insert(texts)