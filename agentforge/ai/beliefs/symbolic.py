import torch, re
from typing import List, Dict
from pydantic import BaseModel, Field
from agentforge.interfaces import interface_interactor
from agentforge.utils import Parser
from agentforge.ai.beliefs.linker import EntityLinker
from agentforge.ai.beliefs.opql import OPQLMemory
from agentforge.ai.beliefs.classifier import Classifier
from agentforge.ai.agents.context import Context

class QueryInterface(BaseModel):
    text: str
    relation: str
    object: str
    type: str

### Wrapper for OPQLMemory, allows the agent to learn and query from our symbolic memory
class SymbolicMemory:
    def __init__(self) -> None:
        self.entity_linker = EntityLinker()
        self.opql_memory = OPQLMemory()
        self.bs_filter = OPQLMemory() # Our bullshit filter stores negations, i.e. the earth is not flat.
        self.llm = interface_interactor.get_interface("llm")
        # self.db = interface_interactor.get_interface("db")
        # self.vectorstore = interface_interactor.get_interface("vectorstore")
        self.parser = Parser()
        self.classifier = Classifier()
        # TODO: Move to env
        self.ATTENTION_TTL_DAYS = 7 # The TTL for attention documents is set to 7 days

    # Given a query (w/response) and context we learn an object, predicate, subject triplet
    # Returns: True/False + results if information was successfully learned or not
    def learn(self, query: QueryInterface, context: Context):
        prompt = context.prompts[f"{query['type']}.cot.prompt"]
        args = {"query": query['text'], "response": context.get("instruction")}
        results = self.classifier.classify(args, prompt, context)
        print(results)
        if len(results) == 0:
            print("Error with classification. See logs.")
            return False, []
        # For string types the results fo classification are a List[str] corresponding to the subject
        if query['type'] == "string":
            for subject in results:
                subject = subject.replace(" ", "-").strip() # If any spaces are involved they will break PDDL
                print("[SYMBOLIC] ", subject)
                self.create_predicate("User", query["relation"], subject) # TODO: Need to pull user name
            return True, results
        # For Boolean the results are True, False, or None. Subject is capture in query context.
        elif query['type'] == "boolean":    
            if results[0].lower() in  ["true", "yes", "1"]:
                self.create_predicate("User", query["relation"], query["object"]) # TODO: Need to pull user name
                return True, results
            elif results[0].lower() in  ["false", "no", "0"]:
                self.create_negation("User", query["relation"], query["object"]) # TODO: Need to pull user name
                return True, results
            else:
                return False, []
        return False, []

    # Unguided entity learner using old-school NLP techniques
    # Problematic! -- We need to use few-shot CoT LLMs for greater depth of reasoning.
    def entity_learn(self, query: QueryInterface):
        print("Learning...", query)
        obj, relation, subject = self.entity_linker.link_relations(query['text'])
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


def test():
    pass