import os

from langchain import PromptTemplate, LLMChain
from langchain.agents import initialize_agent
from historica import helpers
from langchain.agents import Tool
from langchain.llms import HuggingFaceModel
from langchain.utilities import SearxSearchWrapper
from langchain.chains.conversation.memory import ConversationBufferMemory
from .prompt import Prompt
from historica.helpers import Parser

SEARX_HOST = "https://searx.work/"
AGENT_MODEL = "OpenAssistant/oasst-sft-1-pythia-12b"
CONFIG_NAME = "logical"

os.environ["LANGCHAIN_HANDLER"] = "langchain"

# Dectorator to enable chat memory for the agent and get the prompt
## Future access to tools/plugins/retrieval

### Agent -- Layer over LLMChain Agent system to provide a more user friendly interface w/tools and reasoning
class Agent():
  def __init__(self, opts={}) -> None:
    self.memories = {}
    self.parser = Parser()  # brain soup

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

  def set_avatar_context(self, avatar):
    # grab the config
    if "prompt_context" in avatar:
      self.prompt_context = avatar["prompt_context"]
    else:
      raise Exception(f"Should contain prompt_context: {avatar}")

  def get_prompt_type(self):
    # TODO: Grab data using Config(models.json) and return the prompt type based on model
    # from the UI
    return "instruct_w_memory"

  # Get the prompt based on the current model key
  def get_prompt(self, **kwargs):
    # If memory is an argument let's extract relevant information from it
    kwargs.update(self.prompt_context)
    prompt_type = self.get_prompt_type()
    return self.prompt_manager.get_prompt(prompt_type, **kwargs)

  def configure(self, config):
    self.set_avatar_context(config["avatar"])
    self.setup_memory(ai_prefix=self.prompt_context["name"], human_prefix=config["human_name"])

  # Saves a current speech artifact to the memory
  def save_speech(self, speech):
    if self.memory:
      self.memory.chat_memory.add_user_message(speech)

  # Saves a response from another individual to the memory
  def save_response(self, speech):
    if self.memory:
      self.memory.chat_memory.add_ai_message(speech)

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

  def init_tools(self):
    self.search = SearxSearchWrapper(searx_host=SEARX_HOST)
    self.tools = [
      Tool(
          name = "[Current Search]",
          func=self.search.run,
          description="useful for when you need to answer questions about current events or the current state of the world"
      ),
    ]

  def test_agent(self):
    a = Agent()
    a.setup()
