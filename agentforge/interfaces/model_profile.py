### For web agentforge ModelProfile data comes from the request but for client production
### systems we will need to do a lookup through the KVStore adapter
from typing import Any, Optional, Dict
from agentforge.interfaces import interface_interactor

# Handles key creation, document retrieval and deletion
class ModelProfile():
    def __init__(self):
        self.db = interface_interactor.get_interface("db")
        self.keygen = interface_interactor.get_interface("keygen")

    def create(self, data: Dict) -> None:
        id = self.keygen.generate()
        return self.set(id, data)

    def get(self, id: str) -> Optional[Any]:
        # Construct the key for this user and model-config
        cursor = self.db.get_many("model_profiles", {"_id": id})        
        return {"data": list(cursor.limit(20))}

    def get_by_user(self, id: str) -> Optional[Any]:
        # Construct the key for this user and model-config
        cursor = self.db.get_many("model_profiles", {"user_id": id})        
        return {"data": list(cursor.limit(20))}

    def set(self, id: str, data: Dict) -> None:
        self.db.set("model_profiles", id, data)
        return {"data": data}

    def delete(self, id: str) -> None:
        self.db.delete("model_profiles", id)
        return {}
