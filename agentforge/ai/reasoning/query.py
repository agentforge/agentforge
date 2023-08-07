from agentforge.ai.reasoning.query_engine import QueryEngine
from typing import Any, Dict
from agentforge.interfaces import interface_interactor
from agentforge.ai.beliefs.symbolic import SymbolicMemory
from agentforge.utils.stream import stream_string

### REASONING: Identifies if there is a response to an outgoing query and learns from it

class Query:
  def __init__(self) -> None:
     pass
class Learn:
    def __init__(self):
      self.service = interface_interactor.get_interface("llm")
      self.db = interface_interactor.get_interface("db")
      self.symbolic_memory = SymbolicMemory(self.db)

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
      # # if query exists and is a response, pop
      for query in queries:
          if query is not None and "sent" in query and query["sent"]:
              # feed in to the OQAL
              # raise Exception(context["input"]["prompt"])
              query["response"] = context["input"]["prompt"]
              self.symbolic_memory.learn(query) # TODO: I doubt the user formats the response correctly, we should rely on the LLM here
              query_engine.pop_query()
      return context

class AskQuery:
    def __init__(self):
      self.service = interface_interactor.get_interface("llm")

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
      if len(queries) == 0 and "queries" in context:
         # hack fix for mongo race condition? argh
         queries = context["queries"]
      # if query exists and is a response, pop
      for query in queries:
          if query is not None:
              print("asking ", query)
              query_engine.update_query(sent=True)
              stream_string(query['query'])
              context["response"] = query['query']

              # Return new context to the user w/ response
              return context
      return context
