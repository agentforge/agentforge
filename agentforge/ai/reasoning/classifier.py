import re
from agentforge.interfaces import interface_interactor
from agentforge.utils.parser import Parser
from agentforge.utils import logger

# TODO MOVE TO ENV
MAX_CLASSIFIER_RETRIES = 3

"""
    This classification scheme requires knowing the types and options of
    the classification, generally information gained from PDDL or some other
    knowledge graph or world state.
"""
class Classifier:
    def __init__(self) -> None:
        self.llm = interface_interactor.get_interface("llm")
        self.parser = Parser()

    def validate_classification(self, test):
        pattern = re.compile(r'### Instruction:\s*(.*?)\s*### Input:\s*(.*?)\s*### Thought Process:\s*(.*?)\s*### Response:\s*(.*?)', re.DOTALL)
        pattern2 = re.compile(r'Final Decision: ([\-a-zA-Z0-9, _]+)</s>', re.DOTALL)
        pattern3 = re.compile(r'Final classification: ([\-a-zA-Z0-9, _]+)</s>', re.DOTALL)
        match = pattern.match(test)
        match2 = pattern2.match(test)
        match3 = pattern3.match(test)
        return bool(match) or bool(match2) or bool(match3)
  
    def extract_classification(self, test):
        results = []
        patterns = [
            r'Final Decision: ([\-a-zA-Z0-9, _]+)</s>',
            r'Response: ([\-a-zA-Z0-9, _]+)</s>',
            r'Final classification: ([\-a-zA-Z0-9, _]+)</s>',
            r'Final Answer: ([\-a-zA-Z0-9, _]+)</s>',
            r'Final ([\-a-zA-Z0-9, _]+): ([\-a-zA-Z0-9, _]+)</s>',
        ]
        for p in patterns:
            results.append(self.test(p, test))

        res = [x for x in results if x is not None]
        return res[0] if len(res) > 0 else None

    def test(self, pattern, test):
        match = re.search(pattern, test)
        # Extract the value if found
        extracted_value = match.group(0) if match else None
        if extracted_value:
            return extracted_value
        return None

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
        input_ = {
            "prompt": prompt,
            "generation_config": context.get('model.generation_config'), # TODO: We need to use a dedicated model
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
        value = self.extract_classification(generated)
        if value:
            return [value]

        # Remove eos_token and bos_tokens
        for tok in ["eos_token", "bos_token", 'prefix', 'postfix']:
            if tok in input_["model_config"]:
                generated = generated.replace(input_["model_config"][tok],"")

        # Retry with new prompt
        if retries < MAX_CLASSIFIER_RETRIES:
            return self.classify(args, prompt, context, retries=retries+1)
        return []

        ### Often times we do not actually get a response, but just the Chain of Thought
        ### In this case try to rerun the LLM to get a Response
        # prompts = input_['prompt'].split("\n\n")
        # main_example = prompts[-1]
        # logger.info("[MAIN EXAMPLE]")
        # logger.info(main_example + "\n" + response)
        # logger.info("[MAIN EXAMPLE]")
        # if not self.validate_classification(main_example + "\n" + response):
        #     logger.info("[PROMPTINVALID]")
        #     logger.info(response)
        #     logger.info("[PROMPTINVALID]")
        #     input_["prompt"] = input_["prompt"] + response + "\n### Response:"
        #     input_["generation_config"]["max_new_tokens"] = 128 # limit so we can focus on results
        #     llm_val = self.llm.call(input_)
        #     response = llm_val["choices"][0]["text"]
        #     response = response.replace(input_['prompt'], "")
        # value = self.extract_classification(response)

        # if "Response:" in response:
        #     logger.info("[in response]")
        #     response = response.split("Response:")[-1] # TODO: This probably only really works on WizardLM models
        # logger.info(response)
        # response = response.split("\n")[0] # get rid of additional context usually seperated by newlines

        # response = self.parser.parse_llm_response(response).strip()
        # logger.info("[PROMPTX]")
        # logger.info(response)
        # logger.info("[PROMPTX]")
        # for tok in ["eos_token", "bos_token"]:
        #     if tok in input_["model_config"]:
        #         response = response.replace(input_["model_config"][tok],"")
        return response.split(",")