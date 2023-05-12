### Memory Module for the Agent
### This is the neuro-symbolic core for the long-term memory of the agent
### It is responsible for storing and retrieving memories
### similarity functions to access memories and methods to forget
### Forgetting is an important part of learning and memory

import uuid, datetime, threading
from copy import deepcopy
from langchain.memory import ConversationBufferMemory
from langchain.vectorstores import DeepLake
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document
from langchain.retrievers import TimeWeightedVectorStoreRetriever
import shutil

class MemDoc():
   def __init__(self, text, metadata):
      self.page_content = text
      self.metadata = metadata

class Memory:
  def __init__(self, model_name='sentence-transformers/all-mpnet-base-v2'):
    self.memories = {}
    self.embdeddings = HuggingFaceEmbeddings(model_name=model_name)
    ### FOR TESTING DANGER LIES AHEAD
    directory_path = "/app/cache/deeplake-x27"
    try:
        shutil.rmtree(directory_path)
        print(f"Directory '{directory_path}' has been deleted.")
    except FileNotFoundError:
        print(f"Directory '{directory_path}' not found.")
    except Exception as e:
        print(f"Error while deleting directory '{directory_path}': {e}")
    # Use deeplake for long-term vector memory storage
    self.deeplake = DeepLake(dataset_path="/app/cache/deeplake-x27", embedding_function=self.embdeddings)
    self.long_term_memories = []
    self.retriever = TimeWeightedVectorStoreRetriever(vectorstore=self.deeplake, decay_rate=.0000000000000000000000001, k=4)
    self.human_prefix = "Human"
    self.ai_prefix = "AI"

  # Stores memory for various agent avatars
  def setup_memory(self, ai_prefix = "AI", human_prefix = "Human"):
    self.human_prefix = human_prefix
    self.ai_prefix = ai_prefix
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

  # Does a similarity search to recall memories associated with this prompt
  def recall(self, prompt):
    docs = self.deeplake.search(prompt)
    self.long_term_memories = docs

  # provides long term memories to the prompt manager
  def get_long_term_memories(self, n=2):
    result = ""
    num_documents = min(len(self.long_term_memories), n)
    for i in range(num_documents):
        content = self.long_term_memories[i].page_content.replace('\n', ' ').replace('</s>', '')
        result += content
    return result

  # Async method using threading for memorization -- need app for Flask context
  def remember(self, prompt, text, app):
      remember_thread_args=(prompt, text, app)
      remember_thread = threading.Thread(target=self.remember_with_app_context, args=remember_thread_args )
      remember_thread.start()

  # Locking and thread ontext for async memory processing
  def remember_with_app_context(self, prompt, response, app):
      with app.app_context():
          self.save_interaction(prompt, response)

  # Returns the last 5 interactions from the short term memory
  def chat_history(self):
      mem = self.short_term_memory.load_memory_variables({})
      def get_content(obj):
          prefix = f"{self.human_prefix}: " if obj.__class__.__name__ == "HumanMessage" else f"{self.ai_prefix}: "
          return prefix + obj.content
      # TODO: Need a more robust way to ensure we don't hit token limit for prompt
      return "\n".join(list(map(lambda obj: get_content(obj), mem["history"][-5:]))) if "history" in mem else ""

  # Saves a response from another individual to long-term memory
  def save_interaction(self, prompt, response):
    # Do not save empty interactions
    if prompt.strip() == "":
      return
    interaction = f"""{self.short_term_memory.human_prefix}: {prompt}\n{ self.short_term_memory.ai_prefix}: {response}"""
    if self.deeplake is not None:
        metadata = {"source": self.short_term_memory.ai_prefix}
        self.add_documents(interaction, metadata)


  def add_documents(self, texts, metadata, **kwargs):
      """Add documents to vectorstore."""
      current_time = kwargs.get("current_time", str(datetime.datetime.now()))
      # Avoid mutating input documents
      if "last_accessed_at" not in metadata:
          metadata["last_accessed_at"] = current_time
      if "created_at" not in metadata:
          metadata["created_at"] = current_time
      metadata["buffer_idx"] = len(self.retriever.memory_stream)
      # doc = MemDoc(texts, metadata)
      # ddoc = deepcopy(doc) # Deep copy to avoid mutating input
      # self.retriever.memory_stream.extend([ddoc])
      # raise Exception(str(metadata))
      return self.deeplake.add_texts([texts], [metadata])