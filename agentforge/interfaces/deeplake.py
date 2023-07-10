# TODO: Deeplake specific implementation of VectorStore

### Memory Module for the Agent
### This is the neuro-symbolic core for the long-term memory of the agent
### It is responsible for storing and retrieving memories
### similarity functions to access memories and methods to forget
### Forgetting is an important part of learning and memory
import shutil
from typing import Any, List, Optional, Dict
from langchain.vectorstores import DeepLake
from langchain.embeddings import HuggingFaceEmbeddings
from agentforge.adapters import VectorStoreProtocol

class DeepLakeVectorStore(VectorStoreProtocol):
    def __init__(self, model_name: str, deeplake_path: str, reset: bool) -> None:
        # Initialize your vector store here
        self.embdeddings = HuggingFaceEmbeddings(model_name=model_name)
        self.deeplake_path = deeplake_path
        if reset:
            self.delete()

        # Use deeplake for long-term vector memory storage
        self.deeplake = DeepLake(dataset_path=deeplake_path, embedding_function=self.embdeddings)

    def delete(self) -> None:
        # Delete your vector store here
        try:
            shutil.rmtree(self.deeplake_path)
            print(f"Directory '{self.deeplake_path}' has been deleted.")
        except FileNotFoundError:
            print(f"Directory '{self.deeplake_path}' not found.")
        except Exception as e:
            print(f"Error while deleting directory '{self.deeplake_path}': {e}")

    def search(self, query: str, n: int = 4, **kwargs) -> Any:
        # Perform your search here and return the result
        try:
            docs = self.deeplake.similarity_search(query, n, **kwargs)
        except ValueError as e:
            # Vectorstore is empty
            docs = []
        return docs
    
    def search_with_score(self, query: str, k: int = 4, distance_metric: str = "cos", **kwargs) -> Any:
        # Perform your search here and return the result
        try:
            docs = self.deeplake.similarity_search_with_score(query=query, k=k, distance_metric=distance_metric)
        except ValueError as e:
            # Vectorstore is empty
            docs = []
        return docs

    def add_texts(self, texts: List[str], metadata: List[Any]) -> None:
        return self.deeplake.add_texts(texts, metadata)
