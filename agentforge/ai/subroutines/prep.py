from typing import Any, Dict

### Preps output for end-user, stripping PII/IDs and anything else unserializable
class Prep:
    def __init__(self):
        pass
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        del context['memory']
        context['choices'] = [{"text": context['response']}] # OAI backwargs compatible
        return context