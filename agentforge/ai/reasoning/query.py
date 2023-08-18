from agentforge.ai.reasoning.query_engine import QueryEngine
from typing import Any, Dict
from agentforge.interfaces import interface_interactor
from agentforge.utils.stream import stream_string
from agentforge.ai.agents.context import Context

class AskQuery:
    def __init__(self):
      self.service = interface_interactor.get_interface("llm")

    def execute(self, context: Context) -> Dict[str, Any]:
      # If this is in response to a query from the end-user, parse the response and input into OPQL
      # raise Exception(context)
      user_id = context.get('input.user_id')
      session_id = context.get('input.id')

      # Initialize the query engine for this user and session and run it
      query_engine = QueryEngine(user_id, session_id)

      # First we need to check if there are existing responded-to queries that need
      # to be processed. If so we process them here into OPQL triplets
      queries = query_engine.get_queries()
      if len(queries) == 0 and context.has_key("queries"):
         # hack fix for mongo race condition? argh
         queries = context.get("queries")
      # if query exists and is a response, present it
      for query in queries:
          if query is not None:
              print("asking ", query)
              query_engine.update_query(sent=True)
              stream_string(query['query'])
              context.set("response", query['query'])

              # Return new context to the user w/ response
              return context
      return context
