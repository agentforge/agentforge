from typing import Any, Dict
from agentforge.interfaces import interface_interactor
from agentforge.utils import Parser
from agentforge.utils.stream import stream_string
from agentforge.ai.attention.tasks import TaskManager
from agentforge.utils import logger
from copy import deepcopy

### COMMUNICATION: Handles response generation
class Respond:
    def __init__(self):
        self.task_management = TaskManager()
        self.service = interface_interactor.get_interface("llm")
        # self.tokenizer = interface_interactor.get_interface("tokenizer")
        self.parser = Parser()

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        ### Another subroutine gotchu dawg, bail
        if context.has_key("response"):
            logger.info("Response already exists, skipping response generation")
            return context

        username = context.get("input.user_name") + ":"
        agentname = context.get("model.persona.display_name") + ":"

        formatted = context.get_formatted()
        # response = self.tokenizer.call({'prompt': formatted})
        # token_cnt = int(response['text'])
        # max_tokens = int(context.get('model.model_config.max_tokens'))
        # if token_cnt > max_tokens:
        #     message_cnt = len(context.get('input.messages'))
        #     while token_cnt > max_tokens and message_cnt > 0:
        #         formatted = context.get_formatted(message_cnt-1)
        #         response = self.tokenizer.call({'prompt': formatted})
        #         token_cnt = int(response['text'])
        #         if token_cnt < max_tokens:
        #             break
        #         message_cnt -= 1
        #     if token_cnt > max_tokens:
        #         formatted = context.get_formatted(message_cnt-1, use_memory=False)
        #         response = self.tokenizer.call({'prompt': formatted})
        #         token_cnt = int(response['text'])
        #         if token_cnt > max_tokens:
        #             formatted = context.get_formatted(message_cnt-1, use_memory=False, knowledge=False)


        for tok in ['eos_token', 'bos_token', 'prefix', 'postfix']:
            if context.has_key(f"model.model_config.{tok}"):
                formatted = formatted.replace(context.get(f"model.model_config'.{tok}"), "")

        gen_config = deepcopy(context.get('model.generation_config'))
        context.set("prompt", formatted)

        # add 'User:' and 'Assistant:' type stopping criteria
        gen_config["stopping_criteria_string"] = f"{username},{agentname}"
        input = {
            "prompt": formatted,
            "generation_config": gen_config,
            "model_config": context.get('model.model_config'),
            "user_id": context.get("input.user_id"),
            "user_name": context.get("input.user_name"),
            "agent_name": context.get("model.persona.display_name"),
        }
        response = self.service.call(input)

        if response is not None and "choices" in response:
            response = response["choices"][0]["text"]
            ### We want to parse the output here -- this output goes to end user
            response = response.replace(formatted, "")
            response = self.parser.parse_llm_response(response)
            for tok in ['eos_token', 'bos_token', 'prefix', 'postfix']:
                if context.has_key(f"model.model_config.{tok}"):
                    response = response.replace(context.get(f"model.model_config'.{tok}"), "")
            context.set("response", response)
        return context
