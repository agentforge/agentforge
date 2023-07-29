import argparse
import glob
import json
import os
import random
import sys
import time
from typing import List
import uuid
from agentforge.utils import Parser
from agentforge.interfaces import interface_interactor
# import openai

FAST_DOWNWARD_ALIAS = "lama"
PLAN_DIRECTORY = os.environ.get("PLANNER_DIRECTORY")
DOMAINS = ["garden"]

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
    def __init__(self, input_values: dict):
        # Validate and/or set default values
        def get_arg(arg_name, valid_choices=None, default_value=None):
            value = input_values.get(arg_name, default_value)
            if valid_choices is not None and value not in valid_choices:
                raise ValueError(f"Invalid value for {arg_name}. Must be one of {valid_choices}")
            return value
        
        # initialize the attributes
        self.domain = get_arg("domain", valid_choices=DOMAINS, default_value="garden")
        self.time_limit = get_arg("time_limit", default_value=200)
        self.task = get_arg("task", default_value=0)
        self.run = get_arg("run", default_value=0)
        self.print_prompts = get_arg("print_prompts", default_value=False)

class PlanningController:
    def __init__(self, input_values: dict = {}):
        # for testing
        self.done= False
        self.llm = interface_interactor.get_interface("llm")
        self.db = interface_interactor.get_interface("db")
        # llm is a service that exposes a call method taking a single dictionary of inputs
        
        # Create a PlanningControllerConfig object
        self.config = PlanningControllerConfig(input_values)

        self.context = ("p_example.nl", "p_example.pddl", "p_example.sol")
        tasks = [("p01.nl", "p01.pddl")]
        self.config.task = 0

        # Initialize problem domain
        self.domain = Domain(self.db, self.config.domain)

        # Initialize the planner
        self.planner = Planner(self.llm)

    ### This function maps the contraints of a planning domain, goes through a list of possible goal-states, and
    ### identifies necessary initialization state.

    ### Queries generally come from the following forms:
    ### Define your subjective objects in the planning domain.
    ### How is the world-state currently initialized?
    ### What are your goals for this plan?
  
    def execute(self, input, attention):

        # Grab a standard plan template
        plan_template = """
            (define (problem garden-enhanced-problem)
                (:domain garden)
                (:objects 
                    {objects}
                )
                (:init 
                    {init}
                )
                (:goal
                (and
                    {goals}
                )))
        """      

        ### Attention has been satisfied and we need to construct a plan for this domain
        ### using the PredicateMemory Attention. When we are done and have a relevant plan
        ### we can abandon out current attention focus.
        init = []
        goals = []
        objects = []
        queries = attention['queries']
        for query in queries:
            for effect in query["effect"]:
                for result in query["results"]: # for each result we gathered for goals
                    if effect["type"] == "goal":
                        goals.append(effect["val"].replace("{val}", result))
                    elif effect["type"] == "object":
                        objects.append(effect["val"].replace("{val}", result))
                    elif effect["type"] == "init":
                        init.append(effect["val"].replace("{val}", result))

        plan_template = plan_template.replace("{objects}", "\n".join(objects))
        plan_template = plan_template.replace("{init}", "\n".join(init))
        plan_template = plan_template.replace("{goals}", "\n".join(goals))

        ### Once the problem plan has been generated let's run the planning algorithms
        return llm_ic_pddl_planner(self.config, self.planner, self.domain, input, plan_template) # TODO: Refactor to use our input

### Helper class to build domains in the Database
class DomainBuilder:
    def __init__(self, db):
        self.db = db

    def add_task(self, domain_name: str, nl: str, pddl: str):
        task_key = f"{domain_name}/{str(uuid.uuid1())}"
        task_data = {"domain": domain_name, "nl": nl, "pddl": pddl}
        self.db.sself.planner.domainata = {"nl": nl, "pddl": pddl, "sol": sol}
        self.db.set(collection="contexts", key=domain_name, data=context_data)

    def set_context(self, domain_name: str, nl: str, pddl: str, sol: str):
        context_data = {"nl": nl, "pddl": pddl, "sol": sol}
        self.db.set(collection="contexts", key=domain_name, data=context_data)

    def set_domain_pddl(self, domain_name: str, pddl: str):
        domain_data = self.db.get(collection="domains", key=domain_name) or {}
        domain_data["pddl"] = pddl
        self.db.set(collection="domains", key=domain_name, data=domain_data)

    def set_domain_nl(self, domain_name: str, nl: str):
        domain_data = self.db.get(collection="domains", key=domain_name) or {}
        domain_data["nl"] = nl
        self.db.set(collection="domains", key=domain_name, data=domain_data)
    
    def set_queries(self, domain_name: str, queries: list, folder_path: str):
        # Fetch existing domain data from the database
        domain_data = self.db.get(collection="domains", key=domain_name) or {}

        # Iterate through each query in the list
        for query in queries:
            # Extract the id value from the query
            id = query.get("id")
            file_path = os.path.join(folder_path, f"{id}.prompt")
            if os.path.exists(file_path):
                # Read the file and extract the text
                with open(file_path, 'r') as file:
                    prompt_text = file.read()

                # Assign the text to the 'prompt' key in the query
                query["prompt"] = prompt_text
            else:
                print(f"File not found: {file_path}")

        domain_data["queries"] = queries
        self.db.set(collection="domains", key=domain_name, data=domain_data)

    def upload_documents_from_folder(self, domain_name: str, folder_path: str, context_name: str):
        # try:
        # Validate folder path
        if not os.path.isdir(folder_path):
            print(f"Error: {folder_path} is not a directory")
            return
        
        # Prepare file paths
        nl_file_path = os.path.join(folder_path, f"{context_name}.nl")
        pddl_file_path = os.path.join(folder_path, f"{context_name}.pddl")
        sol_file_path = os.path.join(folder_path, f"{context_name}.sol")
        domain_pddl_file_path = os.path.join(folder_path, "domain.pddl")
        domain_nl_file_path = os.path.join(folder_path, "domain.nl")
        query_file_path = os.path.join(folder_path, "queries.json")

        # Read and set context files
        if os.path.isfile(nl_file_path) and os.path.isfile(pddl_file_path) and os.path.isfile(sol_file_path):
            with open(nl_file_path, 'r') as nl_file, open(pddl_file_path, 'r') as pddl_file, open(sol_file_path, 'r') as sol_file:
                nl = nl_file.read()
                pddl = pddl_file.read()
                sol = sol_file.read()
                self.set_context(domain_name=domain_name, nl=nl, pddl=pddl, sol=sol)
        else:
            print(f"Error: One or more context files (nl, pddl, sol) are missing in {folder_path}")

        if os.path.isfile(query_file_path):
            with open(query_file_path, 'r') as query_file:
                query = json.loads(query_file.read())
                self.set_queries(domain_name=domain_name, queries=query["queries"], folder_path=folder_path)
        else:
            print(f"Error: Query file (queries.json) is missing in {folder_path}")

        # Read and set domain files
        if os.path.isfile(domain_pddl_file_path) and os.path.isfile(domain_nl_file_path):
            with open(domain_pddl_file_path, 'r') as domain_pddl_file, open(domain_nl_file_path, 'r') as domain_nl_file:
                domain_pddl = domain_pddl_file.read()
                domain_nl = domain_nl_file.read()
                self.set_domain_pddl(domain_name=domain_name, pddl=domain_pddl)
                self.set_domain_nl(domain_name=domain_name, nl=domain_nl)
        else:
            print(f"Error: One or more domain files (domain.pddl, domain.nl) are missing in {folder_path}")
    
        # except Exception as e:
        #     print(f"An error occurred while uploading documents from folder: {e}")


### Domain class grabs necessary data about this plan from the database
class Domain:
    def __init__(self, db, name: str = "default"):
        self.db = db
        self.name = name

    def get_context(self):
        try:
            context_data = self.db.get(collection="contexts", key=self.name)
            
            # Check if context_data is a dictionary
            if not isinstance(context_data, dict):
                print(f"Error: Expected a dictionary, but got {type(context_data)}.")
                return None, None, None
            
            # Extract data from context_data
            nl = context_data.get("nl", "")
            pddl = context_data.get("pddl", "")
            sol = context_data.get("sol", "")

            # Post-process the data
            return (self.postprocess(nl), self.postprocess(pddl), self.postprocess(sol))
        
        except Exception as e:
            print(f"An error occurred while getting context: {e}")
            return None, None, None

    def get_queries(self):
        # try:
        domain_data = self.db.get(collection="domains", key=self.name)
        
        # Check if domain_data is a dictionary
        if not isinstance(domain_data, dict):
            print(f"Error: Expected a dictionary, but got {type(domain_data)}.")
            return None
        
        # Extract and post-process data
        domain_queries = domain_data.get("queries", [])
        return domain_queries
        
        # except Exception as e:
        #     print(f"An error occurred while getting domain queries: {e}")
        #     return None

    def get_domain_pddl(self):
        try:
            domain_data = self.db.get(collection="domains", key=self.name)
            
            # Check if domain_data is a dictionary
            if not isinstance(domain_data, dict):
                print(f"Error: Expected a dictionary, but got {type(domain_data)}.")
                return None
            
            # Extract and post-process data
            domain_pddl = domain_data.get("pddl", "")
            return self.postprocess(domain_pddl)
        
        except Exception as e:
            print(f"An error occurred while getting domain PDDL: {e}")
            return None

    def get_domain_pddl_file(self):
        return f"{self.name}/domain.pddl"

    def get_domain_nl(self):
        try:
            domain_data = self.db.get(collection="domains", key=self.name)
            
            # Check if domain_data is a dictionary
            if not isinstance(domain_data, dict):
                print(f"Error: Expected a dictionary, but got {type(domain_data)}.")
                return None
            
            # Extract and post-process data
            domain_nl = domain_data.get("nl", "")
            return self.postprocess(domain_nl)
        
        except Exception as e:
            print(f"An error occurred while getting domain NL: {e}")
            return None

    def get_domain_nl_file(self):
        return f"{self.name}/domain.nl"

    def postprocess(self, data):
        # Assuming postprocess is a method for formatting or cleaning data
        # If postprocess is an external function, this can be replaced with `return postprocess(data)`
        try:
            # Put logic for post-processing here
            # For now, returning data as is
            return data.strip()
        except Exception as e:
            print(f"An error occurred while post-processing: {e}")
            return None


class Garden(Domain):
    name = "garden" # this should match the directory name

###############################################################################
#
# The agent that leverages classical planner to help LLMs to plan
#
###############################################################################


class Planner:
    def __init__(self, llm):
        self.llm = llm

    def create_llm_ic_pddl_prompt(self, task_nl, domain_pddl, context):
        # our method (LM+P), create the problem PDDL given the context
        context_nl, context_pddl, context_sol = context
        prompt = f"I want you to solve planning problems. " + \
                 f"An example planning problem is: \n {context_nl} \n" + \
                 f"The problem PDDL file to this problem is: \n {context_pddl} \n" + \
                 f"Now I have a new planning problem and its description is: \n {task_nl} \n" + \
                 f"Provide me with the problem PDDL file that describes " + \
                 f"the new planning problem that includes :init directly without further explanations?"
        return prompt

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
        result = self.extract_outermost_parentheses(s)

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

    def parse_result(self, pddl_string):
        # remove extra texts
        #try:
        #    beg = pddl_string.find("```") + 3
        #    pddl_string = pddl_string[beg: beg + pddl_string[beg:].find("```")]
        #except:
        #    raise Exception("[error] cannot find ```pddl-file``` in the pddl string")

        # remove comments, they can cause error
        #t0 = time.time()
        #while pddl_string.find(";") >= 0:
        #    start = pddl_string.find(";")
        #    i = 0
        #    while pddl_string[start+i] != ")" and pddl_string[start+i] != "\n":
        #        i += 1
        #    pddl_string = pddl_string[:start] + pddl_string[start+i:]
        #pddl_string = pddl_string.strip() + "\n"
        #t1 = time.time()
        #print(f"[info] remove comments takes {t1-t0} sec")
        return pddl_string

    def plan_to_language(self, plan, task_nl, domain_nl, domain_pddl, input_):
        domain_pddl_ = " ".join(domain_pddl.split())
        task_nl_ = " ".join(task_nl.split())
        prompt = """
                ### Instruction: Your goal is to help the user plan a garden given the PDDL problem and domain. Format the following into a natural language plan. Here is the plan to translate:"""
        prompt += f"{plan} ### Response:"
        # prompt = f"A planning problem is described as: \n {task_nl} \n" + \
        #          f"The corresponding domain PDDL file is: \n {domain_pddl_} \n" + \
        #          f"The optimal PDDL plan is: \n {plan} \n" + \
        #          f"Transform the PDDL plan into a sequence of behaviors without further explanation."
        res = self.query(prompt, input_, extract_parens=False, streaming_override=True).strip() + "\n"
        return res

def llm_ic_pddl_planner(args, planner, domain, input, task_pddl_):
    parser = Parser()
    context = domain.get_context()
    domain_pddl = domain.get_domain_pddl()
    domain_nl = domain.get_domain_nl()

    # Save domain_pddl to files
    # TODO: We need to more tightly integrate fast downward to avoid disk use
    domain_pddl_file_path = f"/tmp/domain_{args.task}.pddl"
    with open(domain_pddl_file_path, "w") as f:
        f.write(domain_pddl)

    task = args.task
    start_time = time.time()

    # A. generate problem pddl file
    task_suffix = "domain.task_suffix"
    # task_nl = input # TODO: We need to pull information from the user and convert it into NL plan
    task_nl = """
        Your goal is to help the user plan a garden given the PDDL problem and domain.
    """
    # task_nl = parser.format_template(input['prompt']['prompt_template'], instruction=task_nl)
    # prompt = planner.create_llm_ic_pddl_prompt(task_nl, domain_pddl, context)
    # raw_result = planner.query(prompt, input)
    # task_pddl_ = planner.parse_result(raw_result)

    # File names for the fast downward call
    plan_file_name = f"/tmp/plan_{args.task}"
    sas_file_name = f"/tmp/sas_{args.task}"
    task_pddl_file_name = f"/tmp/task_{args.task}.pddl"
    
    # Save task_pddl_ to file
    with open(task_pddl_file_name, "w") as f:
        f.write(task_pddl_)

    print("Running fast ")
    # Fast downward call
    func_call = f"python /app/downward/fast-downward.py --alias {FAST_DOWNWARD_ALIAS} " + \
              f"--search-time-limit {args.time_limit} --plan-file {plan_file_name} " + \
              f"--sas-file {sas_file_name} " + \
              f"{domain_pddl_file_path} {task_pddl_file_name}"
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
        plans_nl = planner.plan_to_language(best_plan, task_nl, domain_nl, domain_pddl, input)
        plan_nl_file_name = f"/tmp/plan_nl_{args.task}"
        with open(plan_nl_file_name, "w") as f:
            f.write(plans_nl)
    end_time = time.time()
    if best_plan:
        print(f"[info] task {task} takes {end_time - start_time} sec, found a plan with cost {best_cost}")
        return plans_nl
    else:
        print(f"[info] task {task} takes {end_time - start_time} sec, no solution found")
        return "No plan found."