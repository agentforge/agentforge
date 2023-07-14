from typing import Any, Dict
from agentforge.interfaces.model_profile import ModelProfile
from agentforge.utils import Parser

### Final aggregation of prompt template and other prompt context into
### a single prompt string
class Parse:
    def __init__(self):
        self.parser = Parser()
        self.model_profile = ModelProfile()

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        print(context)
        ### PROD CASE
        # if the dictioary is empty we need to load the model_profile
        if "id" not in context["input"]:
            context["error"] = "ID is not found in API input"
            context["status"] = 500
            raise Exception(context)

        id = context["input"]["id"]
        m_profile = self.model_profile.get(id)
        if m_profile is None:
            context["error"] = "Incorrect Model Profile ID"
            context["status"] = 500
            raise Exception(context)
        else:
            context['model_profile'] = m_profile

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
