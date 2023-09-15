import torch, re
from typing import List, Dict
from pydantic import BaseModel, Field
from agentforge.interfaces import interface_interactor
from agentforge.utils import Parser
from agentforge.ai.beliefs.linker import EntityLinker
from agentforge.ai.beliefs.opql import OPQLMemory
from agentforge.ai.reasoning.classifier import Classifier
from agentforge.ai.reasoning.zeroshot import ZeroShotClassifier
from agentforge.ai.agents.context import Context
from word2number import w2n
from nltk.corpus import wordnet as wn
from agentforge.utils import logger
import pickle

"""
    Split conditional PDDL statement -- maybe move this to PDDL module
    Input: query_str - string with OR conditions "seed-availabel ?plant OR clone-avail ?plant"
    Output: string with comma separated conditions "seed availabel, clone avail"
"""
RELATION_PROMPT =  """### Instruction: Come up with a descriptive verb based on the input output pair, such as 'is a part of' or 'has chosen strain' for instance. Respond with a single verb. ### Input: Input: {{question}} Output: {{response}} ### Response: Verb:"""

def get_multi(query_str):
    # Step 1: Remove any string starting with '?'
    query_str = re.sub(r'\?[\w\-]+', '', query_str)
    # Step 2: Replace hyphens with spaces
    query_str = re.sub('-', ' ', query_str)
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
        self.llm = interface_interactor.get_interface("llm")
        self.db = interface_interactor.get_interface("db")
        # self.vectorstore = interface_interactor.get_interface("vectorstore")
        self.parser = Parser()
        self.entity_linker = EntityLinker()
        self.classifier = Classifier()
        self.zeroshot = ZeroShotClassifier()
        self.opql_memory = OPQLMemory()
        self.bs_filter = OPQLMemory()

    def save(self, key: str):
        collection = "symbolic_memory"

        # Serialize the current object
        data = {"opql_memory": self.opql_memory.serialize(), "bs_filter": self.bs_filter.serialize()}
        serialized_data = pickle.dumps(data)

        # Check if the record already exists
        if self.db.get(collection, key) is not None:
            # Record exists; update it
            self.db.set(collection, key, {"data": serialized_data})
        else:
            # Record doesn't exist; create it
            self.db.create(collection, key, {"data": serialized_data})

    def load(self, key: str):
        collection = "symbolic_memory"
        # Retrieve the serialized data from the database
        stored_data = self.db.get(collection, key)
        
        if stored_data is not None:
            # Deserialize and update the object
            loaded_data = pickle.loads(stored_data["data"])
            deserialized = {}
            for k,v in loaded_data.items():
                deserialized[k] = OPQLMemory.deserialize(v)
            self.__dict__.update(deserialized)

    def get_relation(self, query, result, context):
        relation = self.zeroshot.classify(RELATION_PROMPT, [], {"question": query['text'], "response": result}, context)
        if relation is None:
            return " related to "

    # Given a query (w/response) and context we learn an object, predicate, subject triplet
    # Returns: True/False + results if information was successfully learned or not
    def learn(self, query: QueryInterface, context: Context):
        if "relation" in query:
            relation = query["relation"]
        else:
            relation = " related to "

        object_singular = query["class"]
        user_name = context.get("input.user_id")
        verb = query["goal"]
        condition = query["condition"]
        cot_args = {
                "object_singular": object_singular,
                "verb": verb, "subject": "Human",
                "response": context.get("instruction")
        }
        if " OR " in condition:
            prompt = context.prompts[f"multi.cot.prompt"]
            cot_args["multi"] = get_multi(condition)
        else:
            prompt = context.prompts[f"{query['datatype']}.cot.prompt"]

        prompt = context.process_prompt(prompt, cot_args)

        # args = {"query": query['text'], }
        results = self.classifier.classify(cot_args, prompt, context)
        if len(results) == 0:
            logger.info("Error with classification. See logs.")
            return False, []

        # For string types the results fo classification are a List[str] corresponding to the subject
        if query['datatype'] == "string":
            # None is a specific type of failure for strings
            if len(results) == 0:
                return False, []
            if len(results) > 0 and results[0] == "None":
                return False, [None]
            for subject in results:
                subject = subject.replace(" ", "-").strip() # If any spaces are involved they will break PDDL
                logger.info(f"[SYMBOLIC] {subject}")
                self.create_predicate(user_name, relation, subject) # TODO: Need to pull user name
            return True, results

        # For Boolean the results are True, False, or None. Subject is capture in query context.
        elif query['datatype'] == "boolean":
            if results[0].lower() in  ["true", "yes", "1"]:
                self.create_predicate(user_name, relation, object_singular) # TODO: Need to pull user name
                return True, [True]
            elif results[0].lower() in  ["false", "no", "0"]:
                self.create_negation(user_name, relation, object_singular) # TODO: Need to pull user name
                return True, [False]
            else:
                return False, [None]

        # For Number the results are must adhere to some numeric values. Subject is capture in query context.
        elif query['datatype'] == "numeric":
            try:
                # Try to convert the result to an integer
                if results[0].isdigit():
                    num_value = int(results[0])
                else:
                    num_value = w2n.word_to_num(results[0].lower())
                # Create the predicate with the numeric value
                self.create_predicate(user_name, relation, object_singular, num_value)  # TODO: Need to define amounts
                return True, results
            except ValueError:
                # If conversion to integer fails
                return False, []
            except Exception as e:
                # Handle other exceptions
                logger.info(f"An error occurred: {e}")
                return False, []

        return False, []

    # Unguided entity learner using old-school NLP techniques
    # Problematic! -- We need to use few-shot CoT LLMs for greater depth of reasoning.
    def entity_learn(self, query: QueryInterface):
        logger.info(f"Learning... {query}")
        obj, relation, subject = self.entity_linker.link_relations(query['text'])
        self.create_predicate(obj, relation, subject)

    def create_predicate(self, obj, relation, subject):
        logger.info(f"Object: {obj}\nRelation: {relation}\nSubject: {subject}")
        if obj and relation and subject:
            self.opql_memory.set(obj, relation, subject)
            return {"success": True}
        else:
            return {"success": False, "message": f"Text is not a valid Object<{obj}>/Relation<{relation}>/Subject<{subject}>, please try again."}

    def create_negation(self, obj, relation, subject):
        logger.info(f"Object: {obj}\nRelation: {relation}\nSubject: {subject}")
        if obj and relation and subject:
            self.bs_filter.set(obj, relation, subject)
            return {"success": True}
        else:
            return {"success": False, "message": f"Text is not a valid Object<{obj}>/Relation<{relation}>/Subject<{subject}>, please try again."}

    def get_predicate(self, entity_name, relation):
        most_similar = self.opql_memory.get(entity_name, relation)

        logger.info("Most Similar Embeddings:")
        for key, value, score in most_similar:
            logger.info(f"Key: {key} Value: {value} Score:{score}")
        return most_similar

def test():
    pass