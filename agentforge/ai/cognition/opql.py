import torch
import numpy as np
from transformers import pipeline, BertTokenizer, BertModel


### The OPQL memory is a key-value memory. Keys are computed from embeddings of the topic
## entity, e.g. On the Origin of Species, looked up from the entity embedding table, and relation embeddings from the pretrained relation
## encoder. Values are embeddings of target entities. The memory is constructed from any entity-linked text corpus, e.g. Wikipedia.

class EntityLinker:
    def __init__(self):
        self.nlp = pipeline("ner", aggregation_strategy="simple")
        
    def link_entities(self, text):
        ner_results = self.nlp(text)
        merged_entities = [(entity_group['word'], entity_group['entity_group'])
                           for entity_group in ner_results]
        return merged_entities
    
    def link_relations(self, text):
        entities = self.link_entities(text)
        
        # replace first two entities in the text with special tokens
        if len(entities) >= 2:
            modified_text = text.replace(entities[0][0], "[ENT] [R1]", 1)
            modified_text = modified_text.replace(entities[1][0], "[ENT] [R2]", 1)
            
            return entities[0][0], modified_text, entities[1][0]
        else:
            return None, None, None


class OPQLMemory:
    def __init__(self):
        self.keys = []
        self.values = []
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.model = BertModel.from_pretrained('bert-base-uncased')
        
    def set(self, obj, relation, subj):
        entity_inputs = self.tokenizer(obj, return_tensors="pt")
        entity_outputs = self.model(**entity_inputs)
        entity_embedding = entity_outputs.last_hidden_state.mean(dim=1)

        relation_inputs = self.tokenizer(relation, return_tensors="pt")
        relation_outputs = self.model(**relation_inputs)
        relation_embedding = relation_outputs.last_hidden_state.mean(dim=1)

        key = torch.cat([relation_embedding, entity_embedding], dim=-1)

        self.keys.append(key.detach().numpy().flatten())
        self.values.append(subj)
        
    def get_most_similar(self, query, k=5):
        k = min(k, len(self.keys))
        query = torch.tensor(query.detach().numpy().flatten())
        keys = torch.tensor(np.stack(self.keys))
        dot_products = torch.matmul(keys, query.t())
        
        # Apply softmax to normalize scores
        similarity_scores = torch.nn.functional.softmax(dot_products, dim=-1)
        
        # Get top k similarity scores and indices
        top_scores, top_indices = torch.topk(similarity_scores, k, dim=-1)
        
        # Return the corresponding keys and similarity scores
        return [(self.keys[index], self.values[index], score.item()) for index, score in zip(top_indices, top_scores)]

# Example usage
entity_linker = EntityLinker()
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
    "The concept of zero as a number was developetextd in ancient India.",
    "Twitter was launched by Jack Dorsey, Biz Stone, and Evan Williams in 2006."
]
opql_memory = OPQLMemory()
invalid = []

for text in example_sentences:
  obj, relation, subject = entity_linker.link_relations(text)
  print(f"Object: {obj}\nRelation: {relation}\nSubject: {subject}")
  if obj and relation and subject:
    opql_memory.set(obj, relation, subject)
  else:
    invalid.append(text)

# Test
relation = "launched"
entity_name = "Twitter"

relation_embedding = opql_memory.model(**opql_memory.tokenizer(relation, return_tensors="pt")).last_hidden_state.mean(dim=1)
entity_embedding = opql_memory.model(**opql_memory.tokenizer(entity_name, return_tensors="pt")).last_hidden_state.mean(dim=1)
query_for_most_similar = torch.cat([relation_embedding, entity_embedding], dim=-1)

most_similar = opql_memory.get_most_similar(query_for_most_similar, k=5)

print("Most Similar Embeddings:")
for key, value, score in most_similar:
    print("Key:", key, "Value:", value, "Score:", score)

text = "Charles Darwin published his book On the Origin of Species in 1859."
obj, relation, subject = entity_linker.link_relations(text)
print(f"Object: {obj}\nRelation: {relation}\nSubject: {subject}")
print("Invalid Strings", invalid)