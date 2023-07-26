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
        results = self.vectorstore.search_with_score(user_query, 1, filter={'flow': True}, distance_metric="cos")
        if len(results) > 0:
            return results[0]
        return None, 0.0

    # TODO: We need a more robust method
    ### This basically acts as a controller -- if the user wants to initiate
    ### a certain action or routine
    ### This is better off as a fine-tuned LLM (i.e. HuggingGPT) but a embeddings vectorstore w/ a list of likely candidates
    ### for initiating a new flow into a routine is good enough for now
    def execute_identification(self, user_input: str, user_id: str, session_id: str) -> str:
        # Let's first check to see if any Flows are already in progress
        flow = self.flow_management.active_flow(user_id, session_id)
        if flow is not None:
            print("Flow exists...")
            return flow

        document, similarity = self.search(user_input)
        print(document, similarity)
        if not document: # Nothing came up
            return None
        # Threshold for similarity
        threshold = 0.6

        if similarity >= threshold and 'flow_name' in document.metadata:
            flow_name = document.metadata['flow_name']
            ### Let's check to see if a flow already exists and is no longer active
            flow = self.flow_management.get_flow(user_id, session_id, flow_name)
            ### If the flow is not active, let's restart the flow
            if flow is None:
                self.flow_management.register_flow(user_id, session_id, flow_name)
            elif not flow['is_active']:
                self.flow_management.update_flow(user_id, session_id, flow_name, is_active=True)
            return flow_name
        else:
            return None

        raise Exception(context)
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        print(context)
        orig_prompt = context['input']['prompt']
        user_id = context['input']['user_id']
        agent_id = context['input']['id']
        id = self.execute_identification(orig_prompt, user_id, agent_id)
        if id is None:
            return context
        else:
            raise BreakRoutineException(id)