
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain import PromptTemplate, LLMChain
from langchain.llms import HuggingFacePipeline
import torch, random
from config import Config
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from transformers.configuration_utils import PretrainedConfig


class GPTChatbot:
  def __init__(self):
    self._c = Config()
    self.model_config = PretrainedConfig()
    self.model = AutoModelForCausalLM.from_pretrained(
      self._c.config["gpt_model_cache"],
      
    )
    self.tokenizer = AutoTokenizer.from_pretrained(self._c.config["tokenizer_cache"])

    args = { 
      #"temperature":self._c.config["temperature"], 
      #"max_length":64,
      #"top_k": 100,
      #"top_p": 0.7,
      "revision": "float16",
      "torch_dtype": torch.float16,
    }

    pipe = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer, max_new_tokens=64)
    self.hf = HuggingFacePipeline(pipeline=pipe)
    self.model_kwargs = args
    self.device = 0
    # self.hf = HuggingFacePipeline.from_model_id(model_id=self._c.config["gpt_model_cache"], task="text-generation", device=1, model_kwargs=args)

    template = """You are a teacher in physics for High School student. Given the text of question, it is your job to write a answer that question with example.
    {chat_history}
    Human: {question}
    AI:
    """
    prompt_template = PromptTemplate(input_variables=["chat_history","question"], template=template)
    memory = ConversationBufferMemory(memory_key="chat_history")

    self.llm_chain = LLMChain(
        prompt=prompt_template,
        llm=self.hf,
        verbose=True,
        memory=memory,
    )

  def handle_input(self, input_str, opts):
    self.opts = opts
    self.result = self.llm_chain.predict(question=input_str)
    return {"response": self.result}

  def max_length(self, prompt):
    value = random.randint(self._c.config["max_length_itr_min"], self._c.config["max_length_itr_max"])
    # Returns the optimal max_length for this model
    return int(max(len(prompt) + value, len(prompt)))


if __name__ == "__main__":
  pass
