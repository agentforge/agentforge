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
        )

        context['input']['prompt'] = formatted_template
        context['input']['original_prompt'] = instruction
        context['input']['prompt_template'] = prompt_template

        # Parse ID from frontend and translate into model_profile
        return context
