from typing import Any, Dict
from agentforge.utils import async_execution_decorator
from agentforge.utils.stream import stream_string
from agentforge.ai.beliefs.symbolic import SymbolicMemory
from agentforge.ai.attention.tasks import TaskManager
from agentforge.utils import logger

### BELIEFS: Stores a context for a user in the memory
### Update: Stores symbolic information from query response
class GetResponse:
    def __init__(self, domain):
        self.domain = domain
        self.symbolic_memory = SymbolicMemory()
        self.task_management = TaskManager()
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        # user_id = context['input']['user_id']
        # session_id = context['input']['model_id']
        # key = f"{user_id}:{session_id}:{self.domain}"

        ### UPDATE_BELIEFS
        # # if query exists and is a response, pop
        task = context.get("task")
        # task.pretty_print()
        query = task.get_active_query()
        logger.info("[ACTIVE QUERY]")
        logger.info(query)
        if query is not None:
            # raise ValueError("query not none")
            # feed in to the OPQL
            query["response"] = context.get("instruction") # The user response comes in as a prompt
            logger.info("[PLAN] Learning new information...")
             # TODO: Make channel user specific, make text plan specific
            # stream_string('channel', "One moment while I make a note.", end_token="\n\n")
            logger.info(query)

            learned, results = self.symbolic_memory.learn(query, context)
            logger.info("[LEARNED]")
            logger.info(learned)
            logger.info(results)
            query["results"] = results
            if learned:
                # TODO: Make channel user specific, make text plan specific
                # stream_string('channel', "Okay I've jotted that down.", end_token=" ")
                task.push_complete(query)
                self.task_management.save(task)
            else:
                task.push_failed(query)
                self.task_management.save(task)
        return context

### BELIEFS: Stores a context for a user in the memory
### Remember: Stores message history between user and agent
class Remember:
    def __init__(self):
        pass
    
    @async_execution_decorator
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        # logger.info("[RESPONSE]")
        # logger.info(context.get('response'))
        # raise ValueError("STOP")
        if context.get('response') == None:
            return context

        context.memory.remember(
            context.get('input.user_id'),
            context.get('model.persona.name'),
            context.get('instruction'),
            context.get('response').replace("<s>","").strip(),
        )
        return context

### BELIEFS: Stores a context for a user in the memory
### Update: Stores symbolic information from unstructured text
class TextToSymbolic:
    def __init__(self):
        pass
    
    @async_execution_decorator
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        # TODO: Extract symbolic information from text
        return context
