from typing import Any, Dict

### Recalls a memory given the context
class Recall:
    def __init__(self):
        pass
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        memories = context['memory'].recall(
            context['model_profile']['metadata']['user_id'],
            context['model_profile']['avatar_config']['name'],
            context['input']['prompt']
        )
        working = context['memory'].session_history(
            context['model_profile']['metadata']['user_id'],
            context['model_profile']['avatar_config']['name'],            
        )
        print(working)
        context['recall'] = memories + " \n " + working
        return context
