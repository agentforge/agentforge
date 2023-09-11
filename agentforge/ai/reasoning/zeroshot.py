import re
from agentforge.interfaces import interface_interactor
from agentforge.utils.parser import Parser
from agentforge.utils import logger
from copy import deepcopy

# TODO MOVE TO ENV
MAX_Z0_CLASSIFIER_RETRIES = 1

"""
    Single shot classification
"""

class ZeroShotClassifier:
    def __init__(self) -> None:
        self.llm = interface_interactor.get_interface("llm")
        self.parser = Parser()

    def extract_classification(self, test):
        for klass in self.klasses:
            p = r'<s>\s*{klass}\s*</s>'
            p = p.replace("{klass}", klass)
            logger.info("[TESTING]")
            logger.info(p)
            result = self.test(p, test)
            if result is not None:
                return result
        return None

    def test(self, pattern, test):
        match = re.search(pattern, test)
        # Extract the value if found
        extracted_value = match.group(0) if match else None
        if extracted_value:
            return extracted_value
        return None

    ### Given a query and response use a few-shot CoT LLM reponse to pull information out
    def classify(self, prompt: str, klasses, args, context, retries=0):
        self.klasses = klasses
        for k, v in args.items():
            prompt = prompt.replace(f"{{{k}}}", v)
        
        gen_config = deepcopy(context.get('model.generation_config'))
        input_ = {
            "prompt": prompt,
            "generation_config": gen_config, # TODO: We need to use a dedicated model
            "model_config": context.get('model.model_config'),
            "streaming_override": False, # sets streaming to False
            "sequence_bias": klasses,
        }
        input_["generation_config"]["max_new_tokens"] = 4
        input_["generation_config"]["min_new_tokens"] = 0

        # Disable streaming of classification output -- deepcopy so we don't effect the model_config
        logger.info("[PROMPT]")
        logger.info(input_['prompt'])
        logger.info("[PROMPT]")

        llm_val = self.llm.call(input_)
        if llm_val is None or "choices" not in llm_val:
            return []

        response = llm_val["choices"][0]["text"]
        generated = response.replace(input_['prompt'], "")

        logger.info("[PROMPT REPLACED]")
        logger.info(generated)
        logger.info("[\PROMPT REPLACED]")
        
        # Attempt regex extraction
        value = self.extract_classification(generated)
        if not value:
            # logger.info("[PROMPT REPLACED]")
            # # Retry with new prompt
            # if retries < MAX_Z0_CLASSIFIER_RETRIES:
            #     return self.classify(prompt, klasses, args, context, retries=retries+1)
            return None

        # Remove eos_token and bos_tokens
        for tok in ["eos_token", "bos_token", 'prefix', 'postfix']:
            if tok in input_["model_config"]:
                value = value.replace(input_["model_config"][tok],"")

        return value.strip()
