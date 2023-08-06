from typing import Any, Dict
from agentforge.interfaces.model_profile import ModelProfile
from agentforge.utils import Parser
from agentforge.interfaces import interface_interactor

### Final aggregation of prompt template and other prompt context into
### a single prompt string
class Parse:
    def __init__(self):
        self.parser = Parser()
        self.model_profile = ModelProfile()
        self.db = interface_interactor.get_interface("db")

    def get_model_id(self, context: Dict[str, Any]) -> Dict[str, Any]:
        # if the dictioary is empty we need to load the model_profile
        if "modelId" not in context["input"]:
            raise Exception({"error": "modelId is not found in API input"})

        id = context["input"]["modelId"]
        m_profile = self.model_profile.get(id)
        if m_profile is None:
            raise Exception({"error": "Incorrect Model Profile ID"})
        else:
            context['model_profile'] = m_profile
        return context

    def verify_token_exists(self, context: Dict[str, Any]) -> bool:
        if "apiToken" not in context["input"]:
            raise Exception({"error": "apiToken is not found in API input"})
        token_record = self.db.get("tokens", context["input"]["apiToken"])
        print(token_record)
        if token_record is not None:
            return token_record
        return None
    
    def get_instruction(self, context):
        if 'prompt' in context['input']:
            return context['input']['prompt']
        elif 'messages' in context['input']:
            return context['input']['messages'][-1]['content']
        else:
            raise Exception(f"No valid prompt {context['input']}")

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        ## First check API key for legitimacy
        valid_token = self.verify_token_exists(context)
        if valid_token is None:
            raise Exception(f"Invalid Token {context['input']['apiToken']}")
        # TODO: Bail on this response properly

        context = self.get_model_id(context)

        context["input"]["user_id"] = valid_token["user_id"]
        ### Pull necessary data for prompt template
        prompt_template = context['model_profile']['prompt_config']['prompt_template']
        name = context['model_profile']['avatar_config']['name']
        biography = context['model_profile']['avatar_config']['biography']
        instruction = self.get_instruction(context)
        context['input']['prompt'] = instruction
        memory = context['recall'] if 'recall' in context else ""

        formatted_template = self.parser.format_template(prompt_template,
            name=name,
            instruction=instruction,
            biography=biography,
            memory=memory,
            human="Human"
        )

        ### VALIDATE FORMATTED TEMPLATE
        # formatted_template cannot be greater than the context window size of the model (and is preferably less)
        # we need to tokenize the formatted template and check the length
        # if the length is greater than the context window size, we need to truncate the formatted template
        # To do so we will summarize our most recent memories and truncate the formatted template to fit
        # TODO: Implement this, pull this logic out into it's own function so we can reformat the template
        # i.e. session history back-off, summarization of memories, etc.

        context['input']['formatted'] = formatted_template
        context['input']['prompt_template'] = prompt_template

        # Parse ID from frontend and translate into model_profile
        return context
