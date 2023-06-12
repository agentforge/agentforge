# NoSQL specific code

from typing import Any, Optional, Protocol, Dict
from agentforge.config import DbConfig

class DB(Protocol):
    
    def connection(self, config: DbConfig) -> None:
        pass

    def get(self, collection: str, key: str) -> Optional[Any]:
        pass

    def set(self, collection: str, key: str, data: dict) -> None:
        pass

    def delete(self, collection: str, key: str) -> None:
        pass

    def get_many(self, collection: str, filter: Dict[str, Any]) -> Optional[Any]:
        pass
