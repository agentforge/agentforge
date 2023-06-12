from typing import Any, Dict

### Stores a context for a user in the memory
class Remember:
    def __init__(self):
        pass

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        if 'memory' not in context:
            return # No memory setup
        # raise Exception(context)
        context['memory'].remember(
            context['model_profile']['metadata']['user_id'],
            context['model_profile']['avatar_config']['name'],
            context['input']['original_prompt'],
            context['response']
        )

        return context
