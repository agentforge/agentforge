from typing import Any, Dict
from agentforge.interfaces import interface_interactor
from agentforge.ai.agents.context import Context


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

    def get(self, context: Context, query: Dict) -> Dict[str, Any]:
        if query is None:
          return context
        # # We need to create a query via the LLM using the context and query
        input = context.get_model_input()
        prompt = context.prompts[f"{query['datatype']}.query.prompt"]
        data = {
            "condition": query['text'],
            "goal": query['goal'],
            "type": query['datatype'],
            "object": query['class'].replace("?",""),
            "action": query['action'],
            "biography": context.get('model.persona.biography'),
        }

        # custom generation settings for query
        input['generation_config']['max_new_tokens'] = 512
        input['generation_config']['stopping_criteria'] = input['generation_config']['stopping_criteria'] + ",\n"

        input['prompt'] = context.process_prompt(prompt, data)
        query['condition'] = data['condition']

        conditions = data['condition'].split(" OR ") #conditions can be split by OR
        predicates = {}
        for condition in conditions:  
          datum = condition.split(" ")
          if len(datum) > 1:
              predicates[datum[0]] = datum[1:]
        query['predicates'] = predicates
        query['text'] = self.llm.call(input)["choices"][0]["text"].replace(input['prompt'], "")
        query['text'] = query['text'].split("\n")[0] # Only take the first line
        context.set("response", query['text'])
        return query