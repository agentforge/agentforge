from typing import Any, Dict
from typing import Any, List, Tuple
from agentforge.interfaces import interface_interactor
from agentforge.exceptions import BreakRoutineException
from agentforge.ai.cognition.flow import FlowManagement

### Identify user intent
class Intent:
    def __init__(self):
        self.flows = []
        self.flow_management = FlowManagement()
        self.vectorstore = interface_interactor.get_interface("vectorstore")
    
    def search(self, user_query: str) -> Tuple[str, float]:
        # Search the vectorstore for the top result based on the user query
        results = self.vectorstore.search_with_score(user_query, 1, filter={'flow': True}, return_score=True, distance_metric="cos")
        return results[0]

    # TODO: We need a more robust method
    def execute_identification(self, user_input: str, user_id: str, session_id: str) -> str:
        # Let's first check to see if any Flows are already in progress
        flow = self.flow_management.active_flow(user_id, session_id)
        if flow is not None:
            return flow

        document, similarity = self.search(user_input)
        # Threshold for similarity
        print(f"{document.metadata['name']} = {similarity}")
        threshold = 0.24

        if similarity >= threshold:
            self.flow_management.register_flow(user_id, session_id, document.metadata['name'])
            return document.metadata['name']
        else:
            return None

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        id = self.execute_identification(context['input']['original_prompt'], context['input']['user_id'], context['input']['id'])
        if id is None:
            return context
        else:
            raise BreakRoutineException(id)