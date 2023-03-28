import os
os.environ["LANGCHAIN_HANDLER"] = "langchain"

from langchain import PromptTemplate, LLMChain
from langchain.agents import initialize_agent
from core.cognition.base import LLM
from core.helpers import helpers
from langchain.agents import Tool
from langchain.llms import HuggingFaceModel
from langchain.utilities import SearxSearchWrapper
from langchain.chains.conversation.memory import ConversationBufferMemory
from core.cognition.prompt import Prompt

SEARX_HOST = "https://searx.work/"
AGENT_MODEL = "OpenAssistant/oasst-sft-1-pythia-12b"
CONFIG_NAME = "logical"

# Dectorator to enable chat memory for the agent and get the prompt
def chat_memory_enabled(func):
  def wrapper(self, instruct, **kwargs):
      # Get the prompt from the prompt manager
      instruct = self.get_prompt(instruction=instruct)

      # Call add_user_message before the function is called
      self.memory.chat_memory.add_user_message(instruct)
      
      # Call the original function
      out = func(self, instruct, **kwargs)
      
      # Call add_ai_message after the function returns
      self.memory.chat_memory.add_ai_message(out.response)
      
      # Return the function's original return value
      return out
  return wrapper

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
    self.memories = {}

  # Stores memory for various agent avatars
  def setup_memory(self, ai_prefix = "AI", human_prefix = "Human"):
    if ai_prefix in self.memories:
      self.memory = self.memories[ai_prefix]
    else:
      self.memory = ConversationBufferMemory(return_messages=True)
      self.memory.human_prefix = human_prefix
      self.memory.ai_prefix = ai_prefix
      self.memories[ai_prefix] = self.memory
    # Rebuild the prompt manager
    self.prompt_manager = Prompt(self.memory)

  def configure(self, config):
    super().configure(config)
    self.setup_memory(ai_prefix=self.prompt_context["name"], human_prefix=config["human_name"])

  # Setup Agent and load models
  def setup_agent(self):
    self.init_tools()
    self.load()
    self.load_agent()

    # create a new prompt loaded with memory
    # self.prompt_manager = Prompt(self.memory)

  def load_agent(self):
    # Loads the model and tokenizer into langchain compatible agent class
    self.hfm = HuggingFaceModel(model=self.model, tokenizer=self.tokenizer, device=1, model_kwargs=self.generation_config.to_dict())

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
