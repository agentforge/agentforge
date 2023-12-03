import os
from typing import List, Dict
from agentforge.interfaces import interface_interactor
from agentforge.utils import logger

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
    def remember(self, user_name: str, user_id: str, agent: str, prompt: str, response: str):
        
        # cleanup for vectorstore key validation
        user_id = user_id.replace(" ", "_")
        user_id = user_id.replace("-", "_")

        self.working_memory.remember(user_name, user_id, agent, prompt, response)

        ### Deep memory deprecated for now -- using preloaded vectorstore DB
        logger.info(f"Remembering memories_{user_id}_{agent}: {prompt} - {response}")
        self.deep_memory.remember(user_name, user_id, agent, prompt, response, collection=sanitize_string(f"memories_{user_id}_{agent}"))

    # Recall relevant memories from this agent based on this prompt
    # These are memories between the agent and the user specifically
    def recall(self, user: str, agent: str, prompt: str, n: int = 2):
        # cleanup
        user = user.replace(" ", "_")
        user = user.replace("-", "_")
        filt = {'memory': True}
        logger.info(f"Recalling memories_{user}_{agent}")
        memories = self.deep_memory.recall(prompt, filter=filt, collection=sanitize_string(f"memories_{user}_{agent}"), n=n)
        return memories.strip()

    # This method recalls knowledge from the general knowledge store
    # These are not meant to be memories but are taken as facts
    def knowledge(self, user: str, agent: str, prompt: str, collection: str=MILVUS_COLLECTION, n: int = 2):
        # cleanup
        user = user.replace(" ", "_")
        user = user.replace("-", "_")

        logger.info(f"Recalling memories_{user}_{agent}")
        knowledge = self.deep_memory.recall(prompt, collection=collection, n=n)
        return knowledge.strip()

    # Retrieves the latest N interaction between user and agent
    def session_history(self, user: str, agent: str, session_id: str, n: int = 5):
        self.working_memory.setup_memory(user, agent, user, session_id) # TODO: Differentiate between user name and ID
        session_hist = self.working_memory.recall(self.prefix, self.postfix, n)
        return session_hist

    # Add text data to the vectorstore
    def add_texts(self, texts: List[str], metadata: List[Dict], **kwargs):
        self.deep_memory.add_texts(texts, metadata, **kwargs)
