from typing import Any, Dict
from agentforge.interfaces import interface_interactor
from agentforge.utils import Parser

class Respond:
    def __init__(self):
        self.service = interface_interactor.get_interface("llm")
        self.parser = Parser()

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        ### Another subroutine gotchu dawg, bail
        if "response" in context:
            return context

        input = {
            "prompt": context['input']['prompt'],
            "generation_config": context['model_profile']['generation_config'],
            "model_config": context['model_profile']['model_config'],
        }
        response = self.service.call(input)

        if response is not None and "choices" in response:
            context["response"] = response["choices"][0]["text"]

            ### We want to parse the output here -- this output goes to end user
            context["response"] = context["response"].replace(context['input']['prompt'], "")
            context["response"] = self.parser.parse_llm_response(context["response"])
            for tok in ['eos_token', 'bos_token']:
                if tok in context['model_profile']['model_config']:
                    context["response"] = context["response"].replace(context['model_profile']['model_config'][tok], "")
            print(context["response"])

        return context
