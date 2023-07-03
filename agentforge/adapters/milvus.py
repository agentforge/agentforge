# TODO: Implement milvus vectorstore
from typing import Any, List, Protocol

class MilvusStoreProtocol(Protocol):

    def connections(self, ) -> Anys:
        pass

    def __init__(self, config: Any, reset: bool = False) -> None:
        pass
    
    def search(self, n: int, query: str, filter: dict) -> Any:
        pass

    def add_texts(self, texts: List[str], metadata: List[Any]) -> None:
        pass

    def collection(self, collection_name: str) -> None:
        pass