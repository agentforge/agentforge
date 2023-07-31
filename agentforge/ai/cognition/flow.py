from typing import Any, Dict, Optional
from datetime import datetime
from agentforge.interfaces import interface_interactor

class FlowManagement:
    def __init__(self) -> None:
        self.db = interface_interactor.get_interface("db")
        self.collection = 'flows'

    def register_flow(self, user_id: str, session_id: str, flow_name: str, is_active: bool = True) -> Optional[Any]:
        creation_time = datetime.utcnow().isoformat()
        latest_update_time = creation_time
        flow_data = {
            'user_id': user_id,
            'session_id': session_id,
            'flow_name': flow_name,
            'created_at': creation_time,
            'updated_at': latest_update_time,
            'is_active': is_active
        }
        key = f"{user_id}:{session_id}:{flow_name}"
        return self.db.create(self.collection, key, flow_data)

    def get_flow(self, user_id: str, session_id: str, flow_name: str) -> Optional[Any]:
        key = f"{user_id}:{session_id}:{flow_name}"
        return self.db.get(self.collection, key)

    def update_flow(self, user_id: str, session_id: str, flow_name: str, is_active = None) -> None:
        flow = self.get_flow(user_id, session_id, flow_name)
        print("[FLOW] get_flow:", user_id, session_id, flow_name)
        if flow:
            flow['updated_at'] = datetime.utcnow().isoformat()
            print("FLOW] updaing flow:", is_active)
            if is_active is not None:
                flow['is_active'] = is_active
            key = f"{user_id}:{session_id}:{flow_name}"
            self.db.set(self.collection, key, flow)

    def delete_flow(self, user_id: str, session_id: str, flow_name: str) -> None:
        key = f"{user_id}:{session_id}:{flow_name}"
        self.db.delete(self.collection, key)
        
    def active_flow(self, user_id: str, session_id: str) -> bool:
        filter_criteria = {
            'user_id': user_id,
            'session_id': session_id,
            'is_active': True
        }
        print(filter_criteria)
        active_flows = self.db.get_many(self.collection, filter_criteria)
        for flow in active_flows:
            return flow["flow_name"]
        return None
