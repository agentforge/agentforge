# TODO: Implement generic vectorstore
from typing import Any, List, Protocol

class VectorStoreProtocol(Protocol):
    
    def __init__(self, config: Any, reset: bool = False) -> None:
        pass
    
    def search(self, query: str, n: int, filter: dict, **kwargs) -> Any:
        pass

    def search_with_score(self, query: str, n: int, filter: dict, **kwargs) -> Any:
        pass

    def add_texts(self, texts: List[str], metadata: List[Any], **kwargs) -> None:
        pass
