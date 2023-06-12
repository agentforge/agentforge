from typing import Any, Optional, Protocol, List, Dict

class MemoryProtocol(Protocol):
    
    # Saves the latest interaction between user and agent
    def remember(self, user: str, agent: str, promot: str, response: str) -> Optional[Any]:
        pass
    
    # Recall relevant memories from this agent based on this prompt
    def recall(self, user: str, agent: str, prompt: str):
        pass

    # Retrieves the latest N interaction between user and agent
    def session_history(self, user: str, agent: str, n: int = 5):
        pass

    def ingest(self, texts: List[str], metadata: List[Dict], **kwargs):
        pass
