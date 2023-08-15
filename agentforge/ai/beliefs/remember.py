from typing import Any, Dict
from agentforge.utils import async_execution_decorator
from agentforge.utils.stream import stream_string

### BELIEFS: Stores a context for a user in the memory
### Update: Stores symbolic information from query response
class GetResponse:
    def __init__(self, domain):
        self.domain = domain
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        # user_id = context['input']['user_id']
        # session_id = context['input']['model_id']
        # key = f"{user_id}:{session_id}:{self.domain}"

        ### UPDATE_BELIEFS
        # # if query exists and is a response, pop
        sent = context.query_engine.get_sent_queries()
        if len(sent) > 0:
            query = sent[0]
            # feed in to the OQAL
            # raise Exception(context["input"]["prompt"])
            query["response"] = context["input"]["prompt"] # The user response comes in as a prompt
            print("[PLAN] Learning new information...")
            stream_string('channel', "One moment while I make a note.", end_token=" ") # TODO: Make channel user specific, make text plan specific
            learned, results = self.symbolic_memory.learn(query, context) # TODO: I doubt the user formats the response correctly, we should rely on the LLM here
            print(learned, results)
            if learned:
                stream_string('channel', "Okay I've jotted that down.", end_token=" ") # TODO: Make channel user specific, make text plan specific
                self.symbolic_memory.satisfy_attention(key, query, results)
                context.query_engine.pop_query()
        return context

### BELIEFS: Stores a context for a user in the memory
### Remember: Stores message history between user and agent
class Remember:
    def __init__(self):
        pass
    
    @async_execution_decorator
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        print(context.get('prompt'))
        print(context.get('response'))
        # context.memory.remember(
        #     context.get('input.user_id'),
        #     context.get('model.avatar_config.name'),
        #     context.get('prompt'),
        #     context.get('response')
        # )
        # return context

### BELIEFS: Stores a context for a user in the memory
### Update: Stores symbolic information from unstructured text
class TextToSymbolic:
    def __init__(self):
        pass
    
    @async_execution_decorator
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        # TODO: Extract symbolic information from text
        return context
