from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, ValidationError
from datetime import datetime
from agentforge.interfaces import interface_interactor
from uuid import uuid4

class Node(BaseModel):
    name: str
    metadata: dict = {}

class Edge(BaseModel):
    relationship: str
    metadata: dict = {}

class Triplet(BaseModel):
    id: str = str(uuid4())
    src_node: Node
    dst_node: Node
    edge: Edge
    timestamp: datetime = datetime.utcnow()

class StateManager:
    def __init__(self):
        self.db = interface_interactor.get_interface("db")

    def create_triplet(self, triplet: Triplet) -> Optional[Any]:
        try:
            # Validate the Triplet model
            validated_triplet = Triplet(**triplet.dict())
        except ValidationError as e:
            print(f"Validation Error: {e}")
            return None
        
        # Check if the triplet already exists
        existing_triplet = self.get_triplet(
            validated_triplet.src_node.name, 
            validated_triplet.edge.relationship, 
            validated_triplet.dst_node.name
        )
        
        if existing_triplet:
            print(f"A triplet with src: {validated_triplet.src_node.name}, relationship: {validated_triplet.edge.relationship}, and dst: {validated_triplet.dst_node.name} already exists.")
            return None
        
        return self.db.create("state", validated_triplet.id, validated_triplet.dict())

    def get_triplet(self, src_name: str, relationship: str, dst_name: str) -> Optional[Triplet]:
        filter_query = {
            "src_node.name": src_name,
            "edge.relationship": relationship,
            "dst_node.name": dst_name
        }
        data_cursor = self.db.get_many("state", filter_query)
        
        # Convert the cursor to a list and check if it's empty
        data_list = list(data_cursor)
        if not data_list:
            return None
        
        # Return the first match from the list
        return Triplet(**data_list[0])

    def aggregate(self, pipeline: List[Dict[str, Any]]) -> Optional[Any]:
        return self.db.aggregate("state", pipeline)

def test():
    state_manager = StateManager()
    
    # Create a triplet
    node1 = Node(name="Frank Grove")
    node2 = Node(name="location")
    edge = Edge(relationship="has available outdoor plot")
    triplet = Triplet(src_node=node1, edge=edge, dst_node=node2)

    state_manager.create_triplet(triplet)
    print("Created Triplet:", state_manager.get_triplet("Frank Grove", "has available outdoor plot", "location"))

    # Perform aggregation
    pipeline = [
        {
            "$match": {"src_node.name": "Frank Grove"}
        },
        {
            "$graphLookup": {
                "from": "state",
                "startWith": "$src_node.name",
                "connectFromField": "dst_node.name",
                "connectToField": "src_node.name",
                "as": "connectedEntities"
            }
        }
    ]
    
    result = state_manager.aggregate(pipeline)
    print("Aggregation Result:", result)
