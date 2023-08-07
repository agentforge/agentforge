from typing import Any, Dict
from typing import Any, Tuple
from agentforge.interfaces import interface_interactor
from agentforge.exceptions import BreakRoutineException
from agentforge.ai.attention.tasks import TaskManagement
from agentforge.utils.stream import stream_string
from agentforge.ai.reasoning.query_engine import QueryEngine
from agentforge.ai.attention.attention import Attention
from agentforge.ai.agents.context import Context

### ATTENTION: Identify user intent -- This is always first step in a routine
### Here we determine what our current attention should focus on, the task at hand.
### Determining intent from input allows us to switch conscious attention to a new task.
class Intent:
    def __init__(self):
        self.tasks = []
        self.task_management = TaskManagement()
        self.attention = Attention()
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
    def text_intent(self, user_input: str, user_id: str, session_id: str) -> str:
        # Let's first check to see if any tasks are already in progress
        task = self.task_management.active_task(user_id, session_id)
        query_engine = QueryEngine(user_id, session_id)

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
            task_count = self.task_management.count(user_id, session_id, task_name)

            if task_count == 0:
                task = self.task_management.add_task(user_id, session_id, task_name)
                # Create corresponding attention for this task
                # If the predicate memory attention does not exist, feed plan queries into the current attention
                print("[PLAN] Creating new Attention to Plan")

                response = "Okay let's formulate a plan."
                stream_string('channel', response, end_token=" ")
                # TODO: Make channel user specific, make text plan specific           

                # queries = self.planner.domain.get_queries()
                # query_engine.create_queries(queries)
                self.attention.create_attention(task)

            else:
                print("need to ask queries about existing task?")
                tasks = self.task_management.get_tasks(user_id, session_id, task_name)
                response = "Do you want to talk about\n"
                for task in tasks:
                    response += f"{task['task_name']}\n"
                stream_string('channel', response, end_token=" ")
                # TODO: Make channel user specific, make text plan specific  
                # # TODO: Add query         

                ### Before reactivating the task automatically we need to implement multi-planning
                # self.task_management.update_task(user_id, session_id, task_name, is_active=True)
                pass
            return task_name
        else:
            return None

    def execute(self, context: Context) -> Dict[str, Any]:
       
        user_id = context.get('input.user_id')
        agent_id = context.get('input.model_id')

        # if we are in an active task, attend to it
        active_task = self.task_management.active_task(user_id, agent_id)
        print('[ACTIVE_TASK] ', active_task)
        if active_task is not None:
            raise BreakRoutineException(active_task)

        # else let's see if the user is requesting a task
        id = self.text_intent(context.get('prompt'), user_id, agent_id)
        if id is None:
            # just banter, no tasks here!
            return context
        else:
            raise BreakRoutineException(id)