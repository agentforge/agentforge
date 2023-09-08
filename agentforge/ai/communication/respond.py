from typing import Any, Dict
from agentforge.interfaces import interface_interactor
from agentforge.utils import Parser
from agentforge.utils.stream import stream_string
from agentforge.ai.attention.tasks import TaskManager
from agentforge.utils import logger

### COMMUNICATION: Handles response generation
class Respond:
    def __init__(self):
        self.task_management = TaskManager()
        self.service = interface_interactor.get_interface("llm")
        self.parser = Parser()

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        # logger.info("RESPOND?", context.has_key("response"))
        ### Another subroutine gotchu dawg, bail
        if context.has_key("response"):
            return context

        # Iterate through unsent queries and send the latest if it exists
        task = context.get("task")
        # query_engine = QueryEngine(context.get('input.user_id'), context.get('input.model_id'))
        if task is not None and task.get_active_query() is not None:
            return context

        # If no query exists respond to the user based on the input and context
        formatted = context.get_formatted()

        # If no query exists respond to the user based on the input and context
        formatted = context.get_formatted()
        for tok in ['eos_token', 'bos_token']:
            if context.has_key(f"model.model_config.{tok}"):
                formatted = formatted.replace(context.get(f"model.model_config'.{tok}"), "")

        input = {
            "prompt": formatted,
            "generation_config": context.get('model.generation_config'),
            "model_config": context.get('model.model_config'),
        }
        # Add user and agent name to stopping criteria
        username = context.get('input.user_name', "Human")
        agentname = context.get('model.persona.display_name')
        new_stop = input['generation_config']['stopping_criteria']+ f",{username}:,{agentname}:,### Response:,### Instructions:"
        input['generation_config']['stopping_criteria'] = new_stop
        response = self.service.call(input)

        if response is not None and "choices" in response:
            response = response["choices"][0]["text"]
            ### We want to parse the output here -- this output goes to end user
            response = response.replace(formatted, "")
            response = self.parser.parse_llm_response(response)
            for tok in ['eos_token', 'bos_token']:
                if context.has_key(f"model.model_config.{tok}"):
                    response = response.replace(context.get(f"model.model_config'.{tok}"), "")
            context.set("response", response)
        return context
