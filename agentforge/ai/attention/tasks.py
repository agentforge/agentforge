from typing import Any, Dict, Optional
from datetime import datetime
from agentforge.interfaces import interface_interactor
from agentforge.ai.beliefs.symbolic import SymbolicMemory
class TaskManagement:
    def __init__(self) -> None:
        self.db = interface_interactor.get_interface("db")
        self.collection = 'tasks'

    def add_task(self, user_id: str, session_id: str, task_name: str, is_active: bool = True) -> Optional[Any]:
        creation_time = datetime.utcnow().isoformat()
        latest_update_time = creation_time
        task_data = {
            'user_id': user_id,
            'session_id': session_id,
            'task_name': task_name,
            'created_at': creation_time,
            'updated_at': latest_update_time,
            'is_active': is_active
        }
        key = f"{user_id}:{session_id}:{task_name}"
        return self.db.create(self.collection, key, task_data)

    def get_tasks(self, user_id: str, session_id: str, task_name: str) -> Optional[Any]:
        key = f"{user_id}:{session_id}:{task_name}"
        return self.db.get_many(self.collection, {"_id": key })

    def count(self, user_id: str, session_id: str, task_name: str) -> Optional[Any]:
        key = f"{user_id}:{session_id}:{task_name}"
        return self.db.count(self.collection, {"_id": key })

    def update_task(self, user_id: str, session_id: str, task_name: str, is_active = None) -> None:
        task_ = self.get_task(user_id, session_id, task_name)
        print("[task_] get_task:", user_id, session_id, task_name)
        if task_:
            task_['updated_at'] = datetime.utcnow().isoformat()
            print("task_] updaing task_:", is_active)
            if is_active is not None:
                task_['is_active'] = is_active
            key = f"{user_id}:{session_id}:{task_name}"
            self.db.set(self.collection, key, task_)

    def delete_task(self, user_id: str, session_id: str, task_name: str) -> None:
        key = f"{user_id}:{session_id}:{task_name}"
        self.db.delete(self.collection, key)

    def active_task(self, user_id: str, session_id: str) -> bool:
        filter_criteria = {
            'user_id': user_id,
            'session_id': session_id,
            'is_active': True
        }
        print(filter_criteria)
        active_tasks = self.db.get_many(self.collection, filter_criteria)
        for task in active_tasks:
            return task["task_name"]
        return None
