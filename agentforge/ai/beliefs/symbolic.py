import torch, re
from typing import List, Dict
from pydantic import BaseModel, Field
from agentforge.interfaces import interface_interactor
from agentforge.utils import Parser
from agentforge.ai.beliefs.linker import EntityLinker
from agentforge.ai.beliefs.opql import OPQLMemory
from agentforge.ai.reasoning.classifier import Classifier
from agentforge.ai.agents.context import Context
from word2number import w2n
from nltk.corpus import wordnet as wn

"""
    Split conditional PDDL statement -- maybe move this to PDDL module
    Input: query_str - string with OR conditions "seed-availabel ?plant OR clone-avail ?plant"
    Output: string with comma separated conditions "seed availabel, clone avail"
"""
def get_multi(query_str):
    # Step 1: Replace hyphens with spaces
    query_str = re.sub('-', ' ', query_str)
    # Step 2: Remove any string starting with '?'
    query_str = re.sub(r'\?\w+', '', query_str)
    # Step 3: Split by 'OR'
    query_list = query_str.split('OR')
    # Step 4: Trim extra spaces
    query_list = [x.strip() for x in query_list]
    
    return ", ".join(query_list)

def pluralize_nltk(word):
    synsets = wn.synsets(word, pos=wn.NOUN)
    if not synsets:
        return None  # word not found
    # Get the lemma name which is a standardized form of the word
    lemma = synsets[0].lemmas()[0].name()
    # Check if the word is already plural
    if lemma != word:
        return word
    # A simple rule-based approach to pluralize regular nouns
    if word.endswith('y'):
        return word[:-1] + 'ies'
    elif word[-1] in 'sx' or word[-2:] in ['sh', 'ch']:
        return word + 'es'
    else:
        return word + 's'


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
        if "relation" in query:
            relation = query["relation"]
        else:
            relation = " related to "

        object_singular = query["object"]
        subject = "Human"
        verb = query["goal"]
        condition = query["condition"]
        args = {
                "object_singular": object_singular,
                "verb": verb, "subject": subject,
                "response": context.get("instruction")
        }
        if " OR " in condition:
            prompt = context.prompts[f"multi.cot.prompt"]
            args["multi"] = get_multi(condition)
        else:
            prompt = context.prompts[f"{query['type']}.cot.prompt"]
        prompt = context.process_prompt(prompt, args)

        # args = {"query": query['text'], }
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
                self.create_predicate("Human", relation, subject) # TODO: Need to pull user name
            return True, results
        # For Boolean the results are True, False, or None. Subject is capture in query context.
        elif query['type'] == "boolean":
            if results[0].lower() in  ["true", "yes", "1"]:
                self.create_predicate("Human", relation, object_singular) # TODO: Need to pull user name
                return True, results
            elif results[0].lower() in  ["false", "no", "0"]:
                self.create_negation("Human", relation, object_singular) # TODO: Need to pull user name
                return True, results
            else:
                return False, []
        # For Number the results are must adhere to some numeric values. Subject is capture in query context.
        elif query['type'] == "numeric":
            try:
                # Try to convert the result to an integer
                if results[0].isdigit():
                    num_value = int(results[0])
                else:
                    num_value = w2n.word_to_num(results[0].lower())
                # Create the predicate with the numeric value
                self.create_predicate("Human", relation, object_singular, num_value)  # TODO: Need to define amounts
                return True, results
            except ValueError:
                # If conversion to integer fails
                return False, []
            except Exception as e:
                # Handle other exceptions
                print(f"An error occurred: {e}")
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