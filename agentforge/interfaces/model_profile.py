### For web agentforge ModelProfile data comes from the request but for client production
### systems we will need to do a lookup through the KVStore adapter
from typing import Any, Optional
from agentforge.factories import interface_factory

# Handles key creation, document retrieval and deletion
class ModelProfile():
    def __init__(self):
        self.kvstore = interface_factory.get_interface("kvstore")

    def get(self, user_id: str) -> Optional[Any]:
        # Construct the key for this user and model-config
        cursor = self.kvstore.get_many("model_profiles", {"user_id": user_id})        
        return list(cursor.limit(20))

    def set(self, user_id: str, value: Any) -> None:
        pass

    def delete(self, user_id: str) -> None:
        pass
