import uuid
import base64
import threading
from typing import Optional
from agentforge.adapters import AbstractKVStore
    
### Generates keys for the database
### This is a simple setup that can scale initially but needs
### to be replaced with a more robust solution that does not use
### a lock
class DBKeyGenerator:
    def __init__(self, kvstore: AbstractKVStore):
        self.kvstore = kvstore
        self.lock = threading.Lock()

    def _generate_key(self) -> str:
        return base64.urlsafe_b64encode(uuid.uuid4().bytes).decode('utf-8').rstrip('=\n')

    def _check_key_exists(self, key: str) -> bool:
        return self.kvstore.get(key) is not None

    def _store_key(self, key: str) -> None:
        self.kvstore.set(key, True)

    def get_unique_key(self) -> Optional[str]:
        for _ in range(5):  # Try up to 5 times
            with self.lock:
                new_key = self._generate_key()
                if not self._check_key_exists(new_key):
                    self._store_key(new_key)
                    return new_key
        raise Exception('Failed to generate unique key after multiple attempts')
