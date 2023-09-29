from typing import Any, Dict
from agentforge.ai.agents.context import Context
from agentforge.utils import logger

### BELIEFS: Recalls a memory given the context
class Recall:
    def __init__(self):
        pass
    
    def execute(self, context: Context) -> Dict[str, Any]:
        memories = context.memory.recall(
            context.get('input.user_id'),
            context.get('model.persona.name'),
            context.get('prompt')
        )
        # working = context.memory.session_history(
        #     context.get('input.user_id'),
        #     context.get('model.persona.name'),
        #     context.get('input.id'),
        #     n=4
        # )
        logger.info("RECALLING")
        # logger.info(working)
        memories = memories.strip()
        context.set('recall', memories)
        return context
