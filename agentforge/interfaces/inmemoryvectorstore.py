from typing import List, Tuple
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from transformers import AutoTokenizer, AutoModel
from agentforge.adapters import VectorStoreProtocol

class InMemoryVectorStore(VectorStoreProtocol):
    def __init__(self) -> None:
        self.texts: List[str] = []
        self.vectors: List[np.ndarray] = []
        self.tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
        self.model = AutoModel.from_pretrained('bert-base-uncased')

    def add_texts(self, texts: List[str]) -> None:
        for text in texts:
            inputs = self.tokenizer(text, return_tensors='pt', truncation=True, padding=True)
            outputs = self.model(**inputs)
            self.texts.append(text)
            self.vectors.append(outputs.last_hidden_state.mean(dim=1).detach().numpy())
        self.vectors = np.array(self.vectors).squeeze()  # Convert list of vectors to numpy array for efficient computation

    def search(self, text: str) -> List[Tuple[str, float]]:
        inputs = self.tokenizer(text, return_tensors='pt', truncation=True, padding=True)
        outputs = self.model(**inputs)
        vector = outputs.last_hidden_state.mean(dim=1).detach().numpy().reshape(1, -1)
        similarities = cosine_similarity(self.vectors, vector)
        similarities = similarities.reshape(-1)
        result = sorted(zip(self.texts, similarities), key=lambda x: x[1], reverse=True)
        return result