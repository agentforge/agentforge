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
        print(context["input"]["apiToken"])
        token_record = self.db.get("tokens", {"token": context["input"]["apiToken"]})
        if token_record is not None and "token" in token_record:
            return token_record
        return None

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        ## First check API key for legitimacy
        valid_token = self.verify_token_exists(context)
        if valid_token is None:
            raise Exception("Invalid Token")
        # TODO: Bail on this response properly

        context = self.get_model_id(context)

        ### Pull necessary data for prompt template
        prompt_template = context['model_profile']['prompt_config']['prompt_template']
        name = context['model_profile']['avatar_config']['name']
        biography = context['model_profile']['avatar_config']['biography']
        instruction = context['input']['prompt']
        memory = context['recall'] if 'recall' in context else ""

        formatted_template = self.parser.format_template(prompt_template,
            name=name,
            instruction=instruction,
            biography=biography,
            memory=memory,
            human="Human"
        )

        context['input']['formatted'] = formatted_template
        context['input']['prompt_template'] = prompt_template

        # Parse ID from frontend and translate into model_profile
        return context
