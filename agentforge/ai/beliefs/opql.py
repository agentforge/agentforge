import torch
import numpy as np
from transformers import BertTokenizer, BertModel
from agentforge.ai.beliefs.linker import EntityLinker
from fuzzywuzzy import fuzz

### The OPQL memory is a key-value memory. Keys are computed from embeddings of the topic
## entity, e.g. On the Origin of Species, looked up from the entity embedding table, and relation embeddings from the pretrained relation
## encoder. Values are embeddings of target entities. The memory is constructed from any entity-linked text corpus, e.g. Wikipedia.

class OPQLMemory:
    def __init__(self):
        self.keys = []
        self.pvalues = []
        self.svalues = []
        self.ovalues = []
        self.triplets = []
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

        self.model = BertModel.from_pretrained('bert-base-uncased')
        self.fuzzy_weight = .5
   
    def serialize(self) -> dict:
        # Convert the object to a dictionary
        data = self.__dict__.copy()
        
        # Remove the attributes we don't want to serialize
        del data['tokenizer']
        del data['model']
        
        return data

    @classmethod
    def deserialize(cls, data: dict) -> 'OPQLMemory':
        # Create a new object and populate it from the dictionary
        obj = cls()
        obj.__dict__.update(data)

        # Initialize tokenizer and model
        obj.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        obj.model = BertModel.from_pretrained('bert-base-uncased')

        return obj

    def set(self, obj, relation, subj):
        entity_inputs = self.tokenizer(obj, return_tensors="pt")
        entity_outputs = self.model(**entity_inputs)
        entity_embedding = entity_outputs.last_hidden_state.mean(dim=1)

        relation_inputs = self.tokenizer(relation, return_tensors="pt")
        relation_outputs = self.model(**relation_inputs)
        relation_embedding = relation_outputs.last_hidden_state.mean(dim=1)

        key = torch.cat([relation_embedding, entity_embedding], dim=-1)

        self.keys.append(key.detach().numpy().flatten())
        self.svalues.append(subj)
        self.pvalues.append(relation)
        self.ovalues.append(obj)
        self.triplets.append((obj, relation, subj))

    def get(self, entity_name, relation, k=5, threshold=.90):
        if entity_name in self.svalues:
            idx = self.svalues.index(entity_name)
            return [(self.keys[idx], self.ovalues[idx], 1.0)]

        relation = f"[ENT] [R1] {relation} [ENT] [R2]" # for OPQL format
        relation_inputs = self.tokenizer(relation, return_tensors="pt")
        relation_embedding = self.model(**relation_inputs).last_hidden_state.mean(dim=1)

        entity_inputs = self.tokenizer(entity_name, return_tensors="pt")
        entity_embedding = self.model(**entity_inputs).last_hidden_state.mean(dim=1)

        query_for_most_similar = torch.cat([relation_embedding, entity_embedding], dim=-1)

        k = min(k, len(self.keys))
        query = torch.tensor(query_for_most_similar.detach().numpy().flatten())
        keys = torch.tensor(np.stack(self.keys))
        dot_products = torch.matmul(keys, query.t())

        # Apply softmax to normalize scores
        similarity_scores = torch.nn.functional.softmax(dot_products, dim=-1)

        # Get top k similarity scores and indices
        top_scores, top_indices = torch.topk(similarity_scores, k, dim=-1)

        results = []

        for index, score in zip(top_indices, top_scores):
            stored_entity = self.ovalues[index]
            fuzzy_score = fuzz.ratio(entity_name, stored_entity) / 100.0 # Fuzzy score on a scale of 0 to 1
            # Combine the fuzzy score and similarity score
            combined_score = fuzzy_score * score.item()

            # Apply threshold if provided
            if threshold is None or combined_score >= threshold:
                results.append((self.keys[index], self.svalues[index], combined_score))

        return results

def test():
    # Example usage
    entity_linker = EntityLinker()
    opql_memory = OPQLMemory("test-init")

    example_sentences = [
        "Charles Darwin published his book On the Origin of Species in 1859.",
        "Harry Potter and the Philosopher's Stone was published by J.K. Rowling in 1997.",
        "The Declaration of Independence was signed by 56 delegates on July 4, 1776.",
        "The Godfather, directed by Francis Ford Coppola, was released in 1972.",
        "The theory of relativity was developed by Albert Einstein in the early 20th century.",
        "The Mona Lisa was painted by Leonardo da Vinci in the early 1500s.",
        "Apple Inc. was co-founded by Steve Jobs and Steve Wozniak in 1976.",
        "The Great Wall of China was built by various dynasties over several centuries.",
        "The Adventures of Huckleberry Finn, a novel by Mark Twain, was published in 1885.",
        "The first successful human heart transplant was performed by Dr. Christiaan Barnard in 1967.",
        "The Sistine Chapel's ceiling was painted by Michelangelo between 1508 and 1512.",
        "In 1492, Christopher Columbus set sail with three ships in search of a new route to Asia.",
        "Mount Everest was first summited by Edmund Hillary and Tenzing Norgay in 1953.",
        "Google was created by Larry Page and Sergey Brin in 1998.",
        "The Periodic Table was developed by Dmitri Mendeleev in 1869.",
        "The Little Prince, written by Antoine de Saint-Exupéry, was published in 1943.",
        "In 1969, Neil Armstrong and Buzz Aldrin landed on the Moon as part of NASA's Apollo 11 mission.",
        "Pride and Prejudice, authored by Jane Austen, first appeared in 1813.",
        "The first photograph was captured by Joseph Nicéphore Niépce in the early 19th century.",
        "The concept of zero as a number was developed in ancient India.",
        "Twitter was launched by Jack Dorsey, Biz Stone, and Evan Williams in 2006.",
        "Frank Grove is growing Cannabis Sativa",
        "Frank Grove lives in Tulsa",
        "Tulsa is in Oklahoma",
        "Frank Grove has a son named Neel Grove"
    ]
    invalid = []

    for text in example_sentences:
        obj, relation, subject = entity_linker.link_relations(text)
        # print(f"Object: {obj}\nRelation: {relation}\nSubject: {subject}")
        if obj and relation and subject:
            opql_memory.set(obj, relation, subject)
        else:
            invalid.append(text)

    # Test
    relation = "is growing"
    entity_name = "Frank Grove"

    most_similar = opql_memory.get(entity_name, relation, k=5, threshold=.9)

    print("Most Similar Embeddings:")
    for _, value, score in most_similar:
        print("Value:", value, "Score:", score)

    # text = "Charles Darwin published his book On the Origin of Species in 1859."
    # obj, relation, subject = entity_linker.link_relations(text)
    # print(f"Object: {obj}\nRelation: {relation}\nSubject: {subject}")
    print("Invalid Strings", f"{len(invalid)} / {len(example_sentences)}")