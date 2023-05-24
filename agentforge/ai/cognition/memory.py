import datetime, threading
from langchain.memory import ConversationBufferMemory
from agentforge.adapters import VectorStoreProtocol

### ShortTermMemory users a simple conversation buffer to store recent interactions
class ShortTermMemory:
  def __init__(self, vectorstore: VectorStoreProtocol = None):
    self.memories = {}
    self.short_term_memory = ConversationBufferMemory(return_messages=True)

  # Stores memory for various agent avatars
  def setup_memory(self, ai_prefix = "AI", human_prefix = "Human"):
    self.human_prefix = human_prefix
    self.ai_prefix = ai_prefix
    # Supports short-term memory for multiple people
    if ai_prefix in self.memories:
      self.short_term_memory = self.memories[ai_prefix]
    else:
      self.short_term_memory.human_prefix = human_prefix
      self.short_term_memory.ai_prefix = ai_prefix
      self.memories[ai_prefix] = self.short_term_memory

  # Saves a response from another individual to short-term memory
  def save_interaction(self, prompt, response):
    # Do not save empty interactions
    if prompt.strip() == "":
      return
    if self.short_term_memory:
        self.short_term_memory.chat_memory.add_user_message(prompt)
        self.short_term_memory.chat_memory.add_ai_message(response)

  # Returns the last 5 interactions from the short term memory
  def chat_history(self):
      mem = self.short_term_memory.load_memory_variables({})
      def get_content(obj):
          prefix = f"{self.human_prefix}: " if obj.__class__.__name__ == "HumanMessage" else f"{self.ai_prefix}: "
          postfix = f" {self.human_postfix}" if obj.__class__.__name__ == "HumanMessage" else f" {self.human_postfix}"
          return prefix + obj.content + postfix
      # TODO: Need a more robust way to ensure we don't hit token limit for prompt
      return "\n".join(list(map(lambda obj: get_content(obj), mem["history"][-5:]))) if "history" in mem else ""

### LongTermMemory makes use of the VectorStoreProtocol to store and retrieve memories
### uses a similarity function to access memories and methods to forget
### VectorStoreProtocol is an interface that can be implemented by any vector store
### and uses metadata filters to filter on user, agent, and other metadata
class LongTermMemory:
  def __init__(self, vectorstore: VectorStoreProtocol = None):
    self.vectorstore = vectorstore

  # Does a similarity search to recall memories associated with this prompt
  def recall(self, prompt):
    docs = self.vectorstore.search(prompt)
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

  # Saves a response from another individual to long-term memory
  def save_interaction(self, prompt, response):
    # Do not save empty interactions
    if prompt.strip() == "":
      return
    interaction = f"""{self.short_term_memory.human_prefix}: {prompt}\n{ self.short_term_memory.ai_prefix}: {response}"""
    if self.vectorstore is not None:
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
      return self.vectorstore.add_texts([texts], [metadata])