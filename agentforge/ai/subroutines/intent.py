from typing import Any, Dict
from typing import Any, List, Tuple
from agentforge.ai.cognition.flow import Flow
from agentforge.interfaces import interface_interactor
from agentforge.exceptions import BreakRoutineException

### Identify user intent
class Intent:
    def __init__(self):
        self.flows = []
        self.vectorstore = interface_interactor.get_interface("vectorstore")
    
    def search(self, user_query: str) -> Tuple[str, float]:
        # Search the vectorstore for the top result based on the user query
        results = self.vectorstore.search_with_score(user_query, 1, filter={'flow': True}, return_score=True, distance_metric="cos")
        return results[0]

    # TODO: We need a more robust method
    def execute_identification(self, user_input: str) -> str:
        document, similarity = self.search(user_input)
        # Threshold for similarity
        print(f"{document.metadata['name']} = {similarity}")
        threshold = 0.24

        if similarity >= threshold:
            return document.metadata['name']
        else:
            return None

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        id = self.execute_identification(context['input']['original_prompt'])
        if id is None:
            return context
        else:
            raise BreakRoutineException(id)