from agentforge.ai.cognition.query_engine import QueryEngine
from typing import Any, Dict
from agentforge.interfaces import interface_interactor
from agentforge.ai.cognition.opql import PredicateMemory

### Identifies if there is a response to an outgoing query and learns from it
class Learn:
    def __init__(self):
      self.service = interface_interactor.get_interface("llm")
      self.predicate_memory = PredicateMemory()

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
      # If this is in response to a query from the end-user, parse the response and input into OPQL
      # raise Exception(context)
      user_id = context['input']['user_id']
      session_id = context['input']['id']

      # Initialize the query engine for this user and session and run it
      query_engine = QueryEngine(user_id, session_id)

      # First we need to check if there are existing responded-to queries that need
      # to be processed. If so we process them here into OPQL triplets
      queries = query_engine.get_queries()
      # if query exists and is a response, pop
      print(queries)
      for query in queries:
          if query is not None and "sent" in query and query["sent"]:
              # feed in to the OQAL
              # raise Exception(context["input"]["original_prompt"])
              query["response"] = context["input"]["original_prompt"]
              self.predicate_memory.learn(query) # TODO: I doubt the user formats the response correctly, we should rely on the LLM here
              query_engine.pop_query()
      return context

class Query:
    def __init__(self):
      self.service = interface_interactor.get_interface("llm")
      self.predicate_memory = PredicateMemory()

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
      # If this is in response to a query from the end-user, parse the response and input into OPQL
      # raise Exception(context)
      user_id = context['input']['user_id']
      session_id = context['input']['id']

      # Initialize the query engine for this user and session and run it
      query_engine = QueryEngine(user_id, session_id)
      
      # First we need to check if there are existing responded-to queries that need
      # to be processed. If so we process them here into OPQL triplets
      queries = query_engine.get_queries()
      # if query exists and is a response, pop
      print(queries)
      for query in queries:
          if query is not None:
              # Create a query via LLM response
              input = {
                  "prompt": query['query'],
                  "generation_config": context['model_profile']['generation_config'],
                  "model_config": context['model_profile']['model_config'],
              }

              # response = self.service.call(input)

              # if response is not None and "choices" in response:
              #     context["response"] = response["choices"][0]["text"]

              context["response"] = f"This is a test response to {query['query']}"

              # Update this query and store it in the KVStore
              query = query_engine.update_query(query=context["response"], sent=True)

              # Return new context to the user w/ response
              return context
      return context
