from datetime import datetime
from typing import List, Tuple, Optional
from pydantic import BaseModel, Field
from transformers import BertTokenizer, BertModel
import torch
import numpy as np

class SPOTriplet(BaseModel):
    subject: str
    predicate: str
    object: str
    poignancy_score: float = Field(0.0, ge=0.0, le=1.0)
    keywords: List[str] = []
    description: Optional[str] = None
    expiration_date: Optional[datetime] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class KnowledgeGraph:
    def __init__(self, semantic_weight=0.5, recency_weight=0.25, relevance_weight=0.25, time_decay=0.99):
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.model = BertModel.from_pretrained('bert-base-uncased')
        self.time_decay = time_decay
        self.semantic_weight = semantic_weight
        self.recency_weight = recency_weight
        self.relevance_weight = relevance_weight

    def _get_embedding(self, text: str):
        inputs = self.tokenizer(text, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

    def _calculate_similarity(self, vec1: np.array, vec2: np.array, recency: float):
        semantic_similarity = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
        relevance_score = 1.0  # Placeholder for relevance score (to be obtained from LLM)
        combined_similarity = (semantic_similarity * self.semantic_weight +
                               recency * self.recency_weight +
                               relevance_score * self.relevance_weight)
        return combined_similarity

    def _calculate_recency(self, timestamp: datetime):
        time_diff = (datetime.utcnow() - timestamp).total_seconds()
        recency = self.time_decay ** time_diff
        return recency

    def add_triplet(self, triplet: SPOTriplet):
        embedding_length = self._get_embedding(triplet.subject).shape[0]
        concatenated_embedding = np.concatenate([
            self._get_embedding(triplet.subject),
            self._get_embedding(triplet.predicate),
            self._get_embedding(triplet.object)
        ])
        text_representation = f"{triplet.subject} {triplet.predicate} {triplet.object}"
        self.graph['subject'].append({'text': triplet.subject, 'embedding': concatenated_embedding[:embedding_length], 'timestamp': triplet.timestamp})
        self.graph['predicate'].append({'text': triplet.predicate, 'embedding': concatenated_embedding[embedding_length:2*embedding_length], 'timestamp': triplet.timestamp})
        self.graph['object'].append({'text': triplet.object, 'embedding': concatenated_embedding[2*embedding_length:], 'timestamp': triplet.timestamp})

    def _get_all_combinations_embedding(self):
        predicate_embeddings = [value['embedding'] for value in self.graph['predicate']]
        predicate_texts = [value['text'] for value in self.graph['predicate']]
        object_embeddings = [value['embedding'] for value in self.graph['object']]
        object_texts = [value['text'] for value in self.graph['object']]

        return np.stack(predicate_embeddings), predicate_texts, np.stack(object_embeddings), object_texts


    def query_masked_S(self, predicate: str, object: str) -> List[Tuple[str, float]]:
        results = []
        masked_embedding = self._get_embedding(f"[MASK] {predicate} {object}")
        for item in self.graph['triplets']:
            recency = self._calculate_recency(item['triplet'].timestamp)
            similarity = self._calculate_similarity(masked_embedding, item['embedding'], recency)
            results.append((item['triplet'], similarity))
        return results

    def _calculate_all_similarities(self, predicate_embeddings, object_embeddings):
        predicate_norm = np.linalg.norm(predicate_embeddings, axis=1)
        object_norm = np.linalg.norm(object_embeddings, axis=1)
        
        # Calculate recency for predicates and objects
        recency_predicates = np.array([self._calculate_recency(value['timestamp']) for value in self.graph['predicate']])
        recency_objects = np.array([self._calculate_recency(value['timestamp']) for value in self.graph['object']])
        recency = np.outer(recency_predicates, recency_objects)

        # Placeholder for relevance score (to be obtained from LLM)
        relevance_score = 1.0
        semantic_similarity = (predicate_embeddings @ object_embeddings.T) / np.outer(predicate_norm, object_norm)
        combined_similarity = (semantic_similarity * self.semantic_weight +
                            recency * self.recency_weight +
                            relevance_score * self.relevance_weight)
        return combined_similarity


    def query_all_combinations(self) -> List[Tuple[str, float]]:
        predicate_embeddings, predicate_texts, object_embeddings, object_texts = self._get_all_combinations_embedding()
        similarities = self._calculate_all_similarities(predicate_embeddings, object_embeddings)
        all_results = []
        for i in range(similarities.shape[0]):
            for j in range(similarities.shape[1]):
                all_results.append((f"{predicate_texts[i]} {object_texts[j]}", similarities[i, j]))
        return all_results


# Example Usage
kg = KnowledgeGraph()
triplet = SPOTriplet(subject="cat", predicate="is", object="animal", poignancy_score=0.8)
kg.add_triplet(triplet)
query_result = kg.query_all_combinations()
query_result
