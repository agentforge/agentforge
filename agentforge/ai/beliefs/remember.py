from typing import Any, Dict
from agentforge.utils import async_execution_decorator

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
