from typing import List, Dict
from agentforge.interfaces import interface_interactor

### Memory accesses underlying long-term and working memory

class Memory:
    def __init__(self) -> None:
        self.working_memory = interface_interactor.get_interface("working_memory")

    # Saves the latest interaction between user and agent
    def remember(self, user: str, agent: str, promot: str, response: str):
        pass
    
    # Recall relevant memories from this agent based on this prompt
    def recall(self, user: str, agent: str, prompt: str):
        pass

    # Retrieves the latest N interaction between user and agent
    def session_history(self, user: str, agent: str, n: int = 5):
        pass

    def ingest(self, texts: List[str], metadata: List[Dict], **kwargs):
        pass