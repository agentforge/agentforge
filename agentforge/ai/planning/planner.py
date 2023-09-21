import glob
import os
import time
from typing import List, Dict, Any, Optional
import uuid
from agentforge.interfaces import interface_interactor
from agentforge.ai.planning.pddl import PDDLGraph
from collections import defaultdict
from agentforge.utils import logger

# TODO: make env files for this
FAST_DOWNWARD_ALIAS = "lama"

PLANNER_DIRECTORY = os.environ.get("PLANNER_DIRECTORY")
TYPE_KLASSES = ["boolean", "object", "numeric", "string", "array", "null"]

"""
    Creates a PDDL plan using the Fast Downward planner.
    Typically requires a domain and problem file.

    Input - domain: The domain of the plan to be created.
    Output - A plan in PDDL format and Natural Language format.

    Calls the LLM to generate a plan in natural language format.
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

    def get_cost(self, x):
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

    # TODO: Refactor for new query system
    def execute(self, input, task, problem_data):

        # Grab a standard plan template
        plan_template = """
            (define (problem user-problem)
                (:domain {task.name})
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
        for effect in problem_data:
            val = effect["val"]
            if val not in pddl_context[effect["type"]]:
                pddl_context[effect["type"]].append(val)

        plan_template = plan_template.replace("{object}", "\n".join(pddl_context["object"]))
        plan_template = plan_template.replace("{init}", "\n".join(pddl_context["init"]))
        plan_template = plan_template.replace("{goal}", "\n".join(pddl_context["goal"]))
        plan_template = plan_template.replace("{task.name}", task.name)
        logger.info(plan_template)

        ### Once the problem plan has been generated let's run the planning algorithms
        # TODO: Refactor to use our input
        return self.llm_ic_pddl_planner(input, plan_template)

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
        for tok in ['eos_token', 'bos_token', 'prefix', 'postfix']:
            if tok in input_['model_config']:
                result_text = result_text.replace(input_['model_config'][tok], "")
        return result_text

    def plan_to_language(self, plan, input_):
        prompt = """
                ### Instruction: Your goal is to help the user plan. Transform the PDDL plan into a sequence of behaviors without further explanation. Format the following into a natural language plan. Here is the plan to translate:"""
        prompt += f"{plan} ### Response:"
        logger.info("plan_to_language")
        logger.info(prompt)
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

        logger.info("Running fast downward...")
        # Fast downward call
        func_call = f"python /app/downward/fast-downward.py --alias {FAST_DOWNWARD_ALIAS} " + \
                f"--search-time-limit {self.config.time_limit} --plan-file {plan_file_name} " + \
                f"--sas-file {sas_file_name} " + \
                f"{self.config.domain_pddl_file_path} {task_pddl_file_name}"
        logger.info(func_call)
        os.system(func_call)

        # D. collect the least cost plan
        best_cost = 1e10
        best_plan = None
        for fn in glob.glob(f"{plan_file_name}.*"):
            with open(fn, "r") as f:
                plans = f.readlines()
                cost = self.get_cost(plans[-1])
                if cost < best_cost:
                    best_cost = cost
                    best_plan = "\n".join([p.strip() for p in plans[:-1]])

        # E. translate the plan back to natural language, and write it to result
        if best_plan:
            plans_nl = self.plan_to_language(best_plan, input)
            self.best_plan = best_plan
            self.best_cost = best_cost
            self.plans_nl = plans_nl

        end_time = time.time()
        if best_plan:
            logger.info(f"[info] task {task} takes {end_time - start_time} sec, found a plan with cost {best_cost}")
            return plans_nl
        else:
            logger.info(f"[info] task {task} takes {end_time - start_time} sec, no solution found")
            return "No plan found."

"""
    Config object for the PlanningController
"""
class PlanningControllerConfig:
    def __init__(self, domain: str):        
        # initialize the attributes
        self.domain = domain
        self.domain_pddl_file_path = f"{PLANNER_DIRECTORY}/{domain}/domain.pddl"
        self.domain_pddl_problem_path = f"{PLANNER_DIRECTORY}/{domain}/test.pddl"
        self.time_limit = 200
        self.task = uuid.uuid4()
        self.run = 0
        self.print_prompts = False
        self.best_plan = "None"
        self.best_cost = 0