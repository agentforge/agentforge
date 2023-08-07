from typing import Any, Dict
from agentforge.utils import async_execution_decorator
from agentforge.utils.stream import stream_string
from agentforge.ai.reasoning.query_engine import QueryEngine


### BELIEFS: Stores a context for a user in the memory
### Update: Stores symbolic information from query response
class GetResponse:
    def __init__(self, domain):
        self.domain = domain
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        query_engine = QueryEngine(context["input"]['user_id'], context["input"]['model_id'])
        user_id = context['input']['user_id']
        session_id = context['input']['model_id']
        key = f"{user_id}:{session_id}:{self.domain}"

        ### UPDATE_BELIEFS
        # # if query exists and is a response, pop
        print("[INPUT] ", context["input"])
        sent = query_engine.get_sent_queries()
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
                query_engine.pop_query()
        return context

### BELIEFS: Stores a context for a user in the memory
### Remember: Stores message history between user and agent
class Remember:
    def __init__(self):
        pass
    
    @async_execution_decorator
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        prompt = context['input']['prompt'] if 'prompt' in context['input'] else context['input']['messages'][-1]['content']
        if 'memory' not in context:
            print("No memory")
            return context # No memory setup -- return context
        # raise Exception(context)
        context['memory'].remember(
            context['model_profile']['metadata']['user_id'],
            context['model_profile']['avatar_config']['name'],
            prompt,
            context["response"]
        )
        return context

### BELIEFS: Stores a context for a user in the memory
### Update: Stores symbolic information from unstructured text
class TextToSymbolic:
    def __init__(self):
        pass
    
    @async_execution_decorator
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        prompt = context['input']['prompt'] if 'prompt' in context['input'] else context['input']['messages'][-1]['content']
        if 'memory' not in context:
            print("No memory")
            return context # No memory setup -- return context


        return context
