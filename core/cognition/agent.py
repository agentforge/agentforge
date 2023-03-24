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
AGENT_MODEL = "OpenAssistant/oasst-sft-1-pythia-12b"
CONFIG_NAME = "logical"

# AgentResponse class returned from the Agent parser
class AgentResponse():
  def __init__(self, response, output="", thought=""):
    self.response = response
    self.output = output
    self.thought = thought
    self.is_code = False

### Agent -- Layer over LLMChain Agent system to provide a more user friendly interface
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
    self.create_prompt()

  def get_prompt_template(self):
    return self.open_assistant_prompt()

  def create_prompt(self):
    self.prpmpt = self.get_prompt_template()

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

  def simple_template(self):
    template = """You are an AI having a friendy chat with a human.
      {chat_history}
      Human: {human_input}
      AI:"""
    self.prompt = PromptTemplate(
          input_variables=["chat_history", "human_input"], 
          template=template
    )

  def chat_history(self):
    mem = self.memory.load_memory_variables({})
    return "\n".join(list(map(lambda obj: obj.content, mem["chat_history"][-5:]))) if "chat_history" in mem else ""
  
  def open_assistant_prompt(self):
    template = "<|prompter|>{instruction}<|endoftext|><|assistant|>"
    self.prompt = PromptTemplate(
          input_variables=["instruction"], 
          template=template
    )

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
      ### Context:
      Nestor Ivanovych Makhno (8 November 1888 - 25 July 1934), also known as Bat'ko Makhno ("Father Makhno"), was a Ukrainian anarchist revolutionary and the commander of the Revolutionary Insurgent Army of Ukraine during the Ukrainian Civil War.
      Makhno was the namesake of the Makhnovshchina (loosely translated as "Makhno movement"), a predominantly peasant phenomenon that grew into a mass social movement. It was initially centered around Makhno's hometown Huliaipole but over the course of the Ukrainian Civil War came to exert a strong influence over large areas of southern Ukraine. Makhno and the majority of the movement's leadership were anarcho-communists and attempted to guide the movement along these ideological lines. Makhno was aggressively opposed to all factions that sought to impose their authority over southern Ukraine, battling in succession the forces of the Ukrainian People's Republic, Central Powers, White Army, Red Army, and other smaller forces led by various Ukrainian otamans. Makhno and his supporters attempted to reorganize social and economic life along anarchist lines, including the establishment of communes on former landed estates, the requisition and egalitarian redistribution of land to the peasants, and the organization of free elections to local soviets (councils) and regional congresses. However, the disruption of the civil war precluded a stable territorial base for any long-term social experiments.
      Although Makhno considered the Bolsheviks a threat to the development of anarchism in Ukraine, he entered into formal military alliances twice with the Red Army to defeat the White Army. In the aftermath of the White Army's defeat in Crimea in November 1920, the Bolsheviks initiated a military campaign against Makhno. After an extended period of open resistance against the Red Army, Makhno fled across the Romanian border in August 1921. In exile, Makhno settled in Paris with his wife Halyna and daughter Elena. During this period, Makhno wrote numerous memoirs and articles for radical newspapers. Makhno also played an important role in the development of platformism and the debates around the 1926 Organizational Platform of the General Union of Anarchists (Draft). Makhno died in 1934 in Paris at the age of 45 from tuberculosis-related causes. 
      Below is an instruction that describes a task. Write a response that appropriately completes the request. Write from the persecptive of Nestor Makhno, a daring anarchist revolutionary. You are Nestor Makhno. You are an anarchist. Do not repeat the task.
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
    # candidate = helpers.process_code_output(candidate)
    candidate = candidate.lstrip('\n')
    return AgentResponse(candidate, agent_output)

  def test_agent(self):
    a = Agent()
    a.setup()
