from typing import Any, Dict
from agentforge.utils import async_execution_decorator

### Stores a context for a user in the memory
class Remember:
    def __init__(self):
        pass
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        print('memory' not in context)
        print('response' not in context)
        if 'memory' not in context or 'response' not in context:
            return context # No memory setup -- return context
        # raise Exception(context)
        context['memory'].remember(
            context['model_profile']['metadata']['user_id'],
            context['model_profile']['avatar_config']['name'],
            context['input']['original_prompt'],
            context['response']
        )
        print("memoized")
        return context
