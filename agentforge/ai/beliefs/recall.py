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
            context.get_messages(prefix="", postfix="", n=2),
        )
        knowledge = context.memory.knowledge(
            context.get('input.user_id'),
            context.get('model.persona.name'),
            context.get('instruction'),
            collection='knowledge',
            n=1
        )
        extra_data = context.memory.knowledge(
            context.get('input.user_id'),
            context.get('model.persona.name'),
            context.get('instruction'),
            collection='strains',
            n=2
        )
        # working = context.memory.session_history(
        #     context.get('input.user_id'),
        #     context.get('model.persona.name'),
        #     context.get('input.id'),
        #     n=4
        # )
        logger.info(f"RECALLING {context.get('instruction')}")
        context.set('recall', memories)
        context.set('knowledge', knowledge)
        context.set('additional_knowledge', extra_data)
        return context
