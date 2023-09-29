from typing import Any, Dict
from typing import Any, Tuple
from agentforge.interfaces import interface_interactor
from agentforge.ai.attention.tasks import TaskManager
from agentforge.utils.stream import stream_string
from agentforge.ai.agents.context import Context
from agentforge.ai.reasoning.zeroshot import ZeroShotClassifier
from agentforge.utils import logger

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
        
        # The user is bantering with us - let us respond
        if not task_intent_exists:
            return None
        
        ### Let's check to see if a task already exists and is no longer active
        task_name = document.metadata['name']
        task_count = self.task_management.count(user_id, session_id, task_name)
        if task_count == 0:
            new_task = self.task_management.init_task(context, task_name)
            self.task_management.save(new_task)

            # Create corresponding attention for this task
            # If the predicate memory attention does not exist, feed plan queries into the current attention

            response = "Okay let's formulate a plan."
            stream_string('channel', response, end_token=" ")
            return new_task
        else:
            tasks = self.task_management.get_tasks(user_id, session_id, task_name)
            response = "Do you want to talk about\n"
            for task in tasks:
                response += f"{task['name']}\n"
            stream_string('channel', response, end_token=" ")
            # TODO: Make channel user specific, make text plan specific  
            return tasks[0]
        

    def execute(self, context: Context) -> Dict[str, Any]:
        user_input = context.get('instruction')

        # z_val = z.classify("### Instruction: Does this mean the user wants to initiate a new garden plan? Respond with Yes or No. ### Input: {{user_input}} ### Response: ", ["Yes", "No"], {"user_input": user_input}, context)
        # logger.info(f"PLAN A GARDEN: {z_val}")

        user_id = context.get('input.user_id')
        agent_id = context.get('input.model_id')

        # if we are in an active task, attend to it
        active_task = self.task_management.active_task(user_id, agent_id)

        if active_task is not None:
            context.set("task", active_task)
            context = active_task.run(context)
            return context

        # else let's see if the user is requesting a task
        task = self.text_intent(context, user_id, agent_id)
        if task is None:    
            # just bante'r, no tasks here!
            return context
        else:
            context.set("task", task)
            context = task.run(context)
            return context
