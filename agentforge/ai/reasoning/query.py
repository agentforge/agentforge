from typing import Any, Dict
from agentforge.interfaces import interface_interactor
from agentforge.ai.agents.context import Context
from copy import deepcopy
from agentforge.utils import logger

"""
  Query: Generates a query for the user to respond to and any other query reasoning

"""
class Query:
    def __init__(self):
      self.llm = interface_interactor.get_interface("llm")

    """
    Input - context: Context object
            query: Dict object

    Output - Dict:  Adds a query to the active list from the queue by calling the LLM
    """

    def get(self, context: Context, query: Dict, streaming: bool = True) -> Dict[str, Any]:
        if query is None:
          return context
        
        # # We need to create a query via the LLM using the context and query
        input = deepcopy(context.get_model_input())
        prompt = context.prompts[f"{query['datatype']}.query.prompt"]
        data = {
            "condition": query['condition'],
            "goal": query['goal'],
            "type": query['datatype'],
            "object": query['class'].replace("?",""),
            "action": query['action'],
            "biography": context.get('model.persona.biography'),
        }

        # custom generation settings for query
        input['model_config']['streaming'] = streaming
        input['generation_config']['max_new_tokens'] = 512
        input['prompt'] = context.process_prompt(prompt, data)

        conditions = data['condition'].split(" OR ") #conditions can be split by OR
        predicates = {}
        for condition in conditions:  
          datum = condition.split(" ")
          if len(datum) > 1:
              predicates[datum[0]] = datum[1:]

        query['condition'] = data['condition']
        query['predicates'] = predicates

        query['text'] = self.llm.call(input)["choices"][0]["text"].replace(input['prompt'], "")
        logger.info("TEXT")
        logger.info(query['text'])

        # Clean output text -- # TODO: move these to a shared context function
        for tok in ['eos_token', 'bos_token', 'prefix', 'postfix']:
            if tok in context.get('model.model_config'):
                query['text'] = query['text'].replace(context.get('model.model_config')[tok], "")

        query['text'] = query['text'].strip().split("\n")[0] # Only take the first line -- usually garbage after that here
        context.set("query", query['text'])
        return query