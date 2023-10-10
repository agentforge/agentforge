import os
from typing import List, Dict
from agentforge.interfaces import interface_interactor

### Memory accesses underlying long-term and working memory
### This abstract class allows us to access a singular memory instance
### and generalize those memories to multiple memory stores

MILVUS_COLLECTION = os.environ.get("MILVUS_COLLECTION") #general knowledge store for this client

import re

def sanitize_string(input_string):
    return re.sub(r'[^a-zA-Z0-9_]', '_', input_string)

class Memory:
    def __init__(self, prefix: str="", postfix: str="") -> None:
        self.working_memory = interface_interactor.get_interface("working_memory")
        self.deep_memory = interface_interactor.get_interface("vectorstore_memory")
        self.prefix = prefix
        self.postfix = postfix

    # Saves the latest interaction between user and agent
    def remember(self, user: str, agent: str, prompt: str, response: str):
        self.working_memory.remember(user, agent, prompt, response)

        ### Deep memory deprecated for now -- using preloaded vectorstore DB
        # self.deep_memory.remember(user, agent, prompt, response, collection=sanitize_string(f"memories_{user}_{agent}"))

    # Recall relevant memories from this agent based on this prompt
    def recall(self, user: str, agent: str, prompt: str):
        knowledge = self.deep_memory.recall(prompt, collection=MILVUS_COLLECTION)
        memories = self.deep_memory.recall(prompt, collection=sanitize_string(f"memories_{user}_{agent}"))
        return knowledge + memories

    # Retrieves the latest N interaction between user and agent
    def session_history(self, user: str, agent: str, session_id: str, n: int = 5):
        self.working_memory.setup_memory(user, agent, user, session_id) # TODO: Differentiate between user name and ID
        session_hist = self.working_memory.recall(self.prefix, self.postfix, n)
        return session_hist

    # Add text data to the vectorstore
    def add_texts(self, texts: List[str], metadata: List[Dict], **kwargs):
        self.deep_memory.add_texts(texts, metadata, **kwargs)
