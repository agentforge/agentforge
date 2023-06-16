from typing import Any, Dict

### Recalls a memory given the context
class Recall:
    def __init__(self):
        pass
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        print(context['memory'])
        memories = context['memory'].recall(
            context['model_profile']['metadata']['user_id'],
            context['model_profile']['avatar_config']['name'],
            context['input']['prompt']
        )
        print(memories)
        working = context['memory'].session_history(
            context['model_profile']['metadata']['user_id'],
            context['model_profile']['avatar_config']['name'],            
        )
        context['recall'] = memories + " \n " + working
        return context
