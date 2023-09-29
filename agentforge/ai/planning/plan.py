import os, json
from typing import Any, Dict, List
from agentforge.ai.planning.planner import PlanningController
from agentforge.ai.beliefs.symbolic import SymbolicMemory
from agentforge.ai.attention.tasks import TaskManager
from agentforge.utils.stream import stream_string
from agentforge.interfaces import interface_interactor
from agentforge.utils import logger
from agentforge.ai.planning.pddl import PDDLGraph, PDDL
from agentforge.ai.reasoning.query import Query
from agentforge.ai.reasoning.relation import Relation
from agentforge.ai.agents.context import Context
from agentforge.ai.reasoning.zeroshot import ZeroShotClassifier

### PLANNING SUBROUTINE: Executes PDDL plans with help from LLM resource
class Plan:
    ### Executes PDDL plans with help from LLM resource
    def __init__(self, domain: str, goals: List[str]):
        self.llm = interface_interactor.get_interface("llm")
        self.planner = PlanningController(domain)
        self.task_management = TaskManager()
        self.domain = domain
        self.goals = goals
        domain_file = self.planner.config.domain_pddl_file_path
        problem_file = self.planner.config.domain_pddl_problem_path
        self.pddl_graph = PDDLGraph(domain_file, problem_file, domain)
        self.pddl = PDDL(self.pddl_graph)

    """
        Gether information phase of the planning task
        -- gather from user, environment, and memory
    """
    def gather(self, goal: str, user_name: str) -> List[Dict[str, Any]]:
        # Creates queries for the planning task
        seeds = self.pddl_graph.get_seed_queries(goal, user_name)
        goal_data = goal.split(" ")
        goal = goal_data[0] # split the goal into the goal and the object, 1st is always predicate

        logger.info(f"{seeds=}")
        queries = []
        for action_name, seed_list in seeds.items():
            for seed in seed_list:
                seed['goal']  = goal
                seed['metatype']  = "query"
                seed['action'] = action_name
                queries.append(seed)
        return queries

    # Helper function to explore knowledge graph/PDDL and create queries for our plan
    # if we need them
    def init_queries(self, task, context):
        user_name = context.get('input.user_name')
        # Get the current goal
        goal = self.goals[task.stage]
        logger.info(f"GOAL {goal}")
        queries = self.gather(goal, user_name)
        logger.info(f"{queries=}")
        if len(queries) == 0:
            return context
        list(map(task.push, queries)) # efficiently push queries to the task
        logger.info(f"{task=}")
        self.task_management.save(task)
        return self.init_query(task, context)

    # Helper function to activate a query
    def init_query(self, task, context):
        query = task.activate_query()
        logger.info(f"INIT QUERY {query}")
        if query is not None:
            if 'text' in query:
                response = query['text']
            else:
                # only stream the new query if we are on the happy path
                query = Query().get(context, query, streaming=False)
                ## Capture Relational Information
                # query = Relation().extract(context, query)
                logger.info(f"{query=}")
                # raise ValueError("STOP")
                response = query['text']

            context.set("query", response)
            context.set("task", task)
            self.task_management.save(task)
        return context

    def execute(self, context: Context) -> Dict[str, Any]:
        user_id = context.get('input.user_id')
        session_id = context.get('input.model_id')
        key = f"{user_id}:{session_id}:{self.domain}"

        ## TODO: CHECK BELIEFS
        ## Check if a plan already exists and there is no other queries in progress
        ## If this is the case we enquire if the user wants to browse other plans or
        ## create a new plan
        ## This step is the confirmation step preferably a`chieved by CoT Reasoning Engine

        ### PLANNING
        # If there are no remaining queries for the planning task, we can execute the plan
        task = context.get("task")

        ### If there is no task we should not engage in planning at this time...
        if task is None:
            return context

        user_done = False
        agent_done = True #TODO: When we add agent actions we need to make this smarter

        ### Check additional user intent on plan
        plan = task.get_active_plan()
        user_input = context.get("instruction")

        ## TEST: Determine if the user has completed a plan
        if plan is not None:
            z = ZeroShotClassifier()
            prompt = context.prompts["boolean.plan-complete.prompt"]
            z_val = z.classify(prompt, ["Yes", "No"], {"user_input": user_input}, context)
            logger.info(f"YAASIFYING: {z_val}")
            if z_val == "Yes":
                plan = self.pddl.execute(plan, context)
                task.push_complete(plan)
                task.iterate_stage_and_flush()
                user_done = True
                self.task_management.save(task)
                ## Move the plan to the next stage and trace graph to create new queries.
                if task.stage >= len(self.goals):
                    ## If the next stage does not exist, congragulate the user! Job well done
                    stream_string('channel', f"You've done it! You've completed the {task.name} plan.", end_token=" ")
                    # TODO: save and return here
                else:
                    # create new quer
                    logger.info("CREATE NEW QUERIES FOR NEXT STAGE")
                    context = self.init_queries(task, context)
                    # # If we have some newly staged queries we can return
                    # if not task.is_empty_queue() or not task.is_empty_active():
                    #     return context
            else:
                # stream_string('channel', "<PLAN-ACTIVE>", end_token=" ")
                logger.info("PLAN NOT COMPLETE")
                context.set("plan", plan['plan_nl'])

        logger.info(f"CHECKING TASK STATE")
        # Sample these after plan management
        empty_queue = task.is_empty_queue()
        empty_active = task.is_empty_active()
        empty_complete = task.is_empty_complete()
        plan = task.get_active_plan()
        logger.info(f"empty_queue: {empty_queue}, empty_active: {empty_active}, plan: {plan}, empty_complete: {empty_complete}")

        # GATHER NEW QUERIES FOR THIS STATE
        # if task in progress but no queries, generate them and create the PDDL Plan callback
        # Triggers when we have no actions queued/active and we are either at an end-stage
        # point initiated by the user/agent or 
        if empty_queue and empty_active and ((user_done and agent_done) or task.is_empty_complete()):
            logger.info("GATHERING NEW QUERIES")
            context = self.init_queries(task, context)

        # QUERY USER: Activate a query if we have none active
        elif not empty_queue and empty_active:
            logger.info("ACTIVATING QUERY")
            context = self.init_query(task, context)

        # Activate existing query
        elif not empty_active and context.get("query") is None:
            logger.info("ENSURING ACTIVE QUERY")
            context = self.init_query(task, context)

        # PLAN: Not a new instance/stage and no queries, we're at planning time
        if plan is None and context.get("query") is None:
            task = context.get("task") # update task
            logger.info("PLANNING")
            ## Queries complete, let's execute the plan
            finalize_reponse = "I have all the info I need, let me finalize the current plan."

            goal = self.goals[task.stage]
            problem_data = self.pddl.create_pddl_problem_state(task, goal)
            logger.info(problem_data)
            logger.info("Creating PDDL Plan")

            # TODO: Make channel user specific
            stream_string('channel', finalize_reponse, end_token=" ")

            best_plan, best_cost = self.planner.execute(context.get_model_input(), task, problem_data)

            if best_plan == "":
                logger.info("NO PLAN FOUND")
                return context

            dir_name = os.getenv("PLANNER_DIRECTORY")
            filename = "actions.json"
            actions = {}
            with open(f"{dir_name}/{self.domain}/{filename}", 'r') as f:
                actions = json.load(f)

            plan_nl = self.plan_to_language(best_plan, context.get_model_input(), actions)

            task.active = True
            # setup plan as next action in task sequence
            plan_task = {
                "plan_nl": plan_nl,
                "plan": best_plan,
                "cost": best_cost,
                "metatype": "plan",
                "state": problem_data,
            }
            task.push(plan_task)
            task.activate_plan()
            self.task_management.save(task)
            self.task_management.save_state(context.get('input.user_name'), problem_data)
            context.set("response", plan_nl)
            context.set("task", task)
            return context
        return context

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

    def plan_to_language(self, plan, input_, actions={}):
        keys = self.extract_action_keys(plan)
        explanations = []
        for key in keys:
            if key not in actions:
                continue
            explanations.append(f"{key}: {actions[key]}")

        prompt = """### Instruction: Your goal is to help the user plan. Transform the PDDL plan into a sequence of behaviors without further explanation. Format the following into a natural language plan. Action Definitions: {explanations}
        Here is the plan to translate: {plan} ### Response:"""

        prompt = prompt.replace("{plan}", plan)
        prompt = prompt.replace("{explanations}", "\n".join(explanations))

        logger.info("plan_to_language")
        logger.info(prompt)
        res = self.query(prompt, input_, extract_parens=False, streaming_override=True).strip() + "\n"
        return res
    
    def extract_action_keys(self, plan):
        keys = []
        for line in plan.split("\n"):
            line = line.replace("(", "").replace(")", "")
            action = line.split(" ")[0]
            keys.append(action)
        return keys