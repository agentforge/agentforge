# TODO: Implement generic vectorstore
from typing import Any, List, Protocol

class VectorStoreProtocol(Protocol):
    
    def __init__(self, config: Any) -> None:
        pass
    
    def search(self, n: int, query: str, filter: dict) -> Any:
        pass

    def add_texts(self, texts: List[str], metadata: List[Any]) -> None:
        pass
