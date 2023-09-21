from typing import Any, Dict
from agentforge.interfaces import interface_interactor
from agentforge.ai.agents.context import Context
from agentforge.ai.reasoning.classifier import Classifier


"""
  Relation: Extracts a relation from the user's response

  Input - context: Context object
          query: Dict object

  Output - Dict:  Adds a relation to the query

"""
class Relation:
    def __init__(self):
      self.classifier = Classifier()

    def extract(self, context: Context, query: Dict) -> Dict[str, Any]:
        # # We need to create a query via the LLM using the context and query
        new_prompt = context.prompts["relation.prompt"]
        args = {
          "object": query['object'].replace("?","").strip().title(),
          "subject": "User",
          "goal": query['goal'],
          "action": query['action'],
        }
        results = self.classifier.classify(args, new_prompt, context)
        query['relation'] = results[0].strip()
        return query
