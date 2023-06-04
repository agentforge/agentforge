from agentforge.adapters import VectorStoreProtocol
import threading, datetime

### LongTermMemory makes use of the VectorStoreProtocol to store and retrieve memories
### uses a similarity function to access memories and methodsSaves to forget
### VectorStoreProtocol is an interface that can be implemented by any vector store
### and uses metadata filters to filter on user, agent, and other metadata
class VectorStoreMemory:
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

  # TODO: Return a summarization of the session history parsed via summarization model if available
  def session_history(self, user: str, agent: str):
     return ""

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
        self.ingest(interaction, metadata)

  def ingest(self, texts, metadata, **kwargs):
      """Add documents to vectorstore."""
      current_time = kwargs.get("current_time", str(datetime.datetime.now()))
      # Avoid mutating input documents
      if "last_accessed_at" not in metadata:
          metadata["last_accessed_at"] = current_time
      if "created_at" not in metadata:
          metadata["created_at"] = current_time
      metadata["buffer_idx"] = len(self.retriever.memory_stream)
      return self.vectorstore.add_texts([texts], [metadata])