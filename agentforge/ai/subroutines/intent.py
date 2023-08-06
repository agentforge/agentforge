from typing import Any, Dict
from typing import Any, List, Tuple
from agentforge.interfaces import interface_interactor
from agentforge.exceptions import BreakRoutineException
from agentforge.ai.cognition.tasks import TaskManagement

### Identify user intent
class Intent:
    def __init__(self):
        self.tasks = []
        self.task_management = TaskManagement()
        self.vectorstore = interface_interactor.get_interface("vectorstore")
    
    def search(self, user_query: str) -> Tuple[str, float]:
        # Search the vectorstore for the top result based on the user query
        results = self.vectorstore.search_with_score(
            user_query,
            n=4,
            collection="tasks"
        )
        if len(results) > 0:
            return results[0]
        return None, 0.0

    ### Identify user intent based on the user input
    ### and add a task to the task management system if necessary
    def execute_identification(self, user_input: str, user_id: str, session_id: str) -> str:
        # Let's first check to see if any tasks are already in progress
        task = self.task_management.active_task(user_id, session_id)
        if task is not None: # we are currently in an active task
            return task

        document, similarity = self.search(user_input)
        if not document: # Nothing came up
            return None
        # Threshold for similarity
        threshold = 0.6

        if similarity >= threshold and 'task_name' in document.metadata:
            task_name = document.metadata['task_name']
            ### Let's check to see if a task already exists and is no longer active
            task = self.task_management.get_task(user_id, session_id, task_name)
            ### If the task is not active, let's restart the task
            if task is None:
                self.task_management.add_task(user_id, session_id, task_name)
            elif not task['is_active']:
                ### Before reactivating the task automatically we need to implement multi-planning
                # self.task_management.update_task(user_id, session_id, task_name, is_active=True)
                pass
            return task_name
        else:
            return None

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        orig_prompt = context['input']['prompt'] if 'prompt' in context['input'] else context['input']['messages'][-1]['content']
        user_id = context['input']['user_id']
        agent_id = context['input']['modelId']
        id = self.execute_identification(orig_prompt, user_id, agent_id)
        if id is None:  
            return context
        else:
            raise BreakRoutineException(id)