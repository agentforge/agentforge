from agentforge.adapters import VectorStoreProtocol
import threading, datetime

### LongTermMemory makes use of the VectorStoreProtocol to store and retrieve memories
### uses a similarity function to access memories and methodsSaves to forget
### VectorStoreProtocol is an interface that can be implemented by any vector store
### and uses metadata filters to filter on user, agent, and other metadata
class VectorStoreMemory:
  def __init__(self, vectorstore: VectorStoreProtocol = None, app = None):
    self.vectorstore = vectorstore
    self.app = app

  # Does a similarity search to recall memories associated with this prompt
  def recall(self, prompt, filter={}, **kwargs):
    filter["memory"] = True
    docs = self.vectorstore.search(prompt, n=2, filter=filter, **kwargs)
    result = ""
    for doc in docs:
        result += doc.page_content
    return result

  # Async method using threading for memorization -- need app for Flask context
  def remember(self, user: str, agent: str, prompt: str, response: str, **kwargs):
    # Do not save empty interactions
    if prompt.strip() == "":
      return
    interaction = f"""{user}: {prompt}\n{agent}: {response}"""
    if self.vectorstore is not None:
        metadata = {"user": user, "agent": agent, "memory": True}
        self.add_texts(interaction, metadata, **kwargs)

  # TODO: Return a summarization of the session history parsed via summarization model if available
  def session_history(self, user: str, agent: str):
     return ""

  def add_texts(self, interaction, metadata, **kwargs):
      """Add documents to vectorstore."""
      current_time = kwargs.get("current_time", str(datetime.datetime.now()))
      # Avoid mutating input documents
      if "last_accessed_at" not in metadata:
          metadata["last_accessed_at"] = current_time
      if "created_at" not in metadata:
          metadata["created_at"] = current_time
      return self.vectorstore.add_texts([interaction], [metadata], **kwargs)