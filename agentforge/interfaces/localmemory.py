from langchain.memory import ConversationBufferMemory

class LocalMemory:
  def __init__(self):
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
