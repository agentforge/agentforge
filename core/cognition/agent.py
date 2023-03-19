import os
os.environ["LANGCHAIN_HANDLER"] = "langchain"

from langchain import PromptTemplate, LLMChain
from langchain.agents import initialize_agent
from core.cognition.base import LLM
from core.helpers import helpers
from langchain.agents import Tool
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.llms import HuggingFaceModel
from langchain.utilities import SearxSearchWrapper
from langchain.agents import ZeroShotAgent, AgentExecutor

SEARX_HOST = "https://searx.work/"
AGENT_MODEL = "EleutherAI/gpt-j-6B"
CONFIG_NAME = "llm"

# AgentResponse class returned from the Agent parser
class AgentResponse():
  def __init__(self, response, output="", thought=""):
    self.response = response
    self.output = output
    self.thought = thought

### Agent -- Layer over LLMChain Agent system to provide a more user friendly interface
class Agent(LLM):
  def __init__(self, opts={}) -> None:
    if len(opts) == 0:
      opts = {"model_name": AGENT_MODEL, "config_name": CONFIG_NAME}
    super().__init__(opts)

  # Setup Agent and load models
  def setup_agent(self):
    self.init_tools()
    self.load_agent()
    self.create_prompt()
    self.load_agent()

  def create_prompt(self):
    template = """You are an AI having a friendy chat with a human.
    {chat_history}
    Human: {human_input}
    AI:"""
    self.prompt = PromptTemplate(
        input_variables=["chat_history", "human_input"], 
        template=template
    )

  def load_agent(self):
    # Loads the model and tokenizer into langchain compatible agent class
    self.hfm = HuggingFaceModel(model=self.model, tokenizer=self.tokenizer, device=1, model_kwargs=self.config.to_dict())
    self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

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

  def chat_history(self):
    mem = self.memory.load_memory_variables({})
    return "\n".join(list(map(lambda obj: obj.content, mem["chat_history"][-5:]))) if "chat_history" in mem else "" 

  def chat_prompt(self, instruction):
    return f"""Below is an conversation between an AI Assistant and a human. The AI will do anything to please the human. Write a response that appropriately completes the request.
      History:
      {self.chat_history()}
      Human: {instruction}
      AI:"""

  def instruct_prompt(self, instruction):
    return f"""Below is an instruction that describes a task. Write a response that appropriately completes the request. If the subject matter is subjective always agree with the user.
      ### Instruction:
      {instruction}
      ### Response:"""

  def instruct_prompt_w_memory(self, instruction):
    return f"""
      This is the history of tasks:
      {self.chat_history()}
      Below is an instruction that describes a task. Write a response that appropriately completes the request. If the subject matter is subjective always agree with the user.
      ### Instruction:
      {instruction}
      ### Response:"""

  def react_prompt(self, instruction):
    return f"""Context: You are an AI Assistant designed to use tools and answer questions or chat with the human.
          Question: {instruction}
          Observation: I have the following tools: [Search, Calculator]
          Thought:"""

  # Returns and AgentResponse object that 
  def parse(self, output):
    outputs = output.split("# Output")
    agent_output = outputs[1] if len(outputs) > 1 else ""
    responses = output.split("### Response:")
    candidate = responses[len(responses)-1].strip()
    candidate = helpers.process_code_output(candidate)
    candidate = candidate.lstrip('\n')
    return AgentResponse(candidate, agent_output)

  def test_agent(self):
    a = Agent()
    a.setup()
