from typing import Any, Dict

### BELIEFS: Recalls a memory given the context
class Recall:
    def __init__(self):
        pass
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        orig_prompt = context['input']['prompt'] if 'prompt' in context['input'] else context['input']['messages'][-1]['content']
        memories = context['memory'].recall(
            context['model_profile']['metadata']['user_id'],
            context['model_profile']['avatar_config']['name'],
            orig_prompt
        )
        working = context['memory'].session_history(
            context['model_profile']['metadata']['user_id'],
            context['model_profile']['avatar_config']['name'],
            context['input']['id'],            
        )
        context['recall'] = memories + " \n " + working
        return context
