import re
from agentforge.interfaces import interface_interactor
from agentforge.utils.parser import Parser
from agentforge.utils import logger

class Classifier:
  def __init__(self) -> None:
      self.llm = interface_interactor.get_interface("llm")
      self.parser = Parser()

  def validate_classification(self, test):
      pattern = re.compile(r'### Instruction:\s*(.*?)\s*### Input:\s*(.*?)\s*### Thought Process:\s*(.*?)\s*### Response:\s*(.*?)', re.DOTALL)
      match = pattern.match(test)
      return bool(match)

  ### Given a query and response use a few-shot CoT LLM reponse to pull information out
  def classify(self, args, prompt, context):
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
      if llm_val is not None and "choices" in llm_val:
          response = llm_val["choices"][0]["text"]
          response = response.replace(input_['prompt'], "")
          logger.info("[PROMPT REPLACED]")
          logger.info(response)
          logger.info("[\PROMPT REPLACED]")
          for tok in ["eos_token", "bos_token"]:
              if tok in input_["model_config"]:
                  response = response.replace(input_["model_config"][tok],"")
          ### Often times we do not actually get a response, but just the Chain of Thought
          ### In this case try to rerun the LLM to get a Response
          prompts = input_['prompt'].split("\n\n")
          main_example = prompts[-1]
          logger.info("[MAIN EXAMPLE]")
          logger.info(main_example + "\n" + response)
          logger.info("[MAIN EXAMPLE]")
          if not self.validate_classification(main_example + "\n" + response):
              logger.info("[PROMPTINVALID]")
              logger.info(response)
              logger.info("[PROMPTINVALID]")
              input_["prompt"] = input_["prompt"] + response + "\n### Response:"
              input_["generation_config"]["max_new_tokens"] = 128 # limit so we can focus on results
              llm_val = self.llm.call(input_)
              response = llm_val["choices"][0]["text"]
              response = response.replace(input_['prompt'], "")
          if "Response:" in response:
              response = response.split("Response:")[-1] # TODO: This probably only really works on WizardLM models
          response = response.split("\n")[0] # get rid of additional context usually seperated by newlines
          response = self.parser.parse_llm_response(response).strip()
          logger.info("[PROMPTX]")
          logger.info(response)
          logger.info("[PROMPTX]")
          for tok in ["eos_token", "bos_token"]:
              if tok in input_["model_config"]:
                  response = response.replace(input_["model_config"][tok],"")
          return response.split(",")
      return []