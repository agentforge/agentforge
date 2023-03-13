### Primary Class for Agent Executor 

from langchain.agents import Tool
from langchain.chains.conversation.memory import ConversationBufferMemory
from core.llm.transformer import LLM
from langchain.utilities import GoogleSearchAPIWrapper
from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
from langchain.llms import HuggingFaceModel
from langchain import PromptTemplate, LLMChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory, ConversationSummaryMemory, CombinedMemory
from langchain.utilities import SearxSearchWrapper
from langchain.agents import initialize_agent

SEARX_HOST = "https://searx.work/"
AGENT_MODEL = "EleutherAI/gpt-j-6B"
CONFIG_NAME = "llm.json"

### Inherits from the LLM class giving the agent access to its own LLM
class Agent(LLM):
  def __init__(self) -> None:
    super().__init__(AGENT_MODEL, CONFIG_NAME, {})
    self.setup()

  # Setup Agent and load models
  def setup(self):
    self.setup_tools()
    self.load()

    # Loads the model and tokenizer into langchain compatible class

    args = {}
    self.hfm = HuggingFaceModel(model=self.model, tokenizer=self.tokenizer, device=1, model_kwargs=args)

    # summary_memory = ConversationSummaryMemory(llm=self.hf, input_key="question")
    # prompt_template = PromptTemplate(input_variables=["history","chat_history","question"], template=template)
    # conv_memory = ConversationBufferWindowMemory(k=5, memory_key="chat_history", input_key="question", ai_prefix="Sydney", human_prefix="Human")

    # memory = CombinedMemory(memories=[conv_memory, summary_memory])
    memory = ConversationBufferMemory(memory_key="chat_history")

    self.llm_chain = LLMChain(
        llm=self.hfm,
        verbose=True,
        # memory=conv_memory,
    )

    self.agent_chain = initialize_agent(self.tools, self.llm_chain, agent="conversational-react-description", verbose=True, memory=memory)

  def run(self, question):
    # Run the agent
    response = self.agent_chain.run(question)

    return response
  
  def setup_tools(self):
    self.search = SearxSearchWrapper(searx_host=SEARX_HOST)
    self.tools = [
      Tool(
          name = "Current Search",
          func=self.search.run,
          description="useful for when you need to answer questions about current events or the current state of the world"
      ),
    ]