from typing import Any, Dict
from typing import Any, Tuple
from agentforge.interfaces import interface_interactor
from agentforge.exceptions import BreakRoutineException
from agentforge.ai.attention.tasks import TaskManager
from agentforge.utils.stream import stream_string
from agentforge.ai.agents.context import Context

### ATTENTION: Identify user intent -- This is always first step in a routine
### Here we determine what our current attention should focus on, the task at hand.
### Determining intent from input allows us to switch conscious attention to a new task.
class Intent:
    def __init__(self):
        self.tasks = []
        self.task_management = TaskManager()
        self.vectorstore = interface_interactor.get_interface("vectorstore")

    def search(self, user_query: str) -> Tuple[str, float]:
        # Search the vectorstore for the top result based on the user query
        results = self.vectorstore.search_with_score(
            user_query,
            collection="tasks"
        )
        print(results)
        if len(results) > 0:
            return results[0]
        return None, 0.0

    """
    Input - context: Context object, user_id: str, session_id: str
    Output - task_name: str = intended to be executed by user
    
    User intent based on the user input
    and add a task to the task management system if detected

    """
    def text_intent(self, context: Context, user_id: str, session_id: str) -> str:
        user_input = context.get('instruction')
        # Let's first check to see if any tasks are already in progress
        task = self.task_management.active_task(user_id, session_id)

        if task is not None: # we are currently in an active task
            context.set("task", task)
            return task

        document, similarity = self.search(user_input)
        if not document: # Nothing came up
            return None

        # TODO: Make this more robust
        # Threshold for similarity - determine if task intent exists
        threshold = 0.6
        task_intent_exists = similarity >= threshold and 'name' in document.metadata
        print("time to plan? ", task_intent_exists)
        
        # The user is bantering with us - let us respond
        if not task_intent_exists:
            return None
        
        ### Let's check to see if a task already exists and is no longer active
        name = document.metadata['name']
        task_count = self.task_management.count(user_id, session_id, name)
        if task_count == 0:
            new_task = self.task_management.add_task(user_id, session_id, name)
            # Create corresponding attention for this task
            # If the predicate memory attention does not exist, feed plan queries into the current attention
            print("[PLAN] Creating new Attention to Plan")

            response = "Okay let's formulate a plan."
            stream_string('channel', response, end_token=" ")
            return new_task
        else:
            print("need to ask queries about existing task?")
            tasks = self.task_management.get_tasks(user_id, session_id, name)
            response = "Do you want to talk about\n"
            for task in tasks:
                response += f"{task['name']}\n"
            stream_string('channel', response, end_token=" ")
            # TODO: Make channel user specific, make text plan specific  
            return tasks[0]
        

    def execute(self, context: Context) -> Dict[str, Any]:
       
        user_id = context.get('input.user_id')
        agent_id = context.get('input.model_id')

        # if we are in an active task, attend to it
        active_task = self.task_management.active_task(user_id, agent_id)
        print('[ACTIVE_TASK] ', active_task)

        if active_task is not None:
            print("[INTENT] active task:", active_task.name)
            context.set("task", active_task)
            active_task.run(context)

        # else let's see if the user is requesting a task
        task = self.text_intent(context, user_id, agent_id)
        if task is None:
            # just banter, no tasks here!
            return context
        else:
            context.set("task", task)
            task.run(context)
