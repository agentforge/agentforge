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

    def search(self, text: str, n: int, filter: dict) -> List[Tuple[str, float]]:
        inputs = self.tokenizer(text, return_tensors='pt', truncation=True, padding=True)
        outputs = self.model(**inputs)
        vector = outputs.last_hidden_state.mean(dim=1).detach().numpy().reshape(1, -1)
        
        # Debug: 
        print("[DEBUG][inmemoryvectorstore][search] vector.shape: ", vector.shape)

        # For the first response
        if isinstance(self.vectors, list):
            # print("[DEBUG][inmemoryvectorstore][search] self.vectors: ", self.vectors)
            # print("[DEBUG][inmemoryvectorstore][search] len(self.vectors): ", len(self.vectors))
            self.vectors = np.array(self.vectors).squeeze()  # Convert list of vectors to numpy array for efficient computation

        # Debug: 
        # print("[DEBUG][inmemoryvectorstore][search] Pre-shaping self.vectors.shape: ", self.vectors.shape)

        # Reshape for single sample or empty sample 
        self.vectors = self.vectors.reshape(1, -1)
        # print("[DEBUG][inmemoryvectorstore][search] Post-shaping self.vectors.shape: ", self.vectors.shape)

        # Initialise similarities with 0s
        similarities = np.zeros(vector.shape)
        
        # If the initial self.vectors is an empty sample, then do not try to call cosine_similarity 
        if self.vectors.shape[1] != 0:
            similarities = cosine_similarity(self.vectors, vector)
            similarities = similarities.reshape(-1)

        result = sorted(zip(self.texts, similarities), key=lambda x: x[1], reverse=True)
        return result