import os
from typing import List, Dict
from agentforge.interfaces import interface_interactor

### Memory accesses underlying long-term and working memory
### This abstract class allows us to access a singular memory instance
### and generalize those memories to multiple memory stores

MILVUS_COLLECTION = os.environ.get("MILVUS_COLLECTION") #general knowledge store for this client

class Memory:
    def __init__(self) -> None:
        self.working_memory = interface_interactor.get_interface("working_memory")
        self.deep_memory = interface_interactor.get_interface("vectorstore_memory")

    # Saves the latest interaction between user and agent
    def remember(self, user: str, agent: str, prompt: str, response: str):
        self.working_memory.remember(user, agent, prompt, response)

        ### Deep memory deprecated for now -- using preloaded vectorstore DB
        # self.deep_memory.remember(user, agent, prompt, response)

    # Recall relevant memories from this agent based on this prompt
    def recall(self, user: str, agent: str, prompt: str):
        return self.deep_memory.recall(prompt, collection=MILVUS_COLLECTION)
        # return self.deep_memory.recall(prompt, filter={"user": user, "agent": agent, "memory": True})

    # Retrieves the latest N interaction between user and agent
    def session_history(self, user: str, agent: str, session_id: str, n: int = 5):
        self.working_memory.setup_memory(user, agent, user, session_id) # TODO: Differentiate between user name and ID
        return self.working_memory.recall(user, agent, n)

    # Add text data to the vectorstore
    def add_texts(self, texts: List[str], metadata: List[Dict], **kwargs):
        self.deep_memory.add_texts(texts, metadata, **kwargs)
