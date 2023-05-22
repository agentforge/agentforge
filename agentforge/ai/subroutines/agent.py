import os

from langchain import PromptTemplate, LLMChain
from langchain.agents import initialize_agent
from agentforge import helpers
from langchain.agents import Tool
from langchain.llms import HuggingFaceModel
from langchain.utilities import SearxSearchWrapper
from .prompt import Prompt
from agentforge.helpers import Parser
from agentforge.agent import Memory
from agentforge.config import config

from agentforge import LLM_CONFIG_FILE

SEARX_HOST = "https://searx.work/"

os.environ["LANGCHAIN_HANDLER"] = "langchain"

# Dectorator to enable chat memory for the agent and get the prompt
## Future access to tools/plugins/retrieval

### Agent -- Layer over LLMChain Agent system to provide a more user friendly interface w/tools and reasoning
### TODO: Probably deprecated, we aren't currently using tools in production but this can be added
class Agent():
  def __init__(self, opts={}) -> None:
    self.config = config.Config(None)
    # load models.json
    self.config.load_config(LLM_CONFIG_FILE)
    self.parser = Parser()
    self.memory = Memory()

  def set_avatar_context(self, avatar):
    # grab the config
    if "prompt_context" in avatar:
      self.prompt_context = avatar["prompt_context"]
    else:
      raise Exception(f"Should contain prompt_context: {avatar}")

  def get_prompt_type(self, config):
    # TODO: Grab data using Config(models.json) and return the prompt type based on model
    # from the UI
    model_config = self.config.get_config(config["model_key"])
    return model_config["prompt_type"]

  # Get the prompt based on the current model key
  def process_prompt(self, config = {}, **kwargs):
    # Seed context from the avatar json file
    kwargs.update(self.prompt_context)
    kwargs["human_name"] = config["human_name"]
    kwargs["long_term_memories"] = self.memory.get_long_term_memories()
    # get the prompt template
    prompt_type = self.get_prompt_type(config)
    # process the prompt template
    return self.prompt_manager.get_prompt(prompt_type, **kwargs)
  
  # Takes the output from the model and processes it before returning it to the user
  def process_completion(self, text, config, skip_tokens=[]):
    text = self.parser.parse_llm_response(text, skip_tokens=skip_tokens)
    # Remove agent name from the output, sometimes chatbots like to add their name
    return text.replace(config["avatar"]["prompt_context"]["name"] + ":", "")

  # TODO: this is clunky and should be more reactive/data-driven
  def configure(self, config):
    self.set_avatar_context(config["avatar"])
    self.memory.setup_memory(ai_prefix=self.prompt_context["name"], human_prefix=config["human_name"])
    # Rebuild the prompt manager
    self.prompt_manager = Prompt(self.memory)

  # Saves a current speech artifact to the memory
  def save_speech(self, speech):
    if self.memory:
      self.memory.save_speech(speech)

  # Saves a response from another individual to the memory
  def save_response(self, speech):
    if self.memory:
      self.memory.save_response(speech)

  # Setup Agent and load models
  def setup_agent(self):
    self.init_tools()
    self.load()
    self.load_agent()

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
