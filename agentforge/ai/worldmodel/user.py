# TODO: Implment User <-> KVStore


### Basically a way for the AI to access the user's data
### that is not stored via the language model embeddings
### i.e. the user's name, age, etc.

from typing import Any

class User():
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        pass