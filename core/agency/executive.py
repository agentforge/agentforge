### Primary Class for Agent Executor 

from langchain.agents import Tool
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.llms import HuggingFaceModel
from langchain import PromptTemplate, LLMChain
from langchain.utilities import SearxSearchWrapper
from langchain.agents import initialize_agent

class ExecutiveCognition():
  def __init__(self) -> None:
    pass

