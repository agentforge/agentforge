# TODO: Deeplake specific implementation of VectorStore

### Memory Module for the Agent
### This is the neuro-symbolic core for the long-term memory of the agent
### It is responsible for storing and retrieving memories
### similarity functions to access memories and methods to forget
### Forgetting is an important part of learning and memory
import shutil
from typing import Any, List, Dict
from langchain.vectorstores import DeepLake
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.retrievers import TimeWeightedVectorStoreRetriever
from agentforge.adapters import VectorStoreProtocol

class DeepLake(VectorStoreProtocol):
    def __init__(self, model_name: str) -> None:
        # Initialize your vector store here
        self.embdeddings = HuggingFaceEmbeddings(model_name=model_name)

        ### TODO: Remove deletion of directory when runnnig in production
        self.delete()

        # Use deeplake for long-term vector memory storage
        self.deeplake = DeepLake(dataset_path=DEEPLAKE_PATH, embedding_function=self.embdeddings)
        self.retriever = TimeWeightedVectorStoreRetriever(vectorstore=self.deeplake, decay_rate=.0000000000000000000000001, k=4)

    def delete(self) -> None:
        # Delete your vector store here
        try:
            shutil.rmtree(DEEPLAKE_PATH)
            print(f"Directory '{DEEPLAKE_PATH}' has been deleted.")
        except FileNotFoundError:
            print(f"Directory '{DEEPLAKE_PATH}' not found.")
        except Exception as e:
            print(f"Error while deleting directory '{DEEPLAKE_PATH}': {e}")

    def search(self, query: str) -> Any:
        # Perform your search here and return the result
        docs = self.deeplake.search(query)
        return docs

    def add_texts(self, texts: List[str], metadata: List[Any]) -> None:
        # Add your texts here
        return self.deeplake.add_texts([texts], [metadata])
