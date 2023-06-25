from langchain.memory import MongoDBChatMessageHistory
from agentforge.config import DbConfig
from urllib.parse import quote_plus

class MongoMemory:
  def __init__(self, config: DbConfig):
    username = quote_plus(config.username)
    password = quote_plus(config.password)
    host = config.host
    port = config.port
    connection_string = f"mongodb://{username}:{password}@{host}:{port}"
    session = "user_test-Sam-session-XYZ"
    self.short_term_memory = MongoDBChatMessageHistory(
        connection_string=connection_string, session_id=session
    )
    
  # Stores memory for various agent avatars
  def setup_memory(self, ai_prefix = "AI", human_prefix = "Human"):
    self.human_prefix = human_prefix
    self.ai_prefix = ai_prefix

  # Saves a response from another individual to short-term memory
  def remember(self, user: str, agent: str, prompt: str, response: str):
    # Do not save empty interactions
    if prompt.strip() == "":
      return
    if self.short_term_memory:
        self.short_term_memory.add_user_message(prompt)
        self.short_term_memory.add_ai_message(response)

  # Returns the last 5 interactions from the short term memory
  def recall(self, user: str, agent: str, n: int = 5):
      mem = self.short_term_memory.messages
      def get_content(obj):
          prefix = f"{self.human_prefix}: " if obj.__class__.__name__ == "HumanMessage" else f"{self.ai_prefix}: "
          # postfix = f" {self.human_postfix}" if obj.__class__.__name__ == "HumanMessage" else f" {self.human_postfix}"
          return prefix + obj.content # + postfix
      # TODO: Need a more robust way to ensure we don't hit token limit for prompt
      hist = "\n".join(list(map(lambda obj: get_content(obj), mem[-5:])))
      return hist
