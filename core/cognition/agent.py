
from langchain import PromptTemplate, LLMChain
from langchain.agents import initialize_agent
from core.cognition.base import LLM
from langchain.agents import Tool
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.llms import HuggingFaceModel
from langchain.utilities import SearxSearchWrapper
from langchain.agents import ZeroShotAgent, AgentExecutor

SEARX_HOST = "https://searx.work/"
AGENT_MODEL = "EleutherAI/gpt-j-6B"
CONFIG_NAME = "llm"

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
    # template = """You are an AI having a friendy chat with a human.
    # {chat_history}
    # Human: {human_input}
    # AI:"""
    # self.prompt = PromptTemplate(
    #     input_variables=["chat_history", "human_input"], 
    #     template=template
    # )
    prefix = """Answer the following questions as best you can. You have access to the following tools:"""
    suffix = """be polite!

    Question: {input}
    {agent_scratchpad}"""

    self.prompt = ZeroShotAgent.create_prompt(
        self.tools, 
        prefix=prefix, 
        suffix=suffix, 
        input_variables=["input", "agent_scratchpad"]
    )

  def load_agent(self):
    # Loads the model and tokenizer into langchain compatible agent class
    self.hfm = HuggingFaceModel(model=self.model, tokenizer=self.tokenizer, device=1, model_kwargs=self.config.to_dict())
    memory = ConversationBufferMemory(memory_key="chat_history")
    self.llm_chain = LLMChain(
        prompt=self.prompt,
        llm=self.hfm,
        verbose=True,
        memory=memory,
    )
    self.agent_chain = initialize_agent(self.tools, self.hfm, agent="conversational-react-description", verbose=True, memory=memory)
    tool_names = [tool.name for tool in self.tools]
    self.agent_exec = ZeroShotAgent(llm_chain=self.llm_chain, allowed_tools=tool_names)

  def generate(self, prompt):
    response = self.llm_chain.run(prompt)
    return response

  def run(self, question):
    # Run the agent
    response = self.agent_exec.run(question)
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