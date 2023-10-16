import re
from agentforge.interfaces import interface_interactor
from agentforge.utils.parser import Parser
from agentforge.utils import logger
from copy import deepcopy

# TODO MOVE TO ENV
MAX_CLASSIFIER_RETRIES = 3

"""
    This classification scheme requires knowing the types and options of
    the classification, generally information gained from PDDL or some other
    knowledge graph or world state.
"""

def extract_classification(val):
    results = []
    patterns = [
        r'[\s\S]*?Final Decision: ([\-a-zA-Z0-9, _]+)\s*(</s>)?',
        r'[\s\S]*?Response: ([\-a-zA-Z0-9, _]+)\s*(</s>)?',
        r'[\s\S]*?Final classification: ([\-a-zA-Z0-9, _]+)\s*(</s>)?',
        r'[\s\S]*?Final Answer: ([\-a-zA-Z0-9, _]+)\s*(</s>)?',
        r'[\s\S]*?Final Output: ([\-a-zA-Z0-9, _]+)\s*</s>',
        r'[\s\S]*?Response: \[(\"?)([a-zA-Z0-9\s]+)(\"?)\]\s*(</s>)?',
        r'[\s\S]*?[a-zA-Z0-9\s]+: \[?\"?([a-zA-Z0-9\s]+)\"?\]?\s*(</s>)?'
        # r'[\s\S]*?Final ([\-a-zA-Z0-9, _]+): ([\-a-zA-Z0-9, _]+)</s>',
    ]
    for p in patterns:
        ret = test(p, val)
        results.append(ret)

    res = [x for x in results if x is not None]
    return res[0] if len(res) > 0 else None

def test(pattern, v):
    match = re.search(pattern, v)
    # Extract the value if found
    extracted_value = match.groups()[0] if match else None
    if extracted_value:
        return extracted_value
    return None

class Classifier:
    def __init__(self) -> None:
        self.llm = interface_interactor.get_interface("llm")
        self.parser = Parser()

    """
        Given a query and response use a few-shot CoT LLM reponse to pull information out
        
        Input - context: Context object
        prompt = context.prompts["relation.prompt"]
        args = {
          "object": query['object'].replace("?","").strip().title(),
          "subject": "User",
          "goal": query['goal'],
          "action": query['action'],
        }
    """
    def classify(self, args, prompt, context, retries=0):
        for k, v in args.items():
            prompt = prompt.replace(f"{{{k}}}", v)
        gen_config = deepcopy(context.get('model.generation_config'))
        gen_config['stopping_criteria'] = []
        input_ = {
            "prompt": prompt,
            "generation_config": gen_config, # TODO: We need to use a dedicated model
            "model_config": context.get('model.model_config'),
            "streaming_override": False, # sets streaming to False
        }
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
        value = extract_classification(generated)
        logger.info(f"EXTRACTED ==> {value}")
        if value:
            logger.info("RETURNING VALUE")
            return [value]

        # Remove eos_token and bos_tokens
        for tok in ["eos_token", "bos_token", 'prefix', 'postfix']:
            if tok in input_["model_config"]:
                generated = generated.replace(input_["model_config"][tok],"")

        # Retry with new prompt
        if retries < MAX_CLASSIFIER_RETRIES:
            return self.classify(args, prompt, context, retries=retries+1)
        return []
