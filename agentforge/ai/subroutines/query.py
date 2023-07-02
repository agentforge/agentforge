from agentforge.ai.cognition.query_engine import QueryEngine
from typing import Any, Dict
from agentforge.interfaces import interface_interactor

### Query the world-state to gather necessary information for a task
class Query:
    def __init__(self):
      self.query_engine = QueryEngine()
      self.service = interface_interactor.get_interface("llm")

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
      # If this is in response to a query from the end-user, parse the response and input into OPQL
      # raise Exception(context)
      user_id = context['input']['user_id']
      session_id = context['input']['id']
      query = self.query_engine.get_query(user_id, session_id)
      
      # If this user input is a response to the query
      if query is not None and query['sent']:
        self.query_engine.parse_response(query, context)

      # Identify if there are queries we need to make according to the current context
      next_query = self.query_engine.get_query(user_id, session_id)
      if next_query is not None:

        # Create a query via LLM response
        input = {
            "prompt": next_query,
            "generation_config": context['model_profile']['generation_config'],
            "model_config": context['model_profile']['model_config'],
        }

        response = self.service.call(input)

        if response is not None and "choices" in response:
            context["response"] = response["choices"][0]["text"]

        # Update this query and store it in the KVStore
        query = self.query_engine.update_query(user_id, session_id, query=context["response"], sent=True)

        # Return new context to the user w/ response
        return context
      pass