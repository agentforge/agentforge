
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain import PromptTemplate, LLMChain
from langchain.llms import HuggingFacePipeline
import torch, random
from config import Config
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from transformers.configuration_utils import PretrainedConfig
from langchain.agents import initialize_agent
from langchain.agents import load_tools

class GPTChatbot:
  def __init__(self):
    self._c = Config()
    self.model_config = PretrainedConfig()
    self.model = AutoModelForCausalLM.from_pretrained(
      self._c.config["gpt_model_cache"],
      revision="float16",
      torch_dtype=torch.float16,
    )
    self.tokenizer = AutoTokenizer.from_pretrained(self._c.config["tokenizer_cache"])

    args = { 
      "temperature":self._c.config["temperature"], 
      #"max_length":64,
      "top_k": 100,
      "top_p": 0.7,
      #"revision": "float16",
      #"torch_dtype": torch.float16,
    }


    # device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    # self.model = self.model.to(device)
    pipe = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer, device=0, model_kwargs=args, max_new_tokens=256)
    self.hf = HuggingFacePipeline(pipeline=pipe)
    self.model_kwargs = args
    self.device = 0
    # self.hf = HuggingFacePipeline.from_model_id(model_id=self._c.config["gpt_model_cache"], task="text-generation", device=1, model_kwargs=args)

    template = """You are a friendly AI having a conversation with a Human. Be nice.
    {chat_history}
    Human: {question}
    Answer:
    """

    prompt_template = PromptTemplate(input_variables=["chat_history","question"], template=template)
    memory = ConversationBufferWindowMemory(k=2, memory_key="chat_history")

    self.llm_chain = LLMChain(
        prompt=prompt_template,
        llm=self.hf,
        verbose=True,
        memory=memory,
    )

    self.tools = load_tools(["google-search"], llm=self.llm_chain)

    agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

  def handle_input(self, input_str, opts):
    self.opts = opts
    stop_words = ["Human:", "human:", "AI:", "Assistant:", "assistant:"]
    self.result = self.llm_chain.predict(stop=stop_words, question=input_str)
    return {"response": self.result}

if __name__ == "__main__":
  pass
