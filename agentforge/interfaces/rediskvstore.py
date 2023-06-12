import redis
from agentforge.adapters import AbstractKVStore
from agentforge.config import DbConfig
from typing import Any, Optional, Dict

class RedisKVStore(AbstractKVStore):
    def __init__(self, config: DbConfig):
        self.db = redis.Redis(host=config.host, port=config.port, db=config.db)

    def get(self, key: str):
        return self.db.get(key)

    def set(self, key: str, value: Any) -> None:
        self.db.set(key, value)

    def delete(self, key: str) -> None:
        self.db.delete(key)

    def get_many(self, filter: Dict[str, Any]) -> Optional[Any]:
        # Redis doesn't natively support querying by filters
        # So we return None. Alternatively, you can implement a filtering logic here
        return None
