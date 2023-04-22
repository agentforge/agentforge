### Memory Module for the Agent
import uuid, datetime, threading
from langchain.memory import ConversationBufferMemory
from langchain.vectorstores import DeepLake
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter

class Memory:
  def __init__(self, model_name="decapoda-research/llama-7b-hf"):
    self.memories = {}
    # self.embdeddings = HuggingFaceEmbeddings(model_name=model_name)
    # Use deeplake for long-term vector memory storage
    # self.deeplake = DeepLake(dataset_path="/app/cache/deeplake2", embedding_function=self.embdeddings)

  # Stores memory for various agent avatars
  def setup_memory(self, ai_prefix = "AI", human_prefix = "Human"):
    # Supports short-term memory for multiple people
    if ai_prefix in self.memories:
      self.short_term_memory = self.memories[ai_prefix]
    else:
      self.short_term_memory = ConversationBufferMemory(return_messages=True)
      self.short_term_memory.human_prefix = human_prefix
      self.short_term_memory.ai_prefix = ai_prefix
      self.memories[ai_prefix] = self.short_term_memory

  # Saves a current speech artifact to the memory
  def save_speech(self, speech):
    if self.short_term_memory:
      self.short_term_memory.chat_memory.add_user_message(speech)

  # Saves a response from another individual to the memory
  def save_response(self, speech):
    if self.short_term_memory:
      self.short_term_memory.chat_memory.add_ai_message(speech)

  def recall(self, prompt):
    pass
    # docs = self.deeplake.similarity_search(prompt)
    # print(docs)

  # Async method using threading for memorization -- need app for Flask context
  def remember(self, prompt, text, app):
      remember_thread_args=(prompt, text, app)
      remember_thread = threading.Thread(target=self.remember_with_app_context, args=remember_thread_args )
      remember_thread.start()

  # Locking and thread ontext for async memory processing
  def remember_with_app_context(self, prompt, response, app):
      with app.app_context():
          self.agent.memory.save_interaction(prompt, response)

  # Saves a response from another individual to long-term memory
  def save_interaction(self, prompt, response):
    # Do not save empty interactions
    if prompt.strip() == "":
      return
    interaction = f"""{self.short_term_memory.human_prefix}: {prompt}\n{ self.short_term_memory.ai_prefix}: {response}"""
    self.deeplake.add_texts(
      [interaction], [{"source": self.short_term_memory.ai_prefix, "time": datetime.datetime.now()}], [uuid.uuid4()]
    )