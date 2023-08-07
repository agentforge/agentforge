from typing import Any, Dict
from agentforge.interfaces import interface_interactor
from agentforge.ai.reasoning.query_engine import QueryEngine
from agentforge.utils import Parser
from agentforge.utils.stream import stream_string

### COMMUNICATION: Handles response generation
class Respond:
    def __init__(self):
        self.service = interface_interactor.get_interface("llm")
        self.parser = Parser()

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        print("RESPOND")
        ### Another subroutine gotchu dawg, bail
        if "response" in context:
            return context
        
        # Iterate through unsent queries and send the latest if it exists
        query_engine = QueryEngine(context["input"]['user_id'], context["input"]['model_id'])
        for query in query_engine.get_queries():
            print("[QUERY]", query)
            if query is not None:
                print("[QUERY] asking a query", query['query'])
                query_engine.update_query(sent=True)
                stream_string('channel', query['query']) # TODO: Make channel user specific
                context["response"] = query['query']
                # Return new context to the user w/ response
                return context

        # If no query exists respond to the user based on the input and context
        input = {
            "prompt": context['input']['formatted'],
            "generation_config": context['model_profile']['generation_config'],
            "model_config": context['model_profile']['model_config'],
        }

        print("[RESPOND][PROMPT] ", context['input']['formatted'])
        response = self.service.call(input)

        if response is not None and "choices" in response:
            context["response"] = response["choices"][0]["text"]

            ### We want to parse the output here -- this output goes to end user
            context["response"] = context["response"].replace(context['input']['formatted'], "")
            context["response"] = self.parser.parse_llm_response(context["response"])
            for tok in ['eos_token', 'bos_token']:
                if tok in context['model_profile']['model_config']:
                    context["response"] = context["response"].replace(context['model_profile']['model_config'][tok], "")

        return context
