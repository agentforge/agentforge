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
        if context.has_key("response"):
            return context
        
        # Iterate through unsent queries and send the latest if it exists
        query_engine = QueryEngine(context.get('input.user_id'), context.get('input.model_id'))
        for query in query_engine.get_queries():
            print("[QUERY]", query)
            if query is not None:
                print("[QUERY] asking a query", query['query'])
                query_engine.update_query(sent=True)
                stream_string('channel', query['query']) # TODO: Make channel user specific
                context.set("response", query['query'])
                # Return new context to the user w/ response
                return context

        # If no query exists respond to the user based on the input and context
        formatted = context.get_formatted()
        input = {
            "prompt": formatted,
            "generation_config": context.get('model.generation_config'),
            "model_config": context.get('model.model_config'),
        }

        response = self.service.call(input)

        if response is not None and "choices" in response:
            response = response["choices"][0]["text"]
            ### We want to parse the output here -- this output goes to end user
            response = response.replace(formatted, "")
            response = self.parser.parse_llm_response(response)
            for tok in ['eos_token', 'bos_token']:
                if context.has_key(f"model_profile.model_config.{tok}"):
                    response = response.replace(context.get(f"model_profile.model_config'.{tok}"), "")
            context.set("response", response)
        return context
