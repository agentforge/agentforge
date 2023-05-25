# TODO: Implment ModelProfile <-> KVStore
### For web agentforge ModelProfile data comes from the request but for client production
### systems we will need to do a lookup through the KVStore adapter
from typing import Any

class ModelProfile():
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        pass