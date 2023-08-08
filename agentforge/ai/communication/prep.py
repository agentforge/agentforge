from typing import Any, Dict
from agentforge.utils import logger

### COMMUNICATION: Preps output for end-user, stripping PII/IDs and anything else unserializable
### Also implements presentation layer
class Prep:
    def __init__(self):
        pass

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        if context.has_key('memory'):
            context.delete('memory')
        if not context.has_key('response') or context.get('response') is None:
            return context
        # presentation = context['model_config']['presentation'] if 'model_config' in context and 'presentation' in context['model_config'] else "html"
        # if presentation == 'html':
        #     context['response'] = self.convert_html(context['response'])
        #     context['response'] = markdown.markdown(context['response'])
        context.set('choices', [{"text": context.get('response')}]) # OAI backwargs compatible
        logger.info(context.pretty_print())
        return context
