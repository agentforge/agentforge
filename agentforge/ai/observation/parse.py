from typing import Any, Dict
from agentforge.interfaces.model_profile import ModelProfile
from agentforge.interfaces import interface_interactor
from agentforge.ai.agents.context import Context

### OBSERVATION: Final aggregation of prompt template and other prompt context into
### a single prompt string
class Parse:
    def __init__(self):
        self.model_profile = ModelProfile()
        self.db = interface_interactor.get_interface("db")

    def ensure_model_id(self, context: Dict[str, Any]) -> Dict[str, Any]:
        # if the dictioary is empty we need to load the model_profile
        if "model_id" not in context.get("input"):
            raise Exception({"error": "model_id is not found in API input"})

        id = context.get("input.model_id")
        m_profile = self.model_profile.get(id)
        if m_profile is None:
            raise Exception({"error": "Incorrect Model Profile ID"})
        else:
            context.set('model', m_profile)
        return context

    def ensure_instruction(self, context):
        if 'prompt' in context.get('input'):
            return context.get('input.prompt')
        elif 'messages' in context.get('input'):
            return context.get('input.messages')[-1]['content']
        else:
            raise Exception(f"No valid prompt {context.get('input')}")

    def execute(self, context: Context) -> Dict[str, Any]:
        context = self.ensure_model_id(context)
        instruction = self.ensure_instruction(context)
        print(context.pretty_print("model"))
        context.set('instruction', instruction)
        context.set('prompt', instruction)
        # Parse ID from frontend and translate into model_profile
        return context
