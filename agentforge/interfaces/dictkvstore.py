from agentforge.adapters import AbstractKVStore

# Simple implementation of a key-value store using a dictionary
class DictKVStore(AbstractKVStore):
    def __init__(self):
        self.dict = {}

    def get(self, key):
        return self.dict.get(key)

    def set(self, key, value):
        self.dict[key] = value

    def delete(self, key):
        if key in self.dict:
            del self.dict[key]
