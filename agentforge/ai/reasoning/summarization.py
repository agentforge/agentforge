from typing import Any, Dict
from agentforge.interfaces import interface_interactor
from agentforge.utils import Parser
from agentforge.utils.stream import stream_string
from agentforge.ai.attention.tasks import TaskManager
from agentforge.utils import logger
from copy import deepcopy

### COMMUNICATION: Handles response generation
class Summarizer:
    def __init__(self):
        self.service = interface_interactor.get_interface("llm")
        self.tokenizer = interface_interactor.get_interface("tokenizer")
        self.parser = Parser()

    def format_convo(self, conversation: str) -> str:
        return f"### Instruction: Summarize the following conversation. Include all key points and pertinent content. Ignore lists, but include concise comma separated sentences with the same information instead. {conversation} ### Response:"

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        ### Another subroutine gotchu dawg, bail
        gen_config = deepcopy(context.get('model.generation_config'))
        model_config = deepcopy(context.get('model.model_config'))
        username = context.get('input.user_name', "Human")
        agentname = context.get('model.persona.display_name', "Agent")
        conversation, msg_cnt = context.get_messages(prefix=f"\n{username}: ", postfix=f"\n{agentname}:")
        if msg_cnt == 0:
            return context
        logger.info(f"Conversation {msg_cnt}: {conversation}")
        formatted = self.format_convo(conversation)
        response = self.tokenizer.call({'prompt': formatted})
        token_cnt = int(response['text'])
        max_tokens = int(context.get('model.model_config.max_tokens'))
        message_cnt = len(context.get('input.messages'))
        logger.info(f"Token count: {token_cnt}")
        if token_cnt > max_tokens:
            while token_cnt > max_tokens:
                conversation, msg_cnt = context.get_messages(prefix=f"\n{username}: ", postfix=f"\n{agentname}:", n=message_cnt-1)
                formatted = self.format_convo(conversation)
                response = self.tokenizer.call({'prompt': formatted})
                token_cnt = int(response['text'])
                if token_cnt < max_tokens:
                    break
                message_cnt -= 1
            return context

        model_config["streaming"] = False

        input = {
            "prompt": formatted,
            "generation_config": gen_config,
            "model_config": model_config,
            "user_id": context.get("input.user_id"),
            "user_name": context.get("input.user_name"),
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
            context.set("summary", response)
        logger.info(f"SUMMARY: {response}")
        return context
