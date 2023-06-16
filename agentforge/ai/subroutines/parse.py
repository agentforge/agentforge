from typing import Any, Dict
from agentforge.interfaces.model_profile import ModelProfile

### Final aggregation of prompt template and other prompt context into
### a single prompt string
class Parse:
    def __init__(self):
        self.model_profile = ModelProfile()

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        prompt_template = context['model_profile']['prompt_config']['prompt_template']
        name = context['model_profile']['avatar_config']['name']
        biography = context['model_profile']['avatar_config']['biography']
        instruction = context['input']['prompt']
        recall = context['recall'] if 'recall' in context else ""

        print(recall)
        prompt_template = prompt_template.replace("<name>", name)
        prompt_template = prompt_template.replace("<biography>", biography)
        prompt_template = prompt_template.replace("<instruction>", instruction)
        prompt_template = prompt_template.replace("<memory>", recall)

        context['input']['prompt'] = prompt_template
        context['input']['original_prompt'] = instruction

        # Parse ID from frontend and translate into model_profile
        return context
