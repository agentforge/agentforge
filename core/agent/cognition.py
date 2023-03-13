### Primary Class for Agent Executor 

from langchain.agents import Tool
from langchain.chains.conversation.memory import ConversationBufferMemory
from core.llm.transformer import LLM
from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
from langchain.llms import HuggingFaceModel
from langchain import PromptTemplate, LLMChain
from langchain.utilities import SearxSearchWrapper
from langchain.agents import initialize_agent

SEARX_HOST = "https://searx.work/"
AGENT_MODEL = "EleutherAI/gpt-j-6B"
CONFIG_NAME = "llm"

### Inherits from the LLM class gi  ving the agent access to its own LLM
class Agent(LLM):
  def __init__(self) -> None:
    super().__init__({"model_name": AGENT_MODEL, "config_name": CONFIG_NAME})

  # Setup Agent and load models
  def setup(self):
    self.init_tools()
    self.load()
    self.create_prompt()
    self.agent()

  def create_prompt(self):
    template = """You are an AI having a friendy chat with a human.
    {chat_history}
    Human: {human_input}
    AI:"""
    self.prompt = PromptTemplate(
        input_variables=["chat_history", "human_input"], 
        template=template
    )

  def agent(self):
    # Loads the model and tokenizer into langchain compatible agent class
    self.hfm = HuggingFaceModel(model=self.model, tokenizer=self.tokenizer, device=1)
    memory = ConversationBufferMemory(memory_key="chat_history")
    self.llm_chain = LLMChain(
        prompt=self.prompt,
        llm=self.hfm,
        verbose=True,
        memory=memory,
    )
    self.agent_chain = initialize_agent(self.tools, self.hfm, agent="conversational-react-description", verbose=True, memory=memory)

  def run(self, question):
    # Run the agent
    response = self.llm_chain.run(question)
    return response
  
  def init_tools(self):
    self.search = SearxSearchWrapper(searx_host=SEARX_HOST)
    self.tools = [
      Tool(
          name = "Current Search",
          func=self.search.run,
          description="useful for when you need to answer questions about current events or the current state of the world"
      ),
    ]

  def test_agent(self):
    a = Agent()
    a.setup()