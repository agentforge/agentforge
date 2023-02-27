
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


    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    self.model = self.model.to(device)
    pipe = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer, device=0, model_kwargs=args, max_new_tokens=64)
    self.hf = HuggingFacePipeline(pipeline=pipe)
    self.model_kwargs = args
    self.device = 0
    # self.hf = HuggingFacePipeline.from_model_id(model_id=self._c.config["gpt_model_cache"], task="text-generation", device=1, model_kwargs=args)

    template = """You are a teacher in physics for High School student. Given the text of question, it is your job to write a answer that question with example.
    {chat_history}
    Human: {question}
    Answer in MarkDown:
    """
    assistant_template = """Assistant is a large language model trained by OpenAI.

    Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

    Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

    Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.

    {chat_history}
    Human: {question}
    Assistant:"""

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
    stop_words = ["Human:", "human:", "AI:", "Assistant:", "assistant:"]
    self.result = self.llm_chain.predict(stop=stop_words, question=input_str)
    return {"response": self.result}

if __name__ == "__main__":
  pass
