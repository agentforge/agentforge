# TODO: Implement generic kvstore
# NoSQL specific code

from typing import Any, Optional, Protocol, Dict
from agentforge.config import DbConfig

class AbstractKVStore(Protocol):
    
    def connection(self, config: DbConfig) -> None:
        pass

    def get(self, key: str) -> Optional[Any]:
        pass

    def set(self, key: str, value: Any) -> None:
        pass

    def delete(self, key: str) -> None:
        pass

    def get_many(self, filter: Dict[str, Any]) -> Optional[Any]:
        pass
