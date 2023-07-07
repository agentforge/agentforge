import torch
import numpy as np
from datetime import datetime, timedelta
from transformers import pipeline, BertTokenizer, BertModel
from typing import List
from agentforge.interfaces import interface_interactor
from functools import wraps

def check_ttl(func):
    @wraps(func)
    def wrapper(self, key, *args, **kwargs):
        # Fetching the attention document
        attention_doc = self.db.get("attention", key)
        if attention_doc:
            # Checking the TTL
            timestamp = datetime.fromisoformat(attention_doc["timestamp"])
            if datetime.utcnow() - timestamp > timedelta(days=self.ATTENTION_TTL_DAYS):
                # Deleting expired attention document
                self.db.delete("attention", key)
                return None
            return func(self, attention_doc, key, *args, **kwargs)
        return None
    return wrapper

### Wrapper for OPQLMemory, allows the agent to learn and query from our symbolic memory
class PredicateMemory:
    def __init__(self) -> None:
        self.entity_linker = EntityLinker()
        self.opql_memory = OPQLMemory()
        self.bs_filter = OPQLMemory() # Our bullshit filter stores negations, i.e. the earth is not flat.
        self.llm = interface_interactor.get_interface("llm")
        self.db = interface_interactor.get_interface("db")
        # TODO: Move to env
        self.ATTENTION_TTL_DAYS = 7 # The TTL for attention documents is set to 7 days

    ### Given a query and response use a few-shot CoT LLM reponse to pull information out
    def classify(self, query, response, prompt, context):
        input = {
            "prompt": prompt.replace("{response}", response).replace("{query}", query),
            "generation_config": context['model_profile']['generation_config'], # TODO: We need to use a dedicated model
            "model_config": context['model_profile']['model_config'],
        }
        response = self.llm.call(input)
        if response is not None and "choices" in response:
            response = response["choices"][0]["text"]
            response = response.replace(input['prompt'], "")
            for tok in ["eos_token", "bos_token"]:
                if tok in input["model_config"]:
                    response = response.replace(input["model_config"][tok],"")
            return response.split(",")
        return []

    # Given a query (w/response) and context we learn an object, predicate, subject triplet
    # Returns: True/False + results if information was successfully learned or not
    def learn(self, query, context):
        results = self.classify(query['query'], query['response'], query['prompt'], context)
        if len(results) == 0:
            print("Error with classification. See logs.")
            return False, []
        # For string types the results fo classification are a List[str] corresponding to the subject
        if query['type'] == "string":
            for subject in results:
                self.create_predicate("User", query["relation"], subject) # TODO: Need to pull user name
            return True, results
        # For Boolean the results are True, False, or None. Subject is capture in query context.
        elif query['type'] == "boolean":
            if results[0].lower() in  ["true", "yes", "1"]:
                self.create_predicate("User", query["relation"], query["subject"]) # TODO: Need to pull user name
                return True, results
            elif results[0].lower() in  ["false", "no", "0"]:
                self.create_negation("User", query["relation"], query["subject"]) # TODO: Need to pull user name
                return True, results
            else:
                return False, []
        return False, []

    # Unguided entity learner using old-school NLP techniques
    # Problematic! -- We need to use few-shot CoT LLMs for greater depth of reasoning.
    def entity_learn(self, query):
        print("Learning...", query)
        obj, relation, subject = self.entity_linker.link_relations(query['query'])
        self.create_predicate(obj, relation, subject)

    def create_predicate(self, obj, relation, subject):
        print(f"Object: {obj}\nRelation: {relation}\nSubject: {subject}")
        if obj and relation and subject:
            self.opql_memory.set(obj, relation, subject)
            return {"success": True}
        else:
            return {"success": False, "message": f"Text is not a valid Object<{obj}>/Relation<{relation}>/Subject<{subject}>, please try again."}

    def create_negation(self, obj, relation, subject):
        print(f"Object: {obj}\nRelation: {relation}\nSubject: {subject}")
        if obj and relation and subject:
            self.bs_filter.set(obj, relation, subject)
            return {"success": True}
        else:
            return {"success": False, "message": f"Text is not a valid Object<{obj}>/Relation<{relation}>/Subject<{subject}>, please try again."}

    def get_predicate(self, relation, entity_name):
        relation_embedding = self.opql_memory.model(**self.opql_memory.tokenizer(relation, return_tensors="pt")).last_hidden_state.mean(dim=1)
        entity_embedding = self.opql_memory.model(**self.opql_memory.tokenizer(entity_name, return_tensors="pt")).last_hidden_state.mean(dim=1)
        query_for_most_similar = torch.cat([relation_embedding, entity_embedding], dim=-1)

        most_similar = self.opql_memory.get_most_similar(query_for_most_similar, k=1, threshold=0.1)

        print("Most Similar Embeddings:")
        for key, value, score in most_similar:
            print("Key:", key, "Value:", value, "Score:", score)

    ### When you need to acquire some information, let's apply some attention to the situation
    ### so we can remember what we have learned and what we still need to learn
    def create_attention(self, queries: List[str], key: str) -> None:
        # Creating an attention document with queries and timestamp
        if queries is not None and len(queries) > 0:
            attention_doc = {
                "queries": queries,
                "satisfied": [False] * len(queries),
                "timestamp": datetime.utcnow().isoformat()
            }
            self.db.create("attention", key, attention_doc)
        else:
            raise ValueError(f"Attempted to create attention with queries {queries}")

    @check_ttl
    def satisfy_attention(self, attention_doc, key: str, query: str, results: List[str]) -> None:
        # Fetching the attention document
        attention_doc = self.db.get("attention", key)
        # Marking the query as satisfied
        for idx, q in enumerate(attention_doc["queries"]):
            if q["query"] == query["query"]:
                print("That's satisfaction baby")
                attention_doc["satisfied"][idx] = True
                attention_doc["queries"][idx]["results"] = results
                break
        # Updating the attention document
        self.db.set("attention", key, attention_doc)

    @check_ttl
    def attention_satisfied(self, attention_doc, key: str) -> bool:
        # Checking if all queries are satisfied
        return all(attention_doc["satisfied"])

    @check_ttl  
    def get_attention(self, attention_doc, key: str) -> bool:
        # Fetching the attention document
        return attention_doc

    @check_ttl
    def attention_exists(self, _, key: str) -> bool:
        # Fetching the attention document
        return True

### Uses Named Entity Recognition to map entities to subject and objects
### TODO: Needs some work to evaluate results and improve them
class EntityLinker:
    def __init__(self):
        self.nlp = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english", aggregation_strategy="simple")

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

### The OPQL memory is a key-value memory. Keys are computed from embeddings of the topic
## entity, e.g. On the Origin of Species, looked up from the entity embedding table, and relation embeddings from the pretrained relation
## encoder. Values are embeddings of target entities. The memory is constructed from any entity-linked text corpus, e.g. Wikipedia.

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
    
    def get_most_similar(self, query, k=5, threshold=None):
        k = min(k, len(self.keys))
        query = torch.tensor(query.detach().numpy().flatten())
        keys = torch.tensor(np.stack(self.keys))
        dot_products = torch.matmul(keys, query.t())
        
        # Apply softmax to normalize scores
        similarity_scores = torch.nn.functional.softmax(dot_products, dim=-1)
        
        # Get top k similarity scores and indices
        top_scores, top_indices = torch.topk(similarity_scores, k, dim=-1)
        
        # Filter by threshold if provided
        if threshold is not None:
            filtered_results = [(self.keys[index], self.values[index], score.item()) 
                                for index, score in zip(top_indices, top_scores) if score.item() >= threshold]
            return filtered_results
        else:
            # Return the corresponding keys and similarity scores
            return [(self.keys[index], self.values[index], score.item()) for index, score in zip(top_indices, top_scores)]


def test():
    # Example usage
    entity_linker = EntityLinker()
    opql_memory = OPQLMemory()
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

    most_similar = opql_memory.get_most_similar(query_for_most_similar, k=1, threshold=0.1)

    print("Most Similar Embeddings:")
    for key, value, score in most_similar:
        print("Key:", key, "Value:", value, "Score:", score)

    text = "Charles Darwin published his book On the Origin of Species in 1859."
    obj, relation, subject = entity_linker.link_relations(text)
    print(f"Object: {obj}\nRelation: {relation}\nSubject: {subject}")
    print("Invalid Strings", invalid)