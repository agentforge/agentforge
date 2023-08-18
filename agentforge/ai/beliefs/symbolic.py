import torch, re
from agentforge.interfaces import interface_interactor
from agentforge.utils import Parser
from agentforge.ai.beliefs.linker import EntityLinker
from agentforge.ai.beliefs.opql import OPQLMemory

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

        # TODO: Move to env
        self.ATTENTION_TTL_DAYS = 7 # The TTL for attention documents is set to 7 days

    def validate_classification(self, test):
        pattern = re.compile(r'### Instruction:\s*(.*?)\s*### Input:\s*(.*?)\s*### Thought Process:\s*(.*?)\s*### Response:\s*(.*?)', re.DOTALL)
        match = pattern.match(test)
        return bool(match)

    ### Given a query and response use a few-shot CoT LLM reponse to pull information out
    def classify(self, query, response, prompt, context):
        input_ = {
            "prompt": prompt.replace("{response}", response).replace("{query}", query),
            "generation_config": context.get('model.generation_config'), # TODO: We need to use a dedicated model
            "model_config": context.get('model.model_config'),
            "streaming_override": False, # sets streaming to False
        }
        # Disable streaming of classification output -- deepcopy so we don't effect the model_config
        print("[PROMPT]")
        print(input_['prompt'])
        print("[PROMPT]")
        llm_val = self.llm.call(input_)
        if llm_val is not None and "choices" in llm_val:
            response = llm_val["choices"][0]["text"]
            response = response.replace(input_['prompt'], "")
            for tok in ["eos_token", "bos_token"]:
                if tok in input_["model_config"]:
                    response = response.replace(input_["model_config"][tok],"")
            ### Often times we do not actually get a response, but just the Chain of Thought
            ### In this case try to rerun the LLM to get a Response
            prompts = input_['prompt'].split("\n\n")
            main_example = prompts[-1]
            print("[MAIN EXAMPLE]")
            print(main_example + "\n" + response)
            print("[MAIN EXAMPLE]")    
            if not self.validate_classification(main_example + "\n" + response):
                print("[PROMPTINVALID]")
                print(response)
                print("[PROMPTINVALID]")
                input_["prompt"] = input_["prompt"] + response + "\n### Response:"
                input_["generation_config"]["max_new_tokens"] = 128 # limit so we can focus on results
                llm_val = self.llm.call(input_)
                response = llm_val["choices"][0]["text"]
                response = response.replace(input_['prompt'], "")
            if "### Response:" in response:
                response = response.split("### Response:")[1] # TODO: This probably only really works on WizardLM models
            response = self.parser.parse_llm_response(response)
            print("[PROMPTX]")
            print(response)
            print("[PROMPTX]")
            for tok in ["eos_token", "bos_token"]:
                if tok in input_["model_config"]:
                    response = response.replace(input_["model_config"][tok],"")
            return response.split(",")
        return []

    # Given a query (w/response) and context we learn an object, predicate, subject triplet
    # Returns: True/False + results if information was successfully learned or not
    def learn(self, query, context):
        prompt = context.prompts[f"{query['type']}.cot.prompt"]
        results = self.classify(query['text'], context.get("instruction"), prompt, context)
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
                self.create_predicate("User", query["relation"], query["class"]) # TODO: Need to pull user name
                return True, results
            elif results[0].lower() in  ["false", "no", "0"]:
                self.create_negation("User", query["relation"], query["class"]) # TODO: Need to pull user name
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