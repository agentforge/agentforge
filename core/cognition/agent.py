import os
os.environ["LANGCHAIN_HANDLER"] = "langchain"

from langchain import PromptTemplate, LLMChain
from langchain.agents import initialize_agent
from core.cognition.base import LLM
from core.helpers import helpers
from langchain.agents import Tool
from langchain.llms import HuggingFaceModel
from langchain.utilities import SearxSearchWrapper

SEARX_HOST = "https://searx.work/"
AGENT_MODEL = "OpenAssistant/oasst-sft-1-pythia-12b"
CONFIG_NAME = "logical"

# AgentResponse class returned from the Agent parser
class AgentResponse():
  def __init__(self, response, output="", thought=""):
    self.response = response
    self.output = output
    self.thought = thought
    self.is_code = False

### Agent -- Layer over LLMChain Agent system to provide a more user friendly interface w/tools and reasoning
class Agent(LLM):
  def __init__(self, opts={}) -> None:
    if len(opts) == 0:
      opts = {"model_name": AGENT_MODEL, "config": CONFIG_NAME}
    super().__init__(opts)

  # Setup Agent and load models
  def setup_agent(self):
    self.init_tools()
    self.load()
    self.load_agent()

    # create a new prompt loaded with memory
    self.prompt_manager = Prompt(self.memory)

  def load_agent(self):
    # Loads the model and tokenizer into langchain compatible agent class
    self.hfm = HuggingFaceModel(model=self.model, tokenizer=self.tokenizer, device=1, model_kwargs=self.config.to_dict())

  def think(self):
    pass

  def init_tools(self):
    self.search = SearxSearchWrapper(searx_host=SEARX_HOST)
    self.tools = [
      Tool(
          name = "[Current Search]",
          func=self.search.run,
          description="useful for when you need to answer questions about current events or the current state of the world"
      ),
    ]

  # Returns and AgentResponse object that 
  def parse(self, output):
    outputs = output.split("# Output")
    agent_output = outputs[1] if len(outputs) > 1 else ""
    responses = output.split("### Response:")
    candidate = responses[len(responses)-1].strip()
    # candidate = helpers.process_code_output(candidate)
    candidate = candidate.lstrip('\n')
    return AgentResponse(candidate, agent_output)

  def test_agent(self):
    a = Agent()
    a.setup()
