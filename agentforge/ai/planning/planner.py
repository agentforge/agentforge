import glob
import os
import time
from typing import List, Dict, Any
import uuid
from agentforge.interfaces import interface_interactor
from agentforge.ai.planning.pddl_to_graph import get_seed_queries
from collections import defaultdict

# TODO: make env files for this
FAST_DOWNWARD_ALIAS = "lama"
PLANNER_DIRECTORY = os.environ.get("PLANNER_DIRECTORY")
TYPE_KLASSES = ["boolean", "object", "numeric", "string", "array", "null"]

def get_cost(x):
    splitted = x.split()
    counter = 0
    found = False
    cost = 1e5
    for i, xx in enumerate(splitted):
        if xx == "cost":
            counter = i
            found = True
            break
    if found:
        cost = float(splitted[counter+2])
    return cost
class PlanningControllerConfig:
    def __init__(self, domain: str):        
        # initialize the attributes
        self.domain = domain
        self.domain_pddl_file_path = f"{PLANNER_DIRECTORY}/{domain}/domain.pddl"
        self.domain_pddl_problem_path = f"{PLANNER_DIRECTORY}/{domain}/p01.pddl"
        self.time_limit = 200
        self.task = uuid.uuid4()
        self.run = 0
        self.print_prompts = False
"""
Creates PDDL plans using the Fast Downward planner.
Input - domain: The domain of the plan to be created.
Output - A plan in PDDL format and Natural Language format.
"""
class PlanningController:
    def __init__(self, domain: str):
        # for testing
        self.done= False
        self.llm = interface_interactor.get_interface("llm")
        self.db = interface_interactor.get_interface("db")
        self.domain = domain
        
        # Create a PlanningControllerConfig object
        self.config = PlanningControllerConfig(domain)

    # TODO: Refactor for new query system
    def execute(self, input, attention):

        # Grab a standard plan template
        plan_template = """
            (define (problem user-problem)
                (:domain {domain})
                (:objects 
                    {object}
                )
                (:init 
                    {init}
                )
                (:goal
                (and
                    {goal}
                )))
        """      

        ### Attention has been satisfied and we need to construct a plan for this domain
        ### using the SymbolicMemory Attention. When we are done and have a relevant plan
        ### we can abandon out current attention focus.
        pddl_context = {
            "init": [],
            "goal": [],
            "object": [],
        }
        queries = attention['queries']['complete']
        for query in queries:
            for effect in query["effect"]:
                for result in query["results"]: # for each result we gathered for goals, innits, objects
                    if effect["type"] in ["goal", "object", "init"]:
                        val = effect["val"].replace("{val}", result)
                        if val not in pddl_context[effect["type"]]:
                            pddl_context[effect["type"]].append(val)

        plan_template = plan_template.replace("{object}", "\n".join(pddl_context["object"]))
        plan_template = plan_template.replace("{init}", "\n".join(pddl_context["init"]))
        plan_template = plan_template.replace("{goal}", "\n".join(pddl_context["goal"]))
        print(plan_template)

        ### Once the problem plan has been generated let's run the planning algorithms
        # TODO: Refactor to use our input
        return self.llm_ic_pddl_planner(input, plan_template)

    def init_simple_effects(self, goal: str, klass: str):
        return [{   
                "val":f"({goal}" + " {val})",
                "type": "goal"
            },
            {   "val": "{val} - " + klass,
                "type": "object"
            }]

    def init_subtype_predicates(self, predicate: str):
        return [{
                "val": "{val}-{subtype} - {subtype}",
                "type": "object"
            },
            {
                "val": f"({predicate} " + "{val}-{subtype} {val})",
                "type": "init"
            }]

    """
    Input - seed: The seed of the plan to be created. i.e. "(growing ?plant)"
    Output - A question in Natural Language format
    """
    def create_query(self, obj: str, template: str, datatype: str, effects: List[Dict]) -> str:
        query = {}
        query['object'] = obj.replace("?","").replace("-", " ")
        query['text'] = template
        query['type'] = datatype
        query['effect'] = effects
        return query
    
    """
    Predicates come in a handfule of types, we need to support and determine
    what type of predicate, that will determine how we build our PDDL plan.

    1. Simple predicates are predicates that are just a single predicate/obj, i.e. plot-fertilized ?plot"
    2. Subtype predicates start with 'has', include a subtype obj and primary type obj, i.e. has-seed-type ?seed ?plant"
    2. 
    
    """
    def analyze_predicates(self):
        pass

    """
    Input - goal: The goal of the plan to be created. i.e. "growing ?plant"
    Output - A list of queries in Dictionary
    Creates queries using PDDL Graph functionality.
    """
    def create_queries(self, goal: str) -> List[Dict]:
        # Get the PDDL documents
        domain_file = self.config.domain_pddl_file_path
        problem_file = self.config.domain_pddl_problem_path
        ret = []
        predicates = []

        seeds = self.seed_queries = get_seed_queries(goal, domain_file, problem_file)
        goal_data = goal.split(" ")
        goal = goal_data[0] # split the goal into the goal and the object, 1st is always predicate

        print(f"{seeds=}")

        # TODO: Refactor this to use LLMs to automatically generate queries
        # using the given context here
        templates = {
            'string': "What kind of {klass} do you want {goal}?",
            'boolean': 'Do you have a {klass}?',
            'or': "Are you {goal} a {values}?",
            'numeric': "How many {klass} do you want {goal}?"
        }
        relations = {
            'string': '[ENT] [R1] {goal} [ENT] [R2]',
            'boolean': '[ENT] [R1] has a [ENT] [R2]',
            'or': '[ENT] [R1] has a [ENT] [R2]',
            'numeric': '[ENT] [R1] has [ENT] [R2]',
        }
        hierarchy = defaultdict(list)
        for seed_key, seed in seeds.items():
            klass = seed['class'] # ?plant
            datatype = seed['type']
            parent = seed['parent']

            effects = self.init_simple_effects(goal, klass)

            template = templates[datatype]
            if parent not in TYPE_KLASSES and parent not in hierarchy:
                # check to see if we have asked the parent question already
                hierarchy[parent].append(seed_key)

            elif parent in hierarchy:
                template = templates['or']
                hierarchy[parent].append(seed_key)
                template = template.replace("{values}", " or ".join(hierarchy))   
            
            else:
                template = template.replace("{klass}", seed_key)
            

            template = template.replace("{goal}", goal)
            query = self.create_query(seed_key, template, datatype, effects)
            relation = relations[datatype].replace("{goal}", goal)

            query["relation"] = relation
            query["goal"] = goal
            query["class"] = klass
            query["type"] = seed['type']
            ret.append(query)

            # Extract the predicates from the seeds
            for predicate in seed['predicates']:
                # for each predicate we need to create a object and init
                predicate = predicate.split(" ")
                # Grab the predicate and add it to the init
                predicates.append(predicate)

        # print(f"{subtypes=}")
        # # Followup for subtypes, i.e. ?object has-x, has-y, has-z
        # if len(subtypes) > 0:
        #     values = " or ".join(subtypes)
        #     template = templates['or']
        #     template.replace("{values}", values)
        #     template.replace("{goal}", goal)
        #     sub_effects = self.init_subtype_predicates(predicate)
        #     query = self.create_query(seed_key, template, "string", effects)
        #     ret.append(query)
        print(hierarchy)
        raise ValueError("STOP") 
        return ret

    def extract_outermost_parentheses(self, s):
        # Indexes of the outermost opening and closing parentheses
        open_idx = None
        close_idx = None
        
        # Counter for the depth of nested parentheses
        depth = 0

        # Loop through each character in the string
        i = 0
        while i < len(s):
            char = s[i]
            # Increment the depth counter if an opening parenthesis is found
            if char == '(':
                depth += 1
                # If this is the first opening parenthesis, store its index
                if depth == 1:
                    open_idx = i
            # Decrement the depth counter if a closing parenthesis is found
            elif char == ')':
                depth -= 1
                # If the depth is back to 0, store the index of this closing parenthesis
                if depth == 0:
                    close_idx = i
                    break

            i += 1

        # If opening and closing parentheses are found, return the contents within them
        if open_idx is not None and close_idx is not None:
            return '(' + s[open_idx + 1: close_idx] + ')'
        # If not, return an empty string
        else:
            return ''

    def test_extract_outermost_parentheses(self, s):
        # Example Usage
        s = "Here is some text (I want (only this) part) and this is not needed."
        return self.extract_outermost_parentheses(s)

    def query(self, prompt_text, input_config, extract_parens=True, streaming_override=False):
        result_text = "()"
        input_ = {
            "prompt": prompt_text,
            "generation_config": input_config['generation_config'],
            "model_config": input_config['model_config'],
            "streaming_override": streaming_override,
        }
        response = self.llm.call(input_)
        result_text = response['choices'][0]['text']
        result_text = result_text.replace(input_['prompt'], "")
        if extract_parens:
            result_text = self.extract_outermost_parentheses(result_text)
        for tok in ['eos_token', 'bos_token']:
            if tok in input_['model_config']:
                result_text = result_text.replace(input_['model_config'][tok], "")
        return result_text

    def plan_to_language(self, plan, input_):
        prompt = """
                ### Instruction: Your goal is to help the user plan. Transform the PDDL plan into a sequence of behaviors without further explanation. Format the following into a natural language plan. Here is the plan to translate:"""
        prompt += f"{plan} ### Response:"
        print("plan_to_language", prompt)
        res = self.query(prompt, input_, extract_parens=False, streaming_override=True).strip() + "\n"
        return res

    # TODO: Extract this to its own separate service -- CPU intensive process blocks API
    def llm_ic_pddl_planner(self, input, task_pddl_):
        task = self.config.task
        start_time = time.time()

        # File names for the fast downward call
        plan_file_name = f"/tmp/plan_{self.config.task}"
        sas_file_name = f"/tmp/sas_{self.config.task}"
        task_pddl_file_name = f"/tmp/task_{self.config.task}.pddl"
        
        # Save task_pddl_ to file
        with open(task_pddl_file_name, "w") as f:
            f.write(task_pddl_)

        print("Running fast downward...")
        # Fast downward call
        func_call = f"python /app/downward/fast-downward.py --alias {FAST_DOWNWARD_ALIAS} " + \
                f"--search-time-limit {self.config.time_limit} --plan-file {plan_file_name} " + \
                f"--sas-file {sas_file_name} " + \
                f"{self.config.domain_pddl_file_path} {task_pddl_file_name}"
        print(func_call)
        os.system(func_call)

        # D. collect the least cost plan
        best_cost = 1e10
        best_plan = None
        for fn in glob.glob(f"{plan_file_name}.*"):
            with open(fn, "r") as f:
                plans = f.readlines()
                cost = get_cost(plans[-1])
                if cost < best_cost:
                    best_cost = cost
                    best_plan = "\n".join([p.strip() for p in plans[:-1]])

        # E. translate the plan back to natural language, and write it to result
        if best_plan:
            plans_nl = self.plan_to_language(best_plan, input)
        
        end_time = time.time()
        if best_plan:
            print(f"[info] task {task} takes {end_time - start_time} sec, found a plan with cost {best_cost}")
            return plans_nl
        else:
            print(f"[info] task {task} takes {end_time - start_time} sec, no solution found")
            return "No plan found."