# TODO: Implement generic kvstore -- i.e. MongoDB
# NoSQL specific code

from typing import Any, Optional, Protocol
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
