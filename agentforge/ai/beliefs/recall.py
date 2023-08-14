from typing import Any, Dict
from agentforge.ai.agents.context import Context

### BELIEFS: Recalls a memory given the context
class Recall:
    def __init__(self):
        pass
    
    def execute(self, context: Context) -> Dict[str, Any]:
        memories = context.memory.recall(
            context.get('input.user_id'),
            context.get('model.avatar_config.name'),
            context.get('prompt')
        )
        working = context.memory.session_history(
            context.get('input.user_id'),
            context.get('model.avatar_config.name'),
            context.get('input.id'),
        )
        context.set('recall', memories + " \n " + working)
        return context
